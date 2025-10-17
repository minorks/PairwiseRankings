# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:26:40 2025

@author: hokie
"""

from buildSeasons import Season
from solvers import Solvers
import unittest
import numpy as np


class seasonTests(unittest.TestCase):
    pSeason = Season("Test",rwrP = 0.75)
    sol = Solvers()

    def testColley(self):
        perfC = np.array(([4,-1,-1],[-1,4,-1],[-1,-1,4])).astype(float)
        self.assertTrue(np.array_equal(perfC,self.pSeason.tbls[0][0]))
        
        perfB = np.array(([2,1,0])).astype(float)
        self.assertTrue(np.array_equal(perfB, self.pSeason.tbls[0][1]))
        
        perfSol = self.sol.LinearSolver(C=perfC,b=perfB)
        self.assertTrue(np.array_equal(perfSol,
                         self.sol.LinearSolver(C=self.pSeason.tbls[0][0], 
                                      b=self.pSeason.tbls[0][1])))
        
    def testMassey(self):
        perfC = np.array(([2,-1,-1],[-1,2,-1],[1,1,1])).astype(float)
        self.assertTrue(np.array_equal(perfC,self.pSeason.tbls[1][0]))
        
        perfB = np.array(([3,0,0])).astype(float)
        self.assertTrue(np.array_equal(perfB, self.pSeason.tbls[1][1]))
        
        perfSol = self.sol.LinearSolver(C=perfC,b=perfB)
        self.assertTrue(np.array_equal(perfSol,
                         self.sol.LinearSolver(C=self.pSeason.tbls[1][0], 
                                      b=self.pSeason.tbls[1][1])))
        
# =============================================================================
#     def testNeumann(self):
#         perfC = np.array(([0,1,1],[0,0,1],[0,0,0]))
# =============================================================================
        
    def testRWR(self):
        perfD = np.array(([-0.5,0.75,0.75],[0.25,-1,0.75],[0.25,0.25,-1.5]))
        self.assertTrue(np.array_equal(perfD,self.pSeason.tbls[3]))
        
        perfSol = self.sol.RWRSolver(D=perfD)
        self.assertTrue(np.array_equal(perfSol,
                         self.sol.RWRSolver(D=self.pSeason.tbls[3])))
        
        tSeason = Season("Test",rwrP = 0.6)
        testD = np.array(([-0.8,0.6,0.6],[0.4,-1,0.6],[0.4,0.4,-1.2]))
        testSol = self.sol.RWRSolver(D=testD)
        self.assertTrue(np.array_equal(testSol,
                         self.sol.RWRSolver(D=tSeason.tbls[3])))
        
sTest = seasonTests()
unittest.main()