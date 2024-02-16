from asyncrisk import app, bcrypt
from asyncrisk.models import Users
from asyncrisk.forms import LoginForm

from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required
from flask import request, render_template, redirect, url_for, flash


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    lform = LoginForm()
    if lform.validate_on_submit():
        user = Users.query.filter_by(email=lform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, lform.password.data):
            login_user(user, remember=lform.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login failed. Submit valid credentials.', 'danger')

    return render_template('login.html', title='Login', form=lform)
