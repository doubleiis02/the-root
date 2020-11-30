import boto3
import json

comprehend = boto3.client('comprehend', aws_access_key_id="AKIAIXIDPQMROWFOJLZQ", aws_secret_access_key="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", region_name='us-east-1')

                
text = "I don't understand the pythagorean theorem."

print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')