from tools import *


#(4312628943026710128, 4, 20)
#(8015813439583669720, 3, 30)
#(2885641106912702946, 4, 22)
def run(time,n,T):
	
	for z in range(time):
		seed = setseed(4312628943026710128)
		#(5,25), (6,18), (4,40) bound for n,T to have decent timing in 1 round.
		
		
		v = [vtype("uniform",T,low_b=0,up_b=T*T) for i in range(n)]
		T2 = T
		#Modification of 1st example
		it = (1,2,0,5)
		T2 = T - sum(it)
		for i in range(len(v)):
			v[i] = [0] + v[i][it[i]+1:it[i]+T2+1]
		
		v.pop()
		n = 3
		#marginal valuation for bidder 1
		#v[0] = vtype("custom",T,vals=[T+1]*T)
		#marginal valuation for bidder 2
		#for i in range(1,n):
		#	v[i] = vtype("custom",T,vals=[T]*(T//(n-1))+[0]*(T-T//(n-1)))
		
		
		#Check that v1/v2 are non-increasing ?
		
		vf = [cumulative(v[i]) for i in range(n)]
		
		# for i in range(n):
			# print(v[i],vf[i])
		
		bid,price = game(vf,n,T2)
		if(sorted(price,reverse=True) != price or True):
			plt.figure()
			for i in range(n):
				plt.plot([bid[j][i] for j in range(T2)],'-o')
			plt.show()
			plt.figure()
			for i in range(n):
				plt.plot(range(1,T2+1),v[i][1:],'-d')
			plt.show()
			
			return vf

def init(T,player,l_vf):
	if(player == len(l_vf) - 1):
		return [(T,)]
	if(T == 0):
		return [(0,)*(len(l_vf)-player)]
	
	rec = [init(T-i,player+1,l_vf) for i in range(T+1)]


	tab = []
	for i in range(T+1):
		for j in rec[i]:
			tab += [(i,)+j]
	
	return tab 
	
def next_it(it,i):
	return tuple(it[j]+(i==j) for j in range(len(it)))
	
def sgpe2(l_vf):
	T = len(l_vf[0]) - 1
	nb_p = len(l_vf)
	value = [0]*(T+1)
	winner = [0]*(T+1)
	price_t = [0]*(T+1)
	bids_t = [0]*(T+1)
	for i in range(T+1):
		value[i] = {j:0 for j in init(i,0,l_vf)} #Creation of nodes
		winner[i] = {j:0 for j in init(i,0,l_vf)} #Creation of nodes	
		price_t[i] = {j:0 for j in init(i,0,l_vf)}
		bids_t[i] = {j:0 for j in init(i,0,l_vf)}
	winner.pop()
	price_t.pop()
	bids_t.pop()
	
	# print("init done")
	for items in value[T]: #Initialisation of leaves
		value[T][items] = tuple(l_vf[p][items[p]] for p in range(nb_p))
		
	for i in range(T-1,-1,-1): #Number of items sold
		# print(i+1,"items done")
		for items in value[i]:
			mat = [[0]*nb_p for j in range(nb_p)] #Matrice of marginal gain if p1 wins over p2
			for p1 in range(nb_p):
				it_p1_win  = next_it(items,p1)
				
				for p2 in range(nb_p):
					it_p2_win = next_it(items,p2)
					mat[p2][p1] = value[i+1][it_p1_win][p1] - value[i+1][it_p2_win][p1] #p1;p2 if func2, p2;p1 if func
			
			bids_t[i][items],winner,price = func(mat)
			next_iter = next_it(items,winner)
			value[i][items] = tuple(value[i+1][next_iter][p] - (p == winner)*price for p in range(len(value[i+1][next_iter])))
	# print("values done")
	return value,bids_t

def game(l_vf,n,T):
	value,bids_t = sgpe2(l_vf)
	utility = [0]*n
	
	price = [0]*T #Price of different items
	
	nb = (0,)*n
	
	bid = [[0]*n for i in range(T)]
	win = []
	
	for i in range(T):
		# print("Round",i+1)
		win.append(bids_t[i][nb].index(max(bids_t[i][nb])))
		
		bid[i] = bids_t[i][nb]
		# print(bids_t[i][nb])
		price[i] = max([bids_t[i][nb][j] for j in range(n) if j != win[-1]])
			
		# print("Bids:",*bid[i],'->',price[i])
		
		# print("Winner is",win[-1])
		utility[win[-1]] += l_vf[win[-1]][nb[win[-1]]+1] - l_vf[win[-1]][nb[win[-1]]] - price[i]
		
		nb = next_it(nb,win[-1])
			
		# print("\nP:",nb,"items, util",utility)
		# print("\n##############\n")
		
	
	# print("Price:",price)
	# print("Winner:",win)
	
	return bid,price