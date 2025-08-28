from fpdf import FPDF

def create_sample_contract():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SERVICE AGREEMENT CONTRACT", ln=1, align='C')
    pdf.ln(10)
    
    # Jurisdiction
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. JURISDICTION", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This Agreement shall be governed by and construed in accordance with the laws of the State of California, United States. Any dispute arising under this Agreement shall be subject to the exclusive jurisdiction of the courts of California.", align='L')
    pdf.ln(10)
    
    # Confidentiality
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. CONFIDENTIALITY", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="The parties agree to maintain the confidentiality of any proprietary information shared during the course of this agreement. This includes but is not limited to trade secrets, customer data, and technical specifications.", align='L')
    pdf.ln(10)
    
    # Payment Terms
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="3. PAYMENT TERMS", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Payment shall be made within 30 days of invoice receipt. A late payment fee of 2% per month will be applied to any overdue amounts. All fees are non-refundable unless otherwise specified in writing.", align='L')
    pdf.ln(10)
    
    # Termination
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="4. TERMINATION", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Either party may terminate this Agreement with 30 days written notice. Upon termination, all outstanding payments shall become immediately due, and all confidential materials must be returned or destroyed.", align='L')
    pdf.ln(10)
    
    # Liability
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="5. LIABILITY", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="The total liability under this Agreement shall not exceed the total amount paid for services in the preceding 12 months. Neither party shall be liable for any indirect, incidental, or consequential damages.", align='L')
    
    # Save the PDF
    pdf.output("sample_contract.pdf")

if __name__ == "__main__":
    create_sample_contract()
    print("Sample contract has been created as 'sample_contract.pdf'")
