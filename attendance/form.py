from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from attendance.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired("Username length must be between 5 and 20 characters"), Length(min=5, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError("Choose a unique username")

    # def validate_email(self,email):
    #     email = User.query.filter_by(email=email.data).first()
    #     if email:
    #         raise ValidationError("Email is taken. Please enter a different email.")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username :
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class markattendanceForm(FlaskForm):
    entry_number = StringField('Entry Number', validators=[DataRequired()])
    course_id = StringField('Course ID', validators=[DataRequired()])
    submit = SubmitField('Mark Attendance')

class Add_Attendance_Widget_Form(FlaskForm):
    submit = SubmitField('Back to home')
    
class FindDate(FlaskForm):
    start_date = DateField('Start Date(dd/mm/YYYY)', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(' End Date(dd/mm/YYYY)', format='%Y-%m-%d', validators=[DataRequired()])
    course_id = StringField('Course ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
