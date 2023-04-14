#import pymupdf
import fitz

# Open the PDF file
doc = fitz.open('lorem_ipsum.pdf')

# Define the keyword to split the PDF on
keyword = 'aliquid'

# Initialize the page counter and output PDF file counter
page_counter = 0
output_counter = 0

# Loop through each page of the PDF file
for page in doc:

    # Get the xhtml formatted text of the page
    text = page.get_text("xhtml")

    # Check if the keyword exists in the page text
    if keyword in text:

        # Split the PDF at the current page
        out_file_name = f'output_{keyword}_{output_counter}.pdf'
        out_doc = fitz.open()
        out_doc.insert_pdf(doc, from_page=page_counter, to_page=page.number-1)
        out_doc.save(out_file_name)
        out_doc.close()

        # Update the page counter and output PDF file counter
        page_counter = page.number
        output_counter += 1

# If the last keyword was found on the last page of the document, save the remaining pages to a new PDF file
if page_counter < len(doc):
    out_file_name = f'output_{keyword}_{output_counter}.pdf'
    out_doc = fitz.open()
    out_doc.insert_pdf(doc, from_page=page_counter, to_page=len(doc)-1)
    out_doc.save(out_file_name)
    out_doc.close()
