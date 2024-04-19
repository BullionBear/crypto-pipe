import loguru
from pipe.worker.worker_nodes import WorkerNode
import argparse

logger = loguru.logger


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--port', type=int, help='Host Port', default=54412)
    parser.add_argument('--n_workers', type=int, help='Number of workers', default=4)
    args = parser.parse_args()

    # Now you can use args.port where you need the port number
    logger.info(f"Received port: {args.port}")
    worker = WorkerNode(args.port, args.n_workers)
    worker.listen()


if __name__ == "__main__":
    main()
