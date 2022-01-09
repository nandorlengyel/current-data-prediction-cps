from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

def write_to_influx(measurement_name, value, time):
    bucket = "MEASUREMENTS"
    client = InfluxDBClient.from_env_properties()

    point = Point(measurement_name).field("value", value).time(time)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, point)