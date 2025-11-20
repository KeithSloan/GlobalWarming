import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("CERES_EBAF-TOA_L3B004.2.nc")  # path to the file you downloaded
net_flux = ds["toa_net_flux"]  # name of the net flux variable (check the exact name)
# weight by cosine(latitude) to get global mean
weights = np.cos(np.deg2rad(ds["latitude"]))
global_mean = (net_flux * weights).sum(dim=["latitude", "longitude"]) / weights.sum()
global_mean.plot(linewidth=2)
plt.title("CERES TOA Net Flux (Global) — Monthly (EBAF 4.2)")
plt.ylabel("Net Flux (W/m²)")
plt.xlabel("Time")
plt.grid(True)
plt.show()

