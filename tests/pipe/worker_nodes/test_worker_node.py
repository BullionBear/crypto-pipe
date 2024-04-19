import threading
import unittest
import zmq
from pipe.worker.worker_nodes import WorkerNode
from pipe.const import MASTER_CONNECTION_ESTABLISHED, WORKER_CONNECTION_ESTABLISHED_ACK
from pipe.utils import make_cmd


class TestWorkerNode(unittest.TestCase):
    def setUp(self):
        # Setup ZMQ context
        self.context = zmq.Context()

        # Initialize the WorkerNode
        self.worker_node = WorkerNode(port=5555, num_workers=2)

        # Start the WorkerNode in a separate thread
        self.thread = threading.Thread(target=self.worker_node.listen)
        self.thread.start()

        # Setup ZMQ socket to simulate the master
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.connect("tcp://localhost:5555")

    def tearDown(self):
        # Stop the WorkerNode
        self.worker_node.stop()

        # Wait for the thread to finish
        self.thread.join()

        # Close the ZMQ socket and terminate the context
        self.socket.close()
        self.context.term()

    def test_connection_establish(self):
        # Send a connection establish message
        message = make_cmd(MASTER_CONNECTION_ESTABLISHED, {})
        self.socket.send_json(message)

        # Receive the response
        response = self.socket.recv_json()
        expected_response = make_cmd(WORKER_CONNECTION_ESTABLISHED_ACK, {})

        # Check if the response is correct
        self.assertEqual(response, expected_response, "Failed to establish connection correctly.")


# Running the tests
if __name__ == '__main__':
    unittest.main()


# Running the tests
if __name__ == '__main__':
    unittest.main()