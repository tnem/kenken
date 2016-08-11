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
    
incount = 0

def invalidRows(rows):
    global incount
    incount += 1
    for i in range(len(rows[0])):
        col = [item[i] for item in rows]
        #if incount %1000 == 0: print incount, rows, i, col
        if len(col) != len(set(col)):
            return True
    return False
    
def goodRowList(curRows, nextRows):
    goodRows = []
    for i in nextRows:
        if invalidRows(curRows + [i]):
            continue
        else: goodRows += [i]
        
    return goodRows
    
    
def printSquare(square):
    #print square 
    if type(square[0][0]) == int:
        for row in square:
            for cell in row:
                print cell,
            print
    if type (square[0][0]) == str:
        for row in square:
            print ' '.join(row) 
        
    
    
def makeSquares():
    global incount
    squares = []
    cycles = 0
    rows = makeRowList()
    for i in rows:
        cycles += 1
        print "cycle:", cycles, "there are",len(squares),"squares"
        #if cycles > 2: break
        secondRows = goodRowList([i], rows)
#        print "second", len(secondRows)
        for j in secondRows:
            thirdRows = goodRowList([i,j], secondRows)
#            print "third", len(thirdRows), incount
            for k in thirdRows:
                fourthRows = goodRowList([i,j,k], thirdRows)
#                print "4th", len(fourthRows), fourthRows
                for l in fourthRows:
                    fifthRows = goodRowList([i,j,k,l] , fourthRows)
#                    print "5th", len(fifthRows) , incount
                    for m in fifthRows:
                        sixthRows = goodRowList([i,j,k,l,m],  fifthRows)
#                        print "6th", len(sixthRows), incount             
                        for n in sixthRows:
                            if invalidRows([i,j,k,l,m,n]):
                                continue                            
                            squares += [[i,j,k,l,m,n]]
                            
    return squares

#makeSquares() 
                
class Region:
     def __init__(self, cells, operation, answer):
         self.cells = cells
         self.operation = operation
         self.answer = answer         




        
        
def makeRegionList(regSquare):
    regionDict = {}
    for row in range(len(regSquare)):
        for col in range(len(regSquare[row])):  
            curRegNum = regSquare[row][col]
            if curRegNum not in regionDict:
                operation = raw_input("what is the operation for region " + str( curRegNum)+ "?   ")
                answer = int(raw_input("what is the total for region " + str( curRegNum) + "?   "))
                regionDict[curRegNum] = Region([[row, col]], operation, answer)
            else:
                regionDict[curRegNum].cells += [[row,col]]
                
    return regionDict
    
    
                          
def printRegionList(regionDict):
    for region in regionDict:
        print "\nRegion", region
        print "cells in region:", regionDict[region].cells
        print "Operation:", regionDict[region].operation
        print "Result:", regionDict[region].answer
        
         
def getRegions():
    print "lets define the regions"
    regSquare = [['*']*4 for i in range(4)]
    for row in range(len(regSquare)):
        for col in range(len(regSquare[row])):
            regSquare[row][col] = 'X'
            printSquare(regSquare)
            regSquare[row][col] = raw_input("for this one (X)?  ")
    while(True):
        print "\nthe regions are defined as:"
        printSquare(regSquare)
        if raw_input("is this correct? (y/n)  ") == 'y':
            return regSquare
        else:
            coords = raw_input("enter the coordinates of the region which is incorrect  ")
            newreg = raw_input("enter the correct region number  ")
            coords = list(coords.replace(" ",""))
            coords = [int(i) for i in coords]
            regSquare[coords[0]][coords[1]] = newreg
            
            
    
def testRegionAddMul(squareVals, operation, answer):
    #print "add check", squareVals, operation, answer, sum(squareVals) == answer, sum(squareVals) == 20
    if operation == 'a' and sum(squareVals) == answer:
        #print "returning true"
        return True
    if operation == 'm' and prod(squareVals) == answer: 
        #print "returning true"
        return True
    else: return False

def testRegionSub(squareVals, answer):
    if abs(squareVals[0] - squareVals[1]) == answer:
        return True
    else: return False

def testRegionDev(squareVals, answer):
    if squareVals[0]/float(squareVals[1]) == answer:
        return True
    if squareVals[1]/float(squareVals[0]) == answer:
        return True
    else: return False
    
def extractVals(square, cells):
    vals = []
    for cell in cells:
        #print cell, type(cell)
        #print square
        vals += [square[cell[0]][cell[1]]]
    return vals
    
def checkRegions(square, regionDict):
    for region in regionDict:
        test = True
        squarevals = extractVals(square, regionDict[region].cells)
        if regionDict[region].operation == 'a' or regionDict[region].operation == 'm':
            test = testRegionAddMul(squarevals, regionDict[region].operation, regionDict[region].answer)
            #if test: print test, squarevals, regionDict[region].operation, regionDict[region].answer
        elif regionDict[region].operation == 'd':
            test = testRegionDev(squarevals, regionDict[region].answer) 
            #if test: print test, squarevals, regionDict[region].operation, regionDict[region].answer
        elif regionDict[region].operation == 's':
            test = testRegionSub(squarevals, regionDict[region].answer)
            #if test: print test, squarevals, regionDict[region].operation, regionDict[region].answer
        if test == False:
            return False
    else :
        return True

    
def getUserInfo():               
    regSquare = getRegions()                
    regionDict = makeRegionList(regSquare)
    printRegionList(regionDict)
    return regionDict
    
def fileRegionList(regSquare, info):
    regionDict = {}
    for i in range(len(info)/3):
        currentRegion = info[3*i : 3*i + 3]
        curRegNum = currentRegion[0]
        operation = currentRegion [1]
        answer = int(currentRegion[2])
        regionDict[curRegNum] = Region([], operation, answer)
               
    for row in range(len(regSquare)):
        for col in range(len(regSquare[row])):  
            curRegNum = regSquare[row][col]
            if curRegNum not in regionDict:
                print "error "
            else:
                regionDict[curRegNum].cells += [[row,col]]
                
    return regionDict
    
def getFileInfo(filename):
    fi = open(filename,'r')
    info = fi.read()
    info = info.split()
    regSquare = info[0:4]
    info = info[4:]
    regionDict = fileRegionList(regSquare, info)
    printRegionList(regionDict)
    return regionDict
    
    
                    
def solvePuzzle():
    regionDict = getFileInfo('test3.txt')
    squares = makeSquares()
    winSquares = []
    for square in squares:
        if checkRegions(square, regionDict):
            winSquares    += [square]
    print "the winning squares are:"  
    for i in winSquares:
        printSquare(i)
        
                    
#def checkRegions(regions, operations, answers)
    
#k = makeSquares()
#print len(k)
#for i in k:
#    print
#    for j in i:
#        print j

