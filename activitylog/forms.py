from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, DateField, DateTimeField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional, Email, EqualTo
from wtforms.fields.html5 import EmailField


class NewActivityForm(Form):
    name = StringField('Name', validators=[DataRequired()])


class NewLogEntryForm(Form):
    activity = SelectField('Activity', validators=[DataRequired()])
    startTime = DateTimeField('Start Time', validators=[DataRequired()])
    endTime = DateTimeField('End Time', validators=[Optional()])

    def __init__(self, activity_choices):
        super(NewLogEntryForm, self).__init__()
        self.activity.choices = activity_choices


class RegistrationForm(Form):
    username = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Password (again)')


class LoginForm(Form):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
