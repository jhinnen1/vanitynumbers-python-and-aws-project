import json
import boto3
import vanitynumber


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanitynumbers_results')



def lambda_handler(event, context):
    caller_number = event\
        .get("Details", {})\
        .get("ContactData", {})\
        .get("CustomerEndpoint", {})\
        .get("Address", None)
    
    vanity_numbers = vanitynumber.all_wordifications(caller_number)
    
    
    table.put_item(
        Item={
            'caller phone number': caller_number,
            'vanity numbers': vanity_numbers
        
        }
    )    
    
    resultMap = {"vanity numbers":"vanity_numbers"}
    return resultMap
    
    response = {
        'message': 'Item added'
    }
    return {
        'statusCode': 200,
        'body': response
    }