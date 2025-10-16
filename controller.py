# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 13:58:44 2025

@author: hokie
"""

from buildSeasons import Season
from solvers import Solvers
from pandas import DataFrame

sol = Solvers()

# [0] = Season definition
# [1] = Season (constructed)
# [2] = Rankings
toAnalyze = ([("Men's Basketball",2025, 604302, 11590),None,None],
             [("College Football",2001, 41846, 11604),None,None],
             [("College Football",2007, 73929, 11604),None,None])

for s in toAnalyze:
    s[1] = Season(s[0][0],s[0][1],s[0][2],s[0][3])
    comp = DataFrame(data = {"Colley" : sol.LinearSolver(s[1].tbls[0][0], s[1].tbls[0][1])[:,1],
                             "Massey" : sol.LinearSolver(s[1].tbls[1][0], s[1].tbls[1][1])[:,1],
                             "RWR" : sol.RWRSolver(s[1].tbls[3])[:,1]})
    s[2] = comp.map(lambda x: s[1].teams['TeamName'][int(x)-1])
    
    
    
        
    



