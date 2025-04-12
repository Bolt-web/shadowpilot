from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# Sample data generation
def generate_current_status():
    return {
        'beds': {
            'total': 300,
            'occupied': random.randint(180, 250),
            'available': lambda x: x['beds']['total'] - x['beds']['occupied']
        },
        'staff': {
            'nurses': random.randint(40, 60),
            'doctors': random.randint(15, 25),
            'support': random.randint(20, 30)
        },
        'equipment': {
            'ventilators': {
                'total': 50,
                'in_use': random.randint(30, 45)
            },
            'monitors': {
                'total': 100,
                'in_use': random.randint(70, 90)
            }
        },
        'er_wait_time': random.randint(15, 60),
        'icu_availability': random.randint(5, 15)
    }

def generate_predictions():
    dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    return {
        'dates': dates,
        'admissions': [random.randint(50, 120) for _ in range(7)],
        'discharges': [random.randint(40, 100) for _ in range(7)],
        'length_of_stay': [round(random.uniform(2.5, 8.5), 1) for _ in range(7)],
        'beds_needed': [random.randint(180, 280) for _ in range(7)],
        'staff_needed': {
            'nurses': [random.randint(45, 70) for _ in range(7)],
            'doctors': [random.randint(18, 30) for _ in range(7)]
        },
        'equipment_needed': {
            'ventilators': [random.randint(30, 50) for _ in range(7)],
            'monitors': [random.randint(70, 100) for _ in range(7)]
        }
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current_status')
def current_status():
    data = generate_current_status()
    data['beds']['available'] = data['beds']['available'](data)
    return jsonify(data)

@app.route('/api/predictions')
def predictions():
    return jsonify(generate_predictions())

if __name__ == '__main__':
    app.run(debug=True, port=5000)