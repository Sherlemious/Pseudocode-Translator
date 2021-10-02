M = eval(input())
Count = 0
X = eval(input())
while True:
    Cf = 0
    print( "2nd Repeat")
    while True:
        print( "Iter")
        Cf = Cf + 1
        if Cf == 2:
            break
    Count = Count + 1
    print( Count)
    if Count == X:
        break
print( "Done")
