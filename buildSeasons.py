# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 15:36:03 2025

@author: hokie
"""

import pandas as pd
import numpy as np

class Season:
    urlHook = "https://masseyratings.com/scores.php?"
    
    def __init__(self,seasonType, seasonID, subsetID):
        self.seasonType = str(seasonType)
        self.getData(seasonID,subsetID)
        
    def getData(self,seasonID, subsetID):
        self.season = pd.read_csv(Season.urlHook+"s="+str(seasonID)+
                             "&sub="+str(subsetID)+"&all=1&mode=3&sch=on&format=1",
                            header=None,
                            names = ["RawDays","GameDay","Team1","GameLoc1","Score1",
                                     "Team2","GameLoc2","Score2"])
        
        self.teams = pd.read_csv(Season.urlHook+"s="+str(seasonID)+"&sub="+str(subsetID)+
                             "&all=1&mode=3&sch=on&format=2",
                            header=None,
                            names = ["TeamID","TeamName"])
        

    def makeColley(self):
         C = 2*np.eye(len(self.teams))
         WL = np.zeros(shape=(len(self.teams),2))
         b = np.zeros(shape=(len(self.teams),1))
         
         for gm in self.season.itertuples():
             tms = (int(gm.Team1)-1,int(gm.Team2)-1)
             
         	# For the colley matrix, C_ij =
            #     +t_i if i=j, where t_i is the total number of games played by team i
            #     n_ij if i<>j, where n_ij is the number of times team i played team j
             
             for i in range(2):
                C[tms[i],tms[i]] += 1
             C[tms[0],tms[1]] -= 1
             C[tms[1],tms[0]] -= 1
             
             # If team idA beats team idB, 
             # increase the win count for A and the loss count for B.
             
             WL[tms[0]] += (1,0) if int(gm.Score1) > int(gm.Score2) else (0,1)
             WL[tms[1]] += (0,1) if int(gm.Score1) > int(gm.Score2) else (1,0)
             
         for i in range(max(self.teams.TeamID)):
            b[i] = 1 + (0.5*(WL[i,0]-WL[i,1]))
                 
         return(C, WL, b)
     
    def makeMassey(self):
        C = np.eye(len(self.teams))
        PTS = np.zeros(shape=(len(self.teams),2))
        b = np.zeros(shape=(len(self.teams),1))
         
     	# For the Massey matrix, C_ij =
        # t_i if i=j, where t_i is the total number of games played by team i
        # -n_ij if i<>j, where n_ij is the number of times team i played team j
        
        for gm in self.season.itertuples():
            tms = (int(gm.Team1)-1,int(gm.Team2)-1)
            scores = (int(gm.Score1),int(gm.Score2))
            
            for i in range(2):
                for j in range(2):
                    C[tms[i],tms[j]] += 1 if (i == j) else -1
                    PTS[tms[i],j] += scores[0] if (i == j) else scores[1]                    
                    
        for i in range(max(self.teams.TeamID)):
            b[i] = PTS[i,0]-PTS[i,1]
            
        # Fix the rank deficiency by setting the last row of C to 1,
        # and the corresponding entry in b to 0.
        
        C[C.shape[0]-1,:] = 1
        b[C.shape[0]-1,0] = 0
            
        return (C, PTS, b)
    
    def makeNeumann():
        pass
    
    def makeRwr():
        pass
        
MBB25 = Season("Men's Basketball",604302,11590)

# MasseyRatings uses the following conventions for lookups:
# s = "season" [Sport and Year] (e.g., Men's College Basketball 2025 is "604302")
# sub = subset of season (e.g., NCAA Division I is "11590"; NAIA is "12795")
# all = 1 (vice "inter" = 1 [to denote non-confrence only] or 
#       "intra" = 1 [to denote in-conference only])
# mode = {1: "Text"; 2: "CSV Games"; 3: "CSV Teams"; 4: "CSV 'Hyper-Games'"}
# sch and/or exhib = on (use sch=on only to exclude exhibition games)
# format = {1: }
