from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database
attendance = []

# Helper: validate attendance input
def validate_data(data):
    required_fields = ["name", "date", "status"]

    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"

    # Validate date format
    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD"

    # Validate status
    if data["status"] not in ["Present", "Absent", "Late"]:
        return "Status must be Present, Absent, or Late"

    return None


@app.route('/')
def home():
    return "📘 Attendance API is running!"


# GET all or filtered attendance
@app.route('/attendance', methods=['GET'])
def get_attendance():
    name = request.args.get("name")
    date = request.args.get("date")

    results = attendance

    if name:
        results = [r for r in results if r["name"].lower() == name.lower()]

    if date:
        results = [r for r in results if r["date"] == date]

    return jsonify(results)


# ADD attendance
@app.route('/attendance', methods=['POST'])
def add_attendance():
    data = request.get_json()

    error = validate_data(data)
    if error:
        return jsonify({"error": error}), 400

    record = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "date": data["date"],
        "status": data["status"],
        "timestamp": datetime.now().isoformat()
    }

    attendance.append(record)

    return jsonify({
        "message": "✅ Attendance recorded",
        "data": record
    }), 201


# UPDATE attendance
@app.route('/attendance/<record_id>', methods=['PUT'])
def update_attendance(record_id):
    data = request.get_json()

    for record in attendance:
        if record["id"] == record_id:
            record["name"] = data.get("name", record["name"])
            record["date"] = data.get("date", record["date"])
            record["status"] = data.get("status", record["status"])

            return jsonify({
                "message": "✏️ Attendance updated",
                "data": record
            })

    return jsonify({"error": "Record not found"}), 404


# DELETE one record
@app.route('/attendance/<record_id>', methods=['DELETE'])
def delete_attendance(record_id):
    global attendance

    attendance = [r for r in attendance if r["id"] != record_id]

    return jsonify({"message": "🗑️ Record deleted"})


# CLEAR all records
@app.route('/attendance/clear', methods=['DELETE'])
def clear_attendance():
    attendance.clear()
    return jsonify({"message": "⚠️ All records cleared"})


if __name__ == '__main__':
    app.run(debug=True)
