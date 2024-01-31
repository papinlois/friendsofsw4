import pygmt
reg=[minlon-0.02, maxlon+0.02, minlat-0.02, maxlat+0.02]
grid = pygmt.datasets.load_earth_relief(resolution='03s', region=reg) # this gets the dataset. region is [minlon, maxlon, minlat, maxlat]
grid.to_netcdf('msh_topo_15s.nc')
f = '/Users/amt/Documents/cascadia_data_mining/MSH/stingray/msh_topo_03s.nc'
grid = xr.open_dataset(f)
lon = grid['lon'].to_numpy()
lat = grid['lat'].to_numpy()
elev = grid['elevation'].to_numpy()