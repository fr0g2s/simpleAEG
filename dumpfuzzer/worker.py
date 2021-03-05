import inputgen
import os
import subprocess

class Worker():
    def __init__(self, target_bin):
        # set target binary
        self.bin = target_bin
        

    def fuzzing(self):
        for i in range(0, 5, 1):
            data = inputgen.get_data()
            subprocess.Popen([self.target_bin, inputgen.get_data])

    def send_result(self):
        # send result to logger
        pass
    

def main():
    worker = Worker()

if __name__ == "__main__":
    main()
