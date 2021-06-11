import sys
import time
import re
import random

#to do list:
#step 1: in posChoices method, make posChoices a dictionary that assigns that tuple to a set of indices that the word consists of
#step 2: make bruteForce take a 4th arg being the possibleWords of every position in posChoices so that you don't recalculate from the entire word bank every time
#step 2.5: maybe make an method that finds the initial possiblewords that could go in each position in posChoices
#step 3: when you add a word into an index into the puzzle, note which positions in posChoices would actually change based on that decision by checking if the indices of the words overlap
#then make bruteForce accept a 5th argument of the positions in posChoices that actually should be recalculated

#make a method that assigns the positions in posChoices indices, then from there
#make a dictionary of the positions in posChoices that connects to a set of other positions in posChoices that are effected by it
#so that way, when you're finding the possible words, you only need to check those indices and not redo all of the possibleWords
#step 72: Weight words based on the index of the letter too? maybe like vowels in the 2nd or 3rd position can be weighted higher?

#reference sudoku

def print2d(pzl):
    for x in range(HEIGHT):
        print(pzl[x*WIDTH : (x+1)*WIDTH])

def symSquare_method(SIZE):
    toRet = {}
    for x in range(SIZE):
        toRet[x] = SIZE - 1 - x
    return toRet

def findBegRow_method():
    toRet = {}
    current = 0
    for x in range(SIZE):
        if x % WIDTH == 0:
            current = x
            toRet[x] = [x]
        else:
            toRet[current].append(x)
    return toRet

def findEndRow_method():
    toRet = {}
    current = SIZE - 1
    for x in range(SIZE - 1, -1, -1):
        if x % WIDTH == WIDTH - 1:
            current = x
            toRet[x] = [x]
        else:
            toRet[current].append(x)
    return toRet

def findVertRow_method():
    toRet = {}
    for r in range(WIDTH):
        toRet[r] = []
        for h in range(HEIGHT):
            toRet[r].append(r+(WIDTH * h))
    return toRet

def freq():
    dictLetterToVal = {}
    letterOrdered = []
    for word in DICT:
        for letter in word:
            if letter not in dictLetterToVal:
                dictLetterToVal[letter] = 1.0/COUNTLEN
            else:
                dictLetterToVal[letter] += 1.0/COUNTLEN
    for letter in dictLetterToVal:
        letterOrdered.append((dictLetterToVal[letter], letter))
    letterOrdered = sorted(letterOrdered)[::-1]

    return letterOrdered, dictLetterToVal

def initialPosWords(pzl, posChoices):
    toRet = {}
    tupleRemove = ()
    for index, orient, wordLen in posChoices:
        possibleWords = []
        constraints = []
        if orient == "h":
            toAdd = 1
        else:
            toAdd = WIDTH
        for x in range(wordLen):
            if pzl[index+(x*toAdd)] != EMP_SQUARE:
                constraints.append((x, pzl[index + (x*toAdd)]))
        #print(index)
        #print(constraints)
        if pzl[index] == EMP_SQUARE:
            if len(constraints) == 0:
                possibleWords = orgByLen[wordLen]
            else:
                for value, word in orgByLen[wordLen]:
                    cont = True
                    for place, charac in constraints:
                        if word[place] != charac:
                            cont = False
                            break
                    if cont:
                        possibleWords.append((value, word))
        elif pzl[index] != EMP_SQUARE:
            if len(constraints) == wordLen:
                tupleRemove = (index, orient, wordLen)
            else:
                if len(constraints) == 1:
                    possibleWords = orgByLenAndStart[(pzl[index], wordLen)]
                else:
                    for value, word in orgByLenAndStart[(pzl[index], wordLen)]:
                        cont = True
                        for place, charac in constraints:
                            if word[place] != charac:
                                cont = False
                                break
                        if cont:
                            possibleWords.append((value, word))
        toRet[(index, orient, wordLen)] = sorted(possibleWords)[::-1]

    if tupleRemove in posChoices:
        posChoices.remove(tupleRemove)
    return toRet, posChoices

