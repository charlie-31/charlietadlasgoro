from flask import Flask, jsonify, request, render_template_string, redirect, url_for
app = Flask(__name__)
# Sample in-memory database
students = [
    {"id": 1, "name": "John Cruz", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Maria Santos", "grade": 10, "section": "Matthew"}
]
# HTML template for UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Records</title>
    <style>
        body { font-family: Arial; background:#f2f2f2; padding:20px; }
        h1 { text-align:center; }
        table { width:100%; border-collapse: collapse; margin-top:20px; }
        th, td { padding:10px; border:1px solid #ccc; text-align:left; }
        form { display:flex; gap:10px; margin-top:20px; }
        input { flex:1; padding:5px; }
        button { padding:5px 10px; cursor:pointer; }
    </style>
</head>
<body>
<h1>Student Records</h1>
<form method="POST" action="/add_student">
    <input name="name" placeholder="Name" required>
    <input name="grade" placeholder="Grade" type="number" required>
    <input name="section" placeholder="Section" required>
    <button type="submit">Add Student</button>
</form>
<table>
<tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th></tr>
{% for s in students %}
<tr>
<td>{{s.id}}</td>
<td>{{s.name}}</td>
<td>{{s.grade}}</td>
<td>{{s.section}}</td>
</tr>
{% endfor %}
</table>
</body>
</html>
"""
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, students=students)
# API endpoint: get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# API endpoint: get student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if student:
        return jsonify(student)
    return jsonify({"message": "Student not found"}), 404
# Add student via form
@app.route('/add_student', methods=['POST'])
def add_student():
    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": request.form["name"],
        "grade": int(request.form["grade"]),
        "section": request.form["section"]
    }
    students.append(new_student)
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)
