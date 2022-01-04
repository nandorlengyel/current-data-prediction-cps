from dds_threads import ReaderThread
from influx_client import write_to_influx
from datetime import datetime as dt

class dds_topic_0Reader(ReaderThread):
	def process_data(self, sample):
		data = sample.get_dictionary()
		print(self.topic_name + " data received: ", data)
		write_to_influx("CurrentData", data['currentData'], dt.strptime(data['timeStamp'], '%Y-%m-%d %H:%M:%S').astimezone().isoformat())
