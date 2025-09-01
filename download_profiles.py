# download_profiles.py
import os
import requests

def download_file(url, out_folder="data"):
    os.makedirs(out_folder, exist_ok=True)
    local_name = os.path.join(out_folder, os.path.basename(url))
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(local_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_name

if __name__ == "__main__":
    # example usage: edit the URLs list or pass from the output of list_remote_profiles.py
    urls = ["https://data-argo.ifremer.fr/dac/aoml/1901800/profiles/D1901800_000.nc",
            "https://data-argo.ifremer.fr/dac/aoml/1901800/profiles/D1901800_001.nc"
        # "https://data-argo.ifremer.fr/dac/aoml/4904115/profiles/R4904115_001.nc",
        # add the file URLs you want
    ]
    for u in urls:
        try:
            p = download_file(u)
            print("Downloaded:", p)
        except Exception as e:
            print("Failed:", u, e)
