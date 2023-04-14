import fitz
doc = fitz.open('lorem_ipsum.pdf') 

for page in doc:
    text = page.get_text("xhtml")
    print(text)