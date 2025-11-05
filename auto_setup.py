"""
Automatic database table creation for Supabase
"""
from config.database import db
from utils.display import print_separator, print_header


def create_tables_automatically():
    """Create tables directly using Supabase SQL execution"""
    
    print_header("DATABASE AUTO-SETUP", 80)
    print("\n🔧 Creating database tables automatically...\n")
    
    try:
        # SQL commands to create tables
        create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
            rollno INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            father VARCHAR(100) NOT NULL,
            password VARCHAR(50) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_marks_table = """
        CREATE TABLE IF NOT EXISTS marks (
            id SERIAL PRIMARY KEY,
            rollno INTEGER UNIQUE NOT NULL,
            dsp DECIMAL(5,2) NOT NULL CHECK (dsp >= 0 AND dsp <= 100),
            iot DECIMAL(5,2) NOT NULL CHECK (iot >= 0 AND iot <= 100),
            android DECIMAL(5,2) NOT NULL CHECK (android >= 0 AND android <= 100),
            compiler DECIMAL(5,2) NOT NULL CHECK (compiler >= 0 AND compiler <= 100),
            minor DECIMAL(5,2) NOT NULL CHECK (minor >= 0 AND minor <= 100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rollno) REFERENCES students(rollno) ON DELETE CASCADE
        );
        """
        
        print("Creating 'students' table...")
        db.client.rpc('exec_sql', {'query': create_students_table}).execute()
        print("✅ Students table created")
        
        print("Creating 'marks' table...")
        db.client.rpc('exec_sql', {'query': create_marks_table}).execute()
        print("✅ Marks table created")
        
        print_separator()
        print("\n✅ Database setup complete!")
        print("✅ You can now run main.py to use the application")
        print_separator()
        
    except Exception as e:
        print(f"\n⚠️ Note: {e}")
        print("\n📋 Please run these SQL commands manually in Supabase SQL Editor:")
        print_separator()
        print(create_students_table)
        print(create_marks_table)
        print_separator()
        print("\nSteps:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Click 'SQL Editor' in sidebar")
        print("4. Copy and paste the above SQL")
        print("5. Click 'Run'")
        print_separator()


if __name__ == "__main__":
    if db.is_connected():
        create_tables_automatically()
    else:
        print("❌ Failed to connect to database. Check your .env file.")
