"""
Display utilities for formatting output
"""
from tabulate import tabulate
from typing import List, Dict, Any


def print_header(title: str, width: int = 80):
    """Print centered header"""
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def print_separator(char: str = "-", width: int = 100):
    """Print separator line"""
    print(char * width)


def display_students(students: List[Dict[str, Any]]):
    """Display student details in table format"""
    if not students:
        print_separator()
        print("❌ No students found in database")
        print_separator()
        return
    
    # Prepare data for display
    data = [[s['rollno'], s['name'], s['father']] for s in students]
    headers = ["Roll No.", "Name", "Father's Name"]
    
    print("\n📋 Student Details:\n")
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


def display_marks(marks_list: List[Dict[str, Any]]):
    """Display marks details in table format"""
    if not marks_list:
        print_separator()
        print("❌ No marks found in database")
        print_separator()
        return
    
    # Prepare data for display
    data = [[m['rollno'], m['dsp'], m['iot'], m['android'], m['compiler'], m['minor']] 
            for m in marks_list]
    headers = ["Roll No.", "DSP", "IOT", "Android", "Compiler", "Minor"]
    
    print("\n📊 Marks Details:\n")
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


def display_full_details(full_data: List[Dict[str, Any]]):
    """Display combined student and marks details"""
    if not full_data:
        print_separator()
        print("❌ No complete data found")
        print_separator()
        return
    
    # Prepare data for display with calculated totals
    data = []
    for item in full_data:
        total = item['dsp'] + item['iot'] + item['android'] + item['compiler'] + item['minor']
        percentage = (total / 500) * 100
        
        data.append([
            item['rollno'],
            item['name'],
            item['father'],
            item['dsp'],
            item['iot'],
            item['android'],
            item['compiler'],
            item['minor'],
            f"{total:.1f}",
            f"{percentage:.2f}%"
        ])
    
    headers = ["Roll No.", "Name", "Father's Name", "DSP", "IOT", 
               "Android", "Compiler", "Minor", "Total", "Percentage"]
    
    print("\n📋 Full Student + Marks Details:\n")
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


def display_student_detail(student: Dict[str, Any], marks: Dict[str, Any]):
    """Display individual student detail"""
    print_separator()
    print(f"📌 Roll No.: {student['rollno']}")
    print(f"👤 Name: {student['name']}")
    print(f"👨 Father's Name: {student['father']}")
    print_separator()
    print("📊 Marks:")
    print(f"   DSP:      {marks['dsp']}")
    print(f"   IOT:      {marks['iot']}")
    print(f"   Android:  {marks['android']}")
    print(f"   Compiler: {marks['compiler']}")
    print(f"   Minor:    {marks['minor']}")
    print_separator()
    total = marks['dsp'] + marks['iot'] + marks['android'] + marks['compiler'] + marks['minor']
    percentage = (total / 500) * 100
    print(f"📈 Total: {total:.1f} / 500")
    print(f"📊 Percentage: {percentage:.2f}%")
    print_separator()
