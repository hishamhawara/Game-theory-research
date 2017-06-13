import random
import math
import matplotlib.pyplot as plt

T = 4 #Number of round
k = 1
v1 = [0] + sorted([random.randint(0,2*T) for i in range(T)], reverse = True) #marginal valuation for bidder 1
v2 = [0] + [T]*(T//2) + sorted([random.randint(0,T-1) for i in range(T//2)], reverse = True) #marginal valuation for bidder 2


#Check that v1/v2 are non-increasing ?

vf1 = [0]*(T+1) #valuation function for bidder 1
vf2 = [0]*(T+1) #                   for bidder 2

for i in range(T + 1):
    vf1[i] = vf1[i-1] + v1[i] #As vf1[-1] = 0, it's ok
    vf2[i] = vf2[i-1] + v2[i] 

def pivot(v1,v2,T):
    v1 = v1.copy()
    v2 = v2.copy()
    v1[0] = 0
    v2[0] = 0
    vf1 = [0]*(T+1) #valuation function for bidder 1
    vf2 = [0]*(T+1) #                   for bidder 2

    for i in range(T + 1):
        vf1[i] = vf1[i-1] + v1[i] #As vf1[-1] = 0, it's ok
        vf2[i] = vf2[i-1] + v2[i] 

    profit1 = 0 
    profitfo  = 0 
    pivot_price = 0

    profits1 = [0]*(T+1) #marginal valuation for bidder 1
    profits2 = [0]*(T) #marginal valuation for bidder 1

    profits1[0] = vf1[0]
    for k in range(1,T+1):
        profits1[k] = vf1[k] - (k * v2[T+1-k])
    profit1 = max(profits1)
    kstar = profits1.index(profit1)
    print(kstar)
    print("*********1111*****")
    print(profit1)
    print(profits1)
    print("*********1111****")

    profits2[0] = vf1[0]
    for k in range(1, T):
        profits2[k] = (vf1[k+1]-vf1[1]) - k * v2[T-k]
    profitfo = max(profits2)
    print("*********222222*********")
    print(profitfo)
    print(profits2)
    print("*********222222*********")
    #the pivot price calculation
    pivot_price = v1[1] + profitfo - profit1
    print("*********pivot price*****")
    print(pivot_price)
    print("*********pivot price****")

print(v1,vf1)
print(v2,vf2)
#End of inputs (is vf really an input ?)


value_1 = [[0 for j in range(T - i + 1)] for i in range(T+1)] #initialization of vectors
value_2 = [[0 for j in range(T - i + 1)] for i in range(T+1)]

for k1 in range(T + 1): #Initializing the value by the leaves
    k2 = T - k1
    value_1[k1][k2] = vf1[k1]
    value_2[k1][k2] = vf2[k2]
    # print(k1,k2,value_1[k1][k2],value_2[k1][k2])
# print("End of depth",T)
    
for i in range(T-1,-1,-1): #Applying recursion of internal nodes
    for k1 in range(i + 1):
        k2 = i - k1
        
        value_1[k1][k2] = max(value_1[k1][k2+1], value_1[k1+1][k2] - (value_2[k1][k2+1] - value_2[k1+1][k2]))
        value_2[k1][k2] = max(value_2[k1+1][k2], value_2[k1][k2+1] - (value_1[k1+1][k2] - value_1[k1][k2+1]))

        # print(k1,k2,value_1[k1][k2],value_2[k1][k2])
    # print("End of depth",i)
    

#Resolution

utility_1 = 0 #Player 1 utility
utility_2 = 0 #Player 2 utility

price = [0]*T #Price of different items

nb_1 = 0 #Number of items got by player 1
nb_2 = 0 #Number of items got by player 2

winner = 0 #winner for round i
monopoly = 0
win = []

for i in range(1,T+1):
    bid_1 = value_1[nb_1+1][nb_2] - value_1[nb_1][nb_2+1]
    bid_2 = value_2[nb_1][nb_2+1] - value_2[nb_1+1][nb_2]
    
    price[i-1] = min(bid_1,bid_2)
    
    if(v1[nb_1 + 1 + (T - i)] > v2[nb_2 + 1]):#If marginal value are decreasing, check if it is a monopoly
        if(not monopoly):
            monopoly = i
        print("Round",i,"monopoly for player 1")
        
    elif (v2[nb_2 + 1 + (T - i)] > v1[nb_1 + 1]): 
        if(not monopoly):
            monopoly = i
        print("Round",i,"monopoly for player 2")
    else:
        print("Round",i)
    print("Bids:",bid_1,bid_2,'->',price[i-1])
    pivot(v1[nb_1:],v2[nb_2:],T-i+1)
    winner = 1*(bid_1 > bid_2) + 2*(bid_1 < bid_2)
    win.append(winner)
    
    if(winner == 0): #In case of a tie
        winner = random.randint(1,2)
        win[-1] = str(winner)
    
    print("Winner is",winner)
    
    if(winner == 1):
        nb_1 += 1
        utility_1 += v1[nb_1] - price[i-1]
    else:
        nb_2 += 1
        utility_2 += v2[nb_2] - price[i-1]
        
    winner = 0
    print("\nP1:",nb_1,"items, util",utility_1)
    print("P2:",nb_2,"items, util",utility_2)
    print("\n##############\n")
    
print(price)
print(win)
print(monopoly,win[monopoly-1:])


plt.plot(price)
plt.show()