def posChoices_method(pzl):
    toRet = set()
    #for horizontal words
    for beg in begRow:
        end = begRow[beg][WIDTH - 1]
        newBeg = beg
        while newBeg <= end and pzl[newBeg] == BLOCK:
            newBeg += 1
        if newBeg >= end:
            toCont = False
        else:
            foundBlock = pzl.find(BLOCK, newBeg)
            if foundBlock == -1 or foundBlock > end:
                foundBlock = end + 1
                toRet.add((newBeg, "h", foundBlock - newBeg))
            else:
                while foundBlock <= end:
                    toRet.add((newBeg, "h", foundBlock - newBeg))
                    newBeg = foundBlock + 1
                    foundBlock += 1
                    while newBeg <= end and pzl[newBeg] == BLOCK:
                        newBeg = foundBlock + 1
                        foundBlock += 1
                    if newBeg >= end:
                        break
                    foundBlock = pzl.find(BLOCK, newBeg)
                    if foundBlock == -1 or foundBlock > end:
                        foundBlock = end + 1
                        toRet.add((newBeg, "h", foundBlock - newBeg))

    #for vertical words
    for beg in vertRow:
        end = vertRow[beg][HEIGHT - 1]
        newBeg = beg
        while newBeg <= end and pzl[newBeg] == BLOCK:
            newBeg += WIDTH
        if newBeg >= end:
            toCont = False
        else:
            for x in range(HEIGHT):
                foundBlock = newBeg + (WIDTH * x)
                if pzl[foundBlock] == BLOCK:
                    break
                if foundBlock >= end:
                    foundBlock = end + 1
                    break
            if foundBlock > end:
                foundBlock = end + 1
                toRet.add((newBeg, "v", (foundBlock - newBeg)//WIDTH + 1))
            else:
                while foundBlock <= end:
                    if foundBlock - newBeg == 0:
                        break
                    toRet.add((newBeg, "v", (foundBlock - newBeg)//WIDTH))
                    newBeg = foundBlock + WIDTH
                    foundBlock += WIDTH
                    #if newBeg >= SIZE:
                        #break
                    while newBeg <= end and pzl[newBeg] == BLOCK :
                        newBeg = foundBlock + WIDTH
                        foundBlock += WIDTH
                    if newBeg >= end:
                        break
                    for x in range(HEIGHT):
                        foundBlock = newBeg + (WIDTH * x)
                        if pzl[foundBlock] == BLOCK:
                            break
                        if foundBlock >= end:
                            foundBlock = end + 1
                            break
                    if foundBlock > end:
                        foundBlock = end + 1
                        toRet.add((newBeg, "v", (foundBlock - newBeg)//WIDTH + 1))
    #print(toRet)
    return toRet

def connectedPositions_method(posChoices):
    toRet = {}
    toRetFinal = {}
    for index, orient, wordLen in posChoices:
        indices = set()
        if orient == "h":
            toAdd = 1
        else:
            toAdd = WIDTH
        for x in range(wordLen):
            indices.add(index + (x*toAdd))
        toRet[(index, orient, wordLen)] = indices
    for tuple in toRet:
        connectedPos = set()
        for wordIndex in toRet[tuple]:
            for tuple2 in toRet:
                if wordIndex in toRet[tuple2] and tuple2 != tuple:
                    connectedPos.add(tuple2)
        toRetFinal[tuple] = connectedPos
    return toRetFinal

def bruteForcePlace(pzl, usedWords, posChoices, posWords, prevTuple):
    if SIZE >= 200:
        print2d(pzl)
    if len(posChoices) == 0:
        return pzl

    minPossibleWords = [2] * 100000
    tupleOfChoice = (0, "", 0)
    newPosWords = {}
    for tuple in posChoices:
        index, orient, wordLen = tuple
        if len(prevTuple) == 0 or tuple in connectedPositionsGLOB[prevTuple]:
            possibleWords = []
            constraints = []
            if orient == "h":
                toAdd = 1
            else:
                toAdd = WIDTH
            for x in range(wordLen):
                if pzl[index+(x*toAdd)] != EMP_SQUARE:
                    constraints.append((x, pzl[index + (x*toAdd)]))
            #print(index)
            #print(constraints)
            #if pzl[index] == EMP_SQUARE:
            for value, word in posWords[tuple]:
                if word not in usedWords:
                    cont = True
                    for place, charac in constraints:
                        if word[place] != charac:
                            cont = False
                            break
                    if cont:
                        possibleWords.append((value, word))
            if len(possibleWords) == 0:
                return ""
        else:
            #print("NO change")
            #print(tuple)
            possibleWords = posWords[tuple]
        newPosWords[tuple] = possibleWords
        if len(possibleWords) < len(minPossibleWords):
            minPossibleWords = possibleWords
            tupleOfChoice = tuple

    index, orient, wordLen = tupleOfChoice
    #posChoices.remove(tupleOfChoice)
    posChoices2 = [x for x in posChoices]
    posChoices2.remove(tupleOfChoice)
    usedWords2 = {x for x in usedWords}
    for vals, word in minPossibleWords:
        if word not in usedWords2:
            subPzl = insertWord(pzl, index, orient, word)
            usedWords2.add(word)
            newBF = bruteForcePlace(subPzl, usedWords2, posChoices2, newPosWords, tupleOfChoice)
            if newBF:
                return newBF
    return ""

def insertWord(pzl, index, orient, word):
    if orient.lower() == "h":
        pzl = pzl[:index] + word + pzl[index + len(word):]
    else:
        for x in range(len(word)):
            newLoc = index + (WIDTH*x)
            pzl = pzl[0:newLoc] + word[x] + pzl[newLoc + 1:]
    return pzl

def orgByLenAndStart_method():
    toRet = {}
    for word in DICT:
        value = 0
        for letter in word:
            value += dictLetterToVal[letter]
        word = word.lower()
        if (word[0], len(word)) not in toRet:
            toRet[(word[0], len(word))] = [(value, word)]
        else:
            toRet[(word[0], len(word))].append((value, word))
    for tuple in toRet:
        toRet[tuple] = sorted(toRet[tuple])[::-1]
    return toRet

def orgByLen_method():
    toRet = {}
    for word in DICT:
        value = 0
        for letter in word:
            value += dictLetterToVal[letter]
        if len(word) not in toRet:
            toRet[len(word)] = [(value, word.lower())]
        else:
            toRet[len(word)].append((value, word.lower()))
    for length in toRet:
        toRet[length] = sorted(toRet[length])[::-1]
    return toRet

#cardinalSquares is an index assigned to a tuple that has the index as the first arg and then the orientation as the second arg
#1 = down, 2 = right, 3 = up, 4 = left
def cardinalSquares_method(SIZE):
    toRet = {}
    for x in range(SIZE):
        toRet[x] = set()
        listDown = [1]
        listUp = [3]
        listLeft = [4]
        listRight = [2]
        for toAdd in range(3):
            if x + (WIDTH*(toAdd + 1)) < SIZE and len(listDown) == toAdd + 1:
                listDown.append(x + (WIDTH*(toAdd + 1)))
            if (x+toAdd)%WIDTH != (WIDTH - 1) and x+toAdd < SIZE and len(listRight) == toAdd + 1:
                listRight.append((x+toAdd)+1)
            if x-toAdd >= 0 and (x-toAdd)%WIDTH and len(listLeft) == toAdd + 1:
                listLeft.append(x-toAdd-1)
            if x - (WIDTH*(toAdd + 1)) >= 0 and len(listUp) == toAdd + 1:
                listUp.append(x-(WIDTH*(toAdd+1)))
        toRet[x] = [listDown, listRight, listLeft, listUp]
    return toRet

def antiClump_method(SIZE):
    toRet = []
    for x in range(SIZE):
        uD = (x//WIDTH) * (HEIGHT - (x//WIDTH) - 1)
        lR = (x%WIDTH) * (WIDTH - (x%WIDTH) - 1)
        toRet.append((uD-lR, x))
    return sorted(toRet)[::-1]

def placeBlocks(pzl, blocksToBeAdded, checkedAlready):
    pzl, blocksToBeAdded = check3orPlace(pzl, blocksToBeAdded)
    #print("\n")
    #print2d(pzl)
    if not pzl:
        return ""
    if not wordInTwo(pzl):
        return ""

    connectedSquares = isConnected(pzl, pzl.find(EMP_SQUARE), set())
    if len(connectedSquares) != (SIZE - pzl.count(BLOCK)):
        if SIZE - len(connectedSquares) == blocksToBeAddedGLOBAL:
            for ind, char in enumerate(pzl):
                if ind not in connectedSquares and char != BLOCK:
                    pzl = pzl[:ind] + BLOCK + pzl[ind + 1:]
            return pzl
        return ""

    if pzl.count(BLOCK) == blocksToBeAddedGLOBAL:
        return pzl

    if SIZE >= 200:
        #listOfIndices = antiClump_method(SIZE)
        listOfIndices = [x for x in range(len(pzl))]
        random.shuffle(listOfIndices)
        #for ind, char in enumerate(pzl):
        #for val, ind in listOfIndices:
        for ind in listOfIndices:
            if ind not in checkedAlready:
                char = pzl[ind]
                if char == EMP_SQUARE and pzl[symSquares[ind]] == EMP_SQUARE:
                    checkedAlready.add(ind)
                    subPzl = pzl[:ind] + BLOCK + pzl[ind + 1:]
                    radSymLoc = symSquares[ind]
                    checkedAlready.add(radSymLoc)
                    subPzl = subPzl[:radSymLoc] + BLOCK + pzl[radSymLoc + 1:]
                    newPzl = placeBlocks(subPzl, blocksToBeAdded, checkedAlready)
                    if newPzl:
                        return newPzl
    else:
        for ind, char in enumerate(pzl):
            if ind not in checkedAlready:
                char = pzl[ind]
                if char == EMP_SQUARE and pzl[symSquares[ind]] == EMP_SQUARE:
                    checkedAlready.add(ind)
                    subPzl = pzl[:ind] + BLOCK + pzl[ind + 1:]
                    radSymLoc = symSquares[ind]
                    checkedAlready.add(radSymLoc)
                    subPzl = subPzl[:radSymLoc] + BLOCK + pzl[radSymLoc + 1:]
                    newPzl = placeBlocks(subPzl, blocksToBeAdded, checkedAlready)
                    if newPzl:
                        return newPzl
    return ""

#will check if each empty square has at least two empty cardinal squares, which gaurentees that it will be in a 2 words
#returns true or false
def wordInTwo(pzl):
    for ind, char in enumerate(pzl):
        if char != BLOCK:
            even = False
            odd = False
            for card in cardinalSquares[ind]:
                if len(card) > 1:
                    if pzl[card[1]] != BLOCK:
                        if card[0] % 2:
                            even = True
                        else:
                            odd = True
            if not even or not odd:
                return False
    return True

#returns list of the indices that are connected
#whatever method that calls this must then check is the length of what this returns is equal to the number of empty squares in the puzzle
def isConnected(pzl, ind, checked):
    checked.add(ind)
    for card in cardinalSquares[ind]:
        if len(card) > 1:
            if pzl[card[1]] != BLOCK and card[1] not in checked:
                isConnected(pzl, card[1], checked)
    #print(checked)
    return checked

def checkSym(pzl):
    oldPzl = pzl
    prev = -1
    checkedSquares = set()
    for var in range(oldPzl.count(BLOCK)):
        found = oldPzl.find(BLOCK, prev + 1)
        prev = found
        if found not in checkedSquares:
            checkedSquares.add(found)
            checkedSquares.add(symSquares[found])
            if pzl[symSquares[found]] != BLOCK:
                pzl = pzl[:symSquares[found]] + BLOCK + pzl[symSquares[found] + 1:]
    return pzl

#the below method checks if there are a minimum 3 cont spaces in the pzl
#strategy: find a block, check if the surrounding cardinal pieces are NOT blocks, that you can move at least 3 spaces in that dir
#if you cannot, then place a block there and return the new pzl
#theoretically should place all "implied" blocks from one block placement (sym blocks should have already been placed)
#if the puzzle is invalid (like too many implied blocks must be added), returns an empty string!!
def check3orPlace(pzl, blocksToBeAdded):
    #pzl = checkSym(pzl)
    oldPzl = ""
    while oldPzl != pzl:
        oldPzl = pzl
        prev = -1
        for countVar in range(oldPzl.count(BLOCK)):
        #    if blocksToBeAdded < 0:
            #    return "", -1
            if pzl.count(BLOCK) > blocksToBeAddedGLOBAL:
                return "", -1
            ind = oldPzl.find(BLOCK, prev+1)
            prev = ind
            if ind not in checkedBlocksGLOBAL:
                checkedBlocksGLOBAL.add(ind)
                #if ind <= SIZE/2:
                for listOfIndices in cardinalSquares[ind]:
                    pzl, newBlocks = check3(pzl, listOfIndices)
                    if not pzl:
                        return pzl, blocksToBeAdded
                    blocksToBeAdded = blocksToBeAdded - len(newBlocks)
    return pzl, blocksToBeAdded

#returns pzl, number blocks that were added
def check3(pzl, indices):
    makeBlocks = False
    newBlock = []
    if len(indices) > 1 and pzl[indices[1]] == BLOCK:
        return pzl, newBlock
    if len(indices) != 4:
        for ind in indices[1:]:
            if pzl[ind] != BLOCK:
                makeBlocks = True
                break
    else:
        for ind in indices[1:]:
            if pzl[ind] == BLOCK:
                makeBlocks = True
                break
    if makeBlocks:
        for ind in indices[1:]:
            if pzl[ind] != BLOCK and pzl[ind] != EMP_SQUARE:
                return "", 0
            if pzl[ind] != BLOCK:
                pzl = pzl[0:ind] + BLOCK + pzl[ind + 1:]
                radSymLoc = symSquares[ind]
                if pzl[radSymLoc] != EMP_SQUARE and pzl[radSymLoc] != BLOCK:
                    return "", 0
                pzl = pzl[0:radSymLoc] + BLOCK + pzl[radSymLoc + 1:]
                newBlock.append(ind)
                newBlock.append(radSymLoc)
    return pzl, newBlock

def placeSeed(pzl, seedString):
    newBlocks = 0
    orient = seedString[0]
    h = re.findall(r'\d{1,2}(?=x)', seedString)[0]
    w = re.findall(r'(?<=x)\d*', seedString)[0]
    if len(w) == 2:
        input = seedString[seedString.find("x" + w) + 3:]
    else:
        input = seedString[seedString.find("x" + w) + 2:]
    location = (int(h) * WIDTH) + int(w)
    if not input:
        pzl = pzl[0:location] + BLOCK + pzl[location + 1:]
        radSymLocation = symSquares[location]
        pzl = pzl[0:radSymLocation] + BLOCK + pzl[radSymLocation + 1:]
        newBlocks = newBlocks + 2
    else:
        if orient.lower() == "h":
            if not input.count(BLOCK):
                pzl = pzl[0:location] + input.lower() + pzl[location + len(input):]
            else:
                for x in range(len(input)):
                    if input[x] == BLOCK:
                        radSymLoc = symSquares[location + x]
                        pzl = pzl[0:radSymLoc] + BLOCK + pzl[radSymLoc + 1:]
                        newBlocks = newBlocks + 2
                    pzl = pzl[0:location + x] + input[x].lower() + pzl[location + x + 1:]
        else:
            for x in range(len(input)):
                newLoc = location + (WIDTH*x)
                if input[x] == BLOCK:
                    radSymLoc = symSquares[newLoc]
                    pzl = pzl[0:radSymLoc] + BLOCK + pzl[radSymLoc + 1:]
                    newBlocks = newBlocks + 2
                pzl = pzl[0:newLoc] + input[x].lower() + pzl[newLoc + 1:]
    return pzl, newBlocks

CACHE = {}
start = time.time()
temp = sys.argv[1].find("x")
EMP_SQUARE = "-"
BLOCK = "#"
HEIGHT, WIDTH = int(sys.argv[1][0:temp]), int(sys.argv[1][temp + 1:])
SIZE = HEIGHT * WIDTH
symSquares = symSquare_method(SIZE)
cardinalSquares = cardinalSquares_method(SIZE)
checkedBlocksGLOBAL = set()
begRow = findBegRow_method()
endRow = findEndRow_method()
vertRow = findVertRow_method()
pzl = EMP_SQUARE * SIZE
blocksToBeAddedGLOBAL = int(sys.argv[2])
blocksToBeAddedGlob2 = blocksToBeAddedGLOBAL
DICT = sys.argv[3]

DICT = [word for line in open(str(sys.argv[3]), 'r') for word in line.split()]
COUNTLEN = 0
for word in DICT:
    COUNTLEN += len(word)
letterOrdered, dictLetterToVal = freq()
orgByLenAndStart = orgByLenAndStart_method()
orgByLen = orgByLen_method()
inPzl = set()
if len(sys.argv) > 4:
    for arg in sys.argv[4:]:
        pzl, newBlocks = placeSeed(pzl, arg)
        blocksToBeAddedGlob2 = blocksToBeAddedGLOBAL - newBlocks
#finPzl = placeBlocks(pzl, blocksToBeAddedGLOBAL)
#print2d(finPzl)
if SIZE == blocksToBeAddedGLOBAL:
    print2d(BLOCK * SIZE)
else:
    #print("SeedString Puzzle")
    #print2d(pzl)
    if blocksToBeAddedGLOBAL % 2 == 1 and HEIGHT % 2 == 1 and WIDTH % 2 == 1:
        pzl = pzl[:len(pzl)//2] + BLOCK + pzl[len(pzl)//2 + 1:]
    pzl, blocksToBeAddedGlob2 = check3orPlace(pzl, blocksToBeAddedGlob2)
    #print("\n")
    #print("Puzzle with Implied Blocks From SeedString")
    #print2d(pzl)
    pzl = placeBlocks(pzl, blocksToBeAddedGlob2, set())
    #print("\n")
    print("Final Crossword")
    if SIZE == 15*15:
        pzl = "----###----#---------#----#---------#-----------#---#-----###--------------###-------#---------#----#-----------#-----------#----#---------#-------###--------------###-----#---#-----------#---------#----#---------#----###----"
        #pzl = "---###----##--------#----##--------#-----#---#----#---------#-------##-----#--------------###-------#-----------#-------------------###--------------#-----#--------#--------------#---#-----#--------##----#--------##----###---"

        if len(sys.argv) > 4:
            for arg in sys.argv[4:]:
                pzl, newBlocks = placeSeed(pzl, arg)
    print2d(pzl)
    posChoiceGLOB = posChoices_method(pzl)
    #print(posChoiceGLOB)
    posWordsGLOB, posChoiceGLOB2 = initialPosWords(pzl, posChoiceGLOB)
    #print(posWordsGLOB[(4, "v", 4)])
    connectedPositionsGLOB = connectedPositions_method(posChoiceGLOB)
    pzl = bruteForcePlace(pzl, set(), posChoiceGLOB2, posWordsGLOB, ())
    #pzl = insertHorizontal(pzl)
    print("\n")
    print("Filled Out Crossword")
    print2d(pzl)
    print(time.time() - start)

#TODO LIST
#set up brute force so it takes a 4th arg on possible words for each position so then you only have to redo the possible words for ones that would change based on the previous index
#make poschoices a dictionary that connects the the indicies in the words and then if any other word has those same indicies, then it's possible words changed
#set up values of word in list also by position of letter because if there are barely any words with t as the second letter, that isn't good right? right
