# list_remote_profiles.py
import requests
from bs4 import BeautifulSoup
import sys

def list_nc_files(base_url):
    """
    base_url example:
      https://data-argo.ifremer.fr/dac/aoml/4904115/profiles/
    """
    r = requests.get(base_url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    files = [a["href"] for a in soup.find_all("a") if a.get("href","").endswith(".nc")]
    return files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python list_remote_profiles.py <base_url>")
        sys.exit(1)
    base_url = sys.argv[1]
    files = list_nc_files(base_url)
    if not files:
        print("No .nc files found at", base_url)
    else:
        print("Found", len(files), "files. First 20:")
        for f in files[:20]:
            print(f)
