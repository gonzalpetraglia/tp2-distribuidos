from  multiprocessing import Process
from hashlib import md5
from os import listdir, environ
from os.path import isfile, join, dirname
from re import match
import csv
from source import Source

END_TOKEN = 'END'

class Reader(Source):

    def __init__(self, config, incoming_address, incoming_port, reader_number=None, number_of_readers=None):
        INPUT_FILES_DIRECTORY = join(dirname(__file__), config['folder'])

        def lines():
            def _belongs_to_this_reader(filename):
                return number_of_readers == None or \
                       reader_number == None or \
                       int(md5(filename.encode()).hexdigest(), 16) % number_of_readers == reader_number

            files_names = [join(INPUT_FILES_DIRECTORY, entry)  for entry in listdir(INPUT_FILES_DIRECTORY) if match(config['filename_regex'], entry)]
            
            from time import sleep
            sleep(4) ## Temporary hack that lets everything connect before emiting lines

            for file_name in files_names:
                csv_team = match(config['filename_regex'], file_name).group(1)
                if not _belongs_to_this_reader(csv_team):
                    continue

                print(csv_team)
                with open(file_name, 'r') as f:
                    shot_logs_reader = csv.DictReader(f)
                    for line in shot_logs_reader: 
                        line['shoot team'] = csv_team
                        yield (line)

        super(Reader, self).__init__(incoming_address, incoming_port, lines)


