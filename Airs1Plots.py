'''
I can prepare a ready-to-run Python script that takes AIRS spectral data (or MODTRAN simulation) and produces a full Earth outgoing spectrum plot with GHG contributions highlighted, suitable for publication.
Do you want me to do that?

Good question. Below is a Python script skeleton + explanation for downloading AIRS spectral radiance data, plotting the outgoing longwave (IR) spectrum, and optionally comparing with a modeled spectrum (e.g. via a radiative‑transfer model or a simplified toy model).
Key Points / Data Sources
AIRS Level 1B calibrated infrared radiances have 2378 channels. 
AIRS
+1
There is an L1C product with radiances resampled to a fixed spectral grid, removing gaps / bad spectral points. 
AIRS
The L1C data (IR) are available via AWS: AIRICRAD dataset. 
Open Data on AWS
The PyEarthData Python package can fetch AIRS radiances, including outgoing radiation, which simplifies access. 
PyPI
Example Python Script
Here’s a template. You may need to adapt paths, AWS credentials (if needed), time / granule selection, and unit conversion.
'''

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pyearthdata.airs import AIRSData

# -------------------------------
# 1. Download / Load AIRS Spectral Radiance Data
# -------------------------------

# Option A: Use PyEarthData to fetch AIRS L1 data
airs = AIRSData()

# Example: get L1C radiances for a given date / orbit
# (you need to check the PyEarthData docs for exact function signatures)
# This is pseudocode — adapt to PyEarthData version you use
ds = airs.get_l1c_radiances(date="2023-01-01", granule_index=0)

# Option B: Load existing L1C file (NetCDF) from AWS or local
# path_to_file = "path/to/AIRICRAD_file.nc"
# ds = xr.open_dataset(path_to_file)

print(ds)

# The dataset `ds` should have dimensions like (time, along_track, cross_track, channel)
# And a variable for radiance, e.g., `radiance` or `Rad`

# For simplicity, select a single footprint (pixel) or average across footprints
# Here, average over along_track and cross_track to get a mean spectrum
radiance = ds["radiance"].mean(dim=["along_track", "cross_track"])
# Frequency / wavenumber or channel dimension
channel = ds["channel"]  # check exact coordinate name
wavenumber = ds["spectral_freq"]  # check variable name

# Convert wavenumber (cm‑1) to wavelength (microns)
wavelength = 1.0 / (wavenumber * 100) * 1e6  # λ (µm) = 1 / (cm⁻¹) in meters * 1e6

# -------------------------------
# 2. Optional: Simulate a Simple Model Spectrum (Toy Model)
# -------------------------------
# This is just for comparison / illustration.

def toy_co2_spectrum(lam):
    return 240 - 200 * np.exp(-0.5 * ((lam - 15) / 1.5) ** 2)

def toy_h2o_spectrum(lam):
    return 240 - 150 * np.exp(-0.5 * ((lam - 6) / 2) ** 2) - 50 * np.exp(-0.5 * ((lam - 20) / 3) ** 2)

def toy_ch4_spectrum(lam):
    return 240 - 30 * np.exp(-0.5 * ((lam - 7.7) / 0.5) ** 2)

toy_total = toy_co2_spectrum(wavelength) + toy_h2o_spectrum(wavelength) + toy_ch4_spectrum(wavelength)

# -------------------------------
# 3. Plot the Spectra
# -------------------------------
plt.figure(figsize=(12, 6))

# Plot measured radiance spectrum
plt.plot(wavelength, radiance, label="AIRS Observed Radiance", color="black")

# Plot toy spectra
plt.plot(wavelength, toy_co2_spectrum(wavelength), label="CO₂ (toy)", linestyle="--")
plt.plot(wavelength, toy_h2o_spectrum(wavelength), label="H₂O (toy)", linestyle="--")
plt.plot(wavelength, toy_ch4_spectrum(wavelength), label="CH₄ (toy)", linestyle="--")
plt.plot(wavelength, toy_total, label="Total (toy)", color="grey", linestyle=":")

plt.xlabel("Wavelength (µm)")
plt.ylabel("Radiance (W m⁻² sr⁻¹ / cm⁻¹)")  # adjust units to match dataset
plt.title("Outgoing Longwave Spectrum – AIRS vs Toy GHG Model")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


