import random
import math
number_of_rounds = input('how many rounds do you want to play? ')
T = int(number_of_rounds) #Number of round

v1 = [0] + sorted([random.randint(0,2*T) for i in range(T)], reverse = True)
 #marginal valuation for bidder 1

v2 = [0] + [2*T] + sorted([random.randint(0,T-1) for i in range(T-1)], reverse = True)
 #marginal valuation for bidder 2
answer_question1 = input('player1 do you want to set your marginal values? (Y/N)')
if answer_question1 == "Y" :
    for i in range(T):
        input_1 = input("value:")
        v1[i] = int(input_1)
answer_question2 = input('player2 do you want to set your marginal values? (Y/N)')
if answer_question2 == "Y" :
    for i in range(T):
        input_2 = input("value:")
        v2[i] = int(input_2)

#Check that v1/v2 are non-increasing ?

vf1 = [0]*(T+1) #valuation function for bidder 1
vf2 = [0]*(T+1) #                   for bidder 2

for i in range(T + 1):
    vf1[i] = vf1[i-1] + v1[i] #As vf1[-1] = 0, it's ok
    vf2[i] = vf2[i-1] + v2[i] 


print(v1,vf1)
print(v2,vf2)
#End of inputs (is vf really an input ?)


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
    bid_1 = input('player 1 input your bid: ')
    bid_2 = input('player 2 input your bid: ')
    bid_1 = int(bid_1)
    bid_2 = int(bid_2)
    
    price[i-1] = min(bid_1,bid_2)
    
    print("Round",i)
    print("Bids:",bid_1,bid_2,'->',price[i-1])
    
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
        print(v2[nb_2])
        print(price[i-1])
        nb_2 += 1
        utility_2 += v2[nb_2] - price[i-1]
        
    winner = 0
    print("\nP1:",nb_1,"items, util",utility_1)
    print("P2:",nb_2,"items, util",utility_2)
    print("\n##############\n")
    
print(price)
print(win)

import matplotlib.pyplot as plt

plt.plot(price)
plt.show()