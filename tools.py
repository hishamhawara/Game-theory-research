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

    profits1 = [0]*(T)
    profits2 = [0]*(T)

    profits1[0] = vf1[0]
    for k in range(1,T):
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
    return pivot_price


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
    plt.plot(bid_1,'-o')
    plt.plot(bid_2,'-o')
    plt.figure()
    plt.plot(range(1,len(v1)),v1[1:],'-d')
    plt.plot(range(1,len(v2)),v2[1:],'-d')
    plt.show()
    
def func(mat):
    n = len(mat)
    list = [(mat[i][j],i,j) for i in range(n) for j in range(n)]
    list.sort()
    nb_in = [n]*n
    nb_out = [n]*n

    nb_bids = 0
    bid = [0]*n
    winner = -1
    price = -1
    
    for edge in list:
        val,i,j = edge
        if(nb_in[i] == 0):
            continue
        
        nb_out[i] -= 1
        nb_in[j] -= 1
            
        updated_vertices = [(nb_in[j],j)]
        
        mini = min(updated_vertices)
        while(mini[0] == 0):
            updated_vertices.remove(mini)
            k = mini[1]
            bid[k] = val
            nb_bids += 1
            if(nb_bids == n-1):
                price = bid[k]
            if(nb_bids == n):
                bid[k] += 1
                winner = k
            for j in range(n):
                if((mat[k][j],k,j) > edge):
                    nb_in[j] -= 1
                    updated_vertices.append((nb_in[j],j))
            if(updated_vertices):
                mini = min(updated_vertices)
            else:
                mini = ['balbalba']
    return bid,winner,price

def funcbis(mat):
    n = len(mat)
    list = [(mat[i][j],i,j) for i in range(n) for j in range(n)]
    list.sort()
    nb_in = [n]*n
    nb_out = [n]*n

    nb_bids = 0
    bid = [0]*n
    winner = -1
    price = -1
    
    for edge in list:
        val,i,j = edge
        if(nb_in[i] == 0):
            continue
        
        nb_out[i] -= 1
        nb_in[j] -= 1
            
        updated_vertices = [(nb_in[j],val,j)]
        
        mini = min(updated_vertices)
        while(mini[0] == 0):
            updated_vertices.remove(mini)
            k = mini[2]
            bid[k] = val
            nb_bids += 1
            if(nb_bids == n-1):
                price = bid[k]
            if(nb_bids == n):
                bid[k] += 1
                winner = k
            for j in range(n):
                if((mat[k][j],k,j) > edge):
                    nb_in[j] -= 1
                    updated_vertices.append((nb_in[j],mat[k][j],j))
            if(updated_vertices):
                mini = min(updated_vertices)
            else:
                mini = ['balbalba']
    return bid,winner,price
    
    
def func2(mat):
    n = len(mat)
    player_alive = list(range(n))
    end = False
    bid = [0]*n
        
    while(not end):
        max_mat = [(0,-1)]*n
        min_mat = [0]*n
        for p_i in player_alive:
            for p_j in player_alive:
                if(max_mat[p_i][0] < mat[p_i][p_j] or max_mat[p_i][1] == -1):
                    max_mat[p_i] = (mat[p_i][p_j],p_j)
                    
        print(player_alive)
        print(max_mat)
        bid_p1, p2 = max(max_mat[p_i] for p_i in player_alive)
        p1 = max_mat.index((bid_p1,p2))
        bid_p2 = max_mat[p2][0]
        print(p1,bid_p1,p2,bid_p2)
        for p_i in player_alive:
            if(p_i not in [p1,p2]):
                min_mat[p_i] = min(mat[p_i][p_j] for p_j in player_alive if p_j != p_i)
        print(min_mat)
        if(bid_p2 < 0):
            raise Exception(str(mat)+str(bid_p2))
        if max(min_mat[p_i] for p_i in player_alive) <= bid_p2:
            for p_i in player_alive:
                if(p_i not in [p1,p2]):
                    bid[p_i] = min_mat[p_i]
            bid[p1] = bid_p1
            bid[p2] = bid_p2
            end = True
        else:
            bid[p2] = bid_p2
            player_alive.remove(p2)
        print(bid)
    return bid,p1,max(bid[i] for i in range(n) if i != p1)