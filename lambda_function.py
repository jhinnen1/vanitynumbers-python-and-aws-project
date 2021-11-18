import json
import boto3
import vanitynumber

#Sets up the DynamoDB table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanitynumbers_results')

def lambda_handler(event, context):
    #Receives caller's number from Amazon Connect
    inbound_number = event\
        .get("Details", {})\
        .get("ContactData", {})\
        .get("CustomerEndpoint", {})\
        .get("Address", None)
    
    #Changes format from +19995558888 to 1-999-555-8888
    def fix_phone_number():
	    x = inbound_number
	    return('{}-{}-{}-{}'.format(x[1],x[2:5],x[5:8],x[8:]))

    #Performs formatting change on caller's number
    caller_number = fix_phone_number()
    
    #Calls PyPI package and performs wordification
    vanity_numbers = vanitynumber.all_wordifications(caller_number)
    
    
    #Adds item for caller's phone number & vanity numbers in DynamoDB
    table.put_item(
        Item={
            'caller phone number': caller_number,
            'vanity numbers': vanity_numbers
        }
    )    
    
    #Attempts to send the data back to Amazon Connect
    resultMap = {"caller phone number":" ","vanity numbers":" "}
    return resultMap
    
    response = {
        'message': 'Item added'
    }
    return {
        'statusCode': 200,
        'body': response
    }