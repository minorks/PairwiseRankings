# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 15:36:03 2025

@author: hokie
"""

from copy import copy
import pandas as pd
import numpy as np

class Season:
    urlHook = "https://masseyratings.com/scores.php?"
    
    # For testing purposes...
    perfSeason = pd.DataFrame({"RawDays" : [1,1,1],
                              "GameDay" : [20200101, 20200101, 20200101],
                              "Team1" : [1,1,2],
                              "GameLoc1": [1,1,1],
                              "Score1": [10,10,10],
                              "Team2" : [2,3,3],
                              "GameLoc2": [-1,-1,-1],
                              "Score2" : [9,8,9]})

    perfTeams = pd.DataFrame({"TeamID":[1,2,3],
                              "TeamName":["A","B","C"]})
    
    def __init__(self,seasonType, year, seasonID=-1, subsetID=-1, rwrP = 0.75):
        self.seasonType = str(seasonType)
        self.year = year
        self.getData(seasonID,subsetID)
        self.tbls = self.__makeAdjacency__(rwrP)
        
    def getData(self,seasonID, subsetID):
        if (seasonID > 0 and subsetID > 0):
            self.season = pd.read_csv(Season.urlHook+"s="+str(seasonID)+
                                 "&sub="+str(subsetID)+"&all=1&mode=3&sch=on&format=1",
                                header=None,
                                names = ["RawDays","GameDay","Team1","GameLoc1","Score1",
                                         "Team2","GameLoc2","Score2"])
            
            self.teams = pd.read_csv(Season.urlHook+"s="+str(seasonID)+"&sub="+str(subsetID)+
                                 "&all=1&mode=3&sch=on&format=2",
                                header=None,
                                names = ["TeamID","TeamName"])     
        else:
            self.season = self.perfSeason
            self.teams = self.perfTeams
        
    def __makeAdjacency__(self,rwrP):
        MC_C = np.zeros(shape=(self.teams.shape[0],self.teams.shape[0]))
        NP_C = copy(MC_C) # Adjacency for Neumann-Park 
        RWR_N = copy(MC_C) # Adjacency for RWR - games only (existence)
        RWR_B = copy(MC_C)
        WL = np.zeros(shape=(self.teams.shape[0],2))
        PTS = np.zeros(shape=(self.teams.shape[0],2))
        
        for gm in self.season.itertuples():
            tms = (int(gm.Team1)-1,int(gm.Team2)-1)
            scores = (int(gm.Score1),int(gm.Score2))
            
            for i in range(2):
                WL[tms[i]] += (1,0) if (scores[i]>scores[(i+1)%2]) else (0,1)
                RWR_B[tms[i],tms[(i+1)%2]] += 1 if (scores[i]>scores[(i+1)%2]) else -1
                for j in range(2):
                    MC_C[tms[i],tms[j]] += 1 if (i == j) else -1
                    NP_C[tms[i],tms[j]] += 1 if ((i != j) and (scores[j] > scores[i])) else 0
                    RWR_N[tms[i],tms[j]] += 1 if (i != j) else 0
                    PTS[tms[i],j] += scores[0] if (i == j) else scores[1]
     
        colTbls = self.makeColley(MC_C,WL)
        masTbls = self.makeMassey(MC_C,PTS)
        neuTbls = self.makeNeumann(NP_C,np.sum(RWR_N,axis=1))
        rwrTbls = self.makeRwr(RWR_N,RWR_B,WL,rwrP)
        return(colTbls,masTbls,neuTbls,rwrTbls)

    def makeColley(self,C,WL):
        C_Col = C + 2*np.eye(self.teams.shape[0]) # Add 2 to each diagonal element
        b = 1 + (0.5*(WL[:,0]-WL[:,1]))
        return(C_Col,b)
    
    def makeMassey(self,C,PTS):
        b = PTS[:,0]-PTS[:,1]
        C_Mas = copy(C)
        
        # Fix the rank deficiency by setting the last row of C to 1,
        # and the corresponding entry in b to 0.
        C_Mas[C.shape[0]-1,:] = 1
        b[b.shape[0]-1] = 0
        return(C_Mas,b)
    
    def makeNeumann(self, C, GMS):
        C_NP = copy(C)
        alpha = 0 if (max(np.linalg.eigvals(C)) == 0) else 1/self.__getAlpha__(GMS)
        return(C_NP,alpha)
    
    def makeRwr(self,N,B,WL,p):
        D = np.zeros(shape=B.shape)

        for k in range(D.shape[0]):
            D[k,k] = ((-p)*WL[k,1]) - ((1-p)*WL[k,0])
            for j in range(D.shape[1]):
                D[k,j] = ((0.5 * N[k,j])) + (((2*p)-1)/2)*B[k,j] if (j != k) else D[k,j]
                
        return(D)
                    
    def __getAlpha__(self,M):
        k = sum(M)/len(M)       # Mean games played
        k2 = sum(M**2)/len(M)   # MeanSquared games played
        return((k2-k)/(2*k))
        
# =============================================================================
#         FIX THIS STUFF
#         # Mean games played - count of games divided by count of teams
#         mean = (self.season.len * 2) / (len(self.teams.len))
#         
#         # MeanSquare - (actual)^2 divided by (teams-1)
#         # In this case, we'll weight each group of observations by the count
#         meanSquare = sum(M['Count']*(M['Played'])**2) / (len(self.teams)-1)
#         
#         return ((2*mean) / (meanSquare - mean))
# =============================================================================