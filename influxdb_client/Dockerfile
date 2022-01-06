FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV NDDS_DISCOVERY_PEERS="rtps@rti-cloud-discovery.default:7400"
COPY . /app
RUN chmod +x /app/*.py
RUN pip install -r /app/requirements.txt
RUN apt-get update
ENTRYPOINT ["python"]
CMD ["/app/main.py"]	
