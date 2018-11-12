from  multiprocessing import Process
from hashlib import md5
from os import listdir, environ
from os.path import isfile, join, dirname
from re import match
import csv
import zmq

END_TOKEN = 'END'
INPUT_FILES_DIRECTORY = environ.get('INPUT_FILES_DIRECTORY', join(dirname(__file__), '../../../shot-log'))

class Reader(Process):
    def _send_row(self, row):
        self.frontend.send_json(row)

    def __init__(self, incoming_address, incoming_port, reader_number=None, number_of_readers=None):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.reader_number = reader_number
        self.number_of_readers = number_of_readers
        super(Reader, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PUSH)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
    def _belongs_to_this_reader(self, filename):
        return self.number_of_readers == None or \
               self.reader_number == None or  \
               int(md5(filename.encode()).hexdigest(), 16) % self.number_of_readers == self.reader_number
    def run(self):
        self._init()
        files_names = [join(INPUT_FILES_DIRECTORY, entry)  for entry in listdir(INPUT_FILES_DIRECTORY) if match(r'^shot log \w{3}\.csv$', entry)]
        from time import sleep

        sleep(4)
        for file_name in files_names:
            csv_team = match(r'.*shot log (\w{3})\.csv$', file_name).group(1)
            if self._belongs_to_this_reader(csv_team):
                print(csv_team)
                with open(file_name, 'r') as f:
                    shot_logs_reader = csv.DictReader(f)
                    for line in shot_logs_reader: 
                        line['shoot team'] = csv_team
                        self._send_row(line) 


        self._send_row(END_TOKEN)

        print('Finished reading')



        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.context.term()

