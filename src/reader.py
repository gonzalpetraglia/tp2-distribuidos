from  multiprocessing import Process
from os import listdir, environ
from os.path import isfile, join, dirname
from re import match
import csv
import zmq


INPUT_FILES_DIRECTORY = environ.get('INPUT_FILES_DIRECTORY', join(dirname(__file__), '../../shot-log'))

class Reader(Process):
    def _send_row(self, row):
        self.socket.send_pyobj(row)

    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        super(Reader, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
    def run(self):
        self._init()
        files_names = [join(INPUT_FILES_DIRECTORY, entry)  for entry in listdir(INPUT_FILES_DIRECTORY) if match(r'^shot log \w{3}\.csv$', entry)]
        for file_name in files_names:
            csv_team = match(r'.*shot log (\w{3})\.csv$', file_name).group(1)
            print(csv_team)
            with open(file_name, 'r') as f:
                shot_logs_reader = csv.DictReader(f)
                for line in shot_logs_reader: 
                    line['shoot team'] = csv_team
                    self._send_row(line) #send


        self._send_row('END')

        print('Finished reading')



        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()

