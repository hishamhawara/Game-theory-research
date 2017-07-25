import sys
import random

from toolsedit import *
seed = setseed()


def run(T,diff_v,strategies):
    v = [vtype("uniform",T) for i in range(diff_v)]
    
    print(v)
    rprice_cst = sorted([random.randint(1,3*T//2) for i in range(T)]) #increasing reserve price
    
    rprice = rprice_cst
    #Check that v1/v2 are non-increasing ?
    
    
    for r in range(4):
        if(r%2):
            rprice = rprice_cst.copy()
            if(r == 1):
                rprice = rprice[::-1]
        else:
            rprice = [sum(rprice)/len(rprice)*r/2]*T
        
        result = {s1:{s2:0 for s2 in strategies} for s1 in strategies}
        
        for s1 in strategies:
            print(s1)
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
                            bid_1[i] = strat(s1, 1, v=v1, nb=nb_1, other_nb = nb_2, k = i, bid = bid_1, other_bid = bid_2, rprice = rprice, T = T)
                            bid_2[i] = strat(s2, 2, v=v2, nb=nb_2, other_nb = nb_1, k = i, bid = bid_2, other_bid = bid_1, rprice = rprice, T = T)
                        
                            price[i] = max(min(bid_1[i], bid_2[i]),rprice[i])
                            
                            
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
                            
                            
                            if(winner == 0): #In case of a tie
                                winner = random.randint(1,2)
                            
                            if(max(bid_1[i],bid_2[i]) < price[i]):
                                winner = 0
                            win.append(winner)
                            
                            #print("Winner is",winner)
                            
                            if(winner == 1):
                                nb_1 += 1
                                utility_1 += v1[nb_1] - price[i]
                            elif(winner == 2):
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
                        
        yield result,r,rprice


T_list = [5*i for i in range(1,4)] #Number of round
diff_v = 40 #Number of different valuation

strategies = ['learn_a','learn_b','learnR_a','learnR_b','trial', 'reverse']

plot = [[0]*len(T_list) for i in range(4)]

for i in range(len(T_list)):
    for res,r,rprice in run(T_list[i],diff_v,strategies):
        plot[r][i] = [sum(res[k].values()) for k in res]
        
        
        if(len(T_list) < 3):
            print(rprice)
            print_map(res)

if(len(T_list) > 1):
    for r in range(4):
        plt.figure()
        for i in range(len(strategies)):
            plt.plot(T_list,[plot[r][j][i]/((T_list[j]*diff_v)**2) for j in range(len(T_list))], label = strategies[i])
        plt.legend()
        plt.show()