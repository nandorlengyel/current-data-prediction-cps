from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def write_to_influx(measurement_name, value, time):
    token = "ON61BTEsaLZvJLq-dim2D5HB7sKobouYoivC1SCQLsiEv_116xSP8Zk_5uAsKbWrqAaADcoQBTkl5qdHCuF3xQ=="
    org = "CPS_HF"
    bucket = "MEASUREMENTS"

    client = InfluxDBClient(url="http://localhost:8086", token=token)

    point = Point(measurement_name).field("value", value).time(time)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, point)