import os

dan = os.environ.get("DAN")

if dan is not None :
    for i in range(1, 10) :
        print(f"{dan} x {i} = {int(dan)*int(i)}")
else :
    for i in range(1, 10) :
        print(f"{i}단")
        for j in range(1, 10) :
            print(f"{i} x {j} = {int(i)*int(j)}")
        print()