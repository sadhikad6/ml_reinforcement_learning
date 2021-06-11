import sys
import time
import random

def invCount(pz):
    toRet = 0
    pzl = list(pz)
    pzl.remove("_")
    for x in range(len(pzl)):
        for y in range(x+1, len(pzl)):
            if pzl[y] < pzl[x]:
                toRet += 1
    return toRet

def verticalDist(pzl, goal, side):
    i = pzl.find("_")
    row = i // side
    u = goal.find("_")
    rowG = u // side
    count = 0
    return abs(row - rowG)

def neighbor(pzl, side, i):
    column = i % side
    row = i // side
    if (column == 0):
        if(row == 0):
            return [i + 1, i + side]
        if(row == side - 1):
            return [i + 1, i - side]
        return [i + 1, i - side, i + side]
    if (column == side - 1):
        if(row == 0):
            return [i - 1, i + side]
        if (row == side - 1):
            return [i - 1, i - side]
        return [i - 1, i - side, i + side]
    if (row == 0):
        return [i - 1, i + 1, i + side]
    if (row == side - 1):
        return  [i - 1, i + 1, i - side]
    return [i + 1, i - 1, i + side, i - side]


def swap(pzl, i, u):
    if(u <= i):
        return pzl[:u] + pzl[i] + pzl[u+1:i] + pzl[u] + pzl[i+1:]
    return pzl[:i] + pzl[u] + pzl[i+1:u] + pzl[i] + pzl[u+1:]

def format(all, rows):
    toRet = "\n"
    lines = len(all)//7
    for x in range(lines):
        for y in range(rows):
            for pzl in range(7*x, 7*(x+1)):
                toRet += all[pzl][rows*y:rows*(y+1)] + " "
            toRet += "\n"
        toRet += "\n"
    for y in range(rows):
        for pzl in range(7*lines, len(all)):
            toRet += all[pzl][rows*y:rows*(y+1)] + " "
        toRet += "\n"
    return toRet

def solve(pzl, goal, rows):
    start = time.time()
    if pzl == goal:
        return [0, time.time() - start]
    if impossible(pzl, goal, rows):
        return [-1, time.time() - start]
    else:
        parseMe = [pzl]
        dctLevels = {parseMe[0]: 0}
        pos = 0
        while pos < len(parseMe):
            parent = parseMe[pos]
            pos += 1
            indU = parent.find("_")
            for x in neighbor(parent, rows, indU):
                child = swap(parent, x, indU)
                if child == goal:
                    return [dctLevels[parent] + 1, time.time() - start]
                if child not in dctLevels:
                    parseMe.append(child)
                    dctLevels.update({child: dctLevels.get(parent) + 1})

def impossible(pzl, goal, rows):
    if rows % 2 == 1:
        if invCount(pzl) % 2 != invCount(goal) % 2:
            return True
    if rows % 2 == 0:
        vert = verticalDist(pzl, goal, rows)
        if (invCount(pzl) + vert) % 2 != invCount(goal) % 2:
            return True
    return False

def getRan(v):
    n = len(v)
    index = random.randint(0, n - 1)
    num = v[index]
    v[index], v[n - 1] = v[n - 1], v[index]
    v.pop()
    return num

def generateRandom(n):
    toRet = ""
    v = [0] * n
    for i in range(n):
        v[i] = i + 1
    while (len(v)):
        toRet += str(getRan(v))
    return insert(toRet, random.randint(0, 9))

def insert(word, i1):
    return word[:i1] + "_" + word[i1:]

def gen500(size):
    toRet = []
    for x in range(500):
        toRet.append(generateRandom(size))
    return toRet

#Main Code
start = time.time()
size = 8
#pzls = gen500(size)
pzls = [word for line in open(str("eckel.txt"), 'r') for word in line.split()]
rows = int(len(pzls[0])**.5 + .5)
#goal = "12345678_"
goal = "ABCDEFGHIJKLMNO_"
stepCount = 0
total = 0
impCount = 0
bool = True
count = 0
for x in range(len(pzls)):
    if (time.time() - start) < 90:
        for pzl in pzls:
                print(pzl)
                listEvery = solve(str(pzl), goal, rows)
                if listEvery[0] != -1:
                    stepCount += listEvery[0]
                    total += 1
                else:
                    impCount += 1
                print("Pzl " + str(count) + ": " + pzl + " => " + str(listEvery[0]) + "\t\t" + "in " + str('%.2f' % listEvery[1]) + "s")
                count += 1
    if bool and (time.time() - start) > 90:
        print("Impossible count: " + str(impCount))
        print("Ave len for possibles: " + str('%.2f' % (stepCount/total)))
        print("Solved 500 puzzles in " + str('%.2f' % (time.time() - start)) + "s")
        bool = False
