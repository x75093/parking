from __future__ import print_function 
import boto3
import sys
from decimal import Decimal
from datetime import datetime

status_table_name = "Harvard_Allston"
this_node = "Harvard_Allston_01a"
image_name = "test.jpg"
updated = False
ip_address = "test"
sleep = 1
vacancies = 0
capacity = 4
latitude = 1
longitude = 1

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(str(status_table_name))

date = datetime.strftime( datetime.now() , '%Y-%m-%d %H:%M:%S' )

table.put_item(Item={'location_id': this_node, 'image_name': image_name, 'last_updated': date, 'updated': updated, 'ip_address': ip_address,
	'sleep': sleep, 'capacity': capacity, 'vacancies': vacancies, 'latitude': latitude, 'longitude': longitude,}) 

print("Table status:", table.table_status)
