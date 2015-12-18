from activitylog import app, mongo


def get_activities_for_range(startDateTime, endDateTime):
    entries = []
    entries.extend(list(mongo.db.entries.find({
        'startTime':
            {
                '$gte': startDateTime,
                '$lte': endDateTime
            }
    })))

    return entries


class Activity:

    def __init__(self, name, startTime, endTime):
        self.name = name
        self.startTime = self.time_string_to_datetime(startTime)
        self.endTime = self.time_string_to_datetime(endTime)
