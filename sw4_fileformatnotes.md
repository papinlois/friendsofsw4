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
- the origin is in the lower left corner of your grid

## Choosing Grid Spacing
- The number of grid points per shortest wavelength, P, helps measure how well resolved your solution is in your computational domain.
- CIG tutorial suggests P should be greater 6 and 10
- The grid points per wavelength cane be estimated by: 

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
- Lat varies first then longitude

### Example Format
Ln 1. Nlon Nlat

Ln 2. Lon1 Lat1 Elev1

Ln 3. Lon2 Lat2 Elev2

Ln 4. (you get it)

## Material Model
The "pfile" format seems by far the most tractable file type to write yourself. pfiles work by specifying depth profiles at each pair of lat,lon or x,y coordinates in your material model. Important, unit conventions are different depending on if you use geographic or cartesian coordinates.

### General details
- CAUTION velocity in km/s if using geographic coords, velocity in m/s if cartesian coords
- CAUTION depth in km if using geographic coords, depth in m if cartesian coords
- CAUTION units of denisty are g/cm^3 in geographic coordinates BUT if you use cartesian coordinates they are kg/m^3
- The file ending is ".ppmod"
- ∆ is a parameter used for interpolating between depth profiles, their example uses 0.25 and Leighton's uses 40 (look into this)
- Nlat, Nlon, Ndepth are the number of unique/different values you use through out the whole model for each quantity respectively so NLat x Nlon x Ndepth is the total number of points at which you are specifying your material model
- Nlon X Nlat is the number of depth profiles you specify
- longitude varies fastest/first
- ln 6 of the header lets you specify the index of discontinuities includeing "sed", "Moho", "410", and "660" in that order put -99 (like shown here to ignore those)
- If your data has quality factors Qs and Qp chance ln 7 to .TRUE.
- Indexing in each depth profile starts at 1 NOT 0

### Formatting specifics
- the file header is 7 lines long as follows:

	Ln 1. name 
	
	Ln 2. ∆
	
	Ln 3. Nlat(int)    Latmin    Latmax
	
	Ln 4. Nlon(int)    Lonmin    Lonmax
	
	Ln 5. Ndepth(int)  Depthmin  Depthmax
	
	Ln 6. -99          -99       -99       -99
	
	Ln 7. .FALSE.       
- The first line of each depth profile is: 
	
	lat lon Ndepth
- Then you have the following lines for each point in your depth profile formatted as listing with units for geographic coordinates:

	index(starts@1) depth(km) Vp(km/s) Vs(km/s) rho(g/cm^3) Qp Qs

	


