#!/usr/bin/python

import os
import sys

class ErrExistName(Exception):
    def __str__(self):
        return "log dir name already used"

class Logger:
    def __init__(self, log_dir='output'):
        if os.path.isfile(log_dir):
            raise ErrExistName()
        
        self.log_dir = log_dir + '/'
        self.isExist = os.path.exists(self.log_dir)

    def logging(self, filename='tmp.log', result='tmp log'):
        if self.isExist == False:
            os.makedirs(self.log_dir, exist_ok=True)   # make parent dir

        with open(self.log_dir+filename, 'wb') as fp:    # result file must be bytes
            fp.write(result)


def main():
    try:
        logger = Logger(log_dir='output')
        logger.logging(filename='test.log', result=b'this is result data for testing')
    except ErrExistName as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
