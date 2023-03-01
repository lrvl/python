#!/usr/bin/python3
original=int(input())
lastnum=int(original)

def checkpalin(s):
    s=str(s)
    if(s==s[::-1]):
        print(s, "is palindrome of", original)
        quit();
    else:
        print(s)
        return False

def add(num1,num2):
    sum=int(num1+num2)
    return sum

while True:
    checkpalin(lastnum)
    lastnum_str=str(lastnum)
    lastnum_inv=lastnum_str[::-1]
    lastnum=add(lastnum,int(lastnum_inv))
