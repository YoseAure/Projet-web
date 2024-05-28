from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Homepage')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')

@app.route('/account')
def account():
    return render_template('account.html', title='Account Profile')

@app.route('/promotions')
def promotions():
    return render_template('promotions.html', title='Promotions')

@app.route('/olympiades')
def olympiade():
    return render_template("olympiade.html")

if __name__ == '__main__':
    app.run(debug=True)