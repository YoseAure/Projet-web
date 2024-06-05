from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Homepage', css_file='homepage.css')

@app.route('/login')
def login():
    return render_template('login.html', title='Login', css_file='login.css')

@app.route('/register')
def register():
    return render_template('register.html', title='Register', css_file='register.css')

@app.route('/account')
def account():
    return render_template('account.html', title='Account Profile', css_file='account.css')

@app.route('/promotions')
def promotions():
    return render_template('promotions.html', title='Promotions', css_file='promotions.css')

@app.route('/olympiades')
def olympiade():
    return render_template("olympiade.html", title="Olympiades", css_file='olympiades.css')

@app.route('/awards')
def awards():
    return render_template("awards.html", title="Awards", css_file='awards.css')

@app.route('/awards23')
def awards23():
    return render_template("awards23.html", title="Awards 2023", css_file='awards23.css')

if __name__ == '__main__':
    app.run(debug=True)