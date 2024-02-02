# Friends of SW4 reading group notes and scripts

## Session 1

In session 1 we started by just installing SW4 and learning how to run jobs on talapas.  Many of us had the same problem with installation from source so we opened a github issues and Obi-wan Kenobi ([Anders Petersson](https://people.llnl.gov/petersson1)) pointed out that it was an OpenMP issue that could be obviated by running <code>make sw4 openmp=no</code>.

## Session 2

Cancelled by icepocalypse 2024.

## Session 3

Starting with the [LLNL/CIG tutorial](https://github.com/UO-Geophysics/friendsofsw4/blob/main/SW4-tutorial-CIG.pdf), we explored the seismic1.in input file and took some [notes](https://github.com/UO-Geophysics/friendsofsw4/blob/main/sw4_notes.md) on what each component meant.

## Session 4

Kate is going to lead this session and put some notes here.  This [script](https://github.com/UO-Geophysics/friendsofsw4/blob/main/elevation_snippet.py) could be useful for automated download of elevation data.

We appended our notes to the existing [notes](https://github.com/UO-Geophysics/friendsofsw4/blob/main/sw4_notes.md). We focused on modifying seismic1.in to look at what different parameters do to the solution and plotted the outputs. We also went through the input files for the next CIG/LLNL example LOH-1 (Layer over halfspace) to understand what each line of code does.

Homework: (1) run either `LOH.1-h100-mr.in` or `LOH.1-h50.in` on Talapas (slurm or OpenOnDemand) (2) Have topography and velocity models downloaded in some capcity (not necessarily formatted for sw4) (3) Compute the grid resolution you need based on your maximum frequency need using Section 4.4 of the user manual

## Session 5

Look into reading and plotting the `.sw4image` files in python to visualize LOH-1 outputs and... 