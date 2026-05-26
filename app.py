import os
import sys

# Hardcoded absolute root tracking alignment for Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, redirect, url_for
from config import config_by_name
from src.routes import events_bp

# Simplified mock database engine setup
class MockCollection:
    def __init__(self): self.data = []
    def find(self): return self.data
    def insert_one(self, doc): self.data.append(doc); return True

class MockDB:
    def __init__(self): self.events = MockCollection()

db = MockDB()

def create_app(config_name='development'):
    app = Flask(__name__, 
                static_folder='src/static', 
                template_folder='src/templates')
    
    app.config.from_object(config_by_name[config_name])
    app.register_blueprint(events_bp)
    
    @app.route('/')
    def root():
        return redirect(url_for('events.index'))
        
    return app

app = create_app('development')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
