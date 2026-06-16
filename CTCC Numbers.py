# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:14:29 2026

@author: ardfo

Main script of CTCC Number Calculator
"""

import pandas as pd
import numpy as np
from datetime import datetime

from scripts.list import *
from scripts.player import *
from scripts.checker import *
StartTime = datetime.now()

##############################################################################
#Import the data
DataDir = "data"
data = pd.read_csv(DataDir+"/AllMatches.csv")
dataEMWCL = pd.read_csv(DataDir+"/EMWCL.csv")
with open(str(DataDir)+"/OptedOut.txt") as f:
    optout = [line.strip() for line in f]
del f
PreviousNumbers = pd.read_csv(DataDir+"/PreviousNumbers.csv")
##############################################################################

#Initialization
#####################################################################################################################
#Get the Names of all players with a recorded game entry without any duplicates
PlayerNames = pd.concat([data['Player Name'], dataEMWCL['Player Name']]).unique()
#Save a dictionary with keys of the player names, each to a Player object
Players = {}
for name in PlayerNames:
    Players[name] = Player()
    Players[name].name = name

OutputList = CTCCList()

#Update those with a number already/opted out
for player in optout:
    Players[player].Qualified = True
for player,number,date,team,opp in zip(PreviousNumbers['Player'],PreviousNumbers['CTCC Number'],PreviousNumbers['Achieved:'],PreviousNumbers['For:'],PreviousNumbers['Vs:']):
    if Players[player].Qualified == False: #Prevent overwriting lower number
        Players[player].Qualified = True
        Players[player].Number = number
    OutputList.Players.append(player)
    OutputList.ClubNumbers.append(number)
    OutputList.DateOfAchievement.append(date)
    OutputList.TeamAchieved.append(team)
    OutputList.OppositionAchieved.append(opp)
del player,name,date,team,opp #cleanup

#####################################################################################################################
#Set the criteria, was originally 20 first XI games or 150 games overall. Updated in 2025 to 25, 100 and 50 EMWCL. 1st XI is an exlusive qualifyer, do not count together. e.g. 10 1st XI and 75 open age does not qualify
Criteria = [25,100,50] #[1st XI, Open Age, EMWCL]
NextAwardableNumber = max(PreviousNumbers['CTCC Number'])+1

#####################################################################################################################
def RunLoop(data):
    for Player,TeamID,Opposition,Date in zip(data['Player Name'],data['cm_teamID'],data['Opponent'],data['FixtureDate']):
        Pass = CheckIfMet(TeamID,Players[Player],Criteria) #Update and get True/False if met
        if Pass == True:
            global NextAwardableNumber
            OutputList.Players.append(Player)
            OutputList.DateOfAchievement.append(Date)
            OutputList.TeamAchieved.append(TeamID)
            OutputList.OppositionAchieved.append(Opposition)
            OutputList.ClubNumbers.append(NextAwardableNumber)
            Players[Player].Number = NextAwardableNumber
            NextAwardableNumber += 1
RunLoop(data) #Run the loop through Open Age data:
RunLoop(dataEMWCL) #Run the loop through EMWCL data:
        
#####################################################################################################################
#Save
DataFrame = {'CTCC Number':np.asarray(OutputList.ClubNumbers),'Player':OutputList.Players,'Achieved:':OutputList.DateOfAchievement,
             'For:':OutputList.TeamAchieved,'Vs:':OutputList.OppositionAchieved}
ClubNumbers = pd.DataFrame(DataFrame)
del DataFrame
ClubNumbers.to_csv('data/PreviousNumbers.csv',index=False)

#####################################################################################################################
#Find who is close
Names = [Player.name for Player in Players.values()]
Points = [Player.CTCCPoints for Player in Players.values()]
FirstXIGames = [Player.Matches1stXI for Player in Players.values()]
TotalPoints = pd.DataFrame({'Name':Names,'CTCC Points':Points,'1s Matches':FirstXIGames})
del Names,Points,FirstXIGames

print('Complete, Time Taken:',datetime.now()-StartTime)