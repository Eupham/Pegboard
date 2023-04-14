import fitz

# Open the PDF file
doc = fitz.open('lorem_ipsum.pdf')

# Define the keyword to split the PDF on
keyword = 'aliquid'

# Loop through each page of the PDF file
for i, page in enumerate(doc):

    # Get the xhtml formatted text of the page
    text = page.get_text("xhtml")

    # Check if the keyword exists in the page text
    if keyword in text:

        # Split the PDF at the current page
        out_file_name = f'output_{keyword}_{i}.pdf'
        out_doc = fitz.open()
        out_doc.insert_pdf(doc, from_page=i, to_page=i)
        out_doc.save(out_file_name)
        out_doc.close()
