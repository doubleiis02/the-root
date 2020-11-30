from flask import Flask, render_template, request
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('code.html')


@app.route('/about')
def about():
    print("This is the about page")
    return "Welcome to the about page"

if __name__== '__main__':
    app.run(debug=True)

classes = ["class 1", "class 2"]
@app.route('/add_class', methods = ['POST', 'GET'])
def add_class():
    if request.method == 'POST':
        name = request.form['class-name-input']
    else:
        name = request.args.get('class-name-input')
    classes.append(name)
    print(classes)
    return render_template('index.html')

surveys = {"abcdef" : ["Science", "How did you feel about today's lesson?"]}

@app.route("/create_survey", methods=['GET', 'POST'])
def create_survey():
    if request.method == 'POST':
        q = request.form['survey-question']
        lesson = request.form['lesson']
    else:
        q = request.args.get('survey-question')
        lesson = request.form['lesson']
        
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    surveys[code] = [lesson, q]
    return "created survey"

@app.route("/enter_code", methods=['GET', 'POST'])
def enter_code():
    if request.method == 'POST':
        code = request.form['code']
    else:
        code = request.args.get('code')
    return render_template('survey.html', lessonName=surveys[code][0], question=surveys[code][1])

responseList = []

@app.route("/add_response", methods=['GET', 'POST'])
def add_response():
    if request.method == 'POST':
        response = request.form['feedback']
    else:
        response = request.args.get('feedback')
    responseList.append(response)
    print(responseList)
    return render_template('submitted.html')
    









@app.route("/send_sms", methods=['GET', 'POST'])
def send_sms():

    if request.method == 'POST':
        msg = request.form['survey-question']
    else:
        msg = request.args.get('survey-question')

    # account_sid, auth_token, and from_ values are from your free twilio account
    # for security reasons, I (Jiin) can't leave my account sid, auth token, and twilio number on here :( So you'll have to make your own free twilio account. It's super simple to do: 
        # 1. create an account here: https://www.twilio.com/try-twilio?_ga=2.182390127.916037802.1606343073-1380573367.1606343073
        # 2. Find the account SID and auth token here and generate a Twilio phone number here as well: https://www.twilio.com/console
    # after testing, make sure you remove any info related to your account before pushing to the repo

    account_sid = "ACac37375f5a3dfe6441f409bca3991a65"
    auth_token = "9c2286b24b2a3d15c9f39130298d5aa9"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+19496079673", # This is the number that the message will be sent to. Change it to your phone number to test it out
        from_="+12184266434",
        body=msg
    )

    # message_body = request.values.get('Body', None)
    # resp = MessagingResponse()
    # resp.message("thanks!")
    # print(message_body)

    return render_template('createSurvey.html')


@app.route("/respond_sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    message_body = request.values.get('Body', None)

    resp = MessagingResponse()
    resp.message("thanks!")
    print(message_body)

    return str(resp)
