import secrets
import sqlite3
from PIL import Image
import os
from attendance.models import TimeTable, User, Attendance_Entry, takes, Student, Faculty, Teaches, Course

from flask import Flask, render_template, url_for, flash, redirect, request,abort, Response, send_file

from attendance.form import RegistrationForm, LoginForm, UpdateAccountForm, markattendanceForm, Add_Attendance_Widget_Form

from attendance.form import FindDate
# >>>>>>> 7feff037918ef28d6d2435b3d9514df8328f0213
from attendance import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime,date, timedelta
from attendance.camera import camera_stream, authenticate
import json
import xlsxwriter
from io import BytesIO

def xcelwriter(student_id,course_id, attnd):
	# print(attnd)
	output = BytesIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet()

	worksheet.write(0,0,"ID")
	worksheet.write(0,1,student_id)
	worksheet.write(1,0,"Course ID")
	worksheet.write(1,1,course_id)
	worksheet.write(2,0,"Date")
	worksheet.write(2,1,"Time of Entry")


	r = 3
	print(attnd)
	for course_date in attnd:
		val = attnd[course_date] 
		if(val==False):
			val = "Absent"
		worksheet.write(r,0,str(course_date))
		worksheet.write(r,1,val)
		r+=1

	workbook.close()
	output.seek(0)
	# workbook.save("attendance_record.xlsx")

	return send_file(output, attachment_filename="attendance_"+course_id+".xlsx", as_attachment=True)

def get_breakup(course_id):
	stude_list = getregisteredstudents(course_id)
	d = {"0-70":0,"70-80":0,"80-90":0,"90+":0}
	for (_,_,attendance) in stude_list:
		if(attendance<70):
			d["0-70"] = d.get("0-70",0) + 1
		elif(attendance<80):
			d["70-80"] = d.get("70-80",0) + 1
		elif(attendance<90):
			d["80-90"] = d.get("80-90",0) + 1
		else:
			d["90+"] = d.get("90+",0) + 1
	for key in d:
		d[key] = round((d[key]/len(stude_list))*100	,2)
	return d

def get_faculty_attendace_percent(faculty_id):
    # first get the courses.
    # then get the course attendance
    # then just simply put everything in a dictionary
	course_list = Teaches.query.filter_by(Faculty_ID=faculty_id)
	course_list = [x.Course_ID for x in course_list]
	sem_start = datetime(year=2021, month=1, day=1, hour=0, minute=0)
	sem_end = sem_start + timedelta(days=115)
	res = {}
	tot_classes=0
	attended_classes = 0
	for course in course_list:
		R = get_course_wise(sem_start,sem_end,faculty_id,course)
		cnt = 0.0
		for k in R:
			if(R[k] != False):
				attended_classes += 1
				tot_classes += 1
				cnt += 1.0
			else:
				tot_classes += 1
		res[course] = round(cnt / len(R) * 100, 2)
	return res, round((attended_classes/tot_classes)*100, 2)

def get_student_attendace_percent(student_id):
    # first get the courses.
    # then get the course attendance
    # then just simply put everything in a dictionary
	course_list = takes.query.filter_by(User_ID=student_id)
	course_list = [x.Course_ID for x in course_list]
	sem_start = datetime(year=2021, month=1, day=1, hour=0, minute=0)
	sem_end = sem_start + timedelta(days=115)
	res = {}
	tot_classes=0
	attended_classes = 0
	for course in course_list:
		R = get_course_wise(sem_start,sem_end,student_id,course)
		cnt = 0.0
		for k in R:
			if(R[k] != False):
				attended_classes += 1
				tot_classes += 1
				cnt += 1.0
			else:
				tot_classes += 1
		res[course] = round(cnt / len(R) * 100, 2)
	return res, round((attended_classes/tot_classes)*100, 2)

# returning list of (stdent.name, student.entry number)
def getregisteredstudents(course_id):
	student_list = takes.query.filter_by(Course_ID=course_id).all()
	student_list = [x.User_ID for x in student_list]
	stud_list = []
	for x in student_list:
		attendance_percent, _ = get_student_attendace_percent(x)
		name = Student.query.filter_by(Stud_ID = x).all()
		for k in name:
			print(k.Name)
			p = (k.Name,x,attendance_percent[course_id])
		stud_list.append(p)

	return stud_list



