from dds_threads import WriterThread

class dds_topic_1Writer(WriterThread):
	def produce_data(self, output):
	
		# IMPORTANT: Implement logic here, i.e.:
		
		# if self.queue.qsize() >= 2:
		#	print("cache: ", self.cache)							
		#	output.instance.set_dictionary({"x":1,  "y":2})
		# 	print(self.topic_name + " data sent")
		# 	output.write()
