import sys
import random

from toolsedit import *
seed = setseed()


T = 10 #Number of round
diff_v = 10 #Number of different valuation

strategies = ['learn_a','learn_b','learnR_a','learnR_b','trial']

v = [vtype("uniform",T) for i in range(diff_v)]

rprice = vtype("uniform",T,low_b=3,up_b=T/2)

#Check that v1/v2 are non-increasing ?

result = {s1:{s2:0 for s2 in strategies} for s1 in strategies}

for s1 in strategies:
    for s2 in strategies:
        for v1 in v:
            for v2 in v:
                
                #print(v1)
                #print(v2)
                #print(rprice)

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
                    bid_1[i] = strat(s1, 1, v=v1, nb=nb_1, other_nb = nb_2, k = i, bid = bid_1, other_bid = bid_2, rprice = rprice)
                    bid_2[i] = strat(s2, 2, v=v2, nb=nb_2, other_nb = nb_1, k = i, bid = bid_2, other_bid = bid_1, rprice = rprice)
                
                
                    price[i] = min(bid_1[i], bid_2[i])
                    
                    """if(v1[nb_1 + (T - i)] > v2[nb_2 + 1]):#If marginal value are decreasing, check if it is a monopoly
                        if(not monopoly):
                            monopoly = i
                        print("Round",i+1,"monopoly for player 1")
                        
                    elif (v2[nb_2 + (T - i)] > v1[nb_1 + 1]): 
                        if(not monopoly):
                            monopoly = i
                        print("Round",i+1,"monopoly for player 2")
                    else:
                        print("Round",i+1)"""
                    
                    #print("Bids:",bid_1[i],bid_2[i],'->',price[i])
                    
                    winner = 1*(bid_1[i] > bid_2[i]) + 2*(bid_1[i] < bid_2[i])
                    win.append(winner)
                    
                    if(winner == 0): #In case of a tie
                        winner = random.randint(1,2)
                        win[-1] = str(winner)
                    
                    #print("Winner is",winner)
                    
                    if(winner == 1):
                        nb_1 += 1
                        utility_1 += v1[nb_1] - price[i]
                    else:
                        nb_2 += 1
                        utility_2 += v2[nb_2] - price[i]
                        
                    #print("\nP1:",nb_1,"items, util",utility_1)
                    #print("P2:",nb_2,"items, util",utility_2)
                    #print("\n##############\n")
                    
                #print("Price:",price)
                #print("All winners:",win)
                #print("Monopoly from",monopoly,"with results:",win[monopoly:])
                
                result[s1][s2] += utility_1
                result[s2][s1] += utility_2
                

print_map(result)


graph(bid_1,bid_2,v1,v2)
graph(bid_3,bid_4,v1,v2)