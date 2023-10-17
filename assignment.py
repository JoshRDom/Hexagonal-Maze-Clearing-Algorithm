# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:34:06 2023

@author: jrawe
"""
import math
import copy 
import timeit
from gui import runAnimation

# simple insertion sort function for array a containing dictionaries with the cost key
def insertionSort(a):
    for i in range(1,len(a)):
        if a[i]["cost"] < a[i-1]["cost"]:
            temp = a[i]
            j=i
            while j>0 and a[j-1]["cost"]>temp["cost"]:
                a[j] = a[j-1]
                j -= 1
            a[j] = temp

# straight-line distance function specific for hexagonal map with team's chosen axes
def sld(room1,room2):
    d_uv = [room2[0] - room1[0], room2[1] - room1[1]]
    d_xy = [math.sqrt(3)*d_uv[0]/2, -1*d_uv[0]/2-d_uv[1]]
    return math.sqrt(d_xy[0]**2 + d_xy[1]**2)
            

# mapToNavigate is a Map dictionary
# goalRoom is a pair of coordinates (x,y)
def aStar(mapToNavigate,goalRoom):
    if goalRoom in mapToNavigate["x,y"]:
        frontier = [] # Array of pairs of room sequence and cost. Room sequence is a list of rooms
        explored = [] # Array of explored rooms. Algorithm should not revisit explored rooms
        found_goal = False
        
        # initialise frontier
        frontier.append({"sequence":[mapToNavigate["bin"]["currentRoom"]], "cost":0})
        
        while not found_goal:
            # goal test
            if frontier[0]["sequence"][-1] == goalRoom:
                found_goal = True
            else:
                nextRooms = [] # Array of rooms adjacent to last visited room of first element in frontier
                # check if mathematically adjacent rooms exist in the map
                for step in mapToNavigate["steps"]:
                    if ( frontier[0]["sequence"][-1][0]+step[0] , frontier[0]["sequence"][-1][1]+step[1] ) in mapToNavigate["x,y"]:
                        #if mapToNavigate[( frontier[0]["sequence"][-1][0]+step[0] , frontier[0]["sequence"][-1][1]+step[1] )] is None:
                            nextRooms.append((frontier[0]["sequence"][-1][0]+step[0],frontier[0]["sequence"][-1][1]+step[1]))
                explored.append(frontier[0]["sequence"][-1])
                
                # find a path to each room of interest
                for nextRoom in nextRooms:
                    if not nextRoom in explored:
                        # add path to frontier
                        new_path = copy.deepcopy(frontier[0])
                        new_path["sequence"].append(nextRoom)
                        new_path["cost"] += 1 + sld(goalRoom,nextRoom)
                        frontier.append(new_path)
                        
                        # check for redundant paths
                        for i in range(0,len(frontier)-1):
                            if frontier[i]["sequence"][-1] == frontier[-1]["sequence"][-1]:
                                if frontier[i]["cost"] > frontier[-1]["cost"]:
                                    del frontier[i]
                                    break
                                elif frontier[i]["cost"] <= frontier[-1]["cost"] and i != len(frontier)-1:
                                    del frontier[-1]
                                    break
                
                # remove the expanded frontier
                del frontier[0]
                # sort the frontier by path cost
                insertionSort(frontier)
        return frontier[0]["sequence"]
     
# test if adding rubbish will cause bin malfunction
def binMalfunction(rubbishBin,newRubbish):
    Vavailable = rubbishBin["Vmax"]-rubbishBin["Vtotal"]
    Wavailable = rubbishBin["Wmax"]-rubbishBin["Wtotal"]
    return Vavailable < newRubbish[0] or Wavailable < newRubbish[1]

# function to clear the map
# returns the sequence of rooms to visit along with the number of rooms visited
def clear(mapToClear):
    # pre-process map
    # make a copy of the map that is already cleared
    clearedMap = copy.deepcopy(mapToClear)
    for room in clearedMap["x,y"]:
        if type(clearedMap[room]) == tuple:
            clearedMap[room] = None
    
    # find the shortest path from starting room to rubbish
    shortestPathToRubbish = {}
    for room in mapToClear["x,y"]:
        if type(mapToClear[room]) == tuple:
            shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)] = {}
            clearedMap[room] = mapToClear[room]
            shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["sequence"] = aStar(clearedMap,room)
            clearedMap[room] = None
            shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["isObstructed"] = False
            for step in shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["sequence"]:
                if step != shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["sequence"][-1] \
                    and step != shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["sequence"][0]:
                    if type(mapToClear[step]) == tuple:
                        shortestPathToRubbish[(mapToClear["bin"]["currentRoom"],room)]["isObstructed"] = True
                        break
    # find the shortest path between rooms with rubbish
    for i in range(0,len(mapToClear["x,y"])):
        if type(mapToClear[mapToClear["x,y"][i]]) == tuple:
            clearedMap["bin"]["currentRoom"] = mapToClear["x,y"][i]
            for j in range(i+1,len(mapToClear["x,y"])):
                if type(mapToClear[mapToClear["x,y"][j]]) == tuple:
                    shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])] = {}
                    clearedMap[mapToClear["x,y"][j]] = mapToClear[mapToClear["x,y"][j]]
                    shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["sequence"] = aStar(clearedMap,mapToClear["x,y"][j])
                    clearedMap[mapToClear["x,y"][j]] = None
                    shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["isObstructed"] = False
                    for step in shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["sequence"]:
                        if step != shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["sequence"][-1] \
                            and step != shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["sequence"][0]:
                            if type(mapToClear[step]) == tuple:
                                shortestPathToRubbish[(mapToClear["x,y"][i],mapToClear["x,y"][j])]["isObstructed"] = True
                                break
    
    
    # find the nearest disposal room to each rubbish
    nearestDisposalToRubbish = {}
    clearedMap["bin"]["Vtotal"] = clearedMap["bin"]["Vmax"]
    clearedMap["bin"]["Wtotal"] = clearedMap["bin"]["Wmax"]
    for i in range(0,len(mapToClear["x,y"])):
        if type(mapToClear[mapToClear["x,y"][i]]) == tuple:
            clearedMap["bin"]["currentRoom"] = mapToClear["x,y"][i]
            nearestDisposalToRubbish[mapToClear["x,y"][i]] = {}
            nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"] = None
            for j in range(0,len(mapToClear["x,y"])):
                if mapToClear[mapToClear["x,y"][j]] == "disposal":
                    path = aStar(clearedMap,mapToClear["x,y"][j])
                    if nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"] is None or len(path) < len(nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"]):
                        nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"] = path
                        nearestDisposalToRubbish[mapToClear["x,y"][i]]["isObstructed"] = False
                        for step in nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"]:
                            if step != nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"][-1] \
                                and step != nearestDisposalToRubbish[mapToClear["x,y"][i]]["sequence"][0]:
                                if type(mapToClear[step]) == tuple:
                                    nearestDisposalToRubbish[mapToClear["x,y"][i]]["isObstructed"] = True
                                    break
    
    frontier = [] # Array of pairs of outcomes, cost and room sequence. Outcome is a map object
    found_goal = False
    frontier.append({"map":mapToClear, "cost":0, "sequence":[mapToClear["bin"]["currentRoom"]]})
    
    while not found_goal:
        nextRooms = []
        
        # get rooms that Ronny can aim to move to
        for room in frontier[0]["map"]["x,y"]:
            roomType = frontier[0]["map"][room]
            
            # Ronny can move to a room with rubbish if the new rubbish will not cause the bin to stop moving
            if type(roomType) == tuple:
                if not binMalfunction(frontier[0]["map"]["bin"],frontier[0]["map"][room]):
                    nextRooms.append(room)
                    
        # Ronny can move to the room's nearest disposal room if the bin has rubbish
        if frontier[0]["map"]["bin"]["Vtotal"] > 0 and frontier[0]["map"]["bin"]["Wtotal"] > 0:
            nextRooms.append(nearestDisposalToRubbish[frontier[0]["map"]["bin"]["currentRoom"]]["sequence"][-1])
        
        # get outcomes when Ronny visits each nextRoom
        for nextRoom in nextRooms:
            # instantiate a copy of the outcome with the smallest cost
            newOutcome = copy.deepcopy(frontier[0])
            
            # find the shortest sequence of empty rooms to nextRoom
            shortestPath = []
            if type(mapToClear[nextRoom]) == tuple:
                if (frontier[0]["map"]["bin"]["currentRoom"],nextRoom) in shortestPathToRubbish:
                    if not shortestPathToRubbish[(frontier[0]["map"]["bin"]["currentRoom"],nextRoom)]["isObstructed"]:
                        shortestPath = shortestPathToRubbish[(frontier[0]["map"]["bin"]["currentRoom"],nextRoom)]["sequence"]
                    else:
                        shortestPath = aStar(frontier[0]["map"],nextRoom)
                elif (nextRoom,frontier[0]["map"]["bin"]["currentRoom"]) in shortestPathToRubbish:
                    if not shortestPathToRubbish[(nextRoom,frontier[0]["map"]["bin"]["currentRoom"])]["isObstructed"]:
                        shortestPath = shortestPathToRubbish[(nextRoom,frontier[0]["map"]["bin"]["currentRoom"])]["sequence"][::-1]
                    else:
                        shortestPath = aStar(frontier[0]["map"],nextRoom)
                else:
                    shortestPath = aStar(frontier[0]["map"],nextRoom)
            elif mapToClear[nextRoom] == "disposal":
                if not nearestDisposalToRubbish[frontier[0]["map"]["bin"]["currentRoom"]]["isObstructed"]:
                    shortestPath = nearestDisposalToRubbish[frontier[0]["map"]["bin"]["currentRoom"]]["sequence"]
                else:
                    shortestPath = aStar(frontier[0]["map"],nextRoom)
            
            # update sequence
            del newOutcome["sequence"][-1]
            newOutcome["sequence"].extend(shortestPath)
            
            # update cost
            newOutcome["cost"] += len(shortestPath)-1
            
            # update map
            newOutcome["map"]["bin"]["currentRoom"] = nextRoom
            if type(newOutcome["map"][nextRoom]) == tuple:
                newOutcome["map"]["bin"]["Vtotal"] += newOutcome["map"][nextRoom][0]
                newOutcome["map"]["bin"]["Wtotal"] += newOutcome["map"][nextRoom][1]
                newOutcome["map"][nextRoom] = None
            elif newOutcome["map"][nextRoom] == "disposal":
                newOutcome["map"]["bin"]["Vtotal"] = 0
                newOutcome["map"]["bin"]["Wtotal"] = 0
            frontier.append(newOutcome)
            
            # check for redundant path. delete the one with higher path cost
            for i in range(0,len(frontier)-1):
                if frontier[i]["map"] == frontier[-1]["map"]:
                    if frontier[i]["cost"] > frontier[-1]["cost"]:
                        del frontier[i]
                        break
                    elif frontier[i]["cost"] <= frontier[-1]["cost"] and i != len(frontier)-1:
                        del frontier[-1]
                        break
        
        # remove the expanded frontier
        del frontier[0]
        # sort the frontier by path cost
        insertionSort(frontier)
        
        # restrict number of outcomes with same cost
        window_size = 50
        num_to_del = 0
        for i in range(0,len(frontier)):
            if frontier[i]["cost"] > frontier[0]["cost"] and i < window_size:
                break
            elif frontier[i]["cost"] == frontier[0]["cost"] and i < window_size:
                num_to_del += 1
            elif frontier[i]["cost"] == frontier[0]["cost"] and i >= window_size:
                break
        del frontier[window_size:window_size+num_to_del]
                
        print("Number of spaces moved: " + str(frontier[0]["cost"]) + ". Last room visited: " + str(frontier[0]["sequence"][-1]))
        
        # goal test
        found_goal = True
        for room in frontier[0]["map"]["x,y"]:
            if type(frontier[0]["map"][room]) == tuple:
                found_goal = False
        found_goal = found_goal and frontier[0]["map"]["bin"]["Vtotal"] == 0 and frontier[0]["map"]["bin"]["Wtotal"] == 0
    
    print('Solution: ' + str(frontier[0]["sequence"]))            
    return frontier[0]["sequence"]

## driver code
if __name__ == '__main__':
    start_time = timeit.default_timer()
    myMap = {}
    
    # initialise facts
    myMap["x,y"] = []
    myMap["steps"] = [(0,1),(0,-1),(1,0),(1,-1),(-1,0),(-1,1)]
    myMap["bin"] = {}
    myMap["bin"]["Vmax"] = 5
    myMap["bin"]["Wmax"] = 40
    for q in range(0,9):
        for r in range(0,6):
            x = q
            y = r-math.ceil(q/2)
            myMap["x,y"].append((x,y))
            if x==3 and y==-1 or x==2 and y==1:
                myMap[(x,y)] = (1,5)
            elif x==6 and y==1:
                myMap[(x,y)] = (2,5)
            elif x==3 and y==2:
                myMap[(x,y)] = (3,5)
            elif x==0 and y==5:
                myMap[(x,y)] = (1,10)
            elif x==6 and y==-2 or x==4 and y==0:
                myMap[(x,y)] = (2,10)
            elif x==8 and y==-3:
                myMap[(x,y)] = (3,10)
            elif x==4 and y==2:
                myMap[(x,y)] = (1,20)
            elif x==7 and y==-1:
                myMap[(x,y)] = (2,20)
            elif x==7 and y==-4:
                myMap[(x,y)] = (1,30)
            elif x==1 and y==2:
                myMap[(x,y)] = (3,30)
            elif x==2 and y==4 or x==5 and y==-3 or x==8 and y==1:
                myMap[(x,y)] = "disposal"
            else:
                myMap[(x,y)] = None
                
    # initialise mutable data
    myMap["bin"]["Vtotal"] = 0
    myMap["bin"]["Wtotal"] = 0
    myMap["bin"]["currentRoom"] = (0,0)
    
    end_time = timeit.default_timer()
    runAnimation(clear(myMap))
    print("The runtime of the function is {} seconds".format(end_time - start_time))