from fpdf import FPDF

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Simple formatting: Replace markdown bold with plain text for now
    clean_text = text.replace("**", "")
    
    # Multi_cell handles word wrapping
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # Return the PDF as bytes
    return pdf.output(dest='S').encode('latin-1')