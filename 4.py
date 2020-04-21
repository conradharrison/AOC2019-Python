s = 367479
e = 893698

count = 0

for x in range(s, e+1):
    d0 = x % 10
    d1 = (int(x/10)) % 10
    d2 = (int(x/100)) % 10
    d3 = (int(x/1000)) % 10
    d4 = (int(x/10000)) % 10
    d5 = (int(x/100000)) % 10

    # monotonic
    c1 = (d0-d1)>=0 and (d1-d2)>=0 and (d2-d3)>=0 and (d3-d4)>=0 and (d4-d5)>=0

    # only doubles, atleast one double
    c2 = False
    run = 1
    prev_i = -1
    for i in [d5,d4,d3,d2,d1,d0]:
        if i==prev_i:
            run=run+1
        else:
            if run > 2:
                c2 = c2 or False
            elif run == 2:
                c2 = True
            run = 1
        prev_i = i
    if run == 2:
        c2 = True

    if c1 and c2:
        count = count + 1

print(count)
