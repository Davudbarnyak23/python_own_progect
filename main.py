from distutils.command.check import check

from flask import Flask, request, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os

SESSION_USER_ID = 'user_id'

app= Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'school.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'YGBfhLanppV85LPypqvE-jYtPGM-KCDQzp90XKse-VI'
db = SQLAlchemy(app)


# ==== MODELS =========
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)


    def check_password(self, password):
        return check_password_hash(self.password, password)


with app.app_context():
    db.create_all()


# ==== ROUTES =========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/no-slidebar')
def noslidebar():
    return render_template('no-slidebar.html')

@app.route('/two-slidebar')
def twoslidebar():
    return render_template('two-sidebar.html')

#admin

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            message = 'email erorr'
        else:
            if user.check_password(password):
                session[SESSION_USER_ID] = user.id
                return redirect('/')

            message = 'error password '

    return  render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop(SESSION_USER_ID, None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
