"""
Test export functionality
"""
from models.marks import Marks
from utils.export import export_to_excel, export_to_pdf

print("Testing export functionality...\n")

# Get data
data = Marks.get_full_details()
print(f"Found {len(data)} students to export\n")

if data:
    # Test Excel export
    print("=" * 60)
    print("Testing Excel Export...")
    print("=" * 60)
    success = export_to_excel(data, "test_export.xlsx")
    print(f"Excel export: {'✅ SUCCESS' if success else '❌ FAILED'}\n")
    
    # Test PDF export
    print("=" * 60)
    print("Testing PDF Export...")
    print("=" * 60)
    success = export_to_pdf(data, "test_export.pdf")
    print(f"PDF export: {'✅ SUCCESS' if success else '❌ FAILED'}\n")
else:
    print("❌ No data found in database")
