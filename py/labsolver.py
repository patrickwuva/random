def solve_lab(c, a):
    


    a_split = {"t":0,"i":0,"o":0}
    o_bin = 2**c["o"]-1
    i_bin = 2**c["i"]-1

    a_split["o"] = hex(a&o_bin)
    a_split["i"] = hex(a>>c["o"] & i_bin)
    a_split["t"] = hex(a>>(c['o']+c['i']))

    return(a_split)

cache = {"w": 3, "s": 16, "bpb": 8, "o": 3, "i": 4, "td": 384}
cache2 = {"w": 3, "s": 32, "bpb": 4, "o": 2, "i": 5, "td": 384}

print(solve_lab(cache,0xeea))

