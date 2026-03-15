# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 23:16:47 2026

@author: ardfo

Code to handle Meeting Criteria
"""

def CheckIfMet(TeamID,Player,Criteria):
    '''
    Parameters
    ----------
    TeamID : str
        Play cricket team ID from the current match record.
    Player : Player object
        Player object with records of current games, points etc.
    Criteria : List of integers
        [0] - Qualifying number of 1st XI games
        [1] - Qualifying number of Open Age games
        [2] - Qualifying number of EMWCL games

    Returns
    -------
    Passed : boolean
        If player has just met the criteria with this game, returns True, else
        returns False.
    '''
    PointsBefore = Player.CTCCPoints #Get CTCC Points before this match
    FirstXIBefore = Player.Matches1stXI # Get 1st XI games before
    
    #1s
    if (TeamID==8921):
        Player.Matches1stXI += 1
        Player.CTCCPoints += 100/Criteria[1]
    #2s
    if (TeamID==8922):
        Player.Matches2ndXI += 1
        Player.CTCCPoints += 100/Criteria[1]
    #3s
    if (TeamID==77571):
        Player.Matches3rdXI += 1
        Player.CTCCPoints += 100/Criteria[1]
    #4s
    if (TeamID==204987):
        Player.Matches4thXI += 1
        Player.CTCCPoints += 100/Criteria[1]

    #EMWCL        
    if (TeamID==301091 or TeamID==379086 or TeamID==354443):
        Player.MatchesEMWCL += 1
        Player.CTCCPoints += 100/Criteria[2] 
        
    #Check if freshly qualifed        
    if Player.Qualified == False:
        if (PointsBefore<100 and Player.CTCCPoints>=100) or (FirstXIBefore<Criteria[0] and Player.Matches1stXI>=Criteria[0]):
            Player.Qualified = True
            return True
    else:
        return False