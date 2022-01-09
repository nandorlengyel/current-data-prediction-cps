from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

def write_to_influx(measurement_name, value, time):
    bucket = "MEASUREMENTS"

    client = InfluxDBClient(url=os.environ['INFLUXDB_V2_URL'], token=os.environ['INFLUXDB_V2_TOKEN'], debug=True)
    #client = InfluxDBClient(url="http://influxdb-service:8086", token="5NQRQj1ZrNiCMlrg2WQpxn23DYtvkiYptwqdPGBKix9z5zKeuS01HzZP-BaYJzkhXNXEr4WsKmPGx1QpteosPw==", org="CPS_HF", debug=True)   
    #client = InfluxDBClient.from_env_properties()

    point = Point(measurement_name).field("value", value).time(time)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    print(write_api.write(bucket, os.environ['INFLUXDB_V2_ORG'] , point)) 