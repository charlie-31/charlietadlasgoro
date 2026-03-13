from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)
with app.app_context():
    db.create_all()
# HTML templates
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Student Records</title>
    <style>
        body { font-family: Arial; background:#f2f2f2; margin:0; padding:0; }
        .container { width: 80%; margin: 30px auto; background:#fff; padding:20px; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.1);}
        h1 { text-align:center; }
        table { width:100%; border-collapse:collapse; margin-top:20px; }
        th, td { padding:10px; border:1px solid #ccc; text-align:left; }
        form { display:flex; gap:10px; margin-top: 20px; }
        input[type="text"], input[type="number"] { flex:1; padding:5px; }
        button { padding:5px 10px; border:none; cursor:pointer; border-radius:4px; color:#fff; }
        button.add { background:#28a745; }
        button.edit { background:#007bff; }
        button.delete { background:#dc3545; }
    </style>
</head>
<body>
<div class="container">
    <h1>Student Records</h1>
    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Name" required>
        <input type="number" name="grade" placeholder="Grade" required>
        <input type="text" name="section" placeholder="Section" required>
        <button type="submit" class="add">Add</button>
    </form>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student.id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.grade }}</td>
            <td>{{ student.section }}</td>
            <td>
                <a href="/edit/{{ student.id }}"><button class="edit">Edit</button></a>
                <a href="/delete/{{ student.id }}"><button class="delete">Delete</button></a>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""
EDIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Edit Student</title>
    <style>
        body { font-family: Arial; background:#f2f2f2; margin:0; padding:0; }
        .container { width:50%; margin:50px auto; background:#fff; padding:20px; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.1);}
        h1 { text-align:center; }
        form { display:flex; flex-direction:column; gap:10px; margin-top:20px; }
        input[type="text"], input[type="number"] { padding:5px; }
        button { padding:10px; border:none; cursor:pointer; border-radius:4px; color:#fff; background:#007bff; }
    </style>
</head>
<body>
<div class="container">
    <h1>Edit Student</h1>
    <form method="POST">
        <input type="text" name="name" value="{{ student.name }}" required>
        <input type="number" name="grade" value="{{ student.grade }}" required>
        <input type="text" name="section" value="{{ student.section }}" required>
        <button type="submit">Update</button>
    </form>
</div>
</body>
</html>
"""
# Routes
@app.route('/')
def home():
    students = Student.query.all()
    return render_template_string(INDEX_HTML, students=students)
@app.route('/add', methods=['POST'])
def add_student():
    new_student = Student(
        name=request.form['name'],
        grade=request.form['grade'],
        section=request.form['section']
    )
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.grade = request.form['grade']
        student.section = request.form['section']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(EDIT_HTML, student=student)
if __name__ == '__main__':
    app.run(debug=True)

