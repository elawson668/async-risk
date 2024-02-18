from asyncrisk import app, bcrypt, dao
from asyncrisk.models import Users, Friends, Requests, db
from asyncrisk.forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm, AddFriendForm

from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required
from flask import request, render_template, redirect, url_for, flash


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/friends', methods=['GET'])
def friends():
    entries = Friends.query.filter_by(user_id=current_user.id)
    friend_ids = [f.friend_id for f in entries]
    friends = Users.query.filter(Users.id.in_(friend_ids)).order_by(Users.username).all()
    return render_template('friends.html', title='Friends', friends=friends)


@app.route('/friends/add_friend', methods=['GET', 'POST'])
def add_friend():
    af_form = AddFriendForm()
    if af_form.validate_on_submit():
        requested_friend_id = Users.query.filter_by(username=af_form.username.data).first().id
        friend_request = Requests(user_id=requested_friend_id, requester_id=current_user.id)
        dao.save(friend_request)
        flash('Friend request sent')
        return redirect(url_for('friends'))
    return render_template('add_friend.html', form=af_form)


@app.route('/friends/friend_requests', methods=['GET'])
def friend_requests():
    requests_received = Requests.query.filter_by(user_id=current_user.id).all()
    users_received = []
    for r in requests_received:
        users_received.append(Users.query.filter_by(id=r.requester_id).first())

    requests_sent = Requests.query.filter_by(requester_id=current_user.id).all()
    users_sent = []
    for r in requests_sent:
        users_sent.append(Users.query.filter_by(id=r.user_id).first())

    return render_template('friend_requests.html', requests_received=users_received, requests_sent=users_sent)


@app.route('/friends/friend_requests/<int:user_id>/accept_request', methods=['GET', 'POST'])
def accept_request(user_id):
    requester = Users.query.filter_by(id=user_id).first()

    friend_user_to_requester = Friends(user_id=current_user.id, friend_id=requester.id)
    dao.save(friend_user_to_requester)

    friend_requester_to_user = Friends(user_id=requester.id, friend_id=current_user.id)
    dao.save(friend_requester_to_user)

    request = Requests.query.filter(Requests.user_id == current_user.id, Requests.requester_id == requester.id).first()
    dao.delete(request)

    message = 'Friend request approved. You are now friends with ' + requester.username
    flash(message)
    return redirect(url_for('friend_requests'))


@app.route('/friends/friend_requests/<int:user_id>/reject_request', methods=['GET', 'POST'])
def reject_request(user_id):
    requester = Users.query.filter_by(id=user_id).first()

    request = Requests.query.filter(Requests.user_id == current_user.id, Requests.requester_id == requester.id).first()
    dao.delete(request)
    flash('Friend request rejected')
    return redirect(url_for('friend_requests'))


@app.route('/friends/friend_requests/<int:user_id>/revoke_request', methods=['GET', 'POST'])
def revoke_request(user_id):
    user = Users.query.filter_by(id=user_id).first()

    request = Requests.query.filter(Requests.user_id == user.id, Requests.requester_id == current_user.id).first()
    dao.delete(request)
    flash('Friend request revoked')
    return redirect(url_for('friend_requests'))


@app.route('/friends/<int:user_id>/unfriend', methods=['GET', 'POST'])
def unfriend(user_id):

    friend_user_to_friend = Friends.query.filter(Friends.user_id == current_user.id, Friends.friend_id == user_id).first()
    dao.delete(friend_user_to_friend)

    friend_friend_to_user = Friends.query.filter(Friends.user_id == user_id, Friends.friend_id == current_user.id).first()
    dao.delete(friend_friend_to_user)

    unfriended_username = Users.query.filter_by(id=user_id).first().username
    message = 'Unfriended ' + unfriended_username
    flash(message)
    return redirect(url_for('friends'))


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


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))

