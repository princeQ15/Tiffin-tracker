from flask import Flask, render_template, request, jsonify
from surprise_travel.main import SurpriseTravel
import json
from pathlib import Path

app = Flask(__name__)

def load_destinations():
    data_path = Path(__file__).parent / "surprise_travel" / "data" / "destinations.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    destinations = load_destinations()
    return render_template('index.html', destinations=destinations)

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    data = request.json
    planner = SurpriseTravel()
    
    # Set preferences from the request
    preferences = {}
    if 'climate' in data and data['climate']:
        preferences['climate'] = data['climate']
    if 'budget' in data and data['budget']:
        preferences['budget'] = data['budget']
    if 'activity' in data and data['activity']:
        preferences['activity_type'] = data['activity']
    
    if preferences:
        planner.set_preferences(**preferences)
    
    suggestions = planner.get_suggestions()
    return jsonify(suggestions[:5])  # Return top 5 suggestions

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    (Path(__file__).parent / 'templates').mkdir(exist_ok=True)
    app.run(debug=True)
