"""
Student Database Management System
Main application file with Supabase integration
"""
import sys
from config.database import db
from operations.student_ops import (
    accept_student,
    display_students_data,
    search_student,
    update_student,
    delete_student
)
from models.marks import Marks
from utils.display import print_header, print_separator
from utils.export import export_to_excel, export_to_pdf


def display_menu():
    """Display main menu"""
    print_separator('=', 80)
    print_header("STUDENT DATABASE MANAGEMENT SYSTEM", 80)
    print_separator('=', 80)
    print_separator()
    print("""
    📚 MENU OPTIONS:
    
    1. ➕ Add New Student
    2. 📋 Display Student Data
    3. 🔍 Search Student
    4. ✏️  Update Student Data
    5. 🗑️  Delete Student
    6. 📊 Export to Excel
    7. 📄 Export to PDF
    8. ❌ Exit
    """)
    print_separator('=', 80)


def main():
    """Main application loop"""
    
    # Check database connection
    if not db.is_connected():
        print_separator()
        print("❌ Failed to connect to database!")
        print("\n⚙️  Setup Instructions:")
        print("1. Create a Supabase account at https://supabase.com")
        print("2. Create a new project")
        print("3. Copy the .env.example file to .env")
        print("4. Add your Supabase URL and API key to the .env file")
        print("5. Run the setup_database.py script to create tables")
        print_separator()
        sys.exit(1)
    
    display_menu()
    
    while True:
        print_separator()
        try:
            choice = input("Enter your choice (0 to show menu): ").strip()
            
            if choice == "":
                print("❌ Invalid input. Please enter a number from 0 to 8.")
                continue
            
            choice = int(choice)
            
            if choice == 0:
                display_menu()
            
            elif choice == 1:
                accept_student()
            
            elif choice == 2:
                display_students_data()
            
            elif choice == 3:
                search_student()
            
            elif choice == 4:
                update_student()
            
            elif choice == 5:
                delete_student()
            
            elif choice == 6:
                data = Marks.get_full_details()
                export_to_excel(data)
            
            elif choice == 7:
                data = Marks.get_full_details()
                export_to_pdf(data)
            
            elif choice == 8:
                print_separator()
                print("\n" + "="*80)
                print_header("THANK YOU FOR USING STUDENT DATABASE MANAGEMENT SYSTEM", 80)
                print("="*80 + "\n")
                print("Press any key to exit...")
                input()
                break
            
            else:
                print("❌ Invalid choice! Please enter a number between 0 and 8.")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n❌ Program interrupted by user.")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
