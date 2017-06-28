import sys
import random

from tools import *

seed = setseed()

T = 10 #Number of round

#marginal valuation for bidder 1
v1 = vtype("uniform",T,low_b=T,up_b=2*T)
#marginal valuation for bidder 2
v2 = vtype("uniform",T,low_b=T,up_b=2*T)
for i in range(10,len(v2)):
    v2[i] -= T*3//4

"""#marginal valuation for bidder 1
v1 = vtype("custom",T,vals=[T+1]*T)
#marginal valuation for bidder 2
v2 = vtype("custom",T,vals=[T]*(T-1)+[0])
"""


#Check that v1/v2 are non-increasing ?

vf1 = cumulative(v1) #valuation function for bidder 1
vf2 = cumulative(v2) #                   for bidder 2


print(v1,vf1)
print(v2,vf2)
#End of inputs (is vf really an input ?)


value_1,value_2 = sgpe(vf1,vf2)


#Resolution

utility_1 = 0 #Player 1 utility
utility_2 = 0 #Player 2 utility

price = [0]*T #Price of different items

nb_1 = 0 #Number of items got by player 1
nb_2 = 0 #Number of items got by player 2

bid_1 = [0]*T
bid_2 = [0]*T
monopoly = 0
win = []


for i in range(T):
    winner = 0 #winner for round i

    bid_1[i] = strat("sgpe", 1, value_1=value_1, value_2=value_2, nb_1=nb_1, nb_2=nb_2)
    #bid_1[i] = strat("greedy", 1, v1=v1, v2=v2, nb_1=nb_1, nb_2=nb_2, rnd_left=T-i)
    bid_2[i] = strat("sgpe", 2, value_1=value_1, value_2=value_2, nb_1=nb_1, nb_2=nb_2)
    #bid_2[i] = strat("greedy", 2, v1=v1, v2=v2, nb_1=nb_1, nb_2=nb_2, rnd_left=T-i)
    
    price[i] = min(bid_1[i],bid_2[i])
    
    if(v1[nb_1 + (T - i)] > v2[nb_2 + 1]):#If marginal value are decreasing, check if it is a monopoly
        if(not monopoly):
            monopoly = i
        print("Round",i+1,"monopoly for player 1")
        
    elif (v2[nb_2 + (T - i)] > v1[nb_1 + 1]): 
        if(not monopoly):
            monopoly = i
        print("Round",i+1,"monopoly for player 2")
    else:
        print("Round",i+1)
    print("Bids:",bid_1[i],bid_2[i],'->',price[i])
    
    winner = 1*(bid_1[i] > bid_2[i]) + 2*(bid_1[i] < bid_2[i])
    win.append(winner)
    
    if(winner == 0): #In case of a tie
        winner = random.randint(1,2)
        win[-1] = str(winner)
    
    print("Winner is",winner)
    
    if(winner == 1):
        nb_1 += 1
        utility_1 += v1[nb_1] - price[i]
    else:
        nb_2 += 1
        utility_2 += v2[nb_2] - price[i]
        
    print("\nP1:",nb_1,"items, util",utility_1)
    print("P2:",nb_2,"items, util",utility_2)
    print("\n##############\n")
    
print("Price:",price)
print("All winners:",win)
print("Monopoly from",monopoly,"with results:",win[monopoly:])

pivot(v1,v2,T)


graph(bid_1,bid_2,v1,v2)