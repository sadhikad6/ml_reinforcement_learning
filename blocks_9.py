import time
import sys
#placing all block positions vs placing all blocks in one index position
def printCool(pzl):
    side = WIDTH
    for x in range(HEIGHT):
        print(str(pzl[(side*x):(side*(x+1))]))

#Reference: Decomposition: 5x7 3x11 2x1 6x10 4x8
def printDecomp(pzl):
    if pzl == "":
        print("No Solution")
    else:
        toSee = {x for x in blocksListSub.keys()}
        seen = set()
        indSeen = set()
        pzl = pzl.replace("_", ".")
        #pzl = pzl.lower()
        toRet = ""
        for ind, char in enumerate(pzl):
            if char not in seen and char != ".":
                ind2 = ind
                count = 0
                endPoint = (ind2//WIDTH + 1)*WIDTH
                while ind2 < endPoint and pzl[ind2] == char:
                    count += 1
                    ind2 += 1
                seen.add(char)
                width = 0
                height = 0
                var1, var2 = blocksList[char]
                #print(var1)
                #print(var2)
                if var1 == count:
                    width = var1
                    height = var2
                elif var2 == count:
                    width = var2
                    height = var1
                toRet += str(height) + "x" + str(width) + " "
            if char == "." and ind not in indSeen:
                ind2 = ind
                subWid = 0
                while ind2 < len(pzl) and pzl[ind2] == ".":
                    indSeen.add(ind2)
                    subWid += 1
                    ind2 += 1
                subHei = 0
                ind2 = ind
                while ind2 <= len(pzl) - 1 and pzl[ind2] == ".":
                    indSeen.add(ind2)
                    subHei += 1
                    ind2 += WIDTH
                toRet += str(subHei) + "x" + str(subWid) + " "
        printCool(pzl)
        print("Decomposition: " + toRet)

def fits(pzl, height, width, insertPos):
    if height > HEIGHT or width > WIDTH:
        return False
    if ((insertPos//WIDTH) + height) > HEIGHT or ((insertPos%WIDTH) + width) > WIDTH:
        return False
    for row in range(height):
        addVal = row * WIDTH
        if pzl[insertPos + addVal:insertPos + width + addVal].count(".") != width:
            return False
    return True

def fillInSub(pzl, tuple, letter, insertPos):
    height = tuple[0]
    width = tuple[1]
    #print(height)
    #print(width)
    #print(insertPos)
    for row in range(height):
        addVal = row * WIDTH
        pzl = pzl[0:insertPos + addVal] + letter*width + pzl[insertPos + width + addVal:]
        #printCool(pzl)
    #printCool(pzl)
    #print()
    return pzl

def isInvalid(pzl):
    for letter in blocksListSub:
        if pzl.count(letter) != blocksListSub[letter] and pzl.count(letter) != 0:
            #printCool(pzl)
            return True
    return False

def isSolved(pzl):
    if not blocksTupleOrdered:
        return True
    return False

def bruteForce(pzl):
    if not pzl:
        return ""
    #if isInvalid(pzl):
        #return ""
    if isSolved(pzl):
        return pzl

    letter = ""
    letter = blocksTupleOrdered[0][1]
    print(letter)
    blocksTupleOrdered.pop(0)
    if blocksTupleOrdered:
        print(blocksTupleOrdered[0][1])

    cont = False
    if blocksList[letter][1] != blocksList[letter][0]:
        cont = True
    previous = pzl.find(".") - 1
    for num in range(pzl.count(".")):
        insertPos = pzl.find(".", previous + 1)
        previous = insertPos
    #for insertPos, char in enumerate(pzl):
        #if char == ".":
            #print(insertPos)
            #print(blocksList[letter][0])
        if fits(pzl, blocksList[letter][0], blocksList[letter][1], insertPos):
            subPzl = fillInSub(pzl, blocksList[letter], letter, insertPos)
            bF = bruteForce(subPzl)
            if bF:
                return bF
        if cont:
            if fits(pzl, blocksList[letter][1], blocksList[letter][0], insertPos):
                subPzl = fillInSub(pzl, (blocksList[letter][1], blocksList[letter][0]), letter, insertPos)
                bF = bruteForce(subPzl)
                if bF:
                    return bF
    return ""

#reference Input Blocks.py 9x18 4x8 7 5 3x11 6 10
def breakDown():
    bothFill = False
    overallHeight = 0
    overallWidth = 0
    tempHeight = 0
    tempWidth = 0
    toRetSub = {}
    toRet = {}
    toRetOrder = []
    alphaList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
    countAlpha = 0
    for arg in range(len(sys.argv)):
        if arg != 0:
            word = sys.argv[arg]
            if word.find("x") != -1:
                if overallHeight == 0 and overallWidth == 0:
                    overallHeight = int(word[0:word.find("x")])
                    overallWidth = int(word[word.find("x") + 1:])
                else:
                    tempHeight = int(word[0:word.find("x")])
                    tempWidth = int(word[word.find("x") + 1:])
                    bothFill = True
            elif word.find("X") != -1:
                if overallHeight == 0 and overallWidth == 0:
                    overallHeight = int(word[0:word.find("X")])
                    overallWidth = int(word[word.find("X") + 1:])
                else:
                    tempHeight = int(word[0:word.find("X")])
                    tempWidth = int(word[word.find("X") + 1:])
                    bothFill = True
            else:
                if overallHeight == 0:
                    overallHeight = int(word)
                elif overallWidth == 0:
                    overallWidth = int(word)
                elif tempHeight == 0:
                    tempHeight = int(word)
                elif tempWidth == 0:
                    tempWidth = int(word)
                    bothFill = True

            if bothFill:
                tempLetter = alphaList[countAlpha]
                toRet.update({tempLetter: (tempHeight, tempWidth)})
                #if tempHeight != tempWidth:
                #toRet.update({tempLetter.upper(): (tempWidth, tempHeight)})
                toRetSub.update({tempLetter: tempHeight*tempWidth})
                toRetOrder.append((tempHeight*tempWidth, tempLetter))
                #toRetOrder.append((tempHeight*tempWidth, tempLetter.upper()))
                #toRetOrder.update({tempHeight * tempWidth: tempLetter})
                #toRetSub2.update({tempHeight*tempWidth: tempLetter})
                tempHeight = 0
                tempWidth = 0
                bothFill = False
                countAlpha += 1

    return overallHeight, overallWidth, toRetSub, toRet, sorted(toRetOrder, reverse = True)

start = time.time()
HEIGHT, WIDTH, blocksListSub, blocksList, blocksTupleOrdered = breakDown()
#print(blocksTupleOrdered)
#print(blocksList)
#HEIGHT = 9
#WIDTH = 18
#blocksListSub = {"a": 32, "b": 35, "c": 33, "d": 60}
#blocksList = {"a": (4, 8), "A": (8, 4), "b": (5, 7), "B": (7, 5), "c": (11, 3), "C": (3, 11), "d": (6, 10), "D": (6, 10)}

pzl = "." * (WIDTH * HEIGHT)
periodCount = len(pzl) - sum(blocksListSub.values())
if sum(blocksListSub.values()) > len(pzl):
    printDecomp("")
else:
    printDecomp(bruteForce(pzl))
print("Time Taken: " + str('%.4f' % (time.time() - start)) + "s")


#python blocks.py 9x18 4x8 7 5 3x11 6 10
#Decomposition: 5x7 3x11 2x1 6x10 4x8

#DOESN'T WORK IF IT INVOLVES REPEATSSSSSS
#ex 4 8 4x1 1x6 1 3 3x1 1x3 1 3 6x1 1x4

#x could be capitilized
