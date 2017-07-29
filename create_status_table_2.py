import boto3
import sys

dynamodb = boto3.resource('dynamodb')
status_table_name = sys.argv[1]


table = dynamodb.create_table(
    TableName = str(status_table_name),
    KeySchema = [
        {
            'AttributeName': 'location_id',
            'KeyType': 'HASH'  #Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'location_id',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print("Table status:", table.table_status)
