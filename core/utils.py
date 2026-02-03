try:
    from fpdf import FPDF
except ImportError:
    # This prevents the whole app from crashing if the module is missing
    FPDF = None

def create_pdf(text):
    if FPDF is None:
        return b"Error: fpdf module not found. Please run 'pip install fpdf'"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Remove markdown bolding for the PDF
    clean_text = text.replace("**", "")
    
    # Handle South African characters/encoding
    safe_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 10, txt=safe_text)
    
    return pdf.output(dest='S').encode('latin-1')