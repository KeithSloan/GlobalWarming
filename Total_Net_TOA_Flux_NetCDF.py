import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("path_to_CERES_EBAF_TOA_Ed4.2.1.nc")
# Inspect variables
print(ds)

# Suppose the variable for net TOA flux is called “toa_net_flux”
net = ds["toa_net_flux"]  # check actual variable name

# Compute global monthly mean if needed:
# (assuming data is already global monthly mean)
net_mean = net  # or some aggregation if needed

# Convert time and plot
net_mean.plot.line(x="time", figsize=(12,6))
plt.ylabel("Net TOA Flux (W/m²)")
plt.title("CERES EBAF Edition 4.2.1 – Net TOA Flux (Energy Imbalance)")
plt.show()

