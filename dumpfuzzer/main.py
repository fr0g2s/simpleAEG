import inputgen 
import worker
import logger

import sys


def main():
    try:
        worker = worker.Worker(target_bin='../target/copystr')
        worker.fuzzing()
        logger = logger.Logger('main_log')
    except logger.ErrExistName as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
