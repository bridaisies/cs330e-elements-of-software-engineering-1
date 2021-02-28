#!/usr/bin/env python3
from io import StringIO

# -------------
# diplomacy_read
# -------------


SS = "Support"
MM = "Move"
DD = "[dead]"

def diplomacy_read(s):
    """
    reads 3 strings
    s is a string
    """
    
    x = s.split()
    y = []
    if len(x) == 4:
        y= [x[0], x[1], x[2], x[3]]
    else:
        y = [x[0], x[1], x[2]]
    return y


# -------------
# diplomacy_print
# -------------


def diplomacy_print(w, i, j):
    """
    print two strings
    w is writer
    i is army name
    j is location or if they are dead
    """
    
    w.write(str(i) + " " + str(j) + "\n")


# ------------------------
# supported
# ------------------------


def supported(xlist, ydict):
    """
    returns number of supporters for each army
    """

    assert xlist[2] == SS
    if (xlist[3] in ydict):
        ydict.update({xlist[3]: ydict.get(xlist[3]) + 1})
    else:
        ydict.update({xlist[3]: 1})

    return ydict


# -------------------------
# supporters
# -------------------------


def supporters(xlist, ydict):
    """
    returns army and who they support
    """
    assert xlist[2] == SS
    if (ydict == {}):
        ydict = {xlist[0]: xlist[3]}
    else:
        ydict.update({xlist[0]: xlist[3]})

    return ydict


# ----------------------
# starting
# ----------------------


def starting(xlist, ydict):
    """
    return an army's starting location(city)
    """
    if (ydict == {}):
        ydict = {xlist[0]: xlist[1]}
    else:
        ydict.update({xlist[0]: xlist[1]})

    return ydict

# -------------------
# attacked
# -------------------


def attacked(att, city):
    """
    x is army that is attacking: city being attacked
    city is location of army
    """

    a = {}
    for x in att:
        for y in city:
            if (att.get(x) == city.get(y)):
                if ((y in a) == False):
                    lst = []
                if (a == {}):
                    lst = [x]
                    a = {y:lst}
                else:
                    if (a.get(y) == None):
                        lst = [x]
                    else:
                        z = a.get(y)
                        lst = z + [x]
                    a.update({y: sorted(lst)})

    return a

# ------------------
# compare
# ------------------


def compare(atkd, atkr, a, opp, spd, spr, loc):

    if (a in spr):
        spd[spr.get(a)] = spd[spr.get(a)] - 1
        spr.pop(a)

    os = spd.get(opp)
    ars = spd.get(a)

    if (os > ars):
        loc.update({opp: loc.get(a)})
        loc.update({a: DD})
    elif (ars > os):
        loc.update({a: loc.get(a)})
        loc.update({opp: DD})
    else:
        loc.update({opp: DD})
        loc.update({a: DD})

    return spd, spr, loc


# -----------
# winner
# -----------

def winner(x, loc, atkr, spr, spd):

    slist = []

    for a in x:
        slist.append(spd[a])

    maxx = max(slist)
    cnt = 0

    for a in x:

        if spd.get(a) == maxx:
            cnt = cnt + 1

        if cnt > 1:
            for a in x:
                loc.update({a: DD})

            return loc

    for a in x:

        if spd.get(a) == maxx:
            if a in atkr:
                loc.update({a: atkr.get(a)})
        else:
            loc.update({a: DD})

    return loc

# ---------------
# diplomacy_eval
# ---------------


def diplomacy_eval(m, spd, spr, atkd, atkr, loc):
    
    diplo_dict = {}
    
    for x in atkd:
        if x in spr:
            for y in atkd.get(x):
                spd, spr, curr = compare(atkd, atkr, x, y, spd, spr, loc)

    for ct in m:
        a_list = m.get(ct)
        loc = winner(a_list, loc, atkr, spr, spd)

    return loc


# ------------
# want_location
# ------------

def want_location(slist, m, a):

    if slist[2] == MM:

        if m == {}:
            a = [slist[0]]
            m = {slist[3]: a}

        elif slist[3] in m:
            a = m.get(slist[3]) + [slist[0]]
            m.update({slist[3]: a})

        else:
            a = [slist[0]]
            m.update({slist[3]: a})

    else:  

        if m == {}:
            a = [slist[0]]
            m = {slist[1]: a}

        elif slist[1] in m:
            a = m.get(slist[1]) + [slist[0]]
            m.update({slist[1]: a})

        else:
            a = [slist[0]]
            m.update({slist[1]: a})

    return m, a

# ---------------
# diplomacy_solve
# ---------------


def diplomacy_solve(r, w):
    """
    r a reader
    w a writer
    """
    spd, spr, atkr, loc, m = {}, {}, {}, {}, {}
    a = []

    num = 0
    for s in r:
        inf = diplomacy_read(s)
        assert len(inf) > 2 and len(inf) < 5 
        loc = starting(inf, loc)
        m, a = want_location(inf, m, a)

        num = num + 1

        if (len(inf) > 3) and (inf[2] == MM):
            atkr.update({inf[0]: inf[3]})  
        elif (len(inf) > 3) and (inf[2] == SS):
            spd = supported(inf, spd)
            spr = supporters(inf, spr)

    for x in loc:
        if x not in spd:
            spd.update({x: 0})

    atkd = attacked(atkr, loc)

    res = diplomacy_eval(
        m, spd, spr, atkd, atkr, loc)
    res2 = sorted(res.items())

    assert len(res2) == num  

    for y in res2:
        name = y[0]
        loc2 = y[1]
        diplomacy_print(w, name, loc2)
