#!/usr/bin/python 

import inputgen
import os
import subprocess

class Worker():
    def __init__(self, target_bin):
        # set target binary
        self.bin = target_bin


    def fuzzing(self):
        generator = inputgen.Generator()
        stats = []
        err = None
        for i in range(0, 1, 1):
            result = {}
            data = generator.get_data()
            result['stdin'] = data
            try:
                with subprocess.Popen([self.bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                    result = p.communicate(input=data)
                    result['stdout'] = proc.stdout.read()
                    result['stderr'] = proc.stderr.read()
                    stats.append(result)
            except OSError as e:
                err = e
                print(err)
            except SubprocessError as e:
                err = e
                print(err)
            except ValueError as e:
                err = e
                print(err)
        if err == None:
            return stats
        else:
            return -1


    def send_result(self):
        # send result to logger
        pass



def main():
    worker = Worker(target_bin='./target/copystr')
    result = worker.fuzzing()
    if result == -1:
        print('error occured')
        sys.exit(-1)

    print('== result ==')
    print(result)

if __name__ == "__main__":
    main()
