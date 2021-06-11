import sys
import time
CORNERS = {0:{1, 8, 9}, 7:{6, 15, 14}, 56:{48, 49, 57}, 63:{62, 55, 54}}
EDGES = {0:{1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56}, 7:{0, 1, 2, 3, 4, 5, 6, 15, 23, 31, 39, 47, 55, 63}, 56:{0, 8, 16, 24, 32, 40, 48, 56, 57, 58, 59, 60, 61, 62, 63}, 63:{56, 57, 58, 59, 60, 61, 62, 7, 15, 23, 31, 39, 47, 55}}
EDGES_ORDERED = {0:[[1, 2, 3, 4, 5, 6], [8, 16, 24, 32, 40, 48]], 7:[[6, 5, 4, 3, 2, 1], [15, 23, 31, 39, 47, 55]], 56:[[48, 40, 32, 24, 16, 8], [57, 58, 59, 60, 61, 62]], 63:[[62, 61, 60, 59, 58, 57], [55, 47, 39, 31, 23, 15]]}
rowEndLookUp = {}
surroundSquare = {}
rowBeginLookUp = {}
dirAddVal = {}
CACHE = {}
min_score = 64


#mobility advantage :)
#LOOK INTO FRONTIER PIECES so basically
#in checkPlace, when incrementing count, make a list/set that stores the indices that you're going through
#in findBestMove, go through those indice's surroundSquares after the move is made and if any of the surroundSquares are periods
#then that index is a frontier piece, so count each of the frontier pieces for each move
#then pick the move that has the least amount of frontier pieces which is more important in the beginning

def CONVERT():
    toRet = {}
    letter = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for x in range(64):
        temp = letter[x%LENGTH] + str(x//LENGTH + 1)
        toRet[temp] = x
        toRet[temp.lower()] = x
    return toRet

def print2d(pzl):
    for x in range(LENGTH):
        print(pzl[x*LENGTH : (x+1)*LENGTH])

def print2dAsterisks(pzl, POS_MOVES):
    toRet = ""
    for ind, char in enumerate(pzl):
        if ind in POS_MOVES:
            toRet += "*"
        else:
            toRet += char
    print2d(toRet)

def rowBeginLookUps():
    for x in range(64):
        rowBeginLookUp[x] = (x//LENGTH)*LENGTH

def rowEndLookUps():
    for x in range(64):
        rowEndLookUp[x] = (x//LENGTH + 1)*LENGTH

def dirAddVals():
    dirAddVal[1] = LENGTH + 1
    dirAddVal[2] = -(LENGTH + 1)
    dirAddVal[3] = LENGTH - 1
    dirAddVal[4] = -(LENGTH - 1)
    dirAddVal[5] = 1
    dirAddVal[6] = -1
    dirAddVal[7] = LENGTH
    dirAddVal[8] = -LENGTH

def surroundSquares():
    for x in range(64):
        if not (x % LENGTH):
            if x == 0:
                surroundSquare[x] = {1, 8, 9}
            elif x == 56:
                surroundSquare[x] = {57, 48, 47}
            else:
                surroundSquare[x] = {x + LENGTH, x - LENGTH, x + 1, x + LENGTH + 1, x - LENGTH + 1}
        elif x % LENGTH == 7:
            if x == 7:
                surroundSquare[x] = {6, 15, 14}
            elif x == 63:
                surroundSquare[x] = {62, 55, 54}
            else:
                surroundSquare[x] = {x + LENGTH, x - LENGTH, x - 1, x - LENGTH - 1, x + LENGTH - 1}
        elif x//LENGTH == 0:
            surroundSquare[x] = {x + LENGTH, x - 1, x + 1, x + LENGTH + 1, x + LENGTH - 1}
        elif x//LENGTH == 7:
            surroundSquare[x] = {x - LENGTH, x - 1, x + 1, x - LENGTH + 1, x - LENGTH - 1}
        else:
            surroundSquare[x] = {x - LENGTH, x + LENGTH, x + 1, x - 1, x - LENGTH + 1, x - LENGTH - 1, x + LENGTH - 1, x + LENGTH + 1}

def checkPlace(pzl, ind, sym):
    if sym == "x":
        oppSym = "o"
    else:
        oppSym = "x"
    #test off diagonal down
    toRet = []
    count = 0
    indTemp = ind
    while indTemp < 64:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 1, count))
            break
        indTemp += (LENGTH + 1)
        if indTemp > len(pzl):
            break
        if indTemp >= rowEndLookUp[indTemp - 1]:
            break
        count += 1
    #test off diagonal up
    count = 0
    indTemp = ind
    while indTemp > -1:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 2, count))
            break
        indTemp -= (LENGTH + 1)
        if indTemp < -1:
            break
        if indTemp < rowBeginLookUp[indTemp + 1]:
            break
        count += 1
    #test diagonal down
    count = 0
    indTemp = ind
    while indTemp < 64:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 3, count))
            break
        indTemp += (LENGTH - 1)
        if indTemp > len(pzl) - 2:
            break
        if indTemp < rowBeginLookUp[indTemp + 1]:
            break
        count += 1
    #test diagonal up
    count = 0
    indTemp = ind
    while indTemp > 0:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 4, count))
            break
        indTemp -= (LENGTH - 1)
        if indTemp < 1:
            break
        if indTemp >= rowEndLookUp[indTemp - 1]:
            break
        count += 1
    #test horizontal right
    count = 0
    indTemp = ind
    while indTemp < rowEndLookUp[ind]:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 5, count))
            break
        indTemp += 1
        count += 1
    #test horizontal left
    count = 0
    indTemp = ind
    while indTemp >= rowBeginLookUp[ind]:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 6, count))
            break
        indTemp -= 1
        count += 1
    #test vertical down
    count = 0
    indTemp = ind
    while indTemp < 64:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 7, count))
            break
        indTemp += LENGTH
        count += 1
    #test vertical up
    count = 0
    indTemp = ind
    while indTemp > -1:
        if pzl[indTemp] != oppSym and count == 1:
            break
        if pzl[indTemp] == "." and count > 0:
            break
        if pzl[indTemp] == sym and count > 1:
            toRet.append((indTemp, 8, count))
            break
        indTemp -= LENGTH
        count += 1
    if toRet:
        return toRet
    else:
        return -1

