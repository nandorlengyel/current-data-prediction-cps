import abc
from abc import ABCMeta
import threading
import requests

import socket
import datetime
from PicoTechEthernet import PicoTechEthernetCM3
import os 

class ReaderThread(threading.Thread, metaclass=ABCMeta):

    def __init__(self, topic_name, lock, connector, queue):

        self.topic_name = topic_name
        self.lock = lock
        self.connector = connector
        self.queue = queue

        self.subscriber_name = topic_name + "Subscriber"
        self.data_reader_name = topic_name + "Reader"

        threading.Thread.__init__(self, target=self.read_data, name=self.subscriber_name, daemon=True)
            

    def read_data(self):
        while True:
            
            with self.lock: # Protect access to methods on the same Connector
                input = self.connector.get_input(self.subscriber_name + "::" + self.data_reader_name)
            input.wait() # wait outside the lock
            with self.lock: # Take the lock again
                input.take()
                for sample in input.samples.valid_data_iter:
                    self.process_data(sample)

    @abc.abstractmethod
    def process_data(self, sample):
        """Method documentation"""
        return

class WriterThread(threading.Thread, metaclass=ABCMeta):

    cache = []

    def __init__(self, topic_name, lock, timeout, connector, queue):
        
        self.topic_name = topic_name
        self.lock = lock
        self.timeout = timeout
        self.connector = connector
        self.queue = queue

        self.result_dict = {}

        self.publisher_name = topic_name + "Publisher"
        self.data_writer_name = topic_name + "Writer"

        threading.Thread.__init__(self, target=self.write_data, name=self.publisher_name, daemon=True)         

    def write_data(self):

        CM3 = PicoTechEthernetCM3(ip=os.environ['PICO_IP'], port=1)

        self.result_dict = {}

        while True:  # Loop forever

            now = datetime.datetime.now()
            while now.second == 0:
                try:
                    print(CM3.connect())
                    print(CM3.lock())
                    CM3.filter(50)
                    # print(CM3.EEPROM())
                    CM3.set('1w', b'Converting\x00')  # channel setup ??

                    for load in next(CM3):       
                        try:
                            self.result_dict[load['channel']].append(load['value'])
                        except KeyError:
                            self.result_dict[load['channel']] = [load['value']]

                        now = datetime.datetime.now()
                        if now.second == 59:

                            with self.lock: # Protect access to methods on the same Connector                 
                                output = self.connector.get_output(self.publisher_name + "::" + self.data_writer_name)      
                                self.produce_data(output)   

                            self.result_dict = {}

                except requests.exceptions.ConnectionError:
                    print('Connection Error to InfluxDB')
                except socket.timeout:
                    print('Connection timeout to PicoTech device')
            
    @abc.abstractmethod
    def produce_data(self, output):
        """Method documentation"""
        return
