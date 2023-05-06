import requests

# Specify the URL of the indexed database
url = "https://sb.flleg.gov"

# Send a GET request to the database
response = requests.get(url)

# Print the status code and response text
print("Status code:", response.status_code)
print("Response text:", response.text)
