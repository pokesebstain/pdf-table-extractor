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
    elements.append(Paragraph("Business Report - Q1 2024", styles['Heading1']))
    elements.append(Spacer(1, 20))
    
    # Table 1: Department Performance
    data1 = [
        ['Department', 'Revenue', 'Expenses', 'Profit', 'Growth'],
        ['Sales', '$250,000', '$120,000', '$130,000', '15%'],
        ['Marketing', '$180,000', '$90,000', '$90,000', '12%'],
        ['IT', '$320,000', '$180,000', '$140,000', '18%'],
        ['HR', '$80,000', '$60,000', '$20,000', '5%']
    ]
    
    table1 = Table(data1, colWidths=[1*inch]*5)
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
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
    
    elements.append(Paragraph("Table 1: Department Performance", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table1)
    elements.append(Spacer(1, 30))
    
    # Table 2: Customer Satisfaction
    data2 = [
        ['Region', 'Q1 Score', 'Q2 Score', 'Q3 Score', 'Q4 Score'],
        ['North', '4.5', '4.6', '4.7', '4.8'],
        ['South', '4.3', '4.4', '4.5', '4.6'],
        ['East', '4.6', '4.7', '4.8', '4.9'],
        ['West', '4.4', '4.5', '4.6', '4.7']
    ]
    
    table2 = Table(data2, colWidths=[1*inch]*5)
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Table 2: Customer Satisfaction Scores", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table2)
    elements.append(Spacer(1, 30))
    
    # Table 3: Project Status
    data3 = [
        ['Project', 'Start Date', 'End Date', 'Budget', 'Status'],
        ['Mobile App', '2024-01-01', '2024-06-30', '$200,000', 'On Track'],
        ['Website Redesign', '2024-02-15', '2024-05-15', '$150,000', 'Delayed'],
        ['CRM Integration', '2024-03-01', '2024-08-31', '$300,000', 'On Track'],
        ['Cloud Migration', '2024-01-15', '2024-12-31', '$500,000', 'Ahead']
    ]
    
    table3 = Table(data3, colWidths=[1*inch]*5)
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
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
    
    elements.append(Paragraph("Table 3: Project Status Report", styles['Heading2']))
    elements.append(Spacer(1, 10))
    elements.append(table3)
    
    # Generate PDF
    doc.build(elements)

if __name__ == '__main__':
    create_sample_pdf('business_report.pdf')
    print("PDF file generated: business_report.pdf") 