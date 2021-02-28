#!/usr/bin/env python3

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2016
# Glenn P. Downing
# ---------------------------

# ------------
# collatz_read
# ------------


def collatz_read(s):
    """
    read two ints
    s a string
    return a list of two ints, representing the beginning and end of a range, [i, j]
    """
    a = s.split()
    return [int(a[0]), int(a[1])]

# ------------
# collatz_eval
# ------------


cache = {}


def collatz_eval(i, j):
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """
    assert i > 0 and i < 999999 and j > 0 and j < 999999

    # range from low to high
    if(i <= j):
        lo, hi = i, j
    else:
        lo, hi = j, i

    #m = max
    m = 1
    for var in range(lo, hi + 1):
        # c = length of cycle
        c = 1

        if var in cache:
            c = cache[var]
        else:
            x = var
            while(x > 1):
                if x in cache:
                    c = c + (cache[x] - 1)
                    break
                if (x % 2 == 0):
                    x = x >> 1
                    c = c + 1
                else:
                    # optimize for odd numbers
                    x = x + (x >> 1) + 1
                    c = c + 2

        cache[var] = c
        assert cache != {}  # check conditions

        m = max(m, c)

    return m

# -------------
# collatz_print
# -------------


def collatz_print(w, i, j, v):
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# collatz_solve
# -------------


def collatz_solve(r, w):
    """
    r a reader
    w a writer
    """
    for s in r:
        i, j = collatz_read(s)
        v = collatz_eval(i, j)
        collatz_print(w, i, j, v)
