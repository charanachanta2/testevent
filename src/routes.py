import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

# Absolute static pathing layout setup to ensure Vercel can resolve templates effortlessly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

events_bp = Blueprint(
    'events', 
    __name__, 
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

class EventService:
    @staticmethod
    def get_upcoming_events(db):
        return sorted(db.events.find(), key=lambda x: x.get('date_object', datetime.now()))

    @staticmethod
    def create_event(db, form_data):
        raw_tags = form_data.get('tags', 'General')
        processed_tags = [tag.strip().upper() for tag in raw_tags.split(',') if tag.strip()]
        date_raw = form_data.get('date')
        parsed_date = datetime.strptime(date_raw, '%Y-%m-%dT%H:%M') if date_raw else datetime.now()

        event_document = {
            "title": form_data.get('title', 'Untitled Event').strip(),
            "description": form_data.get('description', '').strip(),
            "date_object": parsed_date,
            "location": form_data.get('location', 'Remote Node').strip(),
            "tags": processed_tags or ["GENERAL"]
        }
        return db.events.insert_one(event_document)

@events_bp.route('/hub/events', methods=['GET'])
def index():
    from app import db 
    events = EventService.get_upcoming_events(db)
    return render_template('dashboard.html', events=events)

@events_bp.route('/hub/events/publish', methods=['POST'])
def publish():
    from app import db
    EventService.create_event(db, request.form)
    flash("Event context broadcast successfully initialized.", "success")
    return redirect(url_for('events.index'))
