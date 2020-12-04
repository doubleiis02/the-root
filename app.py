from flask import Flask, render_template, request, redirect, url_for, flash, session
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
client = boto3.client('dynamodb', aws_access_key_id="", aws_secret_access_key="", region_name='us-east-1')
from boto3.dynamodb.conditions import Key, Attr


class Classes:
    def __init__(self, name, bg, blobfill):
        self.name = name
        self.bg = bg
        self.blobfill = blobfill

#class_list = [Classes('English 1A', '#67d7ce', '#b5faf6'), Classes('English 1B', '#91cc49', '#d2f68b'),
#                Classes('English 1C', '#2cb2d6', '#71e9fa'), Classes('English 1D', '#7cb36e', '#b8ebac')]
# Getting email of the teacher
""" if 'email' in session:
    email = session['email']

class_table = dynamodb.Table('classes')
response = class_table.query(
        KeyConditionExpression=Key('email').eq(email)
)
classes = response['Items']
class_list = []
for _classes in classes:
    class_list.append(Classes(_classes['class'], _classes['primary_color'], _classes['secondary_color'])) """



class Lesson:
    def __init__(self, name, className, bg, blobfill, code, questions, responses):
        self.name = name
        self.className = className
        self.bg = bg
        self.blobfill = blobfill
        self.code = code
        self.questions = questions
        self.responses = responses

lesson_list = [
    Lesson('Week 1', 'English 1A', '#67d7ce', '#b5faf6', 'abcde', ["How did you like the class?", "Any suggestions?"], [["Great", "nope"], ["Amazing", "no"]]),
    Lesson('Week 1', 'English 1B', '#91cc49', '#d2f68b', 'fghijk', ["How do you feel about the class?", "How can the class be improved?"], [["It's alright", "idk"], ["Great!", "less homework"]])
]

lesson_list = [] # Create empty lesson list

class_list = [] # Create empty class list


@app.route('/')
def signin():
    return render_template('signup.html')

@app.route('/home')
def index():
    if 'name' in session:
        name = session['name']
    if 'email' in session:
        email = session['email']
    return render_template('index.html', class_list=class_list, name=name)

""" class_table = dynamodb.Table('classes')
    response = class_table.query(
           KeyConditionExpression=Key('email').eq(email)
    )
    classes = response['Items']
    for _classes in classes:
        class_list.append(Classes(_classes['class'], _classes['primary_color'], _classes['secondary_color'])) """
    
if __name__== '__main__':
    app.run(debug=True)



# ---------------------------------------------------------------------

# user clicks on '+' add class button in index.html -> move to addClass.html
@app.route('/add_class_page')
def add_class_page():
    return render_template('addClass.html')

# adds a new class to the list of classes in index.html
@app.route('/add_class', methods = ['POST', 'GET'])
def add_class():
    # getting data from form
    name = request.form['class-name-input']
    primary_color = request.form['pri-class-color-input']
    secondary_color = request.form['sec-class-color-input']

    # insertion into table
    table = dynamodb.Table('classes')
    if 'email' in session:
        email = session['email']
    table.put_item(
        Item={
            'class': name,
            'primary_color': primary_color,
            'secondary_color': secondary_color,
            'email': email
        }
    )
    class_list.append(Classes(name, primary_color, secondary_color)) 
    return redirect(url_for('index', class_list=class_list))

# user clicks on a class icon in index.html -> moves to that class's dashboard
@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        name = session['name']
    className = request.args.get('className')
    color = request.args.get('color')
    #------------------ newly added: passing survey responses into aws comprehend
	# getting all lesson code and feedbacks for a user
    if 'email' in session:
        email = session['email']

    # Get the latest code from the class code, and then pull that data for the feedback displayed
    table = dynamodb.Table('classes')
    response = table.get_item(
        Key={
            'email': email,
            'class': className
        }
    )
    print(response)
    items = response['Item']
    print(items)
    if 'latest_code' in items:        
        latest_code = items['latest_code'][0]
        print(latest_code)
        # Now that we have the latest code, we can pass the feedback into the algorithm
        # get the feedback given the latest code
        table = dynamodb.Table('lessons')
        response = table.get_item(
        Key={
            'email': email,
            'code': latest_code
        }
        ) 
        items = response['Item']
        feedback = items['feedback'] # this is the feedback of the latest code. Will throw this into NLP algorithm
        return render_template('dashboard.html', className=className, color=color, name=name, latestcode=latest_code)
    else:
        # Probably display error message if code is null
        latest_code = "NULL"
        return render_template('dashboard.html', className=className, color=color, name=name, latestcode=latest_code)


    # getting all feedbacks for one survey and pass into the nlp
