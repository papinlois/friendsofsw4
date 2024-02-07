# Quick Guide for Starting and File Formats
(last update 1/22/24)
Once you've installed SW4 using `make`, don't forget you will still have to add the directory for the sw4 executable to your PATH
The executable should be in `[yourpath]/sw4/optimize/`

Since I installed mipch-gcc13 for this project using mac ports, there was an extra step I needed to take that isn't in the install guide for SW4 that sets up the wrapper so it is easy to use from terminal. If you've added SW4 to your PATH and are still getting command not found errors when trying to run SW4, this might be your issue
From macports info for mpich-gcc13:

> The mpicc wrapper (and friends) are installed as:
>
> `${prefix}/bin/mpicc-mpich-gcc13` (likewise mpicxx, ...)
>
> To make mpich-gcc13's wrappers the default (what you get when you execute `mpicc` etc.) please run:
>
> `sudo port select --set mpi mpich-gcc13-fortran`

## Coordinate System and Reference Frame Conventions
- Right-handed coordinates where z-positive is down. Knowing this will be very important for moment tensors. 
- your traction-free surface is z(x,y)=0 for halfspaces
- If you have topography, mean sea level should be zero

## Choosing Grid Spacing
- The number of grid points per shortest wavelength, P, helps measure how well resolved your solution is in your computational domain.
- CIG tutorial suggests P should be greater 6 and 10
- The grid points per wavelenght cane be estimated by: 

	P=minCs/(h*freqmax), where minCs is the minimum shear wave velocity in m/s, h is grid spacing in meters, freqmax is the maximum frequency  of your solution in Hz
- Error associated with your grid is O(h^4)

## Topo Format for Geographic Coordinates
- Latitude and longitude must be either strictly increasing OR strictly decreasing, step size can vary
- Latitude and longitude in degrees
- Elevation is in meters above mean sea level which means that elevations should be entered as positive numbers. The height of the free surface at that location will be equal and opposite the elevation in symbols zmin(x,y)=-Elev becuase of the coordinate system. 
- Lattice points must cover the whole computational domain and be rectangular
- Formatted as an ASCII file
- Nlat = number of latitude points, Nlon = number of longitude points
- ends in .topo
### Example Format
Ln 1. Nlon Nlat

Ln 2. Lon1 Lat1 Elev1

Ln 3. Lon2 Lat2 Elev2

Ln 4. (you get it)

## Material Model



