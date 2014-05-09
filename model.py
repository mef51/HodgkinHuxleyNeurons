#!/usr/bin/python

from __future__ import division
import numpy as np
import pylab
import time

# sauce: http://www.neurdon.com/2011/01/26/neural-modeling-with-python-part-2/

# Potassium (K) Channel
alphaN = np.vectorize(lambda v: 0.01*(10 - v) / (np.exp((10-v)/10) - 1) if v != 10 else 0.1)
betaN  = lambda v: 0.125 * np.exp(-v/80)
nInf   = lambda v: alphaN(v)/(alphaN(v) + betaN(v))

# Sodium (Na) Channel (activating)
alphaM = np.vectorize(lambda v: 0.1*(25-v) / (np.exp((25-v)/10) - 1) if v!= 25 else 1)
betaM = lambda v: 4 * np.exp(-v/18)
mInf = lambda v: alphaM(v)/(alphaM(v) + betaM(v))

# Sodium (Na) Channel (inactivating)
alphaH = lambda v: 0.07 * np.exp(-v/20)
betaH  = lambda v: 1/(np.exp((30-v)/10) + 1)
hInf   = lambda v: alphaH(v)/(alphaH(v) + betaH(v))

# Channel Activity
v = np.arange(-50, 151) # millivolts
pylab.figure()
pylab.plot(v, mInf(v), v, hInf(v), v, nInf(v))
pylab.legend(('m', 'h', 'n'))
pylab.title('Steady state values of ion channel gating variables')
pylab.ylabel('Magnitude')
pylab.xlabel('Voltage (mV)')
pylab.savefig("mhn.jpg")

# Setup parameters and state variables
T    = 55    # ms
dt   = 0.025 # ms
timeLine = np.arange(0, T+dt, dt)

# Hodgkin-Huxley Parametahs (from the papah!)
restingVoltage     = 0      # V_rest (mv)
Cm                 = 1      # uF/cm2
gBarNa             = 120    # mS/cm2
gBarK              = 36     # mS/cm2
gBarL              = 0.3    # mS/cm2
sodiumPotential    = 115    # mV
potassiumPotential = -12    # mv
leakagePotential   = 10.613 # mV

Vm    = np.zeros(len(timeLine)) # The membrane potential we wanna find
Vm[0] = restingVoltage
m     = mInf(restingVoltage)
h     = hInf(restingVoltage)
n     = nInf(restingVoltage)

# Current Stimulus
# This is like a pulse
I = np.zeros(len(timeLine))
for i, t in enumerate(timeLine):
    if 5 <= t <= 30:
        I[i] = 10 # uA/cm2

# Main loop
pylab.figure()
for i in range(1, len(timeLine)):
    sodiumConductance    = gBarNa * (m**3) * h
    potassiumConductance = gBarK  * (n**4)
    leakageConductance   = gBarL

    # integrate the equations on m, h, and n
    m += (alphaM(Vm[i-1]) * (1 - m) - betaM(Vm[i-1])*m) * dt
    h += (alphaH(Vm[i-1]) * (1 - h) - betaH(Vm[i-1])*h) * dt
    n += (alphaN(Vm[i-1]) * (1 - n) - betaN(Vm[i-1])*n) * dt

    # now integrate the changes in V
    sodiumCurrent = sodiumConductance * (Vm[i-1] - sodiumPotential)
    potassiumCurrent = potassiumConductance * (Vm[i-1] - potassiumPotential)
    leakageCurrent = leakageConductance * (Vm[i-1] - leakagePotential)
    Vm[i] = Vm[i-1] + (I[i-1] - sodiumCurrent - potassiumCurrent - leakageCurrent) * dt / Cm

    # update status
    if i % 25 == 0:
        # update status every 25 frames (about a second of video).
        # don't wanna print a lot cuz it slows things down
        print "Time: " + str(i*dt) + ", Saving frame " + str(i)

    # plot a frame of the graph
    pylab.plot(timeLine[:i+1], Vm[:i+1], timeLine[:i+1], I[:i+1])
    pylab.ylim([-20,120])
    pylab.xlim([0,60])
    pylab.title('Hodgkin-Huxley: t = ' + format(i*dt, '.3f') + ' ms')
    pylab.ylabel('Membrane Potential (mV)')
    pylab.xlabel('Time (ms)')
    pylab.savefig("frames/model" + str(i) + ".jpg")
    pylab.clf()

pylab.figure()
pylab.plot(timeLine, Vm, timeLine, I)
pylab.title('Hodgkin-Huxley Example')
pylab.ylabel('Membrane Potential (mV)')
pylab.xlabel('timeLine (msec)')
pylab.savefig("model.jpg")

