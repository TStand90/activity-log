from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, DateField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Optional


class NewActivityForm(Form):
    name = StringField('name', validators=[DataRequired()])


class NewLogEntryForm(Form):
    activity = SelectField('Activity', validators=[DataRequired()])
    date = DateField('date', validators=[Optional()])
    startTime = DateTimeField('Start Time', validators=[Optional()])
    endTime = DateTimeField('End Time', validators=[Optional()])

    def __init__(self, activity_choices):
        super(NewLogEntryForm, self).__init__()
        self.activity.choices = activity_choices