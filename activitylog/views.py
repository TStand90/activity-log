from flask import render_template, flash, redirect, request, session, url_for
from activitylog import app, mongo
from werkzeug.wrappers import Response
from .forms import NewActivityForm, NewLogEntryForm, RegistrationForm, LoginForm
from .user import User
from .session import MongoSessionInterface
from .models import get_activities_for_range
from slugify import slugify

import datetime
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/log/<date>')
def logfordate(date):
    startDateTime = datetime.datetime.today()
    endDateTime = datetime.datetime.today() + datetime.timedelta(days=1)

    entries = get_activities_for_range(startDateTime, endDateTime)

    return render_template('log.html',
                           entries=entries,
                           beginning_date=startDateTime,
                           end_date=endDateTime)


@app.route('/log/today')
def todayslog():
    startDateTime = datetime.datetime.today()
    endDateTime = datetime.datetime.today() + datetime.timedelta(days=1)

    entries = get_activities_for_range(startDateTime, endDateTime)

    return render_template('todays_log.html', entries=entries)


@app.route('/log/week')
def thisweekslog():
    startDateTime = datetime.datetime.today() - datetime.timedelta(days=7)
    endDateTime = datetime.datetime.today()

    entries = get_activities_for_range(startDateTime, endDateTime)

    return render_template('log.html',
                           entries=entries,
                           beginning_date=startDateTime,
                           end_date=endDateTime)


@app.route('/log/month')
def thismonthslog():
    startDateTime = datetime.datetime.today() - datetime.timedelta(days=30)
    endDateTime = datetime.datetime.today()

    entries = get_activities_for_range(startDateTime, endDateTime)

    return render_template('log.html',
                           entries=entries,
                           beginning_date=startDateTime,
                           end_date=endDateTime)


@app.route('/log/new', methods=['GET', 'POST'])
def newlogentry():
    existing_activities = [(activity['name'], activity['name']) for activity in mongo.db.activities.find()]
    existing_activities = set(existing_activities)
    form = NewLogEntryForm(existing_activities)

    if form.validate_on_submit():
        activity = mongo.db.activities.find_one({'name': form.activity.data})

        data = {'name': form.activity.data,
                'username': session['username'],
                'startTime': form.startTime.data,
                'endTime': form.endTime.data,
                'slug': activity['slug']}

        mongo.db.entries.insert_one(data)
        flash('Entry created')
        return redirect('/log/today')

    return render_template('new_log_entry.html', form=form)


@app.route('/activities')
def activities():
    activities = mongo.db.activities.find({'username': session['username']})
    return render_template('activities.html', activities=activities)


@app.route('/activities/<activity_slug>')
def view_activity(activity_slug):
    activity_data = mongo.db.activities.find_one(
        {
            'slug': activity_slug,
            'username': session['username']
        }
    )
    entries_data = mongo.db.entries.find(
        {
            'name': activity_data['name'],
            'username': session['username']
        }
    )
    entries = list(entries_data)
    return render_template('view_activity.html',
                           activity=activity_data,
                           entries=entries)


@app.route('/activities/new', methods=['GET', 'POST'])
def new_activity():
    form = NewActivityForm()
    if form.validate_on_submit():
        data = {'name': form.name.data,
                'username': session['username'],
                'slug': slugify(form.name.data)}
        document = mongo.db.activities.find_one(data)

        if document:
            flash('That activity already exists!')
            return redirect('/activities')
        else:
            mongo.db.activities.insert_one(data)
            flash('Activity created!')
            return redirect('/activities')

    return render_template('new_activity.html', form=form)


@app.route('/users/<user>')
def user_profile(user):
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        data = {'username': new_user.username}
        existing_user = mongo.db.users.find_one(data)

        if existing_user:
            flash('That user already exists')
            return redirect('/register')
        else:
            mongo.db.users.insert_one({'username': new_user.username,
                                       'email': new_user.email,
                                       'password': new_user.password_hash})
            flash('You have been registered')
            return redirect('/register')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {'username': form.username.data}
        existing_user = mongo.db.users.find_one(data)

        if existing_user:
            session['username'] = form.username.data
            flash('You have been logged in')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('index'))
