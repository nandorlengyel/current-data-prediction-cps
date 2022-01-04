#!/usr/bin/python3
import dds_topic_0_publisher as pub_0

import rticonnextdds_connector as rti
import threading, queue
import os
from time import sleep

connector = rti.Connector("time_based_dds_app_1ParticipantLibrary::time_based_dds_app_1Participant", "ParticipantDescriptor.xml")
lock = threading.RLock()

q = queue.Queue()

dds_topic_0_pub_thread = pub_0.dds_topic_0Writer("dds_topic_0", lock, 100, connector, q)
dds_topic_0_pub_thread.start()

while True:
	pass
