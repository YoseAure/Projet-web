from flask_login import UserMixin
from config import mysql, login_manager

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password, promotion_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.promotion_id = promotion_id


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(id=user[0], first_name=user[1], last_name=user[2], email=user[3], password=user[4], promotion_id=user[5])
    return None


def get_all_promotions():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT promotion_id, CONCAT(year, ' - ', name) FROM Promotions ORDER BY year DESC")
    promotions = cur.fetchall()
    cur.close()
    return [(promotion_id, name) for promotion_id, name in promotions]
