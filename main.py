import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def download_files(base_url, save_dir):
    # Create the folder if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Fetch the directory page content
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to access {base_url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    file_count = 0

    for link in tqdm(soup.find_all('a')):
        href = link.get('href')  # Extract the hyperlink
        if href and not href.endswith('/') and not '?' in href:  # Skip folders and query params
            file_url = urljoin(base_url, href)  # Properly join the URL
            file_path = os.path.join(save_dir, os.path.basename(href))  # Get only the file name
            
            # Download the file
            with requests.get(file_url, stream=True) as r:
                if r.status_code == 200:  # Ensure the file is accessible
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                    file_count += 1
                else:
                    print(f"Failed to download {file_url}")
    
    print(f"{file_count} files downloaded.")

# Example Usage
base_url = input("PASTE THE URL HERE: ")
save_dir = r"C:\\Users\\Jason\\Desktop\\New folder"  # Save in your preferred folder location
download_files(base_url, save_dir)
print("Download finished!")
