#!/usr/bin/python
class Logger:
    def __init__(self, log_name):
        self.logfile = log_name
    
    def logging(self, result):
        # logging result
        with open(self.logfile, 'wb') as fp:    # result file must be bytes
            fp.write(result)


def main():
    logger = Logger('test_log.log')
    logger.logging(b'this is result data for testing')

if __name__ == "__main__":
    main()
