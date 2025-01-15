import os
import requests
from bs4 import BeautifulSoup

def download_files(base_url, save_dir):
    #Download all files from a directory URL
    os.makedirs(save_dir, exist_ok=True)  # Create the folder if it doesn't exist
    response = requests.get(base_url)  # Get the page content
    soup = BeautifulSoup(response.text, 'html.parser') 

    file_count = 0

    for link in soup.find_all('a'):
        href = link.get('href')  # Get the link
        if href and not href.endswith('/'):  # Only download files (skip folders)
            file_url = base_url + href
            file_path = os.path.join(save_dir, href)
            with requests.get(file_url, stream=True) as r:
                with open(file_path, 'wb') as f:
                    f.write(r.content)
            file_count += 1

    print(f"{file_count} files downloaded.")

# Example Usage
base_url = "http://intranet-server/path/to/notes/"  # Change to your URL
save_dir = "./Downloaded_Notes"  # Where to save files
download_files(base_url, save_dir)
print("Download finished!")
