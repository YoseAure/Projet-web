from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm
from models import User, load_user, get_all_promotions
from config import app, mysql, bcrypt, login_manager


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = RegistrationForm()
    promotions = get_all_promotions()
    print(promotions)

    if form.validate_on_submit():
        first_name = form.first_name.data.strip().title()
        last_name = form.last_name.data.strip().title()
        email = form.email.data.strip()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        promotion_id = int(request.form.get('annee'))
        print(promotion_id)
        print(type(promotion_id))

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Users (first_name, last_name, email, password, promotion_id) VALUES (%s, %s, %s, %s, %s)",
                        (first_name, last_name, email, hashed_password, promotion_id))
            mysql.connection.commit()
            cur.close()
            flash('Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print('ici')
            flash(f'Erreur lors de la création de votre compte: {e}', 'danger')
            mysql.connection.rollback()

    return render_template('register.html', title='Inscription', css_file='register.css', form=form, promotions=promotions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user[4], password):
            user_obj = User(id=user[0], first_name=user[1],
                            last_name=user[2], email=user[3], password=user[4], promotion_id=user[5])
            login_user(user_obj)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Erreur de connexion. Veuillez vérifier votre email et mot de passe.', 'danger')
    return render_template('login.html', title='Connexion', css_file='login.css', form=form)


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Homepage', css_file='homepage.css')


@app.route('/account', defaults={'user_id': None})
@app.route('/account/<int:user_id>')
@login_required
def account(user_id):
    # Si aucun user_id n'est fourni, afficher le profil de l'utilisateur actuel
    if user_id is None:
        user_id = current_user.id

    # Obtenir les détails de l'utilisateur à afficher
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('promotions'))

    prenom, nom, email = user[1], user[2], user[3]
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM UserDetails WHERE user_id = %s", (user_id,))
    details = cur.fetchone()
    phone = details[1] if details and details[1] else ''
    address = details[2] if details and details[2] else ''
    ville = details[3] if details and details[3] else ''
    code_postal = details[4] if details and details[4] else None
    pays = details[5] if details and details[5] else ''
    company = details[6] if details and details[6] else ''
    twitter = details[7] if details and details[7] else ''
    instagram = details[8] if details and details[8] else ''
    facebook = details[9] if details and details[9] else ''
    github = details[10] if details and details[10] else ''
    cur.close()

    is_current_user = (user_id == current_user.id)

    return render_template('account.html',
                           title='Account Profile',
                           css_file='account.css',
                           nom=nom,
                           prenom=prenom,
                           email=email,
                           phone=phone,
                           address=address,
                           ville=ville,
                           code_postal=code_postal,
                           pays=pays,
                           company=company,
                           twitter=twitter,
                           instagram=instagram,
                           facebook=facebook,
                           github=github,
                           is_current_user=is_current_user)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()

        phone = form.phone.data.strip() or None
        address = form.address.data.strip() or None
        city = form.city.data.strip() or None
        postal_code = form.postal_code.data or None
        country = form.country.data.strip() or None
        company = form.company.data.strip() or None
        twitter = form.twitter.data.strip() or None
        instagram = form.instagram.data.strip() or None
        facebook = form.facebook.data.strip() or None
        github = form.github.data.strip() or None

        try:
            cur.execute("""
                INSERT INTO UserDetails (user_id, phone, address, ville, code_postal, pays, company, twitter, instagram, facebook, github)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    phone = VALUES(phone),
                    address = VALUES(address),
                    ville = VALUES(ville),
                    code_postal = VALUES(code_postal),
                    pays = VALUES(pays),
                    company = VALUES(company),
                    twitter = VALUES(twitter),
                    instagram = VALUES(instagram),
                    facebook = VALUES(facebook),
                    github = VALUES(github)
            """, (current_user.id,
                  phone,
                  address,
                  city,
                  postal_code,
                  country,
                  company,
                  twitter,
                  instagram,
                  facebook,
                  github))
            mysql.connection.commit()
            flash('Your profile has been updated!', 'success')
        except Exception as e:
            flash(
                f'Erreur lors de la mise à jour de votre profil : {e}', 'danger')
            mysql.connection.rollback()
        finally:
            cur.close()

        return redirect(url_for('account', user_id=current_user.id))

    # Pre-fill form with current data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM UserDetails WHERE user_id = %s",
                (current_user.id,))
    details = cur.fetchone()
    if details:
        form.phone.data = details[1]
        form.address.data = details[2]
        form.city.data = details[3]
        form.postal_code.data = details[4]
        form.country.data = details[5]
        form.company.data = details[6]
        form.twitter.data = details[7]
        form.instagram.data = details[8]
        form.facebook.data = details[9]
        form.github.data = details[10]
    cur.close()

    return render_template('edit-profile.html', title='Edit Profile', css_file='edit-profile.css', form=form)


@app.route('/promotions', methods=['GET', 'POST'])
@login_required
def promotions():
    cur = mysql.connection.cursor()

    # Récupération de toutes les promotions
    cur.execute("""
        SELECT p.promotion_id, p.year, p.name, COUNT(u.user_id) as user_count
        FROM Promotions p
        LEFT JOIN Users u ON p.promotion_id = u.promotion_id
        GROUP BY p.promotion_id, p.year, p.name
        ORDER BY p.year DESC""")
    promotions = cur.fetchall()

    cur.execute("SELECT p.name FROM Promotions p JOIN Users u ON u.promotion_id = p.promotion_id WHERE u.user_id = %s", (current_user.id,))
    promotion_name = cur.fetchone()[0]
    cur.execute("SELECT u.user_id, u.first_name, u.last_name FROM Users u WHERE u.promotion_id = %s", (current_user.promotion_id,))
    users = []
    users = cur.fetchall()


    selected_promotion_id = request.form.get('promotion_id')
    if selected_promotion_id:
        cur.execute("SELECT u.user_id, u.first_name, u.last_name FROM Users u WHERE u.promotion_id = %s", (selected_promotion_id,))
        users = cur.fetchall()
        cur.execute("SELECT name FROM Promotions WHERE promotion_id = %s", (selected_promotion_id,))
        promotion_name = cur.fetchone()[0]

    cur.close()

    return render_template('promotions.html', title='Promotions', css_file='promotions.css',
                           promotions=promotions, promotion_name=promotion_name, users=users)


# @app.route('/promotions')
# @login_required
# def promotions():
#     promotions = Promotion.get_all_promotions(mysql)
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT p.name, p.year FROM Promotions p JOIN Users u ON u.promotion_id = p.promotion_id WHERE u.user_id = %s", (current_user.id,))
#     promotion = cur.fetchone()
#     cur.close()

#     promotion_name = promotion[0] if promotion else "No promotion assigned"
#     promotion_year = promotion[1] if promotion else "N/A"

#     return render_template('promotions.html', title='Promotions', css_file='promotions.css', promotions=promotions, promotion_name=promotion_name, promotion_year=promotion_year)


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


@app.route('/messages', methods=['GET', 'POST'])
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
