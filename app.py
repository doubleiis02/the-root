from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


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