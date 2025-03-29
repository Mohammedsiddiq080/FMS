from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['FleetMangementSystem']
drivers_collection = db['drivers']
fleet_collection = db['fleet']
spares_collection = db['spares']
assignments_collection = db['assignment']
billing_collection = db['billing']

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Driver Route
@app.route('/driver', methods=['GET', 'POST'])
def driver():
    if request.method == 'POST':
        driver_data = {
            'driver_id': request.form['driver_id'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'license_number': request.form['license_number']
        }
        drivers_collection.insert_one(driver_data)
        return jsonify({"message": "Driver added successfully!"})
    return render_template('driver.html')

# Fleet Route
@app.route('/fleet', methods=['GET', 'POST'])
def fleet():
    if request.method == 'POST':
        fleet_data = {
            'vehicle_id': request.form['vehicle_id'],
            'model': request.form['model'],
            'reg_no': request.form['reg_no'],
            'last_service': request.form['last_service'],
            'mileage': request.form['mileage']
        }
        fleet_collection.insert_one(fleet_data)
        return jsonify({"message": "Fleet details added successfully!"})
    return render_template('fleet.html')

# Assignment Route
@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    if request.method == 'POST':
        assignment_data = {
            'assignment_id': request.form['assignment_id'],
            'company_name': request.form['company_name'],
            'vehicle_id': request.form['vehicle_id'],
            'start_date': request.form['start_date'],
            'end_date': request.form['end_date']
        }
        assignments_collection.insert_one(assignment_data)
        return jsonify({"message": "Assignment added successfully!"})
    return render_template('assignment.html')

# Billing Route
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        billing_data = {
            'record_id': request.form['record_id'],
            'vehicle_id': request.form['vehicle_id'],
            'assignment_id': request.form['assignment_id'],
            'km_before': request.form['km_before'],
            'km_after': request.form['km_after'],
            'charges_per_km': request.form['charges_per_km'],
            'gst': request.form['gst']
        }
        billing_collection.insert_one(billing_data)
        return jsonify({"message": "Billing record added successfully!"})
    return render_template('billing.html')

# Spares Route
@app.route('/spares', methods=['GET', 'POST'])
def spares():
    if request.method == 'POST':
        spares_data = {
            'spare_id': request.form['spare_id'],
            'vehicle_id': request.form['vehicle_id'],
            'part_name': request.form['part_name'],
            'quantity': request.form['quantity']
        }
        spares_collection.insert_one(spares_data)
        return jsonify({"message": "Spare part added successfully!"})
    return render_template('spares.html')

if __name__ == '__main__':
    app.run(debug=True)
