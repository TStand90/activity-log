from flask import render_template, flash, redirect, request
from app import app, mongo
from .forms import NewActivityForm, NewLogEntryForm

import datetime
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/log')
def todayslog():
    entries = []
    entries.extend(list(mongo.db.activities.find({'date': str(datetime.date.today())})))
    entries.extend(list(mongo.db.activities.find({'startTime': {'$gte': str(datetime.date.today()), '$lte': str(datetime.date.today() + datetime.timedelta(days=1))}})))

    return render_template('todays_log.html', entries=entries)


@app.route('/log/new', methods=['GET', 'POST'])
def newlogentry():
    existing_activities = [(activity['name'], activity['name']) for activity in mongo.db.activities.find()]
    form = NewLogEntryForm(existing_activities)

    if form.validate_on_submit():
        if form.date.data:
            data = {'name': form.activity.data, 'date': str(form.date.data)}
        else:
            data = {'name': form.activity.data, 'startTime': str(form.startTime.data), 'endTime': str(form.endTime.data)}

        mongo.db.activities.insert_one(data)
        flash('Entry created')
        return redirect('/log')

    return render_template('new_log_entry.html', form=form)


@app.route('/activities')
def activities():
    activities = mongo.db.activities.find()
    return render_template('activities.html', activities=activities)


@app.route('/activities/<activity>')
def view_activity(activity):
    return render_template('view_activity.html', activity=activity)


@app.route('/activities/new', methods=['GET', 'POST'])
def new_activity():
    form = NewActivityForm()
    if form.validate_on_submit():
        data = {'name': form.name.data}
        document = mongo.db.activities.find_one(data)

        if document:
            flash('That activity already exists!')
            return redirect('/activities')
        else:
            mongo.db.activities.insert_one(data)
            flash('Activity created!')
            return redirect('/activities')
    
    return render_template('new_activity.html', form=form)


def testactivity():
    logEntry = {
        'user': 'tyler',
        'date': '10-14-15',
        'activities': [
            {
                'name': 'Ate breakfast'
            },
            {
                'name': 'Cardio on bike',
                'startTime': '11:00 AM',
                'endTime': '11:30 AM'
            }
        ]
    }