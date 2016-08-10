# here's what im working on for the new one... no comments yet...
from numpy import prod


def makeRowList():
    posOne = [1,2,3,4,5,6]
    rows = []
    for i in posOne:
        posTwo = list(posOne)
        posTwo.remove(i)
        for j in posTwo:
            posThree = list(posTwo)
            posThree.remove(j)
            for k in posThree:
                posFour = list(posThree)
                posFour.remove(k)
                for l in posFour:
                    posFive = list(posFour)
                    posFive.remove(l)
                    for m in posFive:
                        posSix = list(posFive)
                        posSix.remove(m)
                        rows += [[i,j,k,l,m,posSix[0]]]
    return rows
    

def listToInt(list):
    list = map(str,list)  
    list = ''.join(list)
    return int(list)    
   
    
def validPair(firstRow, secondRow):
    for i in range(len(firstRow)):
        if firstRow[i] == secondRow[i]:
            return False
    return True
            
    
    
def makeRowDict():
    rowList = makeRowList()
    rowDict = {}
    for firstRow in rowList:
        intFirstRow = listToInt(firstRow)
        rowDict[intFirstRow] = []
        for secondRow in rowList:
            if validPair(firstRow, secondRow):
                rowDict[intFirstRow] += [secondRow]
        
    return rowDict

def intersectList(list1, list2):
    outList = []
    for i in list1:
        if i in list2:
            outList += [i]
    return outList
    

    

def dictMakeSquares():
    rowList = makeRowList()
    rowDict = makeRowDict()
    squareList = []
    for firstRow in rowList:
        print firstRow
        secondRowList = rowDict[listToInt(firstRow)]
        for secondRow in secondRowList:
            thirdRowList = intersectList(secondRowList, rowDict[listToInt(secondRow)])
            for thirdRow in thirdRowList:
                fourthRowList = intersectList(thirdRowList, rowDict[listToInt(thirdRow)])
                for fourthRow in fourthRowList:
                    fifthRowList = intersectList(fourthRowList, rowDict[listToInt(fourthRow)])
                    for fifthRow in fifthRowList:
                        sixthRowList = intersectList(fifthRowList, rowDict[listToInt(fifthRow)])
                        for sixthRow in sixthRowList:
                            squareList += [firstRow, secondRow, thirdRow, fourthRow, fifthRow, sixthRow]
        print len(squareList)
        print squareList
        
    return squareList
test = dictMakeSquares()
