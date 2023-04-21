# About
This python program adapts hdf5 snapshots of n-body simulations of isolated galaxies that use star formation, such as those from GADGET-4, allowing the plotting of realistic visualizations that take into account metallicity and particle age of the simulated galaxy.

This small program was created to adapt snapshots exported in hdf5 by the n-body simulator GADGET-4, however, it should work with any other program that uses a similar data structure in its hdf5 snapshot. Basically your hdf5 file must have 'Metallicity' and 'StellarFormationTime' values in the particle group that will be considered in the plotting.

Some explanation of use:

1- The param.ini file has some control options like plotting specifications, rotation of the displayed galaxy, assignment of disk particles etc.

2- The program works very well to plot stars type particles ('[PartType4]') created by star formation because they have metallicity and age information.

3- If you want to plot also the disk type particles (['PartType2]') you will need to estimate an initial metallicity and an initial age for them. Through the param.ini file you can make some choices about this, assigning arbitrary values or using minimum values collected from the star type particles.


# Required libraries

* numpy (python-numpy)
* h5py
* pynbody
* matplotlib

# Usage
 usage: python3 galmock [snapshot --hdf5] param.ini

# License

Feel free to use this code in your work.
