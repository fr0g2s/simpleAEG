#!/usr/bin/python
import pyradamsa
import os.path
import struct

'''
    == Generator == 
    make random.data file for use to fuzzing
    - get_data(): get random data
    - save_data(): save random data to file
'''

class Generator:
    '''
        generate random data via radamsa
    '''
    def __init__(self, target_type='string'):
        self.rad = pyradamsa.Radamsa()

    def get_data(self, seed_name=b'helloworld', max_len=None):
        '''
            include printable string, non-printable data, number
        '''
        base_string = b''
        if os.path.isfile(seed_name):
            with open(seed_name, 'rb') as f:
                base_string = f.read()
        else:
            base_string = seed_name
        new_string = b''
        while new_string == b'':
            new_string = self.rad.fuzz(base_string, max_mut=max_len)
        return new_string

    def save_data(self, filename, data):
        '''
            save data to file
        '''
        with open('./input'+filename, 'wb') as fP:
            fp.write(data)


def main(): # for test
    gen = Generator()
    random_data = gen.get_data()
    gen.save_data('functest', random_data)
     

if __name__ == "__main__":
    main()
