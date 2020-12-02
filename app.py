from flask import Flask, render_template, request, flash
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import random
import string
import pymongo
import boto3

app = Flask(__name__)
app.secret_key="super secret key"

dynamodb = boto3.resource('dynamodb', aws_access_key_id="", aws_secret_access_key="", region_name='us-east-1')
from boto3.dynamodb.conditions import Key, Attr



current_classes = ["English 1B", "English 1C", "English 1D", "English 1E"]

class Classes:
    def __init__(self, name, bg, blobfill):
        self.name = name
        self.bg = bg
        self.blobfill = blobfill

class_list = [Classes('English 1B', '#64dfd4', '#83D4CD'), Classes('English 1C', '#9ed34e', '#9EC95D'),
                Classes('English 1D', '#3fb9d8', '#56B0D2'), Classes('English 1E', '#83b969', '#7EB671')]

@app.route('/')
def signin():
    return render_template('signup.html')

@app.route('/home')
def index():
    return render_template('index.html', current_classes=current_classes, class_list=class_list)

@app.route('/about')
def about():
    print("This is the about page")
    return "<a href='/home'> Return to homepage </a>"

if __name__== '__main__':
    app.run(debug=True)



# ---------------------------------------------------------------------



# adds a new class to the list of classes in index.html
@app.route('/add_class', methods = ['POST', 'GET'])
def add_class():
    if request.method == 'POST':
        name = request.form['class-name-input']
        primary_color = request.form['pri-class-color-input']
        secondary_color = request.form['sec-class-color-input']
    else:
        name = request.args.get('class-name-input')
        primary_color = request.args.get('pri-class-color-input')
        secondary_color = request.args.get('sec-class-color-input')
    new = Classes(name, primary_color, secondary_color)
    class_list.append(new)
    print(class_list)
    return render_template('index.html', class_list=class_list)

@app.route('/add_class_page')
def add_class_page():
    return render_template('addClass.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name-input']
        email = request.form['email-input']
        password = request.form['password-input']
        
        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password
            }
        )

        return render_template('login.html')
    return render_template('signup.html')

@app.route('/login')
def login():    
    return render_template('login.html')


@app.route('/check', methods=['POST'])
def check():
    if request.method=='POST':
        
        email = request.form['email-input']
        password = request.form['password-input']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        print("HELLO")
        print(response)
        items = response['Items']
        if not items:
            msg = "Login Unsuccessful. Double check your information"
            return render_template("login.html", msg = msg)
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            return render_template("index.html", name = name, current_classes=current_classes, class_list=class_list)
    return render_template("login.html")

# a dictionary that keeps track of every survey ever created
# key: the code
# value: a list of size 3, index 0 = the lesson name, index 1 = the survey question, and index 2 = list of student responses
surveys = {}


# the user clicks on a class icon -> moves to createSurvey.html
@app.route('/add_survey', methods = ['GET'])
def add_survey():
    lesson = request.args.get('lessonName')
    return render_template('createSurvey.html', lessonName=lesson)

# the user is at createSurvey.html and then submits a form -> moves to newly created lesson.html
@app.route("/create_survey", methods=['GET', 'POST'])
def create_survey():
    q = request.form['survey-question']
    lesson = request.args.get('lesson')
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    surveys[code] = [lesson, q, []]
    return render_template('lesson.html', code=code, lessonName=lesson, question=q)

# link to the code inputting page for students
@app.route("/goto_code_page")
def goto_code_page():
    return render_template('code.html')

# student is at the code.html and inputs code for the survey -> moves to survey.html
@app.route("/enter_code", methods=['GET', 'POST'])
def enter_code():
    code = request.form['code']
    return render_template('survey.html', code=code, lessonName=surveys[code][0], question=surveys[code][1])

# student submits their response in survey.html -> moves to submitted.html
@app.route("/add_response", methods=['GET', 'POST'])
def add_response():
    response = request.form['feedback']
    code = request.args.get('lessonCode')
    surveys[code][2].append(response)
    print(surveys)
    return render_template('submitted.html')
    




# ---------------------------------------------------------------------




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

    account_sid = "ACCOUNT-SID"
    auth_token = "AUTH-TOKEN"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="TWILIO-NUMBER", # This is the number that the message will be sent to. Change it to your phone number to test it out
        from_="RECEIVER-NUMBER,
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


