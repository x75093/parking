import boto3
import sys
import numpy as np

dynamodb = boto3.resource('dynamodb')

active_nodes = np.array(['wilby_1', 'wilby_2'])

status_table_name = 'Spots'


for node in active_nodes:
	table = dynamodb.Table(node)
	table_status = dynamodb.Table(status_table_name)
	status_response = table_status.get_item( Key = { 'location_id' : node } ) 
	item = status_response[ 'Item' ]  
	current_pic = item[ 'image_name' ]
	current_count = item[ 'vacancies' ]
	table.put_item(Item={'picture_name': current_pic,'current_count': current_count,})