def countFrontier(pzl, sym):
    count = 0
    previous = -1
    for y in range(pzl.count(sym)):
        found = pzl.find(sym, previous + 1)
        previous = found
        for x in surroundSquare[found]:
            if pzl[x] == ".":
                count += 1
                break
    return count

def firstMove(pzl, POS_MOVES, sym, oppSym):
    min = 64
    minStart = -1
    backUp = 0
    for start in POS_MOVES:
        cont = True
        backUp = start
        if start in CORNERS:
            return start
        for corn in CORNERS:
            if pzl[corn] != sym:
                if start in CORNERS[corn]:
                    cont = False
        if cont:
            for corn in CORNERS:
                if pzl[corn] == sym:
                    print(pzl[corn])
                    if start in EDGES[corn]:
                        print("start " + str(start))
                        change = True
                        if (corn - start) < 8 and (corn - start) > 0:
                            for ran in range(start, corn):
                                if pzl[ran] != sym:
                                    change = False
                                    break
                        elif (corn - start) > -8 and (corn - start) < 0:
                            for ran in range(corn, start):
                                if pzl[ran] != sym:
                                    change = False
                                    break
                        elif not (corn - start) % 8 and corn > start:
                            for ran in range(start, corn, 8):
                                if pzl[ran] != sym:
                                    change = False
                                    break
                        else:
                            for ran in range(corn, start, 8):
                                if pzl[ran] != sym:
                                    change = False
                                    break
                        if change:
                            return start
            if pzl.count(".") < 45:
                newPzl = makeMoves(pzl, sym, start, POS_MOVES)
                newPosMoves = posMoves(newPzl, oppSym)
                if len(newPosMoves) < min:
                    min = len(newPosMoves)
                    minStart = start
            else:
                countFrontierOG = countFrontier(pzl, sym)
                newPzl = makeMoves(pzl, sym, start, POS_MOVES)
                countFrontierNew = countFrontier(pzl, sym) - countFrontierOG
                if countFrontierNew < min:
                    min = countFrontierNew
                    minStart = start
    if minStart != -1:
        return minStart
    return backUp

