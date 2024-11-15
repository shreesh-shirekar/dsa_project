from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Existing Student and Teacher Data
student_emails = []
student_ids = []
student_first_names = []
student_last_names = []

teacher_emails = []
teacher_ids = []
teacher_first_names = []
teacher_last_names = []

# New Class Scheduling Data
classes = []
student_registration = defaultdict(list)

# Home Route for Educators Dashboard
@app.route('/teachers_dashboard')
def teachers_dashboard():
    return render_template('teachers_dashboard.html')

# Route to Schedule a Class
@app.route('/schedule-class', methods=['POST'])
def schedule_class():
    data = request.json
    subject = data.get('subject')
    date = data.get('date')
    time_str = data.get('time')
    teacher = data.get('teacher')
    
    try:
        # Parse and store the date and time
        date_time = datetime.strptime(date + " " + time_str, "%d-%m-%Y %H:%M")
        classes.append({
            'subject': subject,
            'date_time': date_time,
            'teacher': teacher
        })
        return jsonify({"message": f"Class scheduled: {subject} on {date_time} by {teacher}", "status": "ok"}), 201
    except ValueError:
        return jsonify({"message": "Invalid date or time format. Please use DD-MM-YYYY for date and HH:MM for time.", "status": "error"}), 400

# Route to Register a Student
@app.route('/register-student', methods=['POST'])
def register_student():
    data = request.json
    student_name = data.get('student_name')
    section_number = int(data.get('section_number'))
    student_email = data.get('student_email')
    
    if 0 <= section_number < len(classes):
        subject = classes[section_number]['subject']
        student_registration[subject].append(student_name)
        return jsonify({"message": f"Student {student_name} registered for {subject}", "status": "ok"}), 201
    else:
        return jsonify({"message": "Invalid class index. Please enter a valid index.", "status": "error"}), 400

# Route to View Scheduled Classes
@app.route('/view-classes', methods=['GET'])
def view_classes():
    if not classes:
        return jsonify({"message": "No classes scheduled.", "status": "ok", "classes": []}), 200
    
    # Format the class information for display
    class_list = [
        {
            "index": i,
            "subject": cls['subject'],
            "date_time": cls['date_time'].strftime("%d-%m-%Y %H:%M"),
            "teacher": cls['teacher']
        }
        for i, cls in enumerate(classes)
    ]
    return jsonify({"classes": class_list, "status": "ok"}), 200
if __name__ == '__main__':
    app.run(debug=True)
