# 🌊 Argo NetCDF → CSV Converter

Easily **download, extract, and convert Argo NetCDF profile files** into clean CSV format.  
This tool makes it simple for **researchers, students, and developers** to work with Argo float data **without needing to manually handle NetCDF files**.

---

## ✨ Features

- 🔽 Download Argo `.nc` files directly from the official portal (given a URL).  
- 📂 Extract & Convert **pressure, temperature, salinity, and metadata** into CSV.  
- 📊 Outputs are analysis-ready for **Python, R, Excel, or ML pipelines**.  
- ⚡ Batch processing for multiple `.nc` files.  
- 🛠 Lightweight and beginner-friendly — no NetCDF knowledge required.  

---

## 📦 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/TeckHack76/netCDF-file_converter.git
cd netCDF-file_converter
pip install -r requirements.txt
```


Requirements:

- Python 3.8+

- pandas

- numpy

- netCDF4

- requests

- tqdm

## 🚀 Usage

1. Convert a single remote file (via URL)
```bash
python main.py https://data-argo.ifremer.fr/latest_data/D20250730_prof_0.nc
```

  This will:
  
- Download the NetCDF file into processed/

- Extract measurements

- Save CSV to:
  ```bash
  processed/D20250730_prof_0.csv
  ```

2. Process local files

Place .nc files inside the data/ folder and run:

```bash
python batch_extract.py
```

This will create per-file CSVs inside processed/ and also combine them into:

- processed/combined.csv

- processed/combined.parquet

3. Output format

Each CSV contains:

platform_number	cycle_num	time	latitude	longitude	pressure_dbar	temperature_C	salinity_psu
2902925	1	2025-07-30 12:40:00	20.9756	127.095	1.5	25.504	34.641
📂 Project Structure
argo-netcdf-csv/
│
├── data/                 # Place raw .nc files here (ignored in git)
├── processed/            # Output CSV & parquet files
│
├── extract_profile.py    # Extracts one NetCDF profile → DataFrame
├── batch_extract.py      # Batch processing of multiple files
├── download_profiles.py  # Utilities for downloading
├── main.py               # CLI entry point (URL → CSV)
│
├── requirements.txt
├── README.md
└── .gitignore

⚠️ Notes

Large .nc files are ignored by default (see .gitignore).

Only variables PRES, TEMP, and PSAL (salinity) are extracted.

Adjust the extractor if you need additional fields.

🤝 Contributing

Contributions are welcome!

Open an issue if you find a bug

Submit a pull request for improvements

💡 Example Workflow
```bash
# 1) Clone repo
git clone https://github.com/TeckHack76/netCDF-file_converter.git
cd argo-netcdf-csv

# 2) Install dependencies
pip install -r requirements.txt

# 3) Convert latest profile from Argo
python main.py https://data-argo.ifremer.fr/latest_data/D20250730_prof_0.nc
```

👉 Output CSV is ready in processed/
