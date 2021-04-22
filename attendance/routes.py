import secrets
import sqlite3
from PIL import Image
import os
from attendance.models import User
from flask import Flask, render_template, url_for, flash, redirect, request,abort, Response
from attendance.form import RegistrationForm, LoginForm, UpdateAccountForm
from attendance import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime,date
from attendance.camera import camera_stream, person_name



@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')


@app.route("/register",methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# generate password hash and create user
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created !','success')
		return redirect(url_for('login'))

	return render_template("register.html", title="Register", form=form)

@app.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data)==True:
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("Login unsuccessful. Check email/password",'danger')
	return render_template("login.html", title="Login", form=form)

@app.route("/forgot_password")
def forgot_password():
	return "Not made"

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/img', picture_fn)

	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn

@app.route("/account",methods=["GET","POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated','success')
		redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename="img/"+current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form= form)



@app.route('/detect')
def detect():
    return render_template('index.html')

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')