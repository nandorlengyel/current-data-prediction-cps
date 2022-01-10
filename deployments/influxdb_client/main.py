#!/usr/bin/python3
import dds_topic_0_subscriber as sub_0 
import dds_topic_1_subscriber as sub_1 

import rticonnextdds_connector as rti
import threading, queue

connector = rti.Connector("time_based_dds_app_2ParticipantLibrary::time_based_dds_app_2Participant", "/app/ParticipantDescriptor.xml")
lock = threading.RLock()

q = queue.Queue()

dds_topic_0_sub_thread = sub_0.dds_topic_0Reader("dds_topic_0", lock, connector, q)
dds_topic_0_sub_thread.start()
dds_topic_1_sub_thread = sub_1.dds_topic_1Reader("dds_topic_1", lock, connector, q)
dds_topic_1_sub_thread.start()

while True:
	pass
