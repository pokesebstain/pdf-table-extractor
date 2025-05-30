from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def create_sample_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    elements.append(Paragraph("Sample PDF File - Multiple Tables", styles['Heading1']))
    elements.append(Spacer(1, 20))
    
    # Table 1: Student Grades
    data1 = [
        ['Student ID', 'Name', 'English', 'Math', 'Science'],
        ['001', 'John Smith', '88', '92', '85'],
        ['002', 'Emma Davis', '92', '88', '90'],
        ['003', 'Michael Wilson', '85', '95', '88'],
        ['004', 'Sarah Brown', '90', '87', '92']
    ]
    
    table1 = Table(data1, colWidths=[1*inch]*5)
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Table 1: Student Grades", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table1)
    elements.append(Spacer(1, 30))
    
    # Table 2: Product Sales
    data2 = [
        ['Product ID', 'Product Name', 'Price', 'Quantity', 'Total'],
        ['P001', 'Laptop', '1299', '50', '64950'],
        ['P002', 'Smartphone', '799', '100', '79900'],
        ['P003', 'Tablet', '499', '75', '37425'],
        ['P004', 'Smartwatch', '299', '150', '44850']
    ]
    
    table2 = Table(data2, colWidths=[1*inch]*5)
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Table 2: Product Sales", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table2)
    elements.append(Spacer(1, 30))
    
    # Table 3: Monthly Expenses
    data3 = [
        ['Month', 'Rent', 'Utilities', 'Transport', 'Food'],
        ['January', '1500', '200', '150', '400'],
        ['February', '1500', '180', '140', '380'],
        ['March', '1500', '220', '160', '420'],
        ['April', '1500', '190', '145', '390']
    ]
    
    table3 = Table(data3, colWidths=[1*inch]*5)
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Table 3: Monthly Expenses", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table3)
    
    # Generate PDF
    doc.build(elements)

if __name__ == '__main__':
    create_sample_pdf('sample_tables_en.pdf')
    print("PDF file generated: sample_tables_en.pdf") 