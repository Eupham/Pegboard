import fitz

# Open the PDF file
doc = fitz.open('lorem_ipsum.pdf')

# Define the keyword to split the PDF on
keyword = 'aliquid'

# Loop through each page of the PDF file
for i, page in enumerate(doc):

    # Get the xhtml formatted text of the page
    text = page.get_text("text")

    # Split the text into segments based on the keyword
    segments = text.split(keyword)

    # Loop through each segment and save as a separate PDF file
    for j, segment in enumerate(segments):

        # Define the output file name for the current segment
        out_file_name = f'output_{keyword}_{i}_{j}.pdf'

        # Create a new PDF document and add the current segment as a new page
        out_doc = fitz.open()
        out_page = out_doc.new_page()
        out_page.insert_text((0, 0), segment)
        
        # Save the new PDF document as a separate file
        out_doc.save(out_file_name)
        out_doc.close()
