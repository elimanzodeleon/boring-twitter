from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, SignupForm, EditProfileForm, EmptyForm
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required # this view can only be seen if logged in
def index():
	posts = [
		{
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
	]
	return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	# if user is logged in, do not show log in page
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	# 1st get request -> valonsub returns false so login form is rendered
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		# check_password not working
		if user is None or not user.check_password(form.password.data):
			flash('invalid username or password')
			return redirect(url_for('index'))
		login_user(user, remember=form.remember_me.data)
		# from url grab whatever 'next' is = to
		next_page = request.args.get('next')
		# if next_page dne or nextpage is relative url(no netloc) ret index
		# else return url for whatever next_page is (full or relative url)
		# http://www.ex.com/index?search=src - netloc = www.ex.com
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	# make sure user is not logged in
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Welcome to Boring Twitter')
		return redirect(url_for('login'))
	return render_template('signup.html', title='Sign up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	# get user. if not exist return 404
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'need a new macbook asap as possible'},
		{'author': user, 'body': 'allez paris'}
	]
	form = EmptyForm()
	return render_template('user.html', user=user, posts=posts, form=form)

# update users last_seen var everytime they make a req to the server
# this decorator execs before view function
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		# no .add bc flask-login invokes user loader callback func which runs a db query that puts target user in db session
		db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	# pass current users username to the form
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Changes have been saved')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		# user requested edit_profile -> fill form with users current info
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(f'{username} does not exist')
			return redirect(url_for('index'))
		if user == current_user:
			flash(f'no')
			return redirect(url_for('index'))
		
		current_user.follow(user)
		db.session.commit()
		
		flash(f'Now following {username}')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))
		
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(f'{username} does not exist')
			return redirect(url_for('index'))
		if user == current_user:
			flash('no')
			return redirect(url_for('index'))
		
		current_user.unfollow(user)
		db.session.commit()
		
		flash(f'Unfollowed {username}')
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))
		