from app import app, db
from flask import request, jsonify
from app.models import Event

#set index rout to return nothing, to prevent error

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
        notes= request.headers.get('notes', '')

        #if any info is missing give back an error
        if not title or not day or not month or not year:
            return jsonify({ 'code' : 306, 'message' : 'Information missing.'})

        # all info was checked and included then save event
        event = Event(title=title, day=day, month=month, year=year, notes=notes)

        # add to database

        db.session.add(event)
        db.session.commit()

        return jsonify({ 'code' : 200, 'message' : 'Event Saved'})
    except:
        return jsonify({ 'code' : 305, 'message' : 'Something went wrong. Try again.'})

@app.route('/api/retrieve', methods=['GET'])
def retrieve():

    try:
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')

        results = []

        if not year:
            return jsonify({'code' : 302, 'message': 'Invalid Year'})
        elif day and not month:
            return jsonify({'code' : 303, 'message': 'Invalid Month'})
        elif year and not month and not day:
            # get the events for the whole year
            results= Event.query.filter_by(year=year).all()
        elif year and month and not day:
            # get the events for the whole month
            results= Event.query.filter_by(year=year, month=month).all()
        elif year and month and day:
            results= Event.query.filter_by(year=year, month=month, day=day).all()
        else:
            return jsonify({'code' : 304, 'message' : 'Something went wrong.'})

        # handle case for no events in a given time frame

        if results == []:
            return jsonify({'code': 200, 'message' : 'No events scheduled'})

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

        return jsonify({'code': 200, 'events': events})



    except:
        return jsonify({
            'code' : 301,
            'message' : 'Something went wrong. Try again.'
        })

@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        #take in an event_id,
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(event_id=event_id).first()

        # check if event doesn't exist, send back error
        if not event:
            return jsonify({'code' : 308, 'message' : 'Event not found.'})

        title = event.title

        db.session.delete(event)
        db.session.commit()

        return jsonify({'code': 200, 'message': f'Event "{title}" was deleted.'})
    except:
        return jsonify({
            'code' : 307,
            'message' : 'Something went wrong. Try again.'
        })
