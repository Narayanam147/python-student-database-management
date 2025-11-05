"""
Marks model for database operations
"""
from typing import Optional, List, Dict, Any
from config.database import db


class Marks:
    """Marks model class"""
    
    TABLE_NAME = "marks"
    
    def __init__(self, rollno: int, dsp: float, iot: float, android: float, 
                 compiler: float, minor: float):
        self.rollno = rollno
        self.dsp = dsp
        self.iot = iot
        self.android = android
        self.compiler = compiler
        self.minor = minor
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert marks object to dictionary"""
        return {
            "rollno": self.rollno,
            "dsp": self.dsp,
            "iot": self.iot,
            "android": self.android,
            "compiler": self.compiler,
            "minor": self.minor
        }
    
    def total(self) -> float:
        """Calculate total marks"""
        return self.dsp + self.iot + self.android + self.compiler + self.minor
    
    def percentage(self) -> float:
        """Calculate percentage (assuming 100 marks per subject)"""
        return (self.total() / 500) * 100
    
    @staticmethod
    def create(rollno: int, dsp: float, iot: float, android: float, 
               compiler: float, minor: float) -> bool:
        """Create marks record"""
        try:
            marks = Marks(rollno, dsp, iot, android, compiler, minor)
            result = db.client.table(Marks.TABLE_NAME).insert(marks.to_dict()).execute()
            
            if result.data:
                print("✅ Marks record created successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error creating marks: {e}")
            return False
    
    @staticmethod
    def get_by_rollno(rollno: int) -> Optional[Dict[str, Any]]:
        """Get marks by roll number"""
        try:
            result = db.client.table(Marks.TABLE_NAME).select("*").eq("rollno", rollno).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"❌ Error fetching marks: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all marks"""
        try:
            result = db.client.table(Marks.TABLE_NAME).select("*").order("rollno").execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"❌ Error fetching marks: {e}")
            return []
    
    @staticmethod
    def update(rollno: int, **kwargs) -> bool:
        """Update marks record"""
        try:
            result = db.client.table(Marks.TABLE_NAME).update(kwargs).eq("rollno", rollno).execute()
            
            if result.data:
                print("✅ Marks updated successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error updating marks: {e}")
            return False
    
    @staticmethod
    def delete(rollno: int) -> bool:
        """Delete marks record"""
        try:
            result = db.client.table(Marks.TABLE_NAME).delete().eq("rollno", rollno).execute()
            
            if result.data:
                print("✅ Marks record deleted successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting marks: {e}")
            return False
    
    @staticmethod
    def get_full_details() -> List[Dict[str, Any]]:
        """Get combined student and marks data"""
        try:
            # Get all students
            students_result = db.client.table("students").select("*").order("rollno").execute()
            students = students_result.data if students_result.data else []
            
            # Get all marks
            marks_result = db.client.table("marks").select("*").order("rollno").execute()
            marks = marks_result.data if marks_result.data else []
            
            # Combine data
            full_data = []
            marks_dict = {m['rollno']: m for m in marks}
            
            for student in students:
                rollno = student['rollno']
                if rollno in marks_dict:
                    combined = {
                        **student,
                        **marks_dict[rollno]
                    }
                    # Remove duplicate rollno
                    full_data.append(combined)
            
            return full_data
        except Exception as e:
            print(f"❌ Error fetching full details: {e}")
            return []
