import pytesseract
from pdf2image import convert_from_path
import io
import PyPDF2

# Path to the input PDF file, you probably want to use pathlib instead of handling paths like this
input_pdf_path = 'path/to/input/pdf'

# Create a PDF file object
with open(input_pdf_path, 'rb') as pdf_file:
    
    # Try to read the PDF using PyPDF2
    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.getNumPages()
        text = ''
        for i in range(num_pages):
            page = pdf_reader.getPage(i)
            text += page.extractText()
            
    # If PyPDF2 fails, use Tesseract OCR to extract text from the PDF
    except PyPDF2.utils.PdfReadError:
        images = convert_from_path(input_pdf_path)
        text = ''
        for image in images:
            with io.BytesIO() as output:
                image.save(output, format='JPEG')
                contents = output.getvalue()
                text += pytesseract.image_to_string(contents)

# Split the text by the word 'Nana'
split_text = text.split('Nana')

# Create a PDF writer object
pdf_writer = PyPDF2.PdfFileWriter()

# Add each split text into a separate PDF page
for i, text in enumerate(split_text):
    pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, 612, 792)
    pdf_page.mergePage(PyPDF2.pdf.PageObject.createFromString(text))
    pdf_writer.addPage(pdf_page)
    
    # Save the PDF file for each split text
    with open(f"output_file_{i}.pdf", "wb") as f:
        pdf_writer.write(f)
    pdf_writer = PyPDF2.PdfFileWriter()
