"""
Student operations - CRUD operations for students
"""
from models.student import Student
from models.marks import Marks
from utils.display import print_separator, display_students, display_marks, display_full_details, display_student_detail


def accept_student():
    """Accept new student data"""
    print_separator()
    print("➕ Add New Student")
    print_separator()
    
    try:
        rollno = int(input("Enter Roll No.: "))
        
        # Check if student exists
        existing = Student.get_by_rollno(rollno)
        if existing:
            print_separator()
            print("❌ Student with this Roll No. already exists!")
            print_separator()
            return
        
        name = input("Enter Name: ").strip()
        father = input("Enter Father's Name: ").strip()
        password = input("Enter Password: ").strip()
        
        if not name or not father or not password:
            print("❌ All fields are required!")
            return
        
        print_separator()
        print("📊 Enter Marks (out of 100):")
        print_separator()
        
        dsp = float(input("DSP: "))
        iot = float(input("IOT: "))
        android = float(input("Android: "))
        compiler = float(input("Compiler: "))
        minor = float(input("Minor: "))
        
        # Validate marks
        marks_list = [dsp, iot, android, compiler, minor]
        if any(mark < 0 or mark > 100 for mark in marks_list):
            print("❌ Marks must be between 0 and 100!")
            return
        
        # Create student and marks records
        student_created = Student.create(rollno, name, father, password)
        if student_created:
            marks_created = Marks.create(rollno, dsp, iot, android, compiler, minor)
            if not marks_created:
                # Rollback student creation if marks creation fails
                Student.delete(rollno)
                print("❌ Failed to create student record")
        
    except ValueError:
        print("❌ Invalid input! Please enter valid numbers.")
    except Exception as e:
        print(f"❌ Error: {e}")


def display_students_data():
    """Display student data with options"""
    print_separator()
    print("📋 Display Options:")
    print("1. Student Details Only")
    print("2. Marks Details Only")
    print("3. Full Details (Student + Marks)")
    print_separator()
    
    try:
        choice = int(input("Enter your choice (1-3): "))
        print_separator()
        
        if choice == 1:
            students = Student.get_all()
            display_students(students)
        elif choice == 2:
            marks = Marks.get_all()
            display_marks(marks)
        elif choice == 3:
            full_data = Marks.get_full_details()
            display_full_details(full_data)
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Invalid input! Please enter a number.")
    except Exception as e:
        print(f"❌ Error: {e}")


def search_student():
    """Search for a student's data"""
    print_separator()
    print("🔍 Search Student")
    print_separator()
    
    try:
        rollno = int(input("Enter Roll No.: "))
        
        # Get student data
        student = Student.get_by_rollno(rollno)
        
        if not student:
            print_separator()
            print("❌ Invalid Roll No. - Student not found!")
            print_separator()
            return
        
        print_separator()
        print(f"✅ Roll No. {rollno} found!")
        print_separator()
        
        # Verify credentials
        name = input("Enter Name: ").strip()
        if name.upper() != student['name'].upper():
            print_separator()
            print("❌ Wrong Name!")
            print_separator()
            return
        
        password = input("Enter Password: ").strip()
        if password != student['password']:
            print_separator()
            print("❌ Wrong Password!")
            print_separator()
            return
        
        # Get marks
        marks = Marks.get_by_rollno(rollno)
        
        if marks:
            display_student_detail(student, marks)
        else:
            print_separator()
            print("⚠️ No marks found for this student")
            print_separator()
            
    except ValueError:
        print("❌ Invalid input! Please enter a valid Roll No.")
    except Exception as e:
        print(f"❌ Error: {e}")


