import boto3
import numpy as np
import requests
import json
import time
import os
from datetime import datetime

class CarCounterClient(object):

    def __init__(self):
        self.bucket_name = "parking-spots"
        self.s3_client = boto3.client('s3')
        self.dynamodb_client = boto3.resource('dynamodb')
        self.car_counter_url = "http://52.207.57.85/count-cars"
        self.tables = { "Spots": self.dynamodb_client.Table("Spots") }

    def fetch_next(self):
        #print "Fetching next spot to update ..."
        spots = self.tables["Spots"].scan()["Items"]
        spot_choice = spots[np.random.choice(len(spots))]
        return spot_choice if spot_choice["updated"] == True else self.fetch_next()

    def download_image(self, image_path, save_as_name = None):
        print "Downloading image: ", image_path, " ..."
        save_as_name = image_path if save_as_name is None else save_as_name
        self.s3_client.download_file(self.bucket_name, image_path, save_as_name)

    def count_cars(self, image_path):
        print "Counting cars ..."
        response = json.loads(requests.post(self.car_counter_url, files={"image": open(image_path, "rb")}).text)
        print response
        return response["car_count"]

    def update_spot(self, location_id, car_count):
        print "Updating spot ...."
        print spot
        update_time = str(str(datetime.strftime( datetime.now() , '%Y-%m-%d %H:%M:%S' )))
        self.tables["Spots"].update_item(
            Key={ 'location_id': location_id },
            UpdateExpression="set vacancies = :v, updated=:u, last_updated=:t",
            ExpressionAttributeValues={
                ':v': car_count,
                ':u': False,
                ':t': update_time
            },
            ReturnValues="UPDATED_NEW"
        )

    def cleanup(self, image_path):
        print "Removing image: ", image_path, " ..."
        os.remove(image_path)
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=image_path)


client = CarCounterClient()
spot = client.fetch_next()
client.download_image(spot["image_name"])
client.update_spot(spot["location_id"], client.count_cars(spot["image_name"]))
client.cleanup(spot["image_name"])
