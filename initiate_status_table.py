from __future__ import print_function 
import boto3
import sys
from decimal import Decimal
from datetime import datetime 

# if len(sys.argv) == 4:
#     status_table_name = str(sys.argv[1])
#     this_node = str(sys.argv[2])
#     this_status = Decimal(sys.argv[3])
#     pic_table_name = str(sys.argv[4]) ## name of picture in table
# elif len(sys.argv) > 4:
#     status_table_name = str(sys.argv[1])
#     this_node = str(sys.argv[2])
#     this_status = Decimal(sys.argv[3])
#     pic_table_name = str(sys.argv[4]) ## name of picture in table
#     ip_address = str(sys.argv[5])
#     user = str(sys.argv[6])
#     sleep = str(sys.argv[7])
# else:
#     print("update_status_table_v2.py requires 4 or 7 arguments via the command line")
#         print("only", len(sys.argv), "argument passed") 
#     print("1: Status Table Name")
#         print("2: Device Name")
#         print("3: Status (1 or 0)")
#         print("4: IP Address")
#         print("5: Username", "\n")
#     sys.exit(0)

status_table_name = "Spots2"
this_node = "wilby"
image_name = "test.jpg"
updated = False
ip_address = "test"
sleep = 1

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(str(status_table_name))

date = datetime.strftime( datetime.now() , '%Y-%m-%d %H:%M:%S' )

table.put_item(Item={'location_id': this_node, 'image_name': image_name, 'last_updated': date, 'updated': updated, 'ip_address': ip_address,
	'sleep': sleep,}) 

print("Table status:", table.table_status)