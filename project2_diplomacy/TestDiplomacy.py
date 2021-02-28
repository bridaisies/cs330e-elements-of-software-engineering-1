#!/usr/bin/env python3

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase


from Diplomacy import diplomacy_read, diplomacy_print, diplomacy_solve, diplomacy_eval, \
     compare, attacked
 

# --------------
# TestDiplomacy
# --------------


class TestDiplomacy(TestCase):

    # ---------------
    # diplomacy_solve
    # ---------------

    def test_solve_1(self):
        r = StringIO(
            "A Tokyo Hold\nB Seoul Support A\nC Beijing Support A\nD Hanoi Support E\nE Shanghai Move Tokyo\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A Tokyo\nB Seoul\nC Beijing\nD Hanoi\nE [dead]\n")

    def test_solve_2(self):
        r = StringIO(
            "A Tokyo Hold\nB Seoul Move Tokyo\nC Beijing Support A\nD Hanoi Move Beijing\nE Shanghai Support D")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A [dead]\nB [dead]\nC [dead]\nD Beijing\nE Shanghai\n")

    def test_solve_3(self):
        r = StringIO(
            "A Tokyo Hold\nB Austin Move LosAngelos\nC Berlin Support A\nD LosAngelos Move Tokyo\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(
            w.getvalue(), "A Tokyo\nB LosAngelos\nC Berlin\nD [dead]\n")

    def test_solve_4(self):
        r = StringIO("A Austin Move Dallas\nB Dallas Support Austin\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(), "A [dead]\nB [dead]\n")

    def test_solve_5(self):
        r = StringIO("A Raleigh Hold\nB Atlanta Hold\nC Tokyo Move Raleigh\nD SanAntonio Support C\nE Beijing Move Atlanta\nF Austin Support E\nG Houston Support F\nH Dallas Support F\nI Chicago Move Austin\n")
        w = StringIO()
        diplomacy_solve(r, w)
        self.assertEqual(w.getvalue(
        ), "A [dead]\nB [dead]\nC Raleigh\nD SanAntonio\nE [dead]\nF Austin\nG Houston\nH Dallas\nI [dead]\n")


    # ------------------
    # attacked
    # ------------------

    def test_attacked_1(self):
        atkr = {'A': 'Tokyo', 'C': 'Tokyo', 'E': 'Seoul'}
        loc = {'A': 'Austin', 'B': 'Tokyo',
                   'C': 'Seoul', 'D': 'NewYork', 'E': 'Dallas'}
        res = attacked(atkr, loc)
        self.assertEqual(res, {'B': ['A', 'C'], 'C': ['E']})


    # ----------------
    # compare
    # ----------------

    def test_compare_1(self):
        atkd = {'D': ['C']}
        atkr = {'C': 'Tokyo'}
        a = 'D'
        opp = 'C'
        spd = {'D': 0, 'C': 0}
        spr = {}
        loc = {'D': 'Tokyo', 'C': 'Seoul'}
        res = compare(
            atkd, atkr, a, opp, spd, spr, loc)
        self.assertEqual(res, ({'D': 0, 'C': 0}, {}, {
                         'D': '[dead]', 'C': '[dead]'}))


if __name__ == "__main__":  # pragma: no cover
    main()


""" #pragma: no cover
$ coverage run --branch TestDiplomacy.py >  TestDiplomacy.out 2>&1


$ cat TestDiplomacy.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s
OK


$ coverage report -m                   >> TestDiplomacy.out



$ cat TestDiplomacy.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s
OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Collatz.py          12      0      2      0   100%
TestCollatz.py      32      0      0      0   100%
------------------------------------------------------------
TOTAL               44      0      2      0   100%
"""
