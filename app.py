#!/usr/bin/env python3
from flask import Flask, send_file, jsonify
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent

@app.route('/')
def index():
    return send_file(BASE_DIR / 'dashboard-youtube-interactivo.html')

@app.route('/api/data')
def get_data():
    response_data = {}
    for period in ['2026-01', '2025-12']:
        filename = f'youtube_analytics_{period.replace("-", "_").lower().replace("2026_01", "jan_26").replace("2025_12", "dec_25")}.json'
        filepath = BASE_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                response_data[period] = json.load(f)
    
    if not response_data:
        return jsonify({'error': 'No data found'}), 404
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
