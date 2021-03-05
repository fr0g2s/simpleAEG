import inputgen 
import worker
import logger
import sys


def main():
    try:
        worker = worker.Worker(target_bin='./target/copystr')
        result = worker.fuzzing()
        logger = logger.Logger(log_dir='logs')
    except logger.ErrExistName as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
