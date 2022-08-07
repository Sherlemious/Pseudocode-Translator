arr=[0 for i in range(1000)]
m=[[0 for i in range(1000)] for f in range(1000)]
M = eval(input())
Count = 0
print("The Count is:", Count)
X = eval(input())
while True:
    Cf = 0
    print("2nd Repeat")
    while True:
        print("Iter")
        Cf = Cf + 1
        if Cf == 2:
            break
    Count = Count + 1
    print(Count)
    if Count == X:
        break
print("Done")
Num1 = 47293
Num2 = 3290
Result = Num1 + Num2
print("The result is:", Result)
i = 10
while i > 0:
    print("Iteration" , i)
    i = i - 1
arr[4] = 5
print(arr[4])
for i in range(0,5):
    arr[i] = i
    print(arr[i])
m[0][1] = 5
print(m[0][1])
input("Press enter to exit ")
