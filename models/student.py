"""
Student model for database operations
"""
from typing import Optional, List, Dict, Any
from config.database import db


class Student:
    """Student model class"""
    
    TABLE_NAME = "students"
    
    def __init__(self, rollno: int, name: str, father: str, password: str):
        self.rollno = rollno
        self.name = name.upper()
        self.father = father.upper()
        self.password = password
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert student object to dictionary"""
        return {
            "rollno": self.rollno,
            "name": self.name,
            "father": self.father,
            "password": self.password
        }
    
    @staticmethod
    def create(rollno: int, name: str, father: str, password: str) -> bool:
        """Create a new student record"""
        try:
            # Check if student already exists
            existing = db.client.table(Student.TABLE_NAME).select("rollno").eq("rollno", rollno).execute()
            
            if existing.data:
                print("❌ Student with this roll number already exists")
                return False
            
            student = Student(rollno, name, father, password)
            result = db.client.table(Student.TABLE_NAME).insert(student.to_dict()).execute()
            
            if result.data:
                print("✅ Student record created successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error creating student: {e}")
            return False
    
    @staticmethod
    def get_by_rollno(rollno: int) -> Optional[Dict[str, Any]]:
        """Get student by roll number"""
        try:
            result = db.client.table(Student.TABLE_NAME).select("*").eq("rollno", rollno).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error fetching student: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all students"""
        try:
            result = db.client.table(Student.TABLE_NAME).select("*").order("rollno").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"❌ Error fetching students: {e}")
            return []
    
    @staticmethod
    def update(rollno: int, **kwargs) -> bool:
        """Update student record"""
        try:
            # Convert name and father to uppercase if provided
            if 'name' in kwargs:
                kwargs['name'] = kwargs['name'].upper()
            if 'father' in kwargs:
                kwargs['father'] = kwargs['father'].upper()
            
            result = db.client.table(Student.TABLE_NAME).update(kwargs).eq("rollno", rollno).execute()
            
            if result.data:
                print("✅ Student record updated successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error updating student: {e}")
            return False
    
    @staticmethod
    def delete(rollno: int) -> bool:
        """Delete student record"""
        try:
            result = db.client.table(Student.TABLE_NAME).delete().eq("rollno", rollno).execute()
            
            if result.data:
                print("✅ Student record deleted successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting student: {e}")
            return False
    
    @staticmethod
    def verify_credentials(rollno: int, name: str, password: str) -> bool:
        """Verify student credentials"""
        try:
            student = Student.get_by_rollno(rollno)
            
            if not student:
                return False
            
            return (student['name'].upper() == name.upper() and 
                    student['password'] == password)
        except Exception as e:
            print(f"❌ Error verifying credentials: {e}")
            return False
