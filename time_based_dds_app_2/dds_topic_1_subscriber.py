from dds_threads import ReaderThread

class dds_topic_1Reader(ReaderThread):
	def process_data(self, sample):
		print(self.topic_name + " data received: ", sample.get_dictionary())
		sample_dict = sample.get_dictionary()
		self.queue.put({"dds_topic_1":sample_dict})	
