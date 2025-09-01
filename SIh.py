import netCDF4 as nc
import pandas as pd
import numpy as np

file_path = r"nodc_13857_prof.nc"
ds = nc.Dataset(file_path)
print("✅ File loaded")

# Safe read helper
def safe_read(var):
    if var in ds.variables:
        data = ds[var][:]
        if hasattr(data, "filled"):  # Masked array
            data = data.filled(np.nan)
        return data
    return None

# Extract arrays (check properly for None instead of using "or")
pres = safe_read("pres")
if pres is None:
    pres = safe_read("pres_adjusted")

temp = safe_read("temp")
if temp is None:
    temp = safe_read("temp_adjusted")

sal = safe_read("PSAL-ADJUSTED")
if sal is None:
    sal = safe_read("PSAL")

lat  = safe_read("latitude")
lon  = safe_read("longitude")
time = safe_read("juld")
platform = safe_read("platform_number")
cycle = safe_read("cycle_number")

# Convert time
if time is not None:
    time = pd.to_datetime(time, origin="1950-01-01", unit="D")

rows = []
n_profiles = temp.shape[0]
n_levels = temp.shape[1]

for i in range(n_profiles):
    for j in range(n_levels):
        row = {
            "platform_number": (
                "".join(platform[i].astype(str)).strip() if platform is not None else "unknown"
            ),
            "cycle_number": int(cycle[i]) if cycle is not None else -1,
            "time": time[i] if time is not None else None,
            "latitude": float(lat[i]) if lat is not None else np.nan,
            "longitude": float(lon[i]) if lon is not None else np.nan,
            "pressure_dbar": float(pres[i, j]) if pres is not None else np.nan,
            "temperature_C": float(temp[i, j]) if temp is not None else np.nan,
            "salinity_psu": (
                float(sal[i, j]) if sal is not None and not np.isnan(sal[i, j]) else np.nan
            ),
        }
        if not np.isnan(row["pressure_dbar"]) and not np.isnan(row["temperature_C"]):
            rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("argo_dataset.csv", index=False)

print("✅ Saved to argo_dataset.csv")
print("📊 Summary:")
print(df.describe(include="all"))
print("\nFirst 5 rows:")
print(df.head())