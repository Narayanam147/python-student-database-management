# Student Database Management System

A comprehensive Python-based Student Database Management System using **Supabase** as the backend database. This system allows you to manage student records, marks, and generate reports in Excel and PDF formats.

## 🌟 Features

- ✅ **Add Student Records** - Add new students with their personal details and marks
- 📋 **Display Records** - View student details, marks, or combined data in formatted tables
- 🔍 **Search Students** - Search for specific student records with authentication
- ✏️ **Update Records** - Modify student information and marks
- 🗑️ **Delete Records** - Remove student records from the database
- 📊 **Export to Excel** - Generate Excel reports with student data
- 📄 **Export to PDF** - Create professionally formatted PDF reports
- 🔒 **Authentication** - Password-based authentication for sensitive operations
- 🎨 **Beautiful UI** - Clean terminal interface with formatted tables

## 📁 Project Structure

```
Student DBMS/
│
├── config/
│   ├── __init__.py
│   └── database.py          # Database connection configuration
│
├── models/
│   ├── __init__.py
│   ├── student.py           # Student model and operations
│   └── marks.py             # Marks model and operations
│
├── operations/
│   ├── __init__.py
│   └── student_ops.py       # CRUD operations for students
│
├── utils/
│   ├── __init__.py
│   ├── display.py           # Display formatting utilities
│   └── export.py            # Export functions (Excel, PDF)
│
├── exports/                 # Generated reports directory
│
├── main.py                  # Main application entry point
├── setup_database.py        # Database setup script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Supabase account (free tier available)

### Step 1: Clone or Download the Project

```bash
cd "c:\Users\ASUS\Desktop\Student DBMS"
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Set Up Supabase

1. Go to [Supabase](https://supabase.com) and create a free account
2. Create a new project
3. Note down your:
   - **Project URL** (found in Settings > API)
   - **Anon/Public Key** (found in Settings > API)

### Step 4: Configure Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```env
   SUPABASE_URL=your_supabase_project_url_here
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

### Step 5: Create Database Tables

1. Run the setup script:
   ```powershell
   python setup_database.py
   ```

2. Copy the displayed SQL commands

3. Go to your Supabase Dashboard → SQL Editor

4. Paste and run the SQL commands

5. Verify tables are created in Table Editor

## 🎮 Usage

### Running the Application

```powershell
python main.py
```

### Main Menu Options

```
1. ➕ Add New Student        - Register a new student with marks
2. 📋 Display Student Data   - View records in table format
3. 🔍 Search Student         - Find specific student details
4. ✏️  Update Student Data   - Modify existing records
5. 🗑️  Delete Student        - Remove student from database
6. 📊 Export to Excel        - Generate Excel report
7. 📄 Export to PDF          - Generate PDF report
8. ❌ Exit                   - Close application
```

### Example Workflow

1. **Add a Student**:
   - Select option 1
   - Enter roll number, name, father's name, and password
   - Enter marks for all subjects (DSP, IOT, Android, Compiler, Minor)

2. **View All Students**:
   - Select option 2
   - Choose display format (Student details, Marks, or Full details)

3. **Search for a Student**:
   - Select option 3
   - Enter roll number, name, and password
   - View complete student details with marks and percentage

4. **Export Reports**:
   - Select option 6 for Excel or 7 for PDF
   - Files are saved in the `exports/` directory

## 📊 Database Schema

### Students Table
| Column | Type | Description |
|--------|------|-------------|
| rollno | INTEGER | Primary Key - Student Roll Number |
| name | VARCHAR(100) | Student's Name |
| father | VARCHAR(100) | Father's Name |
| password | VARCHAR(50) | Authentication Password |
| created_at | TIMESTAMP | Record Creation Time |

### Marks Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary Key (Auto-increment) |
| rollno | INTEGER | Foreign Key → students(rollno) |
| dsp | DECIMAL(5,2) | DSP Subject Marks (0-100) |
| iot | DECIMAL(5,2) | IOT Subject Marks (0-100) |
| android | DECIMAL(5,2) | Android Subject Marks (0-100) |
| compiler | DECIMAL(5,2) | Compiler Subject Marks (0-100) |
| minor | DECIMAL(5,2) | Minor Subject Marks (0-100) |
| created_at | TIMESTAMP | Record Creation Time |
| updated_at | TIMESTAMP | Last Update Time |

## 🔒 Security Features

- **Password Protection**: All sensitive operations require authentication
- **Input Validation**: Validates all user inputs
- **Row Level Security**: Supabase RLS enabled for data protection
- **Environment Variables**: Sensitive credentials stored securely

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Supabase** - PostgreSQL database and backend
- **pandas** - Data manipulation and Excel export
- **openpyxl** - Excel file handling
- **reportlab** - PDF generation
- **matplotlib** - Data visualization
- **tabulate** - Formatted table display
- **python-dotenv** - Environment variable management

## 📝 Notes

- Marks are validated to be between 0 and 100
- Total marks are calculated out of 500 (5 subjects × 100 marks)
- Percentage is automatically calculated in reports
- Exported files are timestamped to avoid overwriting

## 🐛 Troubleshooting

### Connection Issues
- Verify `.env` file has correct Supabase credentials
- Check internet connection
- Ensure Supabase project is active

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Use a virtual environment if needed

### Table Not Found
- Run `setup_database.py` again
- Verify SQL commands were executed in Supabase

## 📧 Support

For issues or questions, please check:
1. Your Supabase dashboard for connection status
2. Python version compatibility (3.8+)
3. All dependencies are installed correctly

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Original Author

Migrated from MySQL to Supabase with enhanced features and modern architecture.

---

**Enjoy managing your student database! 🎓**
