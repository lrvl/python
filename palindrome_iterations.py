#!/usr/bin/env python3
"""Find palindrome of a given number"""

import argparse
import sys


def get_input():
    """Parse command line arguments to get user input"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('start_num', type=int, help='starting number')
    parser.add_argument('max_iter', type=int, help='maximum number of iterations')
    args = parser.parse_args()

    if args.start_num < 0:
        print("Input value must be non-negative")
        sys.exit()

    return args.start_num, args.max_iter


def is_palindrome(num):
    """Check if a number is a palindrome"""

    return str(num) == str(num)[::-1]


def main():
    """Find the palindrome of a given number"""

    start_num, max_iter = get_input()
    last_num = start_num

    for i in range(max_iter):
        if is_palindrome(last_num):
            print(f"{last_num} is a palindrome of {start_num}")
            sys.exit()

        print(last_num)
        last_num_str = str(last_num)
        last_num_inv = last_num_str[::-1]
        last_num += int(last_num_inv)

    print(f"Maximum iterations ({max_iter}) reached without finding a palindrome.")


if __name__ == '__main__':
    main()
