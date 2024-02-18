from asyncrisk import app, bcrypt, dao
from asyncrisk.models import Users, db
from asyncrisk.forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():

        # Create new user
        hashed_password = bcrypt.generate_password_hash(rform.password.data).decode('utf-8')
        user = Users(username=rform.username.data, email=rform.email.data, password=hashed_password)
        dao.save(user)

        flash(f'The account has been created for this user.', 'success')
        return render_template('index.html')
    else:
        return render_template('register.html', title='Register', form=rform)



@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@fresh_login_required
def account():
    aform = UpdateAccountForm()
    if aform.validate_on_submit():
        current_user.username = aform.username.data
        current_user.email = aform.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        aform.username.data = current_user.username
        aform.email.data = current_user.email
    return render_template('account.html', title='Account', form=aform)


@app.route('/change_password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    pform = ChangePasswordForm()
    if pform.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, pform.current_pass.data):
            hashed_password = bcrypt.generate_password_hash(pform.new_pass.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('change_password'))
        else:
            flash('Password update failed. Incorrect password.', 'danger')
    return render_template('change_password.html', title='Change Password', form=pform)

