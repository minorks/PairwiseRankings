# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 17:12:25 2025

@author: hokie
"""
import numpy as np

def LinearSolver(C,b):
    
    r = np.linalg.solve(C,b)
    rnk = np.c_[r, np.linspace(0,r.shape[0],r.shape[0],endpoint=False)]+(0,1)
    rnk = rnk[rnk[:,0].argsort()[::-1]]
    return(rnk)
   