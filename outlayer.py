

strats = gen_samples(n,T,bounds)

j = 0
while(condition):
    j += 1
    
    for i in range(rate_log):
        print((i+1)*j)
        
        fit = tournament(strats, tries)
        
        ordered_strats = order(strats,fit)
        new_strats = mutate(gen_new(ordered_strats))
        
        strats = fusion(ordered_strats, new_strats)
    
    write_log(j,strats,ordered_strats,fit)
        
        
        