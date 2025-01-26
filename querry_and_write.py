from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
from dotenv import load_dotenv
from os import getenv


class influxdbWrapper():
    """Wrapper arund the influxDB API """
    def __init__(self):
        """Initialize the database connection
            Args:
                -
            Return:
                -
        """
        self.client = InfluxDBClient(url=getenv('INFLUXDB_URL'),
                                     token=getenv('INFLUXDB_TOKEN'),
                                     org=getenv('INFLUXDB_ORG'))
        self.bucket = getenv('INFLUXDB_BUCKET')
        self.org = getenv('INFLUXDB_ORG')
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def retreive_lastvalue(self, meassurement: str):
        """Retreive the last value writing to a specific caption from the influx database
            Args:
                meassurement: str
                caption: str
            Return:
                InfluxDB points
        """
        query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: -2h, stop: now())
            |> filter(fn: (r) => r._measurement == "{meassurement}")
            |> last()
            '''
        result = self.client.query_api().query(query)

        # Extract points from the result
        points = []
        for table in result:
            for record in table.records:
                points.append(record.values)
        return points

    def example_query(self):
        """Example query to the influx database that returns all values written in the last hours
            Args:
                -
            Return:
                InfluxDB TableList
        """
        # Use a query API to execute the query
        query_api = self.client.query_api()
        query = f'from(bucket: "{self.bucket}") |> range(start: -2h) |> last()'

        # Execute the query
        result = query_api.query(query)
        return result

    def write_value(self, meassurement: str, tagkey: str, tagvalue: str,
                    fieldname: str, value: float, timestamp: datetime) -> None:
        """Write alarm status update to influx database
            Args:
                meassurement: str
                tagkey: str
                tagvalue: str
                fieldname: str
                value: float
                    actual value
                timestamp: datetime
                    Moment on which the change was detected
            Return:
                -
        """
        point = (
            Point(meassurement)
            .tag(tagkey, tagvalue)
            .field(fieldname, value)
            .time(timestamp)
                )
        # Writing a list of points at once is also supported
        self.write_api.write(bucket=self.bucket,
                             org=self.org,
                             record=point)


if __name__ == "__main__":
    load_dotenv()
    test_db = influxdbWrapper()
    test_db.write_value('meas1', 'tag1', 'temp', 'sensor1', 20.0,
                        timestamp=datetime.now(timezone.utc))
    reply = test_db.retreive_lastvalue('meas1')
    print(reply)
