import json

def lambda_handler(event, context):
    print("hi there from lambda!")
    return {
        'statusCode': 200,
        'body': json.dumps('hi there from lambda!')
    }