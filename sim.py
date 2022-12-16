import sys
import os
import string
from neuron import *
h("strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment")
h.simname=simname = "mtlhpc"
h.allfiles=allfiles = "geom.hoc pyinit.py geom.py network.py params.py run.py"
h.simfiles=simfiles = "pyinit.py geom.py network.py params.py run.py"
h("runnum=1")
runnum = 1.0
h.datestr=datestr = "10dec15"
h.output_file=output_file = "data/10dec13.14"
h.uname=uname = "x86_64"
h.osname=osname="linux"
h("templates_loaded=0")
templates_loaded=0
h("xwindows=1.0")
xwindows = 1.0
h.xopen("nrnoc.hoc")
h.xopen("init.hoc")
from pyinit import *
exec(compile(open("geom.py", "rb").read(), "geom.py", 'exec'))
exec(compile(open("network.py", "rb").read(), "network.py", 'exec'))
exec(compile(open("params.py", "rb").read(), "params.py", 'exec'))
exec(compile(open("run.py", "rb").read(), "run.py", 'exec'))
from pylab import * # need matplotlib

h.tstop = 1e3
if len(sys.argv) > 3:
    h.tstop = float(sys.argv[3])
    print('set h.tstop to',h.tstop)

# scaleihpyr - scale pyramidal cell ih conductance
def scaleihpyr (net,fctr):
    for cell in net.pyr.cell:
        for sec in cell.all_sec:
            sec(0.5).hcurrent.gfactor = fctr

# scaleihbas - scale basket cell ih conductance
def scaleihbas (net,fctr):
    for cell in net.bas.cell:
        cell.soma(0.5).HCN1.gfactor = fctr

# scaleiholm - scale olm cell ih conductance
def scaleiholm (net,fctr):
    for cell in net.olm.cell:
        cell.soma(0.5).Iholmw.gfactor = fctr

#  run sim varying pyr and bas ih
def runihbaspyr ():
    llfp = []
    for ih in [0.0, 0.5, 1.0, 1.5, 2.0]:
        print('setting pyr,bas Ih to', ih , 'X baseline')
        scaleihbas(net,ih)
        scaleihpyr(net,ih)
        h.run()
        net.calc_lfp()
        llfp.append( net.vlfp.to_python() )
    return llfp

llfp = runihbaspyr()

# draw the lfps in order of increasing Ih (bottom to top)
def drawlfps (xl=[-1,-1],killms=200):
    tt = linspace(0,h.tstop/1e3,len(llfp[0]))
    clrs = ['k','r','b','g','DarkOrange']
    sidx,eidx = int(killms/h.dt),int((h.tstop-killms)/h.dt)
    starty = amin(llfp[0])
    for i in range(5):
        na = numpy.array(llfp[i])+starty
        plot(tt[sidx:eidx],na[sidx:eidx],clrs[i])
        starty += amax(llfp[i])
    xlabel('Time (s)');
    if xl[0] > -1 and xl[1] > -1:  xlim(xl)
    tight_layout()

# get a list of PSDs for the different Ih values
def getlpsd (killms=200):
    lpsd = []
    for lfp in llfp:
        na = numpy.array(lfp)
        vec=h.Vector()
        sidx,eidx = int(killms/h.dt),int((h.tstop-killms)/h.dt)
        na = na[sidx:eidx]
        na -= mean(na);
        win = numpy.kaiser(len(na),5);
        na = na * win;
        vec.from_python(na)
        lpsd.append(h.nrnpsd(vec,1e3/h.dt))
        na = numpy.array(lpsd[-1].v[1].to_python())
        win = numpy.kaiser(25,5);
        na = numpy.convolve(na,win,'same');
        lpsd[-1].v[1].from_python(na)
    return lpsd

lpsd = []
if h.tstop >= 7.99e3: lpsd = getlpsd()

# plot the PSD
def plotpsd ():
    clrs = ['k','r','b','g','DarkOrange']
    for i in range(5):
        plot(lpsd[i].v[0].to_python(),lpsd[i].v[1].to_python(),clrs[i]);
        xlim((0,50));

# get the peaks. rns specifies min,max frequencies.
def getpks (rng):
    lx,ly=[],[]
    for psd in lpsd:
        psd.verbose=0
        psd.select('f','[]',rng[0],rng[1])
        pkx,pky = psd.getcol('f').x[int(psd.getcol('pow').max_ind())],psd.getcol('pow').max()
        lx.append(pkx); ly.append(pky)
        psd.verbose=1
    return lx,ly

# plot the peaks
def plotpks (lx,ly,band):
    clrs = ['k','r','b','g','DarkOrange']
    scatter(lx,ly,s=100,c=clrs)
    xlabel(band + ' peak (Hz)')
    ylabel(band + ' Power')
    tight_layout()

# draw the output
def drawfig ():
    if h.tstop >= 7.99e3:
        subplot(3,1,1); drawlfps(xl=[2,3]);
        ltx,lty=getpks([4,12]); subplot(3,1,2); plotpks(ltx,lty,'Theta');
        lgx,lgy=getpks([25,55]); subplot(3,1,3); plotpks(lgx,lgy,'Gamma');
    else:
        drawlfps()
    show()

drawfig()
