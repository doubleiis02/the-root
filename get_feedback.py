# for a user, to get all feedback for a pecific lesson 
from boto3.dynamodb.conditions import Key, Attr
import boto3
import NLP.nlp_algorithms as nlp

dynamodb = boto3.resource('dynamodb', 
                        aws_access_key_id="AKIAQMIVM4QIASTAN2G4", aws_secret_access_key="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", region_name='us-east-1')
table = dynamodb.Table('lessons')

# response will be a dic satisfying the 2 criteria 
response = table.get_item(
    Key={
        'email' : "@gmail.com",
        'code'  : ""
    }
)


# will print the dict containg all info 
# getting all feedbacks for the specific survey 
allfeedback_string = ""
allfeedback_list   = []
feedback           = response['Item']["feedback"]
print(feedback)
for ele in feedback:
    allfeedback_string += ele + " "
    allfeedback_list.append(ele)

recommend = nlp.getRecommendation(allfeedback_list)

print(recommend)