def findBest(pzl, POS_MOVES, sym, oppSym):
    #first = firstMove(pzl, POS_MOVES, sym, oppSym)
    if pzl.count(".") > 15:
        upper = 100000 * len(pzl)
        best = [upper]
        #for maxDepth in range(1, 7, 1):
        maxDepth = 3
        if len(POS_MOVES) > 4:
            maxDepth = 3
        #newPzl = makeMoves(pzl, sym, first, POS_MOVES)
        #newPosMoves = posMoves(newPzl, oppSym)
        #ab = alphaBetaMG(newPzl, POS_MOVES, oppSym, sym, maxDepth - 1, -upper, best[0])
        #if -ab[0] < -best[0]: continue
        #best = ab + [first]
        #print("At Depth {} AB-MG returns {}".format(maxDepth, best))
        for mv in POS_MOVES:
            #if mv != first:
            newPzl = makeMoves(pzl, sym, mv, POS_MOVES)
            #newPosMoves = posMoves(newPzl, oppSym)
            ab = alphaBetaMG(newPzl, oppSym, sym, maxDepth - 1, -upper, best[0])
            if -ab[0] < -best[0]: continue
            best = ab + [mv]
            print("At Depth {} AB-MG returns {}".format(maxDepth, best))
        #print(best)
        return best
        #temp = str(alphaBetaMG(pzl, sym, oppSym, 3, -10000, 10000))[1:-1]
        #return "Score " + temp
    else:
        temp = str(alphaBeta(pzl, POS_MOVES, sym, oppSym, 0, -64, 64))[1:-1]
        return "Score " + temp

def calcBoardStats(pzl, sym, oppSym):
    symCount = pzl.count(sym)
    oppCount = pzl.count(oppSym)
    tokenCount = 0
    if symCount > oppCount:
        tokenCount = (800.0 * symCount)/(symCount + oppCount)
    elif oppCount > symCount:
        tokenCount = -(800.0 * oppCount)/(symCount + oppCount)
    else:
        tokenCount = 0.0
    mobilityVal = mobility(pzl, sym, oppSym)
    cornersVal = anchorSquares(pzl, sym, oppSym)
    cxVal = badCX(pzl, sym, oppSym)
    frontierVal = frontier(pzl, sym, oppSym)
    return (tokenCount) + (mobilityVal * 278.922) + (cornersVal * 2000.724) + (420.026 * cxVal) + (74.396 * frontierVal)
    #return (tokenCount) + (mobilityVal * 700.922) + (cornersVal * 2000.724) + (600.026 * cxVal) + (74.396 * frontierVal)


def frontier(pzl, sym, oppSym):
    symCount = countFrontier(pzl, sym)
    oppCount = countFrontier(pzl, oppSym)
    if symCount > oppCount:
        return -(100.0 * symCount)/(symCount + oppCount)
    elif oppCount > symCount:
        return (100.0 * oppCount)/(symCount + oppCount)
    else:
        return 0.0

def mobility(pzl, sym, oppSym):
    symCount = len(posMoves(pzl, sym))
    oppCount = len(posMoves(pzl, oppSym))
    if symCount > oppCount:
        return (100.0 * symCount)/(symCount + oppCount)
    elif oppCount > symCount:
        return -(100.0 * oppCount)/(symCount + oppCount)
    else:
        return 0.0

def badCX(pzl, sym, oppSym):
    symCount = 0
    oppCount = 0
    for corn in CORNERS:
        if pzl[corn] == ".":
            for cx in CORNERS[corn]:
                if pzl[cx] == sym:
                    if cx in {9, 14, 49, 54}:
                        symCount += 1
                    symCount += 1
                elif pzl[cx] == oppSym:
                    if cx in {9, 14, 49, 54}:
                        oppCount += 1
                    oppCount += 1
    return -12.5 * (symCount - oppCount)

