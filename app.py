"""
Flask Web Application for Student Database Management System
"""
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from config.database import db
from models.student import Student
from models.marks import Marks
from utils.export import export_to_excel, export_to_pdf
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Ensure exports directory exists
os.makedirs("exports", exist_ok=True)


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/check-connection')
def check_connection():
    """Check database connection"""
    if db.is_connected():
        return jsonify({'success': True, 'message': 'Connected to Supabase'})
    return jsonify({'success': False, 'message': 'Database connection failed'}), 500


@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = Student.get_all()
        return jsonify({'success': True, 'data': students})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/students/<int:rollno>', methods=['GET'])
def get_student(rollno):
    """Get student by roll number"""
    try:
        student = Student.get_by_rollno(rollno)
        if student:
            marks = Marks.get_by_rollno(rollno)
            return jsonify({'success': True, 'student': student, 'marks': marks})
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def add_student():
    """Add new student"""
    try:
        data = request.json
        
        # Create student
        student_created = Student.create(
            data['rollno'],
            data['name'],
            data['father'],
            data['password']
        )
        
        if student_created:
            # Create marks
            marks_created = Marks.create(
                data['rollno'],
                float(data['dsp']),
                float(data['iot']),
                float(data['android']),
                float(data['compiler']),
                float(data['minor'])
            )
            
            if marks_created:
                return jsonify({'success': True, 'message': 'Student added successfully'})
            else:
                # Rollback student creation
                Student.delete(data['rollno'])
                return jsonify({'success': False, 'message': 'Failed to add marks'}), 500
        
        return jsonify({'success': False, 'message': 'Failed to add student'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/students/verify', methods=['POST'])
def verify_student():
    """Verify student credentials"""
    try:
        data = request.json
        verified = Student.verify_credentials(
            data['rollno'],
            data['name'],
            data['password']
        )
        
        if verified:
            session['logged_in'] = True
            session['rollno'] = data['rollno']
            return jsonify({'success': True, 'message': 'Verified successfully'})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/students/<int:rollno>', methods=['PUT'])
def update_student(rollno):
    """Update student"""
    try:
        data = request.json
        
        # Verify credentials first
        student = Student.get_by_rollno(rollno)
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'}), 404
        
        if data.get('name') and data['name'].upper() != student['name'].upper():
            return jsonify({'success': False, 'message': 'Name verification failed'}), 401
        
        if data.get('password') and data['password'] != student['password']:
            return jsonify({'success': False, 'message': 'Password verification failed'}), 401
        
        # Update student info
        if 'new_name' in data:
            Student.update(rollno, name=data['new_name'])
        if 'new_father' in data:
            Student.update(rollno, father=data['new_father'])
        if 'new_password' in data:
            Student.update(rollno, password=data['new_password'])
        
        # Update marks
        marks_update = {}
        for subject in ['dsp', 'iot', 'android', 'compiler', 'minor']:
            if subject in data:
                marks_update[subject] = float(data[subject])
        
        if marks_update:
            Marks.update(rollno, **marks_update)
        
        return jsonify({'success': True, 'message': 'Updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/students/<int:rollno>', methods=['DELETE'])
def delete_student(rollno):
    """Delete student"""
    try:
        data = request.json
        
        # Verify credentials
        verified = Student.verify_credentials(
            rollno,
            data['name'],
            data['password']
        )
        
        if not verified:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Delete marks first (foreign key)
        Marks.delete(rollno)
        # Delete student
        Student.delete(rollno)
        
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/full-details', methods=['GET'])
def get_full_details():
    """Get combined student and marks data"""
    try:
        data = Marks.get_full_details()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/export/excel', methods=['GET'])
def export_excel():
    """Export to Excel"""
    try:
        data = Marks.get_full_details()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Student_Report_{timestamp}.xlsx"
        
        if export_to_excel(data, filename):
            filepath = os.path.join("exports", filename)
            return send_file(filepath, as_attachment=True)
        
        return jsonify({'success': False, 'message': 'Export failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    """Export to PDF"""
    try:
        data = Marks.get_full_details()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Student_Report_{timestamp}.pdf"
        
        if export_to_pdf(data, filename):
            filepath = os.path.join("exports", filename)
            return send_file(filepath, as_attachment=True)
        
        return jsonify({'success': False, 'message': 'Export failed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/marks', methods=['GET'])
def get_marks():
    """Get all marks"""
    try:
        marks = Marks.get_all()
        return jsonify({'success': True, 'data': marks})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    if db.is_connected():
        print("✅ Database connected successfully!")
        print("🚀 Starting Flask server...")
        print("📱 Open http://localhost:5000 in your browser")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Database connection failed! Check your .env file.")
