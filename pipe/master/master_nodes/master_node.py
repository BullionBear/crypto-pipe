import zmq
import json
import pipe.const as const
import pipe.utils as utils


class MasterNode:
    def __init__(self):
        self.context = zmq.Context()
        self.worker_connections = {}  # Dictionary to store connections by worker ID

    def connect(self, worker_id: str, ip: str, port: int):
        """
        Establish a connection to a WorkerNode.

        Args:
        worker_id (str): A unique identifier for the worker.
        ip (str): The IP address of the worker.
        port (int): The port number on which the worker is listening.
        """
        address = f"tcp://{ip}:{port}"
        socket = self.context.socket(zmq.DEALER)
        socket.connect(address)
        self.worker_connections[worker_id] = socket
        # Send a connection established command
        cmd = utils.make_cmd(const.MASTER_CONNECTION_ESTABLISHED, {})
        socket.send_json(cmd)
        # Wait for acknowledgment
        response = socket.recv_json()
        print(f"Connected to Worker {worker_id}: {response}")

    def send_task(self, worker_id: str, name: str, *args, **kwargs):
        """
        Send a task to the specified WorkerNode.

        Args:
        worker_id (str): The ID of the worker to which the task will be sent.
        name (str): The name of the task to be executed.
        args (tuple): Positional arguments for the task.
        kwargs (dict): Keyword arguments for the task.
        """
        if worker_id in self.worker_connections:
            socket = self.worker_connections[worker_id]
            task_data = {
                'name': name,
                'args': args,
                'kwargs': kwargs
            }
            cmd = utils.make_cmd(const.MASTER_CREATE_TASK, task_data)
            socket.send_json(cmd)
            # Optionally wait for acknowledgment
            response = socket.recv_json()
            print(f"Task sent to Worker {worker_id}: {response}")
        else:
            print(f"No connection to worker with ID {worker_id}")

