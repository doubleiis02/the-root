from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

current_classes = ["English 1B", "English 1C", "English 1D", "English 1E"]

class Classes:
    def __init__(self, name, bg, blobfill):
        self.name = name
        self.bg = bg
        self.blobfill = blobfill

class_list = [Classes('English 1B', '#64dfd4', '#83D4CD'), Classes('English 1C', '#9ed34e', '#9EC95D'),
                Classes('English 1D', '#3fb9d8', '#56B0D2'), Classes('English 1E', '#83b969', '#7EB671')]

# class_list = [Classes('Science', '#000000', '#cc6464')]

@app.route('/')
def index():
    return render_template('index.html', current_classes=current_classes, class_list=class_list)


@app.route('/about')
def about():
    print("This is the about page")
    return "<a href='/'> Return to homepage </a>"

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