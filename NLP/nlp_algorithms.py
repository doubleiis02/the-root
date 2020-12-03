
# needed packages
import boto3
import json
import pandas as pd
import random

# aws attempts

comprehend = boto3.client('comprehend', aws_access_key_id="", aws_secret_access_key="", region_name='us-east-1')
text = "If you like to have a custom sentiment analyzer for your domain, it is possible to train a classifier using flair using your dataset. The drawback of using a flair pre-trained model for sentiment analysis is that it is trained on IMDB data and this model might not generalize well on data from other domains like twitter."
text2 = "I am confused about the pythagorean theorem. I don't understand the "

# Detecting key phrases
def keyphrase(text):
    # Extract the key phrases
    key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')

    kp = []
    # Parse through and extract the key phrases detected
    for i in key_phrases['KeyPhrases']:
        kp.append(i['Text'])

    # 
    pd.DataFrame(kp.value_counts())

keyphrase(text)

# Sentiment
def feedbackSent(text):
    # Determine sentiment
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    # Return -1 for negative, 0 for neutral, 1 for positive
    if max(sentiment['SentimentScore']) == 'Positive':
        return 1
    elif max(sentiment['SentimentScore']) == 'Neutral':
        return 0
    else:
        return -1
    
# Detecting sentiment
sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')


# Providing recommendations
# For each response, determine pos/negative sentiment
# Identify key phrases
# Random number generator
# Returns recommendation(s)
# feedback is a list of all the recommendations
def getRecommendation(feedback):

    # sentiment
    neg_feedback = []
    for i in feedback:
        if feedbackSent == 'Negative':
            neg_feedback.append(i)

    # identify key phrases from neg_feedback


    # random number generator
    templates = ['Review ',
                 'Consider focusing on ',
                 'Your students want more instruction on ']
    
    recommendation = templates[random.randInt(1,3)]
    