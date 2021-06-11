import time
import sys

def constraintSet():
    constraintSet = {}
    for x in range(side):
        rowIndex = x % side
        constraintSet[x] = {y for y in range((side*rowIndex), (side*(rowIndex+1)))}

    for x in range(side):
        xTemp = x + 9
        columnIndex = x % side
        constraintSet[xTemp] = {((y * side) + columnIndex) for y in range(side)}

    xGlob = 18
    for row in range(height):
        for col in range(width):
            temp = set()
            for num in firstBlock:
                temp.add(num + (row * side * height) + (col * width))
            constraintSet[xGlob] = temp
            xGlob += 1

    return constraintSet

def firstBlock():
    firstBlock = set()
    for r in range(height):
        for c in range(width):
            firstBlock.add(c + side * r)
    return firstBlock

def neighbors():
    neighbors = {}
    for x in range(size):
        #getting horizontal component
        neighbors[x] = {row for row in range((side*(x//side)), (side*((x//side)+1)))}

        #getting vertical component
        neighbors[x].update({((y*side) + (x%side)) for y in range(side)})

        #square component
        row = x // side // height * height
        column = x % side // width * width
        for num in firstBlock:
            neighbors[x].add(num + column + (side * row))

        neighbors[x] = neighbors[x] - {x}

    return neighbors

def checkSum(pzl):
    sum = 0
    for x in pzl:
        sum += ord(x)
    return sum - (48 * (side ** 2))

def isSolved(pzl):
    for x in pzl:
        if x == ".":
            return False
    return True

def bruteForce(pzl, psbl):
    if isSolved(pzl):
        print(pzl)
        return "Check Sum: " + str(checkSum(pzl))

    one = False
    minNotUsed = SYMSET
    minPeriod = 0
    if not psbl:
        previous = -1
        psbl = {}
        for x in range(pzl.count(".")):
            notUsed = set()
            first = pzl.find(".", previous + 1)
            previous = first
            notUsed = SYMSET - {pzl[y] for y in neighbors[first]}
            #Figure out a way to break out of the loop below if 9 - len notUsed is greater than or equal to len minNotUsed
            #for y in neighbors[first]:
                #notUsed.add(pzl[y])
            #notUsed = SYMSET - notUsed
            psbl.update({first: notUsed})
            if len(notUsed) < len(minNotUsed):
                minNotUsed = notUsed
                minPeriod = first
    else:
        for key in psbl:
            if len(psbl[key]) == 0:
                return ""
            if len(psbl[key]) < len(minNotUsed):
                minNotUsed = psbl[key]
                minPeriod = key
            if len(minNotUsed) == 1:
                one = True
                break

    minSymSetChoices = SYMSET
    minSym = 0
    continued = True
    if not one:
        for sym in SYMSET:
            if continued:
                for constraints in constraintSet:
                    bigger = False
                    symSetChoices = set()
                    for constraints2 in constraintSet[constraints]:
                        if len(symSetChoices) > len(minSymSetChoices) - 1:
                            bigger = True
                            break
                        boo = True
                        if pzl[constraints2] == ".":
                            for indNewSym in neighbors[constraints2]:
                                if not boo:
                                    break
                                if pzl[indNewSym] == sym:
                                    boo = False
                            if boo:
                                symSetChoices.add(constraints2)
                    #if len(symSetChoices) < len(minSymSetChoices) and len(symSetChoices) != 0:
                    if not bigger and len(symSetChoices) != 0:
                        minSymSetChoices = symSetChoices
                        minSym = sym
                        if len(minSymSetChoices) == 1:
                            continued = False
                            one = True
                            break
            else:
                break

    if len(minSymSetChoices) < len(minNotUsed):
        for x in minSymSetChoices:
            subPzl = pzl[:x] + minSym + pzl[x+1:]
            #print("SubPzll1: " + subPzl)
            if not one:
                psbl2 = {x:{y for y in psbl[x]} for x in psbl}
                #psbl2 = {x:psbl[x] for x in psbl}
                for key in neighbors[x]:
                    if key in psbl2 and minSym in psbl2[key]:
                        psbl2[key].remove(minSym)
                #for key in psbl2:
                    #if key in neighbors[x]:
                        #if minSym in psbl2[key]:
                            #psbl2[key].remove(minSym)
                psbl2.pop(x, None)
                bF = bruteForce(subPzl, psbl2)
            else:
                for key in neighbors[x]:
                    if key in psbl and minSym in psbl[key]:
                        psbl[key].remove(minSym)
                #for key in psbl2:
                    #if key in neighbors[x]:
                        #if minSym in psbl2[key]:
                            #psbl2[key].remove(minSym)
                psbl.pop(x, None)
                bF = bruteForce(subPzl, psbl)
            if bF:
                return bF
        return ""
    else:
        for x in minNotUsed:
            subPzl = pzl[:minPeriod] + x + pzl[minPeriod+1:]
            #print(psbl)
            #print(minPeriod)
            #print(x)
            #print("SubPzll2: " + subPzl)
            if not one:
                psbl2 = {x:{y for y in psbl[x]} for x in psbl}
                #psbl2 = {x:psbl[x] for x in psbl}
                for ind in neighbors[minPeriod]:
                    if ind in psbl2 and x in psbl2[ind]:
                        psbl2[ind].remove(x)
                psbl2.pop(minPeriod, None)
                bF = bruteForce(subPzl, psbl2)
            else:
                for ind in neighbors[minPeriod]:
                    if ind in psbl and x in psbl[ind]:
                        psbl[ind].remove(x)
                psbl.pop(minPeriod, None)
                bF = bruteForce(subPzl, psbl)
            if bF:
                return bF
        return ""

start = time.time()
file = sys.argv[1]
pzls = [word for line in open(str(file), 'r') for word in line.split()]

size = len(pzls[0])
side = int(size ** 0.5)
height = int((side ** 0.5)//1)
width = int(side/height)//1
SYMSET = {x for x in pzls[0] if x != "."}

#columnSize = 3
#rowSize = 3
#neighbors = lookUpConstraints()
firstBlock = firstBlock()
constraintSet = constraintSet()
neighbors = neighbors()
psbl = {}
#print(constraintSet)
#print(neighbors)
count = 1
for pzl in pzls:
    #if count < 52:
    #if count == 17:
        forPzl = time.time()
        print("Puzzle Number: " + str(count))
        if len(pzl) != size:
            size = len(pzl)
            side = int(size ** 0.5)
            height = int((side ** 0.5)//1)
            width = int(side/height)//1
            SYMSET = {x for x in pzls if x != "."}
        #printCool(pzl, bruteForce(pzl, 0))
        print(pzl)
        print(bruteForce(pzl, {}))
        print("Time Taken: " + str('%.2f' % (time.time() - forPzl)) + "s" + "\n")
        count += 1
    #count += 1

print(str(count - 1) + " Total Puzzles Solved in " + str('%.2f' % (time.time() - start)) + "s")
