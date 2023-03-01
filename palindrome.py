#!/usr/bin/python3
""" Find palindrome of given number """
import sys

STARTNUM=int(input())
LASTNUM=int(STARTNUM)

def checkpalin(lastnum_str):
    """ Takes one number and checks if it is a palindrome """
    lastnum_str=str(lastnum_str)
    if lastnum_str==lastnum_str[::-1]:
        print(lastnum_str, "is palindrome of", STARTNUM)
        sys.exit()
    else:
        print(lastnum_str)
        return False

while True:
    checkpalin(LASTNUM)
    LASTNUM_STR=str(LASTNUM)
    LASTNUM_INV=LASTNUM_STR[::-1]
    LASTNUM=LASTNUM+int(LASTNUM_INV)
