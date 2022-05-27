This simulation was used in the following article:
  Neymotin SA, Hilscher MM, Moulin TC, Skolnick Y, Lazarewicz MT,
  Lytton WW. (2013) Ih Tunes Theta/Gamma Oscillations and
  Cross-Frequency Coupling In an In Silico CA3 Model.  PLoS ONE
  8(10):e76285. doi:10.1371/journal.pone.0076285 Complete article PDF
  is available here: http://neurosimlab.org/pdfs/poneIh13.pdf

For questions email: samn at neurosim dot downstate dot edu

This simulation was tested/developed on LINUX systems, but may run on
Microsoft Windows or Mac OS.

To run, you will need the NEURON simulator (available at
http://www.neuron.yale.edu) compiled with python enabled. To draw the
output you will need to have Matplotlib installed (
http://matplotlib.org/ ).

Instructions:
 Unzip the contents of the zip file to a new directory.

 compile the mod files from the command line with:
  nrnivmodl *.mod

The nrnivmodl command will produce an architecture-dependent folder
with a script called special.  On 64 bit systems the folder is
x86_64. To run the simulation from the command line use: nrniv -python
sim.py [simulation duration in milliseconds] (note that the last
argument is optional, default simulation duration is 1000.0 ms)

This will start NEURON with the python interpreter and load the
mechanisms and simulation. Next, the network and inputs will be setup.
Then the simulation will be run for 1 second of simulation time,
varying the level of Ih conductance (5 levels) in both pyramidal and
basket cells simultaneously. These simulations will take a few minutes
to run (depending on your CPU) and several GB of RAM. Once the
simulations finish running, the simulated local field potentials
(LFPs) will be calculated, along with their power spectral density
(PSD).

The optional last argument on the command line specifies the duration
of tnhe simulation in milliseconds.  It should be <= 8000.0 (for 8
seconds of simulation time). Since many users do not have availability
of high-performance computers, the default simulation duration is
1000.0 ms.  Simulations in the paper were run for 8000.0 ms, so if you
have a high-performance computer available, you can set the duration
to 8000.0 in the command line above. When simulations are run for
8000.0 ms, the PSD is calculated and peak theta,gamma are
displayed. When simulations are run for 1000.0 ms, the theta and gamma
peaks are not calculated, since there is not sufficient time to
extract an accurate response.

Note that since Matlab is not assumed to be available, the results
will appear slightly different from the paper (Matlab's pmtm function
was used to get the power spectra in the paper). Once PSD is
calculated, the peak theta and gamma power for each simulation will be
extracted.  Finally, output will be drawn using matplotlib (similar to
figure 10 of the paper). The top panel will show the LFPs from the
simulations arranged from low Ih to high Ih (going up). These LFPs are
also color coded. The bottom two panels will display the peak
theta,gamma power and frequency with each dot corresponding to the
color code in the top panel (displayed when running simulation for
8000.0 ms; see above). Note that since only a single simulation is run
here there will be some differences from the figure in the paper,
which consisted of multiple simulations.  However, the overall trend
is the same.

20140619 Model updated by Sam Neymotin to supply new versions of
misc.h, misc.mod, stats.mod, vecst.mod which fixes type checking
errors that some compilers generate as reported by a kind modeler.
Also the readme was made narrower for nicer display in modeldb.

20160915 This updated version from the Lytton lab allows their models
which contain misc.mod and misc.h to compile on the mac.

20220523 Updated MOD files to contain valid C++ and be compatible with
the upcoming versions 8.2 and 9.0 of NEURON.
