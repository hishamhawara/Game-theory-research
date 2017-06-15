import sys
import matplotlib.pyplot as plt
import random

#set the seed given or generate a new seed
def setseed(s=None): 
    if(s == None):
        s = random.randint(0,sys.maxsize)
    random.seed(s)
    print("Seed:",s)
    return s

def vtype(type,round,**args):
    v = [0]

    if(type == "uniform"): #Uniform values
        low_b,up_b = args.get("low_b",0),args.get("up_b",2*round)
        
        
        v += sorted([random.randint(low_b,up_b) for i in range(round)], reverse = True)
    
    elif(type == "cst-unif"): #Constant values for cst_t then uniform
        low_b,up_b,cst_t = args.get("low_b",0), args.get("up_b",2*round), args.get("cst_t",round//2)
        
        v += [up_b]*cst_t
        v += sorted([random.randint(low_b,up_b) for i in range(round - cst_t)], reverse = True)
    
    elif(type == "pow"): #pow > 1, more small value, pow < 1, more high value (shape as x^pow)
        low_b,up_b,pow = args.get("low_b",0), args.get("up_b",2*round), args["pow"]
        
        v += sorted([ int(random.random()**(pow)*(up_b-low_b) + low_b) for i in range(round)], reverse = True)
        
    elif(type == "custom"):
        vals = args["vals"]
        v += sorted(vals, reverse = True)
        
    return v

def cumulative(v):
    return [sum(v[0:i+1]) for i in range(len(v))]


def pivot(v1,v2,T):
    v1 = v1.copy()
    v2 = v2.copy()
    v1[0] = 0
    v2[0] = 0
    vf1 = cumulative(v1) #valuation function for bidder 1
    vf2 = cumulative(v2) #                   for bidder 2

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


def sgpe(vf1,vf2):
    T = len(vf1) - 1
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
    return value_1,value_2
    
    
def strat(type,bidder,**args):
    if(type == "sgpe"):
        value_1,value_2,nb_1,nb_2 = args["value_1"], args["value_2"],args["nb_1"],args["nb_2"]
        
        if(bidder == 1):
            bid = value_1[nb_1+1][nb_2] - value_1[nb_1][nb_2+1]
        else:
            bid = value_2[nb_1][nb_2+1] - value_2[nb_1+1][nb_2]
    
    if(type == "greedy"):
        v1,v2,nb_1,nb_2, rnd_left = args["v1"], args["v2"],args["nb_1"],args["nb_2"],args["rnd_left"]
        
        if(bidder == 1):
            bid = pivot(v1[nb_1:],v2[nb_2:],rnd_left)
        else:
            bid = pivot(v2[nb_2:],v1[nb_1:],rnd_left)
            
    return bid
        
def graph(bid_1,bid_2,v1,v2):
    plt.figure()
    plt.plot(bid_1)
    plt.plot(bid_2)
    plt.figure()
    plt.plot(v1[1:])
    plt.plot(v2[1:])
    plt.show()