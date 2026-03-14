# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:14:29 2026

@author: ardfo

Main script of CTCC Number Calculator
"""

import pandas as pd
import numpy as np
from datetime import datetime
StartTime = datetime.now()

##############################################################################
#Import the data
data = pd.read_csv("AllMatches.csv")
dataEMWCL = pd.read_csv("EMWCL.csv")
optout = np.array(pd.read_csv("OptedOut.txt",header = None))
##############################################################################
