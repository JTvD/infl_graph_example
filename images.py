import os
import base64
import cv2
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timezone


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

    def upload_test_imgs(self, image_path: str):
        """Scale an image down to 10% of the original size and
            Upload the images to influxDB
            Args:
                image_path: str
            Return:
                -
        """
        if image_path.endswith(".jpg") or filename.endswith(".png"):
            print(f"uploading {image_path}")
            try:
                img = cv2.imread(image_path)
                height, width = img.shape[:2]
                height = int(height * 0.1)
                width = int(width * 0.1)
                resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
                retval, buffer = cv2.imencode('.png', resized_img)
                # ori_buffer = base64.b64encode(cv2.imencode('.png', img)[1]).decode("utf-8")
                buffer = base64.b64encode(buffer).decode("utf-8")
                # Write metadata and image data to InfluxDB
                timepoint = datetime.now(timezone.utc)
                point = Point("image_data").tag("filename", filename).field("image", buffer).time(timepoint, WritePrecision.NS)
                self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


if __name__ == "__main__":
    load_dotenv()
    test_db = influxdbWrapper()
    imaging_folder = "test_images"
    for filename in os.listdir(imaging_folder):
        test_db.upload_test_imgs(imaging_folder + os.sep + filename)