def get_course_wise(date_lower, date_upper, user_id, course_id):
	records = Attendance_Entry.query.filter(Attendance_Entry.User_ID==user_id, Attendance_Entry.Course_ID==course_id, Attendance_Entry.Date <= date_upper, Attendance_Entry.Date >= date_lower)
	# print([record.Date.day for record in records])
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
				result[curr.strftime("%d-%m-%Y")] = False
				break
			

		if(class_happens):
			for atten in records:
				if(atten.Date.day == curr.day and  atten.Date.time() <= end_time and atten.Date.time() >= st_time ):
					result[curr.strftime("%d-%m-%Y")] = atten.Date.strftime("%H:%M")
			
		curr += timedelta(days=1)
	
	return result


@app.route("/") #index
@app.route("/home",methods=["GET","POST"])
def home():
	if(current_user.is_authenticated and current_user.username[0] == 'F'):
		return redirect(url_for('faculty_home'))
	elif(current_user.is_authenticated):
		student_data = Student.query.filter_by(Stud_ID = current_user.username).first()
		bar_data, percentage = get_student_attendace_percent(current_user.username)
		pie_data = {"Attended":percentage, "Not Attended":100 - percentage}
		plot_data = {"bar":bar_data, "pie":pie_data}
		return render_template('dashboard.html', student_data = student_data, jsonfile = json.dumps(plot_data))
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
		# return "Failed"
		return render_template('authentication_falied.html',form=form)


@app.route('/getcourses')
def getcourses():
	# Shows all courses registered for student
	user_id = request.args.get('user_id')
	course_list = takes.query.all()
	course_list = [x.Course_ID for x in course_list]
	
	# add webpage to show all registered courses, 
	# send course list as a parameter
	return render_template('getcourses.html',course_list = course_list)

@app.route('/getattendance', methods=["GET","POST"])
@login_required
# get attendance corresponding to the courseID
def getattendance():
	# add logic to get attendance
	user_id = request.args.get('user_id')
	form = FindDate()
	if form.validate_on_submit():
		course_id = form.course_id.data
		date_upper = form.end_date.data
		date_lower = form.start_date.data
		# print(date_lower, date_upper)
		result = get_course_wise(date_lower, date_upper, user_id, course_id)
		# print(result)
		return xcelwriter(user_id, course_id, result)
	return render_template("filter_attendance.html", form = form)


# @app.route('/getregisteredstudents')
# # returns the list of students in the course


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

@app.route("/faculty")
def faculty_home():
		faculty_id = current_user.username
		bar_data, percentage = get_faculty_attendace_percent(current_user.username)
		pie_data = {"Attended":percentage, "Not Attended":100 - percentage}
		plot_data = {"bar":bar_data, "pie":pie_data}
		faculty_data = Faculty.query.filter_by(Faculty_ID = faculty_id).first()
		course_teaches = Teaches.query.filter_by(Faculty_ID = faculty_id)
		return render_template('dashboardf.html', faculty_data=faculty_data, course_teaches = course_teaches, jsonfile = json.dumps(plot_data))

@app.route("/course")
def course():	
	c_id = request.args.get('course_id')
	course_name = (Course.query.filter_by(Course_ID = c_id).first()).Name
	faculty_id = request.args.get('faculty_id')
	name = request.args.get('faculty_name')
	reg_students = getregisteredstudents(c_id)
	faculty_id = current_user.username
	faculty_data = Faculty.query.filter_by(Faculty_ID = faculty_id).first()
	course_teaches = Teaches.query.filter_by(Faculty_ID = faculty_id)
	plot_data = get_breakup(c_id)
	return render_template('course.html',c_id = c_id,faculty_data=faculty_data, course_teaches = course_teaches, f_id = faculty_id, name = name, reg_students = reg_students, course_name = course_name,jsonfile = json.dumps(plot_data))
