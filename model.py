#!/usr/bin/python

from __future__ import division
import numpy as np
import pylab

# sauce: http://www.neurdon.com/2011/01/26/neural-modeling-with-python-part-2/

# Potassium (K) Channel
alphaN = np.vectorize(lambda v: 0.01*(10 - v) / (np.exp((10-v)/10) - 1) if v != 10 else 0.1)
betaN  = lambda v: 0.125 * np.exp(-v/80)
nInf   = lambda v: alphaN(v)/(alphaN(v) + betaN(v))

# Sodium (Na) Channel (activating)
alphaM = np.vectorize(lambda v: 0.1*(25-v) / (np.exp((25-v)/10) - 1) if v!= 25 else 1)
betaM = lambda v: 4* np.exp(-v/18)
mInf = lambda v: alphaM(v)/(alphaM(v) + betaM(v))

# Sodium (Na) Channel (inactivating)
alphaH = lambda v: 0.07 * np.exp(-v/20)
betaH  = lambda v: 1/(np.exp((30-v)/10) + 1)
hInf   = lambda v: alphaH(v)/(alphaH(v) + betaH(v))

# Channel Activity
v = np.arangy(-50, 151) # millivolts
