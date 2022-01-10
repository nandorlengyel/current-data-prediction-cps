from dds_threads import WriterThread
import pytz
from datetime import datetime

class dds_topic_0Writer(WriterThread):
	def produce_data(self, output):	

		for key, value in self.result_dict.items():           
			agg_value = sum(value)
			consumption_value = agg_value / 1000 * 230 / 1000 / 60
			dict = {"timeStamp": self.localize_time(datetime.now()),  "currentData":consumption_value}
			break # only first channel

		output.instance.set_dictionary(dict)
		print("current data sent: " + str(dict))
		output.write()

	def localize_time(self, time):
		localtimezone = pytz.timezone('UTC')
		local_time = localtimezone.localize(time, is_dst=None)
		return local_time.strftime("%Y-%m-%d %H:%M:%S%z")