def anchorSquares(pzl, sym, oppSym):
    symCount = 0
    oppCount = 0
    for corn in CORNERS:
        if pzl[corn] == sym:
            symCount += 1
            for lists in EDGES_ORDERED[corn]:
                for edges in lists:
                    if pzl[edges] == sym: symCount += 1
                    else: break
        elif pzl[corn] == oppSym:
            oppCount += 1
            for lists in EDGES_ORDERED[corn]:
                for edges in lists:
                    if pzl[edges] == oppSym: oppCount += 1
                    else: break
    return 25 * (symCount - oppCount)
    '''
    if symCount > oppCount:
        return (100.0 * symCount)/(symCount + oppCount)
    elif oppCount > symCount:
        return -(100.0 * oppCount)/(symCount + oppCount)
    else:
        return 0.0
    '''

def alphaBetaMG(pzl, sym, oppSym, level, lower, upper):
    POS_MOVES = posMoves(pzl, sym)
    if (pzl, sym, lower) in CACHE:
        return CACHE[(pzl, sym, lower)]
    #if not pzl.count("."):
        #return [pzl.count(sym) - pzl.count(oppSym)]
    if not POS_MOVES and not posMoves(pzl, oppSym):
        return [pzl.count(sym) - pzl.count(oppSym)]
    if not level:
        return [calcBoardStats(pzl, sym, oppSym)]
        #brdVal = sum(tpl[i]*statWeights[i] for i in range(len(tpl)))
        #return [brdVal]
    if not POS_MOVES:
        nm = alphaBetaMG(pzl, oppSym, sym, level - 1, -upper, -lower)
        if (pzl, sym, lower) not in CACHE:
            CACHE[(pzl, sym, lower)] = [-nm[0]] + nm[1:] + [-1]
        return [-nm[0]] + nm[1:] + [-1]
    best = [1-lower]
    for mv in POS_MOVES:
        newPzl = makeMoves(pzl, sym, mv, POS_MOVES)
        ab = alphaBetaMG(newPzl, oppSym, sym, level - 1, -upper, -lower)
        '''
        score = -ab[0]
        if score > upper: return [score]
        if score < lower: continue
        best = [score] + ab[1:] + [mv]
        lower = score + 1
        '''
        if -ab[0] > upper: return [-ab[0]]
        if ab[0] < best[0]:
            best = ab + [mv]
            lower = -best[0] + 1
    if (pzl, sym, lower) not in CACHE:
        CACHE[(pzl, sym, lower)] = [-best[0]] + best[1:]
    return [-best[0]] + best[1:]


def alphaBeta(pzl, POS_MOVES, sym, oppSym, level, lower, upper):
    #return as negamax(minSize, reversed move seq.)
    #lower is min acceptable value, upper is max acceptable value
    if (pzl, sym, lower) in CACHE:
        return CACHE[(pzl, sym, lower)]
    if not pzl.count("."):
        return [pzl.count(sym) - pzl.count(oppSym)]
    if not POS_MOVES:
        newPosMoves = posMoves(pzl, oppSym)
        if not newPosMoves:
            return [pzl.count(sym) - pzl.count(oppSym)]
        ab = alphaBeta(pzl, newPosMoves, oppSym, sym, level + 1, -upper, -lower)
        score = -ab[0]
        if score > upper: return [score]
        #if score < lower: continue
        best = [score] + ab[1:] + [-1]
        if (pzl, sym, lower) not in CACHE:
            CACHE[(pzl, sym, lower)] = best
        #if (pzl, oppSym) not in CACHE:
            #CACHE[(pzl, oppSym)] = [-best[0]] + best[1:]
        return best
    else:
        best = [lower - 1]
        for move in POS_MOVES:
            newPzl = makeMoves(pzl, sym, move, POS_MOVES)
            newPosMoves = posMoves(newPzl, oppSym)
            ab = alphaBeta(newPzl, newPosMoves, oppSym, sym, level + 1, -upper, -lower)
            score = -ab[0]
            if score > upper: return [score]
            if score < lower: continue
            #else we have improvement
            best = [score] + ab[1:] + [move]
            lower = score + 1
            if level == 0:
                print("Score " + str(best)[1:-1])
        if (pzl, sym, lower) not in CACHE:
            CACHE[(pzl, sym, lower)] = best
        #if (pzl, oppSym) not in CACHE:
            #CACHE[(pzl, oppSym)] = [-best[0]] + best[1:]
        return best