def update_student():
    """Update student data"""
    print_separator()
    print("✏️ Update Student Data")
    print_separator()
    
    try:
        rollno = int(input("Enter Roll No.: "))
        
        # Get student data
        student = Student.get_by_rollno(rollno)
        
        if not student:
            print_separator()
            print("❌ Invalid Roll No. - Student not found!")
            print_separator()
            return
        
        # Verify credentials
        name = input("Enter Name: ").strip()
        if name.upper() != student['name'].upper():
            print_separator()
            print("❌ Wrong Name!")
            print_separator()
            return
        
        password = input("Enter Password: ").strip()
        if password != student['password']:
            print_separator()
            print("❌ Wrong Password!")
            print_separator()
            return
        
        # Update menu
        while True:
            print_separator()
            print("Update Options:")
            print("1. Update Name")
            print("2. Update Father's Name")
            print("3. Update Password")
            print("4. Update Marks")
            print("5. Exit")
            print_separator()
            
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                new_name = input("Enter new Name: ").strip()
                if new_name:
                    Student.update(rollno, name=new_name)
            
            elif choice == 2:
                new_father = input("Enter new Father's Name: ").strip()
                if new_father:
                    Student.update(rollno, father=new_father)
            
            elif choice == 3:
                while True:
                    new_password = input("Enter new Password: ").strip()
                    if new_password == password:
                        print("❌ New password cannot be the same as old password!")
                    else:
                        confirm_password = input("Re-enter new Password: ").strip()
                        if new_password == confirm_password:
                            Student.update(rollno, password=new_password)
                            password = new_password  # Update local variable
                            break
                        else:
                            print("❌ Passwords do not match!")
            
            elif choice == 4:
                update_marks_submenu(rollno)
            
            elif choice == 5:
                break
            
            else:
                print("❌ Invalid choice!")
                
    except ValueError:
        print("❌ Invalid input!")
    except Exception as e:
        print(f"❌ Error: {e}")


def update_marks_submenu(rollno: int):
    """Submenu for updating marks"""
    while True:
        print_separator()
        print("Select Subject to Update:")
        print("1. DSP")
        print("2. IOT")
        print("3. Android")
        print("4. Compiler")
        print("5. Minor")
        print("6. Back to Main Update Menu")
        print_separator()
        
        try:
            choice = int(input("Enter your choice: "))
            
            if choice == 6:
                break
            
            if choice < 1 or choice > 5:
                print("❌ Invalid choice!")
                continue
            
            mark = float(input(f"Enter new marks (0-100): "))
            
            if mark < 0 or mark > 100:
                print("❌ Marks must be between 0 and 100!")
                continue
            
            subject_map = {
                1: 'dsp',
                2: 'iot',
                3: 'android',
                4: 'compiler',
                5: 'minor'
            }
            
            subject = subject_map[choice]
            Marks.update(rollno, **{subject: mark})
            
        except ValueError:
            print("❌ Invalid input!")
        except Exception as e:
            print(f"❌ Error: {e}")


def delete_student():
    """Delete student data"""
    print_separator()
    print("🗑️ Delete Student")
    print_separator()
    
    try:
        rollno = int(input("Enter Roll No.: "))
        
        # Get student data
        student = Student.get_by_rollno(rollno)
        
        if not student:
            print_separator()
            print("❌ Invalid Roll No. - Student not found!")
            print_separator()
            return
        
        # Verify credentials
        name = input("Enter Name: ").strip()
        if name.upper() != student['name'].upper():
            print_separator()
            print("❌ Wrong Name!")
            print_separator()
            return
        
        password = input("Enter Password: ").strip()
        if password != student['password']:
            print_separator()
            print("❌ Wrong Password!")
            print_separator()
            return
        
        # Confirm deletion
        print_separator()
        confirm = input("⚠️ Are you sure you want to delete this student? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            # Delete marks first (foreign key constraint)
            Marks.delete(rollno)
            # Delete student
            Student.delete(rollno)
            print_separator()
            print("✅ Student deleted successfully!")
        else:
            print("❌ Deletion cancelled!")
        
        print_separator()
        
    except ValueError:
        print("❌ Invalid input!")
    except Exception as e:
        print(f"❌ Error: {e}")
