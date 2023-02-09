import json
import boto3
import botocore

from datetime import datetime, timezone

def lambda_handler(event, context):
   
    client = boto3.client('dynamodb')

    print(json.dumps(event))
    print(json.dumps(context))

    ip = "event['requestContext']['identity']['sourceIp']"
    client.put_item(TableName='visitor_count', Item={'pk':{'S':'visitor_detail'},'sk':{'S': ip}, 'last_visit_date':{'S': datetime.utcnow().isoformat()}})
    try:
        response = client.update_item(TableName='visitor_count',
            Key={'pk': {'S':'visitor_info'}, 'sk':{'S':'visitor_count'}},
            UpdateExpression="set total_visitor_count = total_visitor_count + :i",
            ExpressionAttributeValues={':i': {'N':'1'}},         
            ReturnValues='UPDATED_NEW')        
        return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "https://www.lh-resume.net",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
        "body": json.dumps({
            "visitorCount": response['Attributes']['total_visitor_count']["N"],
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
        }
    except botocore.exceptions.ClientError as err:
        print(err)      
        return {
            'statusCode': 200,
             "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "https://www.lh-resume.net",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
            'visitorCount':0
        }