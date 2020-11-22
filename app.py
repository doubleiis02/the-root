from flask import Flask, render_template

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

