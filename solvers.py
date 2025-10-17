# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 17:12:25 2025

@author: hokie
"""
import numpy as np
from scipy.linalg import null_space

class Solvers:
    
    def __init__(self):
        pass
    
    def __assignRanks__(self,soln):
        rnk = np.c_[soln, np.linspace(0,soln.shape[0],soln.shape[0],endpoint=False)]+(0,1)
        rnk = rnk[rnk[:,0].argsort()[::-1]]
        return(rnk)
    
    def LinearSolver(self,C,b):    
        r = np.linalg.solve(C,b)
        return(self.__assignRanks__(r))
    
    def NewmannSolver(self,C,alpha):
        kout = np.sum(C,axis=1) # Wins from "outward" vectors - sum by row
        kin = np.sum(C,axis=0) # Losses from "inward" vectors - sum by column
        
        MAT = np.eye(C.shape[0]) - alpha*np.transpose(C)
        winScore = np.dot(np.linalg.inv(MAT),np.transpose(kout))
        
        MAT = np.eye(C.shape[0])  - alpha*C
        lossScore = np.dot(np.linalg.inv(MAT), np.transpose(kin))
        
        tScore = winScore-lossScore
        return(self.__assignRanks__(tScore))   

    def RWRSolver(self,D):
        r = null_space(D)   # Returns unitary eigenvector in 2-Norm
        r = r / sum(r)      # Rescales eigenvector 1-Norm to obtain distribution
        return(self.__assignRanks__(r),self.__getQMin__(r))
    
    def __getQMin__(self,ranks):
        q = 0
        for i in range(1,min(5,len(ranks)),1):
            q += ((ranks[i-1] + ranks[i]) / ((ranks[i-1]-ranks[i])**2))-1
        return(q)
            
    
    
   