import concurrent.futures
import time
from queue import Queue, Empty
import loguru
import zmq
import pipe.const as const
import pipe.utils as utils
from pipe.task_registry import TASK_REGISTRY

logger = loguru.logger


class WorkerNode:
    def __init__(self, port: int, num_workers: int = 2):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(f"tcp://*:{port}")
        self.running = False
        self.tasks = Queue()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_workers)

    def listen(self):
        logger.info("Start Listening...")
        self.executor.submit(self.run)
        while True:
            try:
                msg = self.socket.recv_json()
                logger.info(f"Received message: {msg}")
                if msg[const.CMD] == const.MASTER_CONNECTION_ESTABLISHED:
                    response = utils.make_cmd(const.WORKER_CONNECTION_ESTABLISHED_ACK, {})
                    self.socket.send_json(response)
                elif msg[const.CMD] == const.MASTER_CREATE_TASK:
                    data = msg[const.DATA]
                    func = TASK_REGISTRY.get(data['name'], None)
                    if func:
                        args = data.get('args', [])
                        kwargs = data.get('kwargs', {})
                        self.add_task(func, *args, **kwargs)
                        response = utils.make_cmd(const.WORKER_CREATE_TASK_ACK, {})
                        self.socket.send_json(response)
                    else:
                        logger.error(f"Task {data['name']} not found.")
                        # Consider handling this situation more explicitly if needed
                else:
                    logger.error(f"Undefined command: {msg[const.CMD]}")
            except Exception as e:
                logger.error(f"Exception occurred: {e}")
                break  # Optional: Stop listening on fatal error

    def add_task(self, func, *args, **kwargs):
        if func is not None:
            self.tasks.put((func, args, kwargs))

    def run(self):
        self.running = True
        while self.running:
            try:
                func, args, kwargs = self.tasks.get(timeout=10)
                self.executor.submit(func, *args, **kwargs)
            except Empty:
                logger.info("No task in queue.")
            except Exception as e:
                logger.error(f"Error executing task: {e}")

    def stop(self):
        self.running = False
        self.executor.shutdown(wait=True)
        self.socket.close()
        self.context.term()
        logger.info("WorkerNode has been stopped gracefully.")


if __name__ == '__main__':

    # Example of a function to run in the threads
    def example_task(duration, message):
        logger.info(f"Task started: {message}")
        time.sleep(duration)
        logger.info(f"Task finished: {message}")


    # Example usage
    worker = WorkerNode(port=1234, num_workers=4)  # Specify the number of worker threads

    worker.add_task(example_task, 2, "Processing data")
    worker.add_task(example_task, 2, "Loading resources")
    worker.add_task(example_task, 1, "Updating interface")
    worker.add_task(example_task, 1, "Sending email")

    # Ideally, run should be in a separate thread if it has a loop that waits
    import threading
    thread = threading.Thread(target=worker.run)
    thread.start()

    # Wait for a while then stop the worker
    time.sleep(5)
    worker.stop()
    thread.join()  # Ensure the run thread has finished
