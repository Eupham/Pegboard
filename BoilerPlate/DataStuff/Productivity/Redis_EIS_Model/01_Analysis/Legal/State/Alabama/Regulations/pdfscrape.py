import requests
from bs4 import BeautifulSoup
from pathlib import Path

url = 'http://www.doc.state.al.us/regulations'
folder = Path('pdfs')
folder.mkdir(parents=True, exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
pdf_links = soup.find_all('a', href=lambda x: x.endswith('.pdf'))

for link in pdf_links:
    file_url = link.get('href')
    file_name = file_url.split('/')[-1]
    file_path = folder / file_name
    with open(file_path, 'wb') as f:
        response = requests.get(url+file_url)
        f.write(response.content)
