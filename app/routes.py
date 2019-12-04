from app import app, db
from flask import request, jsonify
from app.models import Event
from app.email import sendMail
# set index route to return nothing, just so no error occurs
@app.route('/')
def index():
    return 'You shall not pass'

@app.route('/api/save', methods=['POST'])
def save():
    try:
        # get headers for info
        title = request.headers.get('title')
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        notes = request.headers.get('notes', '')
        email = request.headers.get('email')
        # if any info is missing, give back and error
        if not title or not day or not month or not year or not email:
            return jsonify({ 'code' : 306, 'message' : 'Information missing.' })
        # all info was checked and included, create event and save
        event = Event(title=title, day=day, month=month, year=year, notes=notes)
        # add to db
        db.session.add(event)
        db.session.commit()

        sendMail(title, day, month, year, notes, email)
        return jsonify({ 'code' : 200, 'message' : 'Event saved.' })

    except:
        return jsonify({ 'code' : 305, 'message' : 'Something went wrong. Try again.' })

@app.route('/api/retrieve', methods=['GET'])
def retrieve():
    try:
        # get the header information passed
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        # setup results variable to be looped over later
        results = []
        # year is required, to query day then month is required
        if not year:
            return jsonify({ 'code' : 302, 'message' : 'Invalid year' })
        elif day and not month:
            return jsonify({ 'code' : 303, 'message' : 'Invalid month' })
        elif year and not month and not day:
            # get events for entire year
            results = Event.query.filter_by(year=year).all()
        elif year and month and not day:
            # get events for year and month
            results = Event.query.filter_by(year=year, month=month).all()
        elif year and month and day:
            # get events for year and month and day
            results = Event.query.filter_by(year=year, month=month, day=day).all()
        else:
            return jsonify({ 'code' : 304, 'message' : 'Something went wrong.' })
        # if events is empty, there there are no events, handle case
        if results == []:
            return jsonify({ 'code' : 200, 'message' : 'No events scheduled' })
        # loop over results, create a list to append to and return
        events = []
        for result in results:
            events.append({
                'event_id' : result.event_id,
                'title' : result.title,
                'day' : result.day,
                'month' : result.month,
                'year' : result.year,
                'notes' : result.notes
            })
        return jsonify({ 'code' : 200, 'events' : events })
    except:
        return jsonify({
            'code' : 301,
            'message' : 'Something went wrong. Try again.'
        })
@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        # take in an event id
        event_id = request.headers.get('event_id')
        event = Event.query.filter_by(event_id=event_id).first()
        # check if event doesn't exist, send back error
        if not event:
            return jsonify({ 'code' : 308, 'message' : 'Event not found.' })
        title = event.title
        # remove from the db
        db.session.delete(event)
        db.session.commit()
        return jsonify({ 'code' : 200, 'message' : f'Event "{title}" was deleted.' })
    except:
        return jsonify({
            'code' : 307,
            'message' : 'Something went wrong. Try again.'
        })
