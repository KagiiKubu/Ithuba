from fpdf import FPDF
try:
    from unidecode import unidecode
except ImportError:
    def unidecode(text): return text

def create_pdf(text):
    try:
        # Initialize FPDF
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Define printable area
        L_MARGIN = 20
        R_MARGIN = 20
        WIDTH = 210 - L_MARGIN - R_MARGIN
        
        pdf.set_left_margin(L_MARGIN)
        pdf.set_right_margin(R_MARGIN)
        
        # Clean text for PDF compatibility
        clean_text = unidecode(str(text))
        lines = clean_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Reset X to left margin for every line to prevent "drift"
            pdf.set_x(L_MARGIN)
            
            if not line:
                pdf.ln(5) # Add space for empty lines
                continue
                
            if line.startswith('#'):
                # Main Headers
                pdf.set_font("Helvetica", 'B', size=16)
                clean_line = line.lstrip('#').strip()
                pdf.multi_cell(WIDTH, 10, txt=clean_line, align='L')
                pdf.ln(2)
            elif line.startswith('**') or line.startswith('##'):
                # Sub-headers
                pdf.set_font("Helvetica", 'B', size=12)
                clean_line = line.replace('**', '').replace('##', '').strip()
                pdf.multi_cell(WIDTH, 8, txt=clean_line, align='L')
            else:
                # Body Text
                pdf.set_font("Helvetica", size=11)
                clean_line = line.replace('**', '').replace('*', '').strip()
                pdf.multi_cell(WIDTH, 6, txt=clean_line, align='L')

        # Return as stable bytes for Streamlit
        return bytes(pdf.output())
    except Exception as e:
        print(f"CRITICAL PDF ERROR: {e}")
        return None