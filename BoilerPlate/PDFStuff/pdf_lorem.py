from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from lorem_text import lorem
from PIL import Image, ImageDraw, ImageFont

from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO

def generate_pdf(flattened=False, num_pages=1, file_name="lorem_ipsum.pdf"):
    # Create a new PDF file
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Define the margin and width of the text box
    margin = 0.5*inch
    width = 8.5*inch - 2*margin

    for page in range(num_pages):
        # Generate the text for the PDF
        text = lorem.paragraphs(10)

        text_object = c.beginText(margin, 9*inch - margin - 14)
        text_object.setTextOrigin(margin, 9*inch - margin - 14)
        text_object.setFont("Helvetica", 12)
        lines = text.split("\n")
        for line in lines:
            text_object.textOut(line)
            text_object.moveCursor(0, -20)  # Set the line spacing
        c.drawText(text_object)

        # Move to the next page
        c.showPage()

    # Save the PDF file to memory
    c.save()
    packet.seek(0)
    pdf = PdfReader(packet)

    # Write the PDF to a file
    writer = PdfWriter()
    for page in pdf.pages:
        writer.add_page(page)
    with open(file_name, 'wb') as f:
        writer.write(f)

# Generate a regular PDF file with Lorem Ipsum text and 5 pages
generate_pdf(flattened=False, num_pages=5, file_name="lorem_ipsum.pdf")
