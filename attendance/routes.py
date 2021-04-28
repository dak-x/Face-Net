import secrets
import sqlite3
from PIL import Image
import os
from attendance.models import TimeTable, User, Attendance_Entry, takes, Student, Faculty

from flask import Flask, render_template, url_for, flash, redirect, request,abort, Response
from attendance.form import RegistrationForm, LoginForm, UpdateAccountForm, markattendanceForm, Add_Attendance_Widget_Form
from attendance import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime,date, timedelta
from attendance.camera import camera_stream, authenticate

@app.route("/") #index
@app.route("/home")
def home():
	if(current_user.is_authenticated and current_user.username[0] == 'F'):
		return "Faculty dashboard"
	elif(current_user.is_authenticated):
		student_data = Student.query.filter_by(Stud_ID = current_user.username).first()
		return render_template('dashboard.html', student_data = student_data)
	else:
		return redirect(url_for('login'))


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

@app.route('/markattendance',methods=["GET","POST"])
def markattendance():
	form = markattendanceForm()
	if form.validate_on_submit():
		user_id = form.entry_number.data
		course_id = form.course_id.data
		return redirect(url_for('detect', user_id=user_id, course_id=course_id))
	
	return render_template('mark_attendance.html', form = form)

@app.route('/detect')
def detect():
	user_id = request.args.get('user_id')
	course_id = request.args.get('course_id')
	
	return render_template('index.html', user_id=user_id, course_id=course_id)

@app.route('/addattendance')
def addattendance():
	user_id = request.args.get('user_id')
	course_id = request.args.get('course_id')
	is_true = authenticate(user_id)
	form = Add_Attendance_Widget_Form()
	if(is_true):
		attendance_entry = Attendance_Entry(Course_ID=course_id, User_ID=user_id,Date=datetime.now(),Semester=6)
		print(attendance_entry.Date.strftime("%m/%d/%Y, %H:%M:%S"))
		db.session.add(attendance_entry)
		db.session.commit()
		# todo add new page instead
		return render_template('attendance_added.html',form=form)
	else:
		# todo add extra page with prompt to go back
		# return NOT Authenticate
		return redirect(url_for('markattendance'))


@app.route('/getcourses')
def getcourses():
	# Shows all courses registered for student
	user_id = request.args.get('user_id')
	course_list = takes.query.all()
	course_list = [x.Course_ID for x in course_list]
	
	# add webpage to show all registered courses, 
	# send course list as a parameter
	return "Course List"

@app.route('/getattendance')
# get attendance corresponding to the courseID
def getattendance():
	# add logic to get attendance
	user_id = request.args.get('user_id')
	course_id = request.args.get('course_id')
    # TODO: Get the DateTime objects
	#  from the request form.
	date_upper = request.args.get('date_upper')
	date_lower = request.args.get('date_lower')

	records = Attendance_Entry.query.filter(Attendance_Entry.User_ID==user_id, Attendance_Entry.Course_ID==course_id, Attendance_Entry.Date <= date_upper, Attendance_Entry.Date >= date_lower)

	slots = TimeTable.query.filter(TimeTable.Course_ID==course_id)

	result = dict()

	curr = date_lower
	while(curr <= date_upper):
		class_happens = False
		
		for slot in slots:
			if(slot.Day == curr.weekday()):
				st_time = slot.Start_Time.time()
				end_time = slot.End_Time.time()
				class_happens = True
				result[curr.day] = False
				break
		

		if(class_happens):
			for atten in records:
				if(atten.Date.day == curr.day and  atten.Date.time() <= end_time and atten.Date.time() >= st_time ):
					result[curr.day] = True
		
		curr += timedelta(days=1)

	return result


@app.route('/getregisteredstudents')
# returns the list of students in the course
def getregisteredstudents():
	course_id = request.args.get('course_id')
	student_list = takes.query.filter_by(Course_ID=course_id).all()
	student_list = [x.User_ID for x in student_list]

	print(student_list)
	return "Student List"

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