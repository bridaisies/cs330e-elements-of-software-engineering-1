#!/usr/bin/env python3

# ----------------------------------
# projects/diplomacy/RunDiplomacy.py
# Copyright (C) 2016
# Glenn P. Downing
# ----------------------------------

# -------
# imports
# -------

import sys
from Diplomacy import diplomacy_solve

# ----
# main
# ----

if __name__ == "__main__":
    diplomacy_solve(sys.stdin, sys.stdout)
