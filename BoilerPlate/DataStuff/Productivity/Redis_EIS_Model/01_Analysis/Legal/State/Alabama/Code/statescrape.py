import requests
from bs4 import BeautifulSoup
from pathlib import Path

downloaded_files = [f.stem for f in Path(".").glob("*-*-*.htm")]

# Make a request to the URL
url = "http://alisondb.legislature.state.al.us/alison/CodeOfAlabama/1975/title.htm"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links in the HTML content
links = soup.find_all("a")

# Follow each link and get the links from those pages
for link in links:
    href = link.get("href")
    if href and href.endswith(".htm"):
        full_url = f"{url.rsplit('/', 1)[0]}/{href}"
        sub_response = requests.get(full_url)
        sub_soup = BeautifulSoup(sub_response.content, "html.parser")
        sub_links = sub_soup.find_all("a")
        # Follow links on the second level
        for sub_link in sub_links:
            sub_href = sub_link.get("href")
            if sub_href and sub_href.endswith(".htm"):
                full_url2 = f"{full_url.rsplit('/', 1)[0]}/{sub_href}"
                sub2_response = requests.get(full_url2)
                sub2_soup = BeautifulSoup(sub2_response.content, "html.parser")
                sub2_links = sub2_soup.find_all("a")
                # Follow links on the third level
                for sub2_link in sub2_links:
                    sub2_href = sub2_link.get("href")
                    if sub2_href and sub2_href.endswith(".htm"):
                        # Check if the file has already been downloaded
                        filename = Path(sub2_href).stem
                        if filename in downloaded_files:
                            print(f"Skipping {sub2_href} (already downloaded)")
                            continue
                        # Download the file
                        full_url3 = f"{full_url2.rsplit('/', 1)[0]}/{sub2_href}"
                        sub3_response = requests.get(full_url3)
                        sub3_soup = BeautifulSoup(sub3_response.content, "html.parser")
                        # Write the content of the third level HTML page to a file
                        with open(sub2_href, "w", encoding="utf-8") as f:
                            f.write(sub3_response.text)
                        # Add the filename to the downloaded files list
                        downloaded_files.append(filename)