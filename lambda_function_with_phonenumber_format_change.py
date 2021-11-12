import json
import boto3
import vanitynumber


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vanitynumbers_results')



def lambda_handler(event, context):
    inbound_number = event\
        .get("Details", {})\
        .get("ContactData", {})\
        .get("CustomerEndpoint", {})\
        .get("Address", None)
        
    def fix_phone_number():
	    x = inbound_number
	    return('{}-{}-{}-{}'.format(x[1],x[2:5],x[5:8],x[8:]))

    caller_number = fix_phone_number()
    
    vanity_numbers = vanitynumber.all_wordifications(caller_number)
    
    
    table.put_item(
        Item={
            'caller phone number': caller_number,
            'vanity numbers': vanity_numbers
        
        }
    )    
    
    resultMap = {"vanity_numbers":" "}
    return resultMap
    
    response = {
        'message': 'Item added'
    }
    return {
        'statusCode': 200,
        'body': response
    }