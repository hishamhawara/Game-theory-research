from tools import *

seed = setseed()
#(5,25), (6,18), (4,40)
n = 4
T = 10*(n-1)+1 #Number of round
v = [vtype("uniform",T,low_b=0,up_b=T*T) for i in range(n)]

#marginal valuation for bidder 1
v[0] = vtype("custom",T,vals=[T+1]*T)
#marginal valuation for bidder 2
for i in range(1,n):
	v[i] = vtype("custom",T,vals=[T]*(T//(n-1))+[0]*(T-T//(n-1)))


#Check that v1/v2 are non-increasing ?

vf = [cumulative(v[i]) for i in range(n)]

for i in range(n):
	print(v[i],vf[i])

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
	for i in range(T+1):
		value[i] = {j:0 for j in init(i,0,l_vf)} #Creation of nodes
		winner[i] = {j:0 for j in init(i,0,l_vf)} #Creation of nodes	
	
	winner.pop()
	
	print("init done")
	for items in value[T]: #Initialisation of leaves
		value[T][items] = tuple(l_vf[p][items[p]] for p in range(nb_p))
		
	for i in range(T-1,-1,-1): #Number of items sold
		print(i,"items done")
		for items in value[i]:
			mat = [[0]*nb_p for j in range(nb_p)] #Matrice of marginal gain if p1 wins over p2
			for p1 in range(nb_p):
				it_p1_win  = next_it(items,p1)
				
				for p2 in range(nb_p):
					it_p2_win = next_it(items,p2)
					mat[p1][p2] = value[i+1][it_p1_win][p1] - value[i+1][it_p2_win][p1]
			
			#Assumption on tie: First play
			init_bid = [min([mat[i][j] for j in range(len(mat[i])) if j != i]) for i in range(len(mat))]
			sort_init_bid = sorted(init_bid,reverse = True)
			price = [max(0,sort_init_bid[1]), sort_init_bid[0]]
			if(price[-1] < 0):
				print(mat)
				Exception("We found it!")
				
			max_index = init_bid.index(price[-1])
			while(price[-1] < max([mat[i][max_index] for i in range(len(mat)) if i != max_index])):
				price.append(max([mat[i][max_index] for i in range(len(mat)) if i != max_index]))
				max_index = [mat[i][max_index] for i in range(len(mat))].index(price[-1])
			
			next_iter = next_it(items,max_index)
			winner[i][items] = max_index
			value[i][items] = tuple(value[i+1][next_iter][p] - (p == max_index)*price[-2] for p in range(len(value[i+1][next_iter])))

	print("values done")
	return value,winner

def game(l_vf,n,T):
	value,winner = sgpe2(l_vf)
	utility = [0]*n
	
	price = [0]*T #Price of different items
	
	nb = (0,)*n
	
	bid = [[0]*n for i in range(T)]
	win = []
	
	for i in range(T):
		print("Round",i+1)
		win.append(winner[i][nb])
		
		bid[i] = [value[i+1][next_it(nb,j)][j] - value[i+1][next_it(nb,win[-1])][j] for j in range(n)]
		price[i] = max(bid[i])
		
		bid[i][win[-1]] = value[i+1][next_it(nb,win[-1])][win[-1]] - value[i+1][next_it(nb,bid[i].index(max(bid[i])))][win[-1]]
			
		print("Bids:",*bid[i],'->',price[i])
		
		print("Winner is",win[-1])
		utility[win[-1]] += l_vf[win[-1]][nb[win[-1]]+1] - l_vf[win[-1]][nb[win[-1]]] - price[i]
		
		nb = next_it(nb,win[-1])
			
		print("\nP:",nb,"items, util",utility)
		print("\n##############\n")
		
	
	print("Price:",price)
	print("Winner:",win)
	
	return bid
	
bid = game(vf,n,T)

plt.figure()
for i in range(n):
	plt.plot([bid[j][i] for j in range(T)],'-o')
plt.show()
plt.figure()
for i in range(n):
	plt.plot(range(1,T+1),v[i][1:],'-d')
plt.show()