"""
Database setup script for Supabase
Run this script once to create the required tables
"""
from config.database import db
from utils.display import print_separator, print_header


def create_tables():
    """Create necessary tables in Supabase"""
    
    print_header("DATABASE SETUP", 80)
    print("\n🔧 Creating database tables...\n")
    
    try:
        # Note: In Supabase, you typically create tables via the SQL Editor in the dashboard
        # This script provides the SQL commands you need to run
        
        sql_commands = """
-- Students Table
CREATE TABLE IF NOT EXISTS students (
    rollno INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    father VARCHAR(100) NOT NULL,
    password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marks Table
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_students_rollno ON students(rollno);
CREATE INDEX IF NOT EXISTS idx_marks_rollno ON marks(rollno);

-- Enable Row Level Security (RLS)
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE marks ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (adjust based on your security needs)
CREATE POLICY "Enable all operations for students" ON students
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations for marks" ON marks
    FOR ALL USING (true) WITH CHECK (true);
"""
        
        print_separator()
        print("📋 SQL COMMANDS TO RUN IN SUPABASE SQL EDITOR:")
        print_separator()
        print(sql_commands)
        print_separator()
        print("\n📝 SETUP INSTRUCTIONS:")
        print("\n1. Go to your Supabase project dashboard")
        print("2. Click on 'SQL Editor' in the left sidebar")
        print("3. Copy and paste the SQL commands above")
        print("4. Click 'Run' to execute the commands")
        print("5. Verify that the tables were created in the 'Table Editor' section")
        print_separator()
        
        # Try to verify connection
        if db.is_connected():
            print("\n✅ Database connection successful!")
            print("✅ You can now run the main.py application")
        else:
            print("\n❌ Database connection failed!")
            print("⚠️  Please check your .env file configuration")
        
        print_separator()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print_separator()


def create_sample_data():
    """SQL for creating sample data"""
    
    sample_sql = """
-- Sample Students
INSERT INTO students (rollno, name, father, password) VALUES
    (101, 'JOHN DOE', 'ROBERT DOE', 'pass123'),
    (102, 'JANE SMITH', 'MICHAEL SMITH', 'pass456'),
    (103, 'ALEX JOHNSON', 'DAVID JOHNSON', 'pass789');

-- Sample Marks
INSERT INTO marks (rollno, dsp, iot, android, compiler, minor) VALUES
    (101, 85.5, 90.0, 78.5, 92.0, 88.0),
    (102, 92.0, 88.5, 95.0, 89.0, 91.5),
    (103, 78.0, 82.5, 85.0, 80.0, 87.5);
"""
    
    print("\n" + "="*80)
    print_header("SAMPLE DATA", 80)
    print("="*80)
    print("\n📋 OPTIONAL: Run this SQL to add sample data:")
    print_separator()
    print(sample_sql)
    print_separator()


if __name__ == "__main__":
    create_tables()
    
    print("\n")
    add_sample = input("Would you like to see sample data SQL? (yes/no): ").strip().lower()
    if add_sample == 'yes':
        create_sample_data()
    
    print("\n✅ Setup complete! Run main.py to start the application.")
