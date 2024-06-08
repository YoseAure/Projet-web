from flask import Flask, render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm
from werkzeug.security import check_password_hash
import os
from models import Promotion

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'enac.darties.fr')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'aurelien.collet')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'u27dPvXHAzeUPzp4')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'les_apprentis')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password, promotion_id=None, phone=None, address=None, company=None, twitter=None, instagram=None, facebook=None, github=None, promotion_name=None, promotion_year=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.promotion_id = promotion_id
        self.phone = phone
        self.address = address
        self.company = company
        self.twitter = twitter
        self.instagram = instagram
        self.facebook = facebook
        self.github = github
        self.promotion_name = promotion_name
        self.promotion_year = promotion_year


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT u.*, p.name, p.year FROM Users u LEFT JOIN Promotions p ON u.promotion_id = p.promotion_id WHERE u.user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2], user[3], user[4], user[5])
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT u.*, p.name, p.year FROM Users u LEFT JOIN Promotions p ON u.promotion_id = p.promotion_id WHERE u.email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user[4], password):
            user_obj = User(id=user[0], first_name=user[1], last_name=user[2], email=user[3], password=user[4], promotion_id=user[5])
            login_user(user_obj)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', css_file='login.css', form=form)



@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Homepage', css_file='homepage.css')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                    (form.first_name.data, form.last_name.data, form.email.data, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', css_file='register.css', form=form)


@app.route('/account')
@login_required
def account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (current_user.id,))
    user = cur.fetchone()
    prenom = user[1]
    nom = user[2]
    email = user[3]
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT phone, address, company FROM UserDetails WHERE user_id = %s", (current_user.id,))
    details = cur.fetchone()
    phone = details[0] if details and details[0] else ''
    address = details[1] if details and details[1] else ''
    company = details[2] if details and details[2] else ''
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT twitter, instagram, facebook, github FROM UserDetails WHERE user_id = %s", (current_user.id,))
    social_links = cur.fetchone()
    twitter = social_links[0] if social_links and social_links[0] else ''
    instagram = social_links[1] if social_links and social_links[1] else ''
    facebook = social_links[2] if social_links and social_links[2] else ''
    github = social_links[3] if social_links and social_links[3] else ''
    cur.close()

    return render_template('account.html',
                           title='Account Profile',
                           css_file='account.css',
                           nom=nom,
                           prenom=prenom,
                           email=email,
                           phone=phone,
                           address=address,
                           company=company,
                           twitter=twitter,
                           instagram=instagram,
                           facebook=facebook,
                           github=github)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO UserDetails (user_id, phone, address, company, twitter, instagram, facebook, github)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                phone = VALUES(phone),
                address = VALUES(address),
                company = VALUES(company),
                twitter = VALUES(twitter),
                instagram = VALUES(instagram),
                facebook = VALUES(facebook),
                github = VALUES(github)
        """, (current_user.id, form.phone.data, form.address.data, form.company.data, form.twitter.data, form.instagram.data, form.facebook.data, form.github.data))

        mysql.connection.commit()
        cur.close()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('account'))

    # Pre-fill form with current data
    cur = mysql.connection.cursor()
    cur.execute("SELECT phone, address, company, twitter, instagram, facebook, github FROM UserDetails WHERE user_id = %s", (current_user.id,))
    details = cur.fetchone()
    if details:
        form.phone.data = details[0]
        form.address.data = details[1]
        form.company.data = details[2]
        form.twitter.data = details[3]
        form.instagram.data = details[4]
        form.facebook.data = details[5]
        form.github.data = details[6]

    cur.close()

    return render_template('edit-profile.html', title='Edit Profile', css_file='edit-profile.css', form=form)


@app.route('/promotions')
@login_required
def promotions():
    promotions = Promotion.get_all_promotions(mysql)
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, p.year FROM Promotions p JOIN Users u ON u.promotion_id = p.promotion_id WHERE u.user_id = %s", (current_user.id,))
    promotion = cur.fetchone()
    cur.close()

    promotion_name = promotion[0] if promotion else "No promotion assigned"
    promotion_year = promotion[1] if promotion else "N/A"

    return render_template('promotions.html', title='Promotions', css_file='promotions.css', promotions=promotions, promotion_name=promotion_name, promotion_year=promotion_year)


@app.route('/olympiades')
@login_required
def olympiade():
    return render_template('olympiade.html', title='Olympiades', css_file='olympiades.css')


@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO UserFollowers (follower_id, followed_id) VALUES (%s, %s)",
                (current_user.id, user_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('profile', user_id=user_id))


@app.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM UserFollowers WHERE follower_id = %s AND followed_id = %s",
                (current_user.id, user_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('profile', user_id=user_id))


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()

    cur.execute("SELECT Users.user_id, Users.prenom, Users.nom FROM UserFollowers "
                "JOIN Users ON UserFollowers.followed_id = Users.user_id "
                "WHERE UserFollowers.follower_id = %s", (user_id,))
    following = cur.fetchall()

    cur.execute("SELECT Users.user_id, Users.prenom, Users.nom FROM UserFollowers "
                "JOIN Users ON UserFollowers.follower_id = Users.user_id "
                "WHERE UserFollowers.followed_id = %s", (user_id,))
    followers = cur.fetchall()

    cur.close()

    return render_template('profile.html', user=user, following=following, followers=followers)


@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    message_content = request.form.get('message')

    if receiver_id and message_content:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
            (current_user.id, receiver_id, message_content)
        )
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('messages', user_id=receiver_id))


@app.route('/old-messages')
@login_required
def old_messages():
    return render_template('old-messages.html', css_file="messages.css", title='old messages')


@app.route('/messages')
@login_required
def messages():
    user_id = current_user.id

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT user_id, first_name, last_name FROM Users WHERE user_id != %s", (user_id,))
    users = cur.fetchall()
    cur.close()

    other_user_id = request.args.get('user_id')
    messages = []
    other_user = None
    if other_user_id:
        cur = mysql.connection.cursor()

        # Récupérer les messages
        cur.execute("""
            SELECT m.sender_id, m.receiver_id, m.message, m.timestamp, u.first_name, u.last_name
            FROM Messages m
            JOIN Users u ON m.sender_id = u.user_id
            WHERE (m.sender_id = %s AND m.receiver_id = %s)
               OR (m.sender_id = %s AND m.receiver_id = %s)
            ORDER BY m.timestamp ASC
        """, (user_id, other_user_id, other_user_id, user_id))
        messages = cur.fetchall()

        # Récupérer les informations de l'autre utilisateur
        cur.execute(
            "SELECT user_id, first_name, last_name FROM Users WHERE user_id = %s", (other_user_id,))
        other_user = cur.fetchone()

        cur.close()

    return render_template(
        'messages.html',
        title='Messages',
        users=users,
        messages=messages,
        current_user_id=user_id,
        other_user_id=other_user_id,
        other_user=other_user,
        css_file='messages.css'
    )



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/awards')
def awards():
    return render_template("awards.html", title="Awards", css_file='awards.css')

@app.route('/awards23')
def awards23():
    return render_template("awards23.html", title="Awards 2023", css_file='awards23.css')

if __name__ == '__main__':
    app.run(debug=True)
