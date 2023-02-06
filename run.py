# $Id: run.py,v 1.56 2012/09/20 14:06:03 samn Exp $

from pyinit import *
from geom import *
# from network import *
# from params import *
import sys
try:
    import filt
except:
    print("Couldn't import filt routines used in gethilbnqs")

# sets up external inputs
if net.noise:
    net.set_noise_inputs(h.tstop) #h.tstop sets duration of inpus for make noise case

# handler for printing out time during simulation run
def fi():
    for i in range(0,int(h.tstop),100):
        h.cvode.event(i, "print " + str(i))

fih = h.FInitializeHandler(1, fi)

# initialize random # generators of NetStims - forces it at beginning of each sim
def myInitNetStims():
    net.init_NetStims()

fihns = h.FInitializeHandler(0, myInitNetStims)

# save LFP with current pyramidal cell voltages
_svNUM = 0
def saveLFPInterm (fbase):
    global _svNUM
    fout = fbase + "_svNUM_" + str(_svNUM) + "_lfp.vec"
    print("time is " , h.t, " saving LFP to " , fout)
    net.calc_lfp()
    mysvvec(fout,net.vlfp)
    net.clear_mem()
    _svNUM += 1

# setup events to save LFP intermittently
_svFBase = "./tmp_"
_svINC = 1000
def setSaveLFPEvents ():
    global _svNUM
    _svNUM = 0
    stre = "nrnpython(\"saveLFPInterm(_svFBase)\")"
    for tt in range(_svINC,int(h.tstop),_svINC):
        h.cvode.event(tt,stre)
    h.cvode.event(h.tstop,stre)

# example to save LFP intermittently:
#  fisv = h.FInitializeHandler(0, setSaveLFPEvents)

#save vec to fn (fn is path)
def mysvvec(fn,vec):
    fp = h.File()
    fp.wopen(fn)
    if fp.isopen():
        vec.vwrite(fp)
        fp.close()
    else:
        print("savevec ERR: couldn't open " + fn)

#run a sim and save data
def minrunsv (simstr,tstop=1200,dt=0.1,savevolt=False):
    h.tstop=tstop
    h.dt=dt
    h.run()
    print("saving output data")
    net.calc_lfp()
    fn = "./data/"+simstr+"_lfp.vec"
    mysvvec(fn,net.vlfp)
    net.setsnq() # make NQS with spike times
    fn = "./data/"+simstr+"_snq.nqs"
    net.snq.sv(fn)
    if savevolt:
        nqv = net.getnqvolt()
        nqv.sv('./data/'+simstr+'_nqvolt.nqs')

#read a Vector from file, fn is file-path, vec is a Vector
def myrdvec(fn,vec):
    fp=h.File()
    fp.ropen(fn)
    if not fp.isopen():
        print("myrdvec ERRA: Couldn't open " + fn)
        return False
    vec.vread(fp)
    fp.close()
    return True

# concat a series of LFPs - fbase is base of filename
def catlfp (fbase,svn):
    vlfp, vtmp = h.Vector(), h.Vector()
    for i in range(svn):
        fin = fbase + "_svNUM_" + str(i) + "_lfp.vec"
        if myrdvec(fin,vtmp): vlfp.append(vtmp)
    return vlfp

#load data from minrunsv into net.vlfp,net.snq
def loadminrundat(simstr,datadir="./data/",rdvolt=False):
    fs = datadir+simstr+"_lfp.vec"
    try:
        net.vlfp.resize(0)
    except:
        net.vlfp = h.Vector()
        myrdvec(fs,net.vlfp)
    fs = datadir+simstr+"_snq.nqs"
    try:
        h.nqsdel(net.snq)
    except:
        pass
    try:
        net.snq=h.NQS(fs)
    except:
        print("loadminrundat ERRB: couldn't read snq from " + fs)
    net.snq.verbose=0 # next, copy snq into vectors so can plot with net.rasterplot
    for po in net.cells:
        for i in range(len(po.lidvec)):
            ID = po.cell[i].id
            po.lidvec[i].resize(0)
            po.ltimevec[i].resize(0)
            if net.snq.select("id",ID):
                po.lidvec[i].copy(net.snq.getcol("id"))
                po.ltimevec[i].copy(net.snq.getcol("t"))
    net.snq.verbose=1
    if rdvolt:
        try:
            h.nqsdel(net.nqv)
        except:
            pass
        fs = datadir+simstr+'_nqvolt.nqs'
        try:
            net.nqv=h.NQS(fs)
        except:
            print("loadminrundat ERRC: couldn't read nqvolt from " + fs)

def myrast(spikes,times,sz=12):
    if h.g[0] == None:
        h.gg()
    spikes.mark(h.g[0],times,"O",sz,1,1)
    h.g[0].exec_menu("View = plot")

############################
#   setup multithreading   #
pc = h.ParallelContext()   #
pc.nthread(32)             #
############################
####################################################################################################
