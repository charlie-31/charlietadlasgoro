from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "name": "John Cruz", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Maria Santos", "grade": 10, "section": "Matthew"}
]

@app.route('/')
def home():
    return "Student Record API"

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)
    return jsonify({"message": "Student not found"})

@app.route('/students', methods=['POST'])
def add_student():
    new_student = {
        "id": len(students) + 1,
        "name": request.json["name"],
        "grade": request.json["grade"],
        "section": request.json["section"]
    }
    students.append(new_student)
    return jsonify(new_student)

if __name__ == "__main__":
    app.run(debug=True)
