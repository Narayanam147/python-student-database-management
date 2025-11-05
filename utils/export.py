"""
Export utilities for generating Excel and PDF reports
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def export_to_excel(data: List[Dict[str, Any]], filename: str = None) -> bool:
    """Export data to Excel file"""
    try:
        if not data:
            print("❌ No data available to export")
            return False
        
        # Prepare DataFrame
        df_data = []
        for item in data:
            total = item['dsp'] + item['iot'] + item['android'] + item['compiler'] + item['minor']
            percentage = (total / 500) * 100
            
            df_data.append({
                "Roll No.": item['rollno'],
                "Name": item['name'],
                "Father's Name": item['father'],
                "DSP": item['dsp'],
                "IOT": item['iot'],
                "Android": item['android'],
                "Compiler": item['compiler'],
                "Minor": item['minor'],
                "Total": total,
                "Percentage": f"{percentage:.2f}%"
            })
        
        df = pd.DataFrame(df_data)
        
        # Generate filename with timestamp if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Student_Report_{timestamp}.xlsx"
        
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        filepath = os.path.join("exports", filename)
        
        # Export to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        print(f"\n✅ Data successfully exported to Excel: {filepath}")
        
        # Try to open the file
        try:
            os.startfile(filepath)
        except:
            print(f"📁 File saved at: {os.path.abspath(filepath)}")
        
        return True
        
    except PermissionError:
        print(f"\n❌ ERROR: Cannot write to file — please close the file if it's open and try again.")
        return False
    except Exception as e:
        print(f"\n❌ Error exporting to Excel: {e}")
        return False


def export_to_pdf(data: List[Dict[str, Any]], filename: str = None) -> bool:
    """Export data to PDF file using ReportLab"""
    try:
        if not data:
            print("❌ No data available to export")
            return False
        
        # Generate filename with timestamp if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Student_Report_{timestamp}.pdf"
        
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        filepath = os.path.join("exports", filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Title
        title = Paragraph("Student Marks Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Prepare table data
        table_data = [["Roll No.", "Name", "Father's Name", "DSP", "IOT", 
                      "Android", "Compiler", "Minor", "Total", "%"]]
        
        for item in data:
            total = item['dsp'] + item['iot'] + item['android'] + item['compiler'] + item['minor']
            percentage = (total / 500) * 100
            
            table_data.append([
                str(item['rollno']),
                item['name'],
                item['father'],
                str(item['dsp']),
                str(item['iot']),
                str(item['android']),
                str(item['compiler']),
                str(item['minor']),
                f"{total:.1f}",
                f"{percentage:.1f}"
            ])
        
        # Create table
        table = Table(table_data, repeatRows=1)
        
        # Table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(table)
        
        # Add footer
        elements.append(Spacer(1, 0.5 * inch))
        footer_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer = Paragraph(footer_text, styles['Normal'])
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        print(f"\n✅ Data successfully exported to PDF: {filepath}")
        
        # Try to open the file
        try:
            os.startfile(filepath)
        except:
            print(f"📁 File saved at: {os.path.abspath(filepath)}")
        
        return True
        
    except PermissionError:
        print(f"\n❌ ERROR: Cannot write to file — please close the file if it's open and try again.")
        return False
    except Exception as e:
        print(f"\n❌ Error exporting to PDF: {e}")
        return False
