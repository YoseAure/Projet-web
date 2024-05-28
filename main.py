from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hello, World!"

@app.route('/olympiades')
def olympiade():
    return render_template("olympiade.html")

if __name__ == '__main__':
    app.run(debug=True)

