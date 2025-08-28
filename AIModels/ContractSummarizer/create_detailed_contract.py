from fpdf import FPDF
import textwrap

def create_detailed_contract():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SOFTWARE AS A SERVICE AGREEMENT", ln=1, align='C')
    pdf.ln(10)
    
    def add_section(title, content):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=title, ln=1, align='L')
        pdf.set_font("Arial", size=12)
        # Wrap text to ensure proper formatting
        wrapped_text = textwrap.fill(content, width=85)
        pdf.multi_cell(0, 10, txt=wrapped_text, align='L')
        pdf.ln(5)

    # 1. Definitions
    add_section("1. DEFINITIONS", """
    1.1 'Agreement' means this Software as a Service Agreement and any Exhibits, Schedules, and Amendments hereto.
    1.2 'Service' means the software services provided by the Provider to the Customer under this Agreement.
    1.3 'Customer Data' means any data, information, or material provided or submitted by the Customer to the Service.
    1.4 'Intellectual Property Rights' means all patents, copyrights, design rights, trademarks, service marks, trade secrets, know-how, database rights and other rights in the nature of intellectual property rights.
    """)

    # 2. Service Provision
    add_section("2. SERVICE PROVISION", """
    2.1 Subject to the terms and conditions of this Agreement, Provider hereby grants Customer a non-exclusive, non-transferable right to access and use the Service during the Term of this Agreement.
    2.2 Provider shall provide the Service in accordance with the service levels specified in Schedule A.
    2.3 Provider may modify the Service from time to time by giving not less than 30 days prior written notice to Customer.
    """)

    # 3. Payment Terms
    add_section("3. PAYMENT TERMS", """
    3.1 Customer shall pay to Provider the fees set out in Schedule B ('Fees').
    3.2 All Fees are exclusive of any applicable sales tax, which shall be paid by Customer at the rate and in the manner prescribed by law.
    3.3 Provider shall invoice Customer monthly in advance for the Fees, and Customer shall pay each invoice within 30 days after the date of such invoice.
    3.4 If Customer fails to make any payment due to Provider under this Agreement by the due date for payment, then, without limiting Provider's remedies, Customer shall pay interest on the overdue amount at the rate of 4% per annum above the Bank of England's base rate from time to time.
    """)

    # 4. Confidentiality
    add_section("4. CONFIDENTIALITY", """
    4.1 Each party undertakes that it shall not at any time during this Agreement, and for a period of five years after termination of this Agreement, disclose to any person any confidential information concerning the business, affairs, customers, clients or suppliers of the other party, except as permitted by clause 4.2.
    4.2 Each party may disclose the other party's confidential information:
        (a) to its employees, officers, representatives or advisers who need to know such information for the purposes of exercising the party's rights or carrying out its obligations under or in connection with this Agreement. Each party shall ensure that its employees, officers, representatives or advisers to whom it discloses the other party's confidential information comply with this clause; and
        (b) as may be required by law, a court of competent jurisdiction or any governmental or regulatory authority.
    4.3 No party shall use any other party's confidential information for any purpose other than to exercise its rights and perform its obligations under or in connection with this Agreement.
    """)

    # 5. Data Protection
    add_section("5. DATA PROTECTION", """
    5.1 Both parties will comply with all applicable requirements of the Data Protection Legislation. This clause is in addition to, and does not relieve, remove or replace, a party's obligations under the Data Protection Legislation.
    5.2 The parties acknowledge that:
        (a) if Provider processes any personal data on Customer's behalf when performing its obligations under this Agreement, Customer is the data controller and Provider is the data processor for the purposes of the Data Protection Legislation.
        (b) Schedule C sets out the scope, nature and purpose of processing by Provider, the duration of the processing and the types of personal data and categories of data subject.
    5.3 Without prejudice to the generality of clause 5.1, Customer will ensure that it has all necessary appropriate consents and notices in place to enable lawful transfer of the personal data to Provider for the duration and purposes of this Agreement.
    """)

    # 6. Intellectual Property
    add_section("6. INTELLECTUAL PROPERTY", """
    6.1 Customer acknowledges and agrees that Provider and/or its licensors own all intellectual property rights in the Service. Except as expressly stated herein, this Agreement does not grant Customer any rights to, under or in, any patents, copyright, database right, trade secrets, trade names, trademarks (whether registered or unregistered), or any other rights or licenses in respect of the Service.
    6.2 Provider confirms that it has all the rights in relation to the Service that are necessary to grant all the rights it purports to grant under, and in accordance with, the terms of this Agreement.
    6.3 Customer shall own all right, title and interest in and to all of the Customer Data and shall have sole responsibility for the legality, reliability, integrity, accuracy and quality of the Customer Data.
    """)

    # 7. Liability and Indemnification
    add_section("7. LIABILITY AND INDEMNIFICATION", """
    7.1 Neither party's liability:
        (a) for death or personal injury caused by its negligence or the negligence of its employees or agents;
        (b) for fraud or fraudulent misrepresentation; or
        (c) for any other liability which cannot be limited or excluded by applicable law,
    shall be limited or excluded by this Agreement.
    
    7.2 Subject to clause 7.1, neither party shall be liable to the other party for any:
        (a) loss of profits;
        (b) loss of sales or business;
        (c) loss of agreements or contracts;
        (d) loss of anticipated savings;
        (e) loss of or damage to goodwill;
        (f) loss of use or corruption of software, data or information; or
        (g) any indirect or consequential loss.
    
    7.3 Subject to clauses 7.1 and 7.2, Provider's total aggregate liability to Customer in respect of all other losses arising under or in connection with this Agreement, whether in contract, tort (including negligence), breach of statutory duty, or otherwise, shall in no circumstances exceed the total Fees paid by Customer to Provider under this Agreement in the 12 months preceding the date on which the claim arose.
    """)

    # 8. Term and Termination
    add_section("8. TERM AND TERMINATION", """
    8.1 This Agreement shall commence on the Effective Date and shall continue for the Initial Term. After the Initial Term, this Agreement shall automatically renew for successive periods of 12 months (each a 'Renewal Term'), unless:
        (a) either party notifies the other party of termination, in writing, at least 60 days before the end of the Initial Term or any Renewal Term, in which case this Agreement shall terminate upon the expiry of the applicable Initial Term or Renewal Term; or
        (b) otherwise terminated in accordance with the provisions of this Agreement.
    
    8.2 Without affecting any other right or remedy available to it, either party may terminate this Agreement with immediate effect by giving written notice to the other party if:
        (a) the other party commits a material breach of any term of this Agreement which breach is irremediable or (if such breach is remediable) fails to remedy that breach within a period of 30 days after being notified in writing to do so;
        (b) the other party suspends, or threatens to suspend, payment of its debts or is unable to pay its debts as they fall due;
        (c) a petition is filed, a notice is given, a resolution is passed, or an order is made, for or in connection with the winding up of that other party;
        (d) an application is made to court, or an order is made, for the appointment of an administrator, or if a notice of intention to appoint an administrator is given or if an administrator is appointed, over the other party.
    """)

    # 9. Force Majeure
    add_section("9. FORCE MAJEURE", """
    Neither party shall be in breach of this Agreement nor liable for delay in performing, or failure to perform, any of its obligations under this Agreement if such delay or failure result from events, circumstances or causes beyond its reasonable control. In such circumstances the affected party shall be entitled to a reasonable extension of the time for performing such obligations. If the period of delay or non-performance continues for 3 months, the party not affected may terminate this Agreement by giving 30 days' written notice to the affected party.
    """)

    # 10. Governing Law and Jurisdiction
    add_section("10. GOVERNING LAW AND JURISDICTION", """
    10.1 This Agreement and any dispute or claim (including non-contractual disputes or claims) arising out of or in connection with it or its subject matter or formation shall be governed by and construed in accordance with the law of England and Wales.
    
    10.2 Each party irrevocably agrees that the courts of England and Wales shall have exclusive jurisdiction to settle any dispute or claim (including non-contractual disputes or claims) arising out of or in connection with this Agreement or its subject matter or formation.
    
    10.3 Notwithstanding clause 10.2, Provider shall be entitled to seek injunctive or other equitable relief in any jurisdiction in relation to any actual or threatened breach of its Intellectual Property Rights or rights of confidentiality.
    """)

    # Save the PDF
    pdf.output("detailed_contract.pdf")

if __name__ == "__main__":
    create_detailed_contract()
    print("Detailed contract has been created as 'detailed_contract.pdf'")
