from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import re

app = Flask(__name__)

# MongoDB connection with valid parameters
client = MongoClient(
    'mongodb://localhost:27017/',
    connectTimeoutMS=30000,
    socketTimeoutMS=30000,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=50,
    minPoolSize=10
)

db = client['FleetManagementSystem']

# Collections with validation
drivers_collection = db['drivers']
fleet_collection = db['fleet']
spares_collection = db['spares']
assignments_collection = db['assignments']
billing_collection = db['billing']

# Create indexes for better performance
drivers_collection.create_index([('driver_id', 1)], unique=True)
fleet_collection.create_index([('vehicle_id', 1)], unique=True)
spares_collection.create_index([('spare_id', 1)], unique=True)
assignments_collection.create_index([('assignment_id', 1)], unique=True)
billing_collection.create_index([('record_id', 1)], unique=True)

# Add text indexes for searchable fields
drivers_collection.create_index([('first_name', 'text'), ('last_name', 'text')])
fleet_collection.create_index([('model', 'text'), ('reg_no', 'text')])
spares_collection.create_index([('part_name', 'text')])

# Enhanced get_next_id function
def get_next_id(collection, id_field):
    last_doc = collection.find_one(sort=[(id_field, -1)])
    if last_doc and id_field in last_doc:
        try:
            # Numeric IDs
            if isinstance(last_doc[id_field], (int, float)):
                return last_doc[id_field] + 1
            # Alphanumeric with trailing digits
            elif isinstance(last_doc[id_field], str):
                match = re.search(r'(\d+)$', last_doc[id_field])
                if match:
                    prefix = last_doc[id_field][:match.start()]
                    return f"{prefix}{int(match.group(1)) + 1}"
        except:
            pass
    # Default starting IDs
    default_ids = {
        "driver_id": 1000,
        "vehicle_id": 2000,
        "record_id": 3000,
        "assignment_id": 4000,
        "spare_id": 5000
    }
    return default_ids.get(id_field, 1)

@app.route("/get_next_id/<collection_name>")
def get_next_id_route(collection_name):
    try:
        collection_map = {
            "drivers": (drivers_collection, "driver_id"),
            "fleet": (fleet_collection, "vehicle_id"),
            "billing": (billing_collection, "record_id"),
            "assignments": (assignments_collection, "assignment_id"),
            "spares": (spares_collection, "spare_id")
        }
        
        if collection_name not in collection_map:
            return jsonify({"error": "Invalid collection"}), 400
        
        collection, id_field = collection_map[collection_name]
        next_id = get_next_id(collection, id_field)
        return jsonify({"next_id": next_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        # Basic counts
        drivers_count = drivers_collection.count_documents({})
        fleet_count = fleet_collection.count_documents({})
        assignments_count = assignments_collection.count_documents({})
        billing_count = billing_collection.count_documents({})
        spares_count = spares_collection.count_documents({})
        
        # Advanced calculations
        fleet_in_use = assignments_collection.count_documents({
            'start_date': {'$lte': datetime.now()},
            'end_date': {'$gte': datetime.now()}
        })
        
        fleet_utilization = round((fleet_in_use / fleet_count * 100) if fleet_count > 0 else 0, 2)
        
        stats = {
            'drivers_count': drivers_count,
            'fleet_count': fleet_count,
            'assignments_count': assignments_count,
            'billing_count': billing_count,
            'spares_count': spares_count,
            'fleet_in_use': fleet_in_use,
            'fleet_utilization': fleet_utilization,
            'drivers_available': drivers_count - assignments_count
        }
    except Exception as e:
        stats = {
            'drivers_count': 0,
            'fleet_count': 0,
            'assignments_count': 0,
            'billing_count': 0,
            'spares_count': 0,
            'fleet_in_use': 0,
            'fleet_utilization': 0,
            'drivers_available': 0
        }
        app.logger.error(f"Error getting dashboard stats: {str(e)}")
    
    return render_template('dashboard.html', stats=stats)

@app.route('/driver', methods=['GET', 'POST'])
def driver():
    if request.method == 'GET':
        return render_template('driver.html')
    try:
        data = request.get_json()
        drivers_collection.insert_one(data)
        return jsonify({'message': 'Driver added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/fleet', methods=['GET', 'POST'])
def fleet():
    if request.method == 'GET':
        return render_template('fleet.html')
    try:
        data = request.get_json()
        fleet_collection.insert_one(data)
        return jsonify({'message': 'Vehicle added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    if request.method == 'GET':
        return render_template('assignment.html')
    try:
        data = request.get_json()
        assignments_collection.insert_one(data)
        return jsonify({'message': 'Assignment added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'GET':
        return render_template('billing.html')
    try:
        data = request.get_json()
        data['distance'] = float(data['km_after']) - float(data['km_before'])
        data['subtotal'] = data['distance'] * float(data['charges_per_km'])
        data['gst_amount'] = data['subtotal'] * (float(data['gst']) / 100)
        data['total_amount'] = data['subtotal'] + data['gst_amount']
        billing_collection.insert_one(data)
        return jsonify({'message': 'Billing record added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/spares', methods=['GET', 'POST'])
def spares():
    if request.method == 'GET':
        return render_template('spares.html')
    try:
        data = request.get_json()
        data['total_cost'] = float(data['unit_price']) * int(data['quantity'])
        spares_collection.insert_one(data)
        return jsonify({'message': 'Spare part added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    try:
        client.server_info()
        print("Successfully connected to MongoDB")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Could not connect to MongoDB: {str(e)}")
