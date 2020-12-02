import boto3
dynamodb = boto3.client('dynamodb', aws_access_key_id="AKIAQMIVM4QIASTAN2G4", aws_secret_access_key="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", region_name='us-east-2')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')

# Print out some data about the table.
print(table.item_count)