def combinator(list: list):
    dlist = []
    for i in range(len(list)):
        i2 = i
        while i2 < len(list):
            if i != i2:
                 dlist.append([list[i], list[i2]])
            i2 += 1
    return dlist
