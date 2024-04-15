import concurrent.futures
import time
from queue import Queue, Empty
import loguru

logger = loguru.logger


class Worker:
    def __init__(self, num_workers=2):
        self.tasks = Queue()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_workers)
        self.running = True  # A flag to control the running of the loop in run()

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def run(self):
        while self.running:
            try:
                func, args, kwargs = self.tasks.get(timeout=10)
                self.executor.submit(func, *args, **kwargs)
            except Empty:
                logger.info("No task in queue.")
                continue

    def stop(self):
        self.running = False  # Set the running flag to False to exit the run loop
        self.executor.shutdown(wait=True)  # Shutdown the executor and wait for all threads to finish


# Example of a function to run in the threads
def example_task(duration, message):
    logger.info(f"Task started: {message}")
    time.sleep(duration)
    logger.info(f"Task finished: {message}")


# Example usage
worker = Worker(num_workers=4)  # Specify the number of worker threads

worker.add_task(example_task, 1, "Processing data")
worker.add_task(example_task, 1, "Loading resources")
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
