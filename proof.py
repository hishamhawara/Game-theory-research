from tools import *

#(4312628943026710128, 4, 20)

def run():
	v = [[0, 44, 44, 44, 44, 0, 0, 0, 0], [0, 32, 20, 0, 0, 0, 0, 0, 0], [0, 55, 55, 55, 55, 30, 20, 0, 0]]

	n = len(v)
	nb_p = n
	T2 = len(v[0]) - 1
	#marginal valuation for bidder 1
	#v[0] = vtype("custom",T,vals=[T+1]*T)
	#marginal valuation for bidder 2
	#for i in range(1,n):
	#	v[i] = vtype("custom",T,vals=[T]*(T//(n-1))+[0]*(T-T//(n-1)))
	
	
	#Check that v1/v2 are non-increasing ?
	
	vf = [cumulative(v[i]) for i in range(n)]
	
	# for i in range(n):
		# print(v[i],vf[i])
	
	value,bids_t = sgpe2(vf,[4,2,6])
	
	check = [0]*(T2+1)
	for i in range(T2+1):
		check[i] = {j:False for j in value[i]}

	for i in range(T2):
		for items in value[i]:
			if(check[i][items]):
				print("Checked",items)
			else:
				winner,bid,price = game(value,bids_t,n,T2, items, vf)
				
				fig = plt.figure()
				plt.title(str(items))
				for k in range(n):
					plt.plot([bid[j][k] for j in range(i,T2)],'-o')
				plt.show()
				
				mat = [[0]*nb_p for j in range(nb_p)] #Matrice of marginal gain if p1 wins over p2
				s = ""
				for p1 in range(nb_p):
					it_p1_win  = next_it(items,p1)
					print(p1,':',value[i+1].get(it_p1_win,[0]*nb_p))
					for p2 in range(nb_p):
						it_p2_win = next_it(items,p2)
						mat[p2][p1] = value[i+1].get(it_p1_win,[0]*nb_p)[p1] - value[i+1].get(it_p2_win,[0]*nb_p)[p1] #p1;p2 if func2, p2;p1 if func
				
				for l in mat:
					print(l)
				print(value[i][items])
				x = input("All(a)/One(o)/Err(e): ")
				if(x != "e"):
					check[i][items] = True
				else:
					raise Exception("Problem")
				if(x == "a"):
					it = items
					for j in range(len(winner)):
						it = next_it(it,winner[j])
						check[i+j+1][it] = True
				
				plt.close(fig)		
			
def init(T,player,l_vf, end):
	if(player == len(l_vf) - 1):
		return [(T,)]
	if(T == 0):
		return [(0,)*(len(l_vf)-player)]
	
	rec = [init(T-i,player+1,l_vf, end) for i in range(min(T,end[player])+1)]


	tab = []
	for i in range(min(T,end[player])+1):
		for j in rec[i]:
			tab += [(i,)+j]
	
	return tab 
	
def next_it(it,i):
	return tuple(it[j]+(i==j) for j in range(len(it)))
	
def sgpe2(l_vf, end):
	T = len(l_vf[0]) - 1
	nb_p = len(l_vf)
	value = [0]*(T+1)
	winner = [0]*(T+1)
	price_t = [0]*(T+1)
	bids_t = [0]*(T+1)
	for i in range(T+1):
		x = init(i,0,l_vf, end)
		value[i] = {j:0 for j in x} #Creation of nodes
		winner[i] = {j:0 for j in x} #Creation of nodes	
		price_t[i] = {j:0 for j in x}
		bids_t[i] = {j:0 for j in x}
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
					mat[p2][p1] = value[i+1].get(it_p1_win,[0]*nb_p)[p1] - value[i+1].get(it_p2_win,[0]*nb_p)[p1] #p1;p2 if func2, p2;p1 if func
			
			bids_t[i][items],winner,price = func(mat)
			next_iter = next_it(items,winner)
			value[i][items] = tuple(value[i+1][next_iter][p] - (p == winner)*price for p in range(len(value[i+1][next_iter])))
	# print("values done")
	return value,bids_t

def game(value,bids_t,n,T,nb, l_vf):
	utility = [0]*n
	
	price = [0]*T #Price of different items
	
	
	bid = [[0]*n for i in range(T)]
	win = []
	
	for i in range(sum(nb),T):
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
		
	
	print("Price:",price)
	print("Winner:",win)
	
	return win,bid,price