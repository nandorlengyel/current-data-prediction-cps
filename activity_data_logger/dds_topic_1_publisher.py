from dds_threads import WriterThread
from datetime import datetime
import random

class dds_topic_1Writer(WriterThread):
	def produce_data(self, output):	
		dict = {"timeStamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  "activityData":random.randint(0, 1)}				
		output.instance.set_dictionary(dict)
		print("activity data sent: " + str(dict))
		output.write()
