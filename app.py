from flask import Flask, render_template, request, flash
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
