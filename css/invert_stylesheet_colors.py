with open("pygments.css", 'r') as f:
    data = f.read().split('\n')
    pass

for i in range(len(data)):
    try:
        iof = data[i].index('#')
    except:
        continue

    color = data[i][iof+1:iof+7]
    c = int(color, 16)
    c = 0xffffff - c
    c = hex(c)[2:]
    while len(c) < 6:
        c = "0" + c
        pass
    data[i] = data[i].replace(color, c)
    pass

print data

with open("pygments.css2", 'w') as f:
    f.write("\n".join(data))
    pass
