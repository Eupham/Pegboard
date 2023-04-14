from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from lorem_text import lorem
from PIL import Image, ImageDraw, ImageFont

def generate_pdf(flattened=False, num_pages=1):
    # Create a new PDF file
    c = canvas.Canvas("lorem_ipsum.pdf", pagesize=letter)

    # Define the margin and width of the text box
    margin = 0.5*inch
    width = 8.5*inch - 2*margin

    for page in range(num_pages):
        # Generate the text for the PDF
        text = lorem.paragraphs(10)

        if flattened:
            # Create an image with the text
            font = ImageFont.truetype("LiberationSans-Regular.ttf", 14)
            img_width, img_height = font.getsize(text)
            img = Image.new('RGB', (img_width+10, img_height+10), color = (255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((5,5), text, font=font, fill=(0, 0, 0))

            # Flatten the image to a PNG file
            img_file = f"lorem_ipsum_{page+1}.png"
            img.save(img_file)

            # Insert the image into the PDF
            c.drawImage(ImageReader(img_file), margin, margin, width, img_height)

        else:
            # Create a text object and insert it into the PDF
            c.drawString(margin, 9*inch - margin - 14, text)

        # Move to the next page
        c.showPage()

    # Save the PDF file
    c.save()

# Generate a PDF file with flattened text and 3 pages
generate_pdf(flattened=True, num_pages=3)

# Generate a PDF file with Lorem Ipsum text and 5 pages
generate_pdf(flattened=False, num_pages=5)
