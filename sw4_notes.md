# SW4 Notes

## Running stuff
`mpirun -host localhost -np 2 ../../optimize/sw4 seismic1.in`

## Lambs problem from CIG/LLNL tutorial
This file sets up Lambs problem with a point source aligned with the z - axis  

This line gives the output file name. 

`fileio path=seis-out`

This line sets up the grid with the number of #x elements= #y elements = #z elements = 200.  x grid size is 30 km, y grid size is 30 km and z grid size is 10 km in depth.  Az=0 sets x=North, y=East, and Z=down. The resolution for the grid, which is governed by h in this problem, controls ∆t/sampling rate. 10x finer grid in the domain results in a 10x smaller ∆t.

`grid h=200 x=30e3 y=30e3 z=10e3 az=0`

Set simulation time

`time t=15.0`

Sets velocity model to be vs=1000 m/s, vp=sqrt(3)*1000 m/s, and rho=1500 kg/m^3

`block vp=1.7320508076e+03 vs=1000 rho=1500`

For sources need to prescribe the type=C6SmoothBump, location (x=15e3 y=15e3 z=0), magnitude (10^13 N), frequency (0.42 Hz), and t0 (starting time)

`source type=C6SmoothBump x=15e3 y=15e3 z=0 fz=1e13 freq=0.42 t0=0`

[not] Important [for this example]: To avoid artifacts from a sudden startup, use t0 ≥ 1.35/ω.  So why does above example have t0=0? It turns out that t0≥ 1.35/ω only needs to be true for the 'Ricker' predefined STF, not every STF has sudden startup issues (KS)

Time history of solution along a vertical line aligned with the source.  This puts sensor at x, y, z coordinates, specifies output file names, specifies nsew ground motions, and usgsformat (output all components in an ASCII text file).

`rec x=15e3 y=16e3 z=0 file=v1 nsew=1 usgsformat=1`
`rec x=15e3 y=25e3 z=0 file=v10 nsew=1 usgsformat=1`

The output files that you want to work with are written to `seismic1.out/v1.txt` and `seismic1.out/v10.txt`
The built-in plotting scripts work well if you are willing to use matlab, however, the usgs file formats are also very easy to read using pandas and subsequently plot things from there. 

No suprises here, but here is what we found playing around with source parameters: (1/31/24)
- increasing the magnitude parameter in the stf results in higher amplitudes in the solutions
- Increasing the frequency parameter in the stf WITHOUT adujusting the grid resolution to be smaller results in nonsense solutions
- The frequency parameter means something slightly different in each predefined stf so make sure to look at the user guide to understand what exactly you are doing

## LOH1 (layer over halfspace) problem from CIG/LLNL Tutorial
The directory for this problem `sw4/examples/ llnl-cig-tutorial/LOH-1/` contains two very similar configuration files `LOH.1-h100-mr.in` and `LOH.1-h50.in` that have difference is mesh/grid resolution and refinement.
Like the Lambs example we first set up our grid and simulation time, noting that ln 22 sets up a higher resolution grid for `LOH.1-h100-mr.in` than `LOH.1-h50.in`

`grid h=50 x=30000 y=30000 z=17000
time t=9`

Then `LOH.1-h100-mr.in` uses the command 

`refinement zmax=1000`

which makes the grid size half the grid size the user defined for everythign shallower than `zmax`. `LOH.1-h50.in` does not do this refinement step.

We define the material properties everywhere (half-space). `block` with no `z` parameters makes a block that covers your entire domain

`block vp=6000 vs=3464 rho=2700`

then define the slower material in the top layer (z < 1000 m) `block` with only `z2` parameter sets the bottom of that block and has those material properties extend to the surface

`block vp=4000 vs=2000 rho=2600 z2=1000`

Now we set up our source. 

Gaussian time function gives the velocities directly and sigma is the spread of the Gaussian

sigma=0.05 gives freq=1/sigma=20 (LOH.3)

sigma=0.06 gives freq=1/sigma=16.6667 (LOH.1)

[Important] t0 = 6*sigma = 0.36 avoids (most) startup transients and is consistent with the matlab script PlotAnalyticalLOH1.m

The position of our source in xyz coords is (15km, 15km, 2km) and it is a double couple source where the mxy components of the moment tensor (MT) is the only non-zero components of the MT

`source x=15000 y=15000 z=2000 mxy=1e18 t0=0.36 freq=16.6667 type=Gaussian`

We set up our station timeseries outputs just like the Lambs example 

`rec x=15600 y=15800 z=0 file=sta01 usgsformat=1
rec x=21000 y=23000 z=0 file=sta10 usgsformat=1`

To see a 2D cross section of our model domain for y=15km uses this command:

`image mode=s y=15e3 file=mat cycle=0`

Solution images provide us additional 2D cross sections of the solutions at user defined time intervals
This first one gives us the magnitude of the displacement at the surface at half-second time intervals

`image mode=mag z=0 file=surf timeInterval=0.5`

To see displacements in the same veritcal plane where we previously plotted our material model uses this next line of code. We only output uy (displacement in y dir). No point saving uz and ux on this plane, because they are zero by symmetry.

`image mode=uy y=15e3 file=vert timeInterval=0.5`

Running this example should probably be done on Talapas. Kate's laptop ran out of RAM and crashed when running locally. 

Next up... figuring out how to read the `.sw4image` files outside of the provided matlab tools