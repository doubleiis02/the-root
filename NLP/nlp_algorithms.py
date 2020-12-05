
# needed packages
import boto3
import json
import pandas as pd
from numpy import random
from collections import Counter

# Setting up test data and comprehend client
comprehend = boto3.client('comprehend', 
                       aws_access_key_id="", aws_secret_access_key="", region_name='us-east-1')
                       
text = "If you like to have a custom sentiment analyzer for your domain, it is possible to train a classifier using flair using your dataset. The drawback of using a flair pre-trained model for sentiment analysis is that it is trained on IMDB data and this model might not generalize well on data from other domains like twitter."
text2 = "I am confused about the pythagorean theorem. I don't understand the "
responses = ["I don\'t understand the pythagorean theorem.",
             "I was confused by the calculation of right triangles.",
             "I liked the way you explained scalene angles.",
             "I keep getting the wrong answer when using the pythagorean theorem."]

# Helper functions

# Detecting key phrases
# Takes in a string and returns a list of all key phrases
def keyphrase(text):
    # Extract the key phrases
    key_phrases = comprehend.detect_key_phrases(Text=text, LanguageCode='en')

    kp = []
    # Parse through and extract the key phrases detected
    for i in key_phrases['KeyPhrases']:
        kp.append(i['Text'])
    return kp

# print(keyphrase(text2))

# Sentiment
# Takes in a string and returns a value (-1, 0, 1) denoting the overall sentiment
def feedbackSent(text):
    # Determine sentiment
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    # Return -1 for negative, 0 for neutral, 1 for positive
    if sentiment['Sentiment'] == 'POSITIVE':
        return 1
    elif sentiment['Sentiment'] == 'NEUTRAL':
        return 0
    else:
        return -1
    
# Providing recommendations
# Takes in a list of all student responses
# Returns a recommendations
def getRecommendation(feedback):

    # Pick out negative sentiment responses
    neg_feedback = []
    for i in feedback:
        if feedbackSent(i) == -1:
            neg_feedback.append(i)

    # Identify key phrases from neg_feedback
    neg_kp = []
    for i in neg_feedback:
        neg_kp.extend(keyphrase(i))
    
    # Identify and sort by most repeated key phrases in student feedback
    counts = Counter(neg_kp)
    repeated_kp = counts.most_common()
    print(repeated_kp)
    print(len(repeated_kp))
    # Hard coded random templates for recommendations
    templates = ['Review ',
                 'Consider focusing on ',
                 'Your students want more instruction on ',
                 'Your class is confused about ',
                 'Spend more time going over ']

    # Generate recommendations
    recommendation = []
    if (len(repeated_kp) < 3):
        for i in range(len(repeated_kp)):
            recommendation.append(templates[random.randint(1,len(templates))]+str.strip(repeated_kp[i][0])+'.')
    else:
        for i in range(3):
            recommendation.append(templates[random.randint(1,len(templates))]+str.strip(repeated_kp[i][0])+'.')
    return recommendation

# print(getRecommendation(responses))

# pctNegative function returns total % of students that responded negatively to survey
# Takes in a list of all responses
# Returns a float value rounded to 2 decimal places denoting % of students that responded negatively
def pctNegative(responses):
    
    # Determine sentiment
    numNeg = 0
    for i in responses:
        if feedbackSent(i) == -1:
            numNeg+=1
    
    return round(float(numNeg)/len(responses), 2)

#print(pctNegative(responses))