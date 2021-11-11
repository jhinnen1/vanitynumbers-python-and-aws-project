import json
import boto3
import vanitynumber


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanitynumbers_results')

caller_number = "1-555-975-8822"
vanity_numbers = vanitynumber.all_wordifications(caller_number)

def lambda_handler(event, context):
    table.put_item(
        Item={
            'caller phone number': caller_number,
            'vanity numbers': vanity_numbers
        
        }
    )    
    response = {
        'message': 'Item added'
    }
    return {
        'statusCode': 200,
        'body': response
    }