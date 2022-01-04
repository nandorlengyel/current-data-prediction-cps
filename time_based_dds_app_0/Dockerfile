FROM library/ubuntu:bionic
ENV PYTHONUNBUFFERED=1
ADD ./dds_topic_1_publisher.py dds_topic_1_publisher.py
ADD ./main.py main.py
ADD ./ParticipantDescriptor.xml ParticipantDescriptor.xml
ADD ./dds_threads.py dds_threads.py
RUN apt -y update && \
    apt -y upgrade && \
    apt -y install python3-pip && \
    pip3 install rticonnextdds_connector && \
    chmod +x ./*.py
CMD ["./main.py"]		