"""     for res in response: 
        allfeedback_string = ""
        allfeedback_list   = []
        myitems  = res.items() 
        mylist   = list(myitems)
        code     = mylist[1][1]
        feedback = mylist[2][1]
        for ele in feedback:
            myitems      = ele.items() 
            mylist       = list(myitems)
            eachfeedback = mylist[0][1]
            allfeedback_string += eachfeedback
            allfeedback_list.append(eachfeedback) """
        # now for each code, we have all its feedback, will pass into the nlp
    #print(allfeedback_list) 

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
    # Reset class login to empty so that its not stored if you log out and then login
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
        session['name'] = name
        session['email'] = email
        print(items[0]['password'])
        if password == items[0]['password']:
            # Get classes for that teacher
            class_table = dynamodb.Table('classes')
            response = class_table.query(
                KeyConditionExpression=Key('email').eq(email)
            )
            classes = response['Items']
            if not class_list:
                for _classes in classes:
                    class_list.append(Classes(_classes['class'], _classes['primary_color'], _classes['secondary_color']))
            # Get lessons for that teacher
            lesson_table = dynamodb.Table('lessons')
            response = lesson_table.query(
                KeyConditionExpression=Key('email').eq(email)
            )
            lessons = response['Items']
            print(lessons)
            if lessons: # check if list is empty, skip this if it is
                if not lesson_list:
                    for _lessons in lessons:
                        lesson_list.append(Lesson(_lessons['lesson_name'], _lessons['class_name'], "#67d7ce","#b5faf6",_lessons['code'],_lessons['question'], _lessons['feedback']))
            
            # Return the home page with the teacher name, and classes
            return render_template("index.html", name = name, class_list=class_list)
    return render_template("login.html")

# ---------------------------------------------------------------------


# a dictionary that keeps track of every survey ever created
# key: the code
# value: a list of size 3, index 0 = the lesson name, index 1 = the survey question, and index 2 = list of student responses

@app.route('/lessons')
def lessons():
    return render_template('lessonList.html', lesson_list=lesson_list)

@app.route('/add_survey', methods = ['GET', 'POST'])
def add_survey():
    className = request.args.get('className')
    return render_template('createSurvey.html', className=className)

# the user is at createSurvey.html and then submits a form -> moves to newly created lesson.html
@app.route("/create_survey", methods=['GET', 'POST'])
def create_survey():
    q = request.form['survey-question']
    lesson = request.form['survey-title']
    className = request.args.get('className')
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    # add code to database
    if 'email' in session: # grab email from session
        email = session['email']
    table = dynamodb.Table('lessons')
    feedback = []
    table.put_item(
        Item={
            'email': email,
            'code': code, # add the class name later 
            'question': q,
            'feedback': feedback,
            'class': className,
            'lesson_name': lesson,
            'class_name': className
        }
    )
    lesson_list.append(Lesson(lesson, className, "#67d7ce","#b5faf6", code, q, feedback))
    table = dynamodb.Table('classes')
    result = table.update_item(
        Key={
            'email': email,
            'class': className
        },
        UpdateExpression="SET latest_code = :i",
        ExpressionAttributeValues={
            ':i': [code],
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return render_template('lesson.html', code=code, lessonName=lesson, question=q)

# link to the code inputting page for students
@app.route("/goto_code_page")
def goto_code_page():
    return render_template('code.html')

# student is at the code.html and inputs code for the survey -> moves to survey.html
@app.route("/enter_code", methods=['GET', 'POST'])
def enter_code():
    code = request.form['code']
    # So the code is from the form, but the lesson name and the question should be from the database
    # Get lessonName and question from database
    table = dynamodb.Table('lessons')
    response = table.scan(
        FilterExpression=Attr('code').eq(code)
    ) 
    items = response['Items']
    lessonName = items[0]['lesson_name']
    question = items[0]['question']
    #print(items)
    #print(lessonName)
    #print(question)
    return render_template('survey.html', code=code, lessonName=lessonName, question=question)

# student submits their response in survey.html -> moves to submitted.html
@app.route("/add_response", methods=['GET', 'POST'])
def add_response():
    response = request.form['feedback']
    code = request.args.get('lessonCode')

    # add response to the list attribute of the correct lesson
    if 'email' in session: # grab email from session
        email = session['email']
    table = dynamodb.Table('lessons')
    result = table.update_item(
        Key={
            'email': email,
            'code': code
        },
        UpdateExpression="SET feedback = list_append(feedback, :i)",
        ExpressionAttributeValues={
            ':i': [response],
        },
        ReturnValues="UPDATED_NEW"
    )

    # --------------------------
    #surveys[code][2].append(response)
    #print(surveys)
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

    client.messages.create(
        to="TWILIO-NUMBER", # This is the number that the message will be sent to. Change it to your phone number to test it out
        from_="RECEIVER-NUMBER",
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