def posMoves(pzl, sym):
    toRet = {}
    if sym == "x":
        oppSym = "o"
    else:
        oppSym = "x"
    previous = -1
    seen = set()
    for x in range(pzl.count(oppSym)):
        ind = pzl.find(oppSym, previous + 1)
        previous = ind
        for toCheck in surroundSquare[ind]:
            if toCheck not in seen and pzl[toCheck] == ".":
                temp = checkPlace(pzl, toCheck, sym)
                if temp != -1:
                    toRet[toCheck] = temp
            seen.add(toCheck)
    return toRet

LENGTH = 8

def makeMoves(pzl, sym, ind, POS_MOVES):
    if sym == "x":
        oppSym = "o"
    else:
        oppSym = "x"
    if POS_MOVES:
        for end, dir, num in POS_MOVES[ind]:
            indTemp = ind
            addVal = dirAddVal[dir]
            while indTemp != end:
                pzl = pzl[:indTemp] + sym + pzl[indTemp + 1:]
                indTemp += addVal
    return pzl

def snapShot(pzl, sym, pos, POS_MOVES):
    if sym == "x":
        oppSym = "o"
    else:
        oppSym = "x"
    if not POS_MOVES:
        POS_MOVES = posMoves(pzl, oppSym)
    print(str(sym) + " plays to " + str(pos))
    newPzl = makeMoves(pzl, sym, pos, POS_MOVES)
    POS_MOVES = posMoves(newPzl, oppSym)
    #print(POS_MOVES)
    print2dAsterisks(newPzl, POS_MOVES)
    print("\n")
    print(newPzl + " " + str(newPzl.count("x")) + "/" + str(newPzl.count("o")))
    if not POS_MOVES:
        print("No Moves Possible for " + oppSym)
        POS_MOVES = posMoves(newPzl, sym)
        oppSym = sym

    toPrint = "Possible moves for " + str(oppSym) + ": "
    for x in POS_MOVES:
        toPrint += str(x) + ", "
    print(toPrint[:len(toPrint) - 2])
    print(findBest(newPzl, POS_MOVES, oppSym, sym))
    return POS_MOVES, oppSym, newPzl

start = time.time()
surroundSquares()
rowEndLookUps()
rowBeginLookUps()
dirAddVals()
convert = CONVERT()
startCount = 1
pzl = '.' * 27 + 'ox......xo' + '.' * 27
sym = ""
#POS_MOVES = posMoves(pzl, sym)
POS_MOVES = {}
lenArgs = len(sys.argv)
if lenArgs > 1:
    if len(sys.argv[1]) == 64:
        pzl = sys.argv[1].lower()
        if lenArgs > 2:
            if sys.argv[2].lower() == "x" or sys.argv[2].lower() == "o":
                sym = sys.argv[2].lower()
                startCount = 3
            else:
                startCount = 2
        else:
            startCount = 2
    elif sys.argv[1].lower() == "x" or sys.argv[1].lower() == "o":
        sym = sys.argv[1].lower()
        startCount = 2
    else:
        startCount = 1
else:
    startCount = 1

if not sym:
    if pzl.count(".") % 2:
        sym = "o"
    else:
        sym = "x"
POS_MOVES = posMoves(pzl, sym)
print2dAsterisks(pzl, POS_MOVES)
print("\n")
print(pzl + " " + str(pzl.count("x")) + "/" + str(pzl.count("o")))
#oppSym = sym
if not POS_MOVES:
    if sym == "o":
        sym = "x"
    else:
        sym = "o"
    POS_MOVES = posMoves(pzl, sym)

if sym == "o":
    oppSym = "x"
else:
    oppSym = "o"
if POS_MOVES:
    toPrint = "Possible moves for " + str(sym) + ": "
    for x in POS_MOVES:
        toPrint += str(x) + ", "
    print(toPrint[:len(toPrint) - 2])
else:
    print("No Moves Possible")
print(findBest(pzl, POS_MOVES, sym, oppSym))
print("\n")

for x in sys.argv[startCount:]:
    if x in convert:
        x = convert[x]
    if int(x) > -1:
        POS_MOVES, sym, pzl = snapShot(pzl, sym, int(x), POS_MOVES)
        print("\n")
print(time.time() - start)
