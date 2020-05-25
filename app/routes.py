from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'problem'}
	posts = [
		{
			'author': {'username': 'john'},
			'body': 'I need a new macbook'
		},
		{
			'author': {'username': 'amie'},
			'body': 'going to disneyland. :)'
		}
	]
	return render_template('index.html', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# 1st get request -> valonsub returns false so login form is rendered
	if form.validate_on_submit():
		flash(f'Log in requested for {form.username.data}, remember_me={form.remember_me.data}')
		return redirect(url_for('index'))
	return render_template('login.html', form=form)
