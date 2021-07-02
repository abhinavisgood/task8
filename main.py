import get_num_plate as sa
asd = {'code':'invalid'}
def final(x): 
    global asd
    numpl = sa.get_num(x)[8][:-2]
    try : 

        asd=sa.gvi(numpl)
    except :
        asd = asd 
    return asd
    
