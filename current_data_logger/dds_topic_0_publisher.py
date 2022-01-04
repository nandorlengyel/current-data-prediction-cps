from dds_threads import WriterThread
from datetime import datetime
import random

class dds_topic_0Writer(WriterThread):
	def produce_data(self, output):	
		dict = {"timeStamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  "currentData":random.random()}				
		output.instance.set_dictionary(dict)
		print("current data sent: " + str(dict))
		output.write()
