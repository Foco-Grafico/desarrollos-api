#Generate Batch PDF
from fpdf import FPDF
from fpdf.html import HTMLMixin
import html


class pdf_class(FPDF, HTMLMixin):
        pass

pdf = pdf_class()

def batch_generate_pdf(body: str, status: str, font_size: int, title_pdf: str, doc_name: str):

    try:
        pdf.add_page()

        pdf.set_title(title_pdf)

        pdf.set_font("Arial", size=font_size)

        body1 = pdf.cell(100, 20, txt=body,ln=True)

        status1 = pdf.cell(100, 20, txt=status, ln=True)

        html_code =f"""

        <h1 style = "color: #007BFF;" >Batch PDF</h1>

        <p>{body1}</p>

        <div style = "color: #007BFF;" >Status</div>

        <p>{status1}</p>

        """

        # Unescape HTML characters
        unescaped_html = html.unescape(html_code)

        pdf.write_html(unescaped_html)
        pdf.output(doc_name)
    except (Exception) as e:
        print(e)

batch_generate_pdf(
    body='''
    "id": 1,
    "area": 3232,
    "price": 43434,
    "perimeter": 32323,
    "longitude": 2323,
    "coords": "dfdsfd",
    "amenities": "dfdsfds",
    "development_id": 1,
    "currency": "usd",
    "location": "sdsad",
    "sq_m": 123,
    ''',

    status='''
    "id": 1,
    "name": "Disponible"
    ''',

    font_size=14,

    title_pdf="Colina PDF",

    doc_name="python.pdf"
)



