# -*- coding: utf-8 -*-
# Saahas Buricha , Perm: 3017456 12/6/2024 MP #2
from collections import deque
import heapq
import time

# Global variable to track start time
timerTracker = None

def absolDist(loc1, loc2):
    distOne = abs(loc1[0] - loc2[0]) 
    distTwo = abs(loc1[1] - loc2[1])
    return distOne + distTwo

def findCoinValues(position, coins, penalty_k):
    if not coins:
        return 0

    coinVal = 0
    for coinPos in coins:
        distToCoin = absolDist(position, coinPos)
        net_value = 20 - (distToCoin * penalty_k)

        if net_value > 0:
            coinVal += net_value / (distToCoin + 1)  

    return coinVal

def calcCoinBenefit(position, coins, penalty_k, radius=2):
    if not coins:
        return -float('inf')
    
    totBenefit = 0
    for c in coins:
        if abs(position[0] - c[0]) <= radius and abs(position[1] - c[1]) <= radius:
            dist = absolDist(position, c)

            currbenefit = 10 - (dist * penalty_k)
            if currbenefit > 0:
                totBenefit += currbenefit
    
    return totBenefit



def locGoalPos(currMap):
    for x in range(len(currMap)):
        for y in range(len(currMap[0])):

            if currMap[x][y] == 'goal':
                return (x, y)
    return None

# def findCarDanger(position, carPos):
#     if not carPos:
#         return 0

#     danger = 0
#     for c in carPos:
#         dist = absolDist(position, c)
#         if dist <= 2:
#             danger += (3 - dist) * 5  

#     return danger

def findValidMoves(currMap, position, currCarPositionsall):
    x, y = position
    moves = {
        'W': (x, y - 1),

        'D': (x + 1, y),

        'S': (x, y + 1),

        'A': (x - 1, y),

        'I': (x, y)  
    }

    validMoves = []
    for move, (xprime, yprime) in moves.items():

        if (0 <= xprime < len(currMap) and 0 <= yprime < len(currMap[0])

           and currMap[xprime][yprime] != 'wall'

           and (xprime, yprime) not in currCarPositionsall):

            validMoves.append((move, (xprime, yprime)))

    return validMoves




def calcHueristic(position, goalPos, coins, carPos, Gscore, penalty_k):
    distCost = absolDist(position, goalPos) * penalty_k


    coinPotentialVal = findCoinValues(position, coins, penalty_k)


    # carDanger = findCarDanger(position, carPos)
    return distCost - coinPotentialVal + Gscore

def gAlgorithmCoinCollect(curPos, coins):
    if not coins:
        return None


    nearest = min(coins, key=lambda coin: absolDist(curPos, coin))

    return nearest

def aStarGoal(currMap, start_pos, goalPos, currCoins, currCarPositionsall, penalty_k):
    timerTracker = time.time()
    max_time = 450  #set the lim


    open_set = [(calcHueristic(start_pos, goalPos, currCoins, currCarPositionsall, 0, penalty_k), 0, start_pos, [])]
    heapq.heapify(open_set)


    Gscores = {start_pos: 0}
    closed_set = set()
    best_move = 'I' 

    while open_set:
        if time.time() - timerTracker > max_time:
            return best_move
        fscore, Gscore, current_pos, path = heapq.heappop(open_set)


        if current_pos == goalPos:
            return path[0] if path else 'I'


        if current_pos in closed_set:
            continue



        closed_set.add(current_pos)
        validMoves = findValidMoves(currMap, current_pos, currCarPositionsall)
        for move, next_pos in validMoves:
            if next_pos in closed_set:
                continue
            gValaddPen = Gscore + penalty_k
            if next_pos not in Gscores or gValaddPen < Gscores[next_pos]:
                Gscores[next_pos] = gValaddPen
                Hscore = calcHueristic(next_pos, goalPos, currCoins, currCarPositionsall, gValaddPen, penalty_k)
                new_path = path + [move]
                heapq.heappush(open_set, (Hscore, gValaddPen, next_pos, new_path))
                if Hscore < fscore and new_path:
                    best_move = new_path[0]




    return 'I'

def logic_A(currMap, currPos, currCoins, currCarPositionsall, penalty_k):

    global timerTracker


    if timerTracker is None:
        timerTracker = time.time()


    goalPos = locGoalPos(currMap)

    if not goalPos:
        return 'I'
    if currPos == goalPos:
        return 'I'


    coinBenefit = calcCoinBenefit(currPos, currCoins, penalty_k, radius=2)


    if coinBenefit > 0:
        greedy_target = gAlgorithmCoinCollect(currPos, currCoins)
        if greedy_target:
            ans = aStarGoal(currMap, currPos, greedy_target, currCoins, currCarPositionsall, penalty_k)
            return ans


    if time.time() - timerTracker > 500 or coinBenefit <= 0:
        return aStarGoal(currMap, currPos, goalPos, set(), currCarPositionsall, penalty_k)


    retans =  aStarGoal(currMap, currPos, goalPos, currCoins, currCarPositionsall, penalty_k)
    return retans
