# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:26:40 2025

@author: hokie
"""

from buildSeasons import Season
from solvers import LinearSolver
import unittest
import numpy as np


class seasonTests(unittest.TestCase):
    pSeason = Season("Test")

    def testColley(self):
        perfC = np.array(([4,-1,-1],[-1,4,-1],[-1,-1,4])).astype(float)
        self.assertTrue(np.array_equal(perfC,self.pSeason.tbls[0][0]))
        
        perfB = np.array(([2,1,0])).astype(float)
        self.assertTrue(np.array_equal(perfB, self.pSeason.tbls[0][1]))
        
        perfSol = LinearSolver(perfC,perfB)
        self.assertTrue(np.array_equal(perfSol,
                         LinearSolver(self.pSeason.tbls[0][0], 
                                      self.pSeason.tbls[0][1])))
        
    def testMassey(self):
        perfC = np.array(([2,-1,-1],[-1,2,-1],[1,1,1])).astype(float)
        self.assertTrue(np.array_equal(perfC,self.pSeason.tbls[1][0]))
        
        perfB = np.array(([3,0,0])).astype(float)
        self.assertTrue(np.array_equal(perfB, self.pSeason.tbls[1][1]))
        
        perfSol = LinearSolver(perfC,perfB)
        self.assertTrue(np.array_equal(perfSol,
                         LinearSolver(self.pSeason.tbls[1][0], 
                                      self.pSeason.tbls[1][1])))
        

sTest = seasonTests()
unittest.main()
# =============================================================================
#     runner = unittest.TextTestRunner()
#     runner.run(sTest.testColley())
#     runner.run(sTest.testMassey())
# =============================================================================
    
    


