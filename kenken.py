# This is a program to solve a 4 by 4 KenKen puzzle.

# The goal of the puzzle is to fill a square with numbers 1-4, with each row
# and column having all numbers occuring once.  There are also regions which 
# have a defined operation (addition subtraction multiplication or division),
# and a defined answer.  The numbers in this region have to result in this number
# when you do the defined operation.  For more, google kenken or check out the wiki
# at https://en.wikipedia.org/wiki/KenKen

# This one uses the easier 4 by 4 puzzle, and a simpler method, which turns out 
# to be too slow for the more complecated 6 by 6.  This one works however, so it 
# is a useful place to start.

  
from numpy import prod
import itertools
import copy

def permute(xs, count=None):
    return list(itertools.permutations(xs,count))

def add(vals):
    return [sum(vals)]

def sub(vals):
    return [abs(vals[0] - vals[1])]

def mul(vals):
    return [prod(vals)]

def div(vals):
    return [vals[0] / float(vals[1]), vals[1] / float(vals[0])]

opSwitch = {'a' : add,
            's' : sub,
            'm' : mul,
            'd' : div}

def flatten(xs):
    return [item for sublist in xs for item in sublist]

def newSquare(maxSize):
    return [[0 for x in range(maxSize)] for i in range(maxSize)]

# Now we get to the part which deals with the regions.  This is a class for 
# defining each region, which includes the cells that are in the region, the operation
# and the target solution to the operation.    
                
class Region:
    def __init__(self, cells, operation, answer):
        self.cells = cells
        self.operation = opSwitch[operation]
        self.answer = answer
        
    def hasCorner(self):
        xSet = {x[0] for x in self.cells}
        ySet = {x[1] for x in self.cells}

        if len(xSet) > 1 and len(ySet) > 1:
            return True
        
        return False
    
    # Attempts to find all possible inputs to get answer for operation op across numFields fields.
    # Needs the maxSize of the puzzle because an n-wide puzzle only has digits 1 through n
    # in the future should determine how many of the same digit a region can have
    def possibleAnswers(self, maxSize):
        numPool = range(1, maxSize + 1)
        
        if self.hasCorner(): # in this case we can have 2 of the same digit
            numPool *= 2
            
        availableSets = permute(numPool, len(self.cells))
        workableSets = [x for x in availableSets if self.answer in self.operation(x)]
        
        return workableSets

    # Creates a list of 'partial squares', ex. a square that is all 0s except for the parts this region controls.
    def makeSquareSections(self, maxSize):
        squareList = []

        for answerList in self.possibleAnswers(maxSize):
            square = newSquare(maxSize)
            
            for ndx, answer in enumerate(answerList):
                square[self.cells[ndx][0]][self.cells[ndx][1]] = answer

            squareList.append(square)

        return squareList

def addArrays(arrs):
    return tuple([sum(x) for x in zip(*arrs)])
    
def addSquares(squares):
    return tuple([addArrays(xs) for xs in zip(*squares)])
    
def squareIsValidHoriz(square):
    for idx, row in enumerate(square):
        temp = []
        for item in row:
            if item in temp and item != 0:
                return False
            else:
                temp.append(item)

    return True

def squareIsValid(square):
    # test horizontal
    validHoriz = squareIsValidHoriz(square)

    rotSquare = zip(*square[::-1])
    validVert = squareIsValidHoriz(rotSquare)

    return validHoriz and validVert

## This is kind of the opposite approach of the original scheme.
## We create only valid regions, and then just check to see if they are
## valid squares.
def makeSquareList(maxSize, regions):
    endSquares = regions[0].makeSquareSections(maxSize)

    for region in regions[1:]:
        newSquares = set()
        
        for esquare in endSquares:
            #print "in esquare" + str(esquare)
            for nsquare in region.makeSquareSections(maxSize):
                testSquare = addSquares([esquare, nsquare])

                if squareIsValid(testSquare):
                    newSquares.add(testSquare)

        endSquares = newSquares
                    
    return endSquares
                    
                

# A simple funciton to print the square nicely.

def printSquare(square):
    print square

    for row in square:
        print ' '.join(map(str, row))
    
# this function takes  the list of regions from the user, gets the operations
# and solutions and returns everything as a 
# dictionary of instances of the Region class.      
        
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
    
# This is a function to print the dictionary of regions.    
                          
def printRegionList(regionDict):
    for region in regionDict:
        print "\nRegion", region
        print "cells in region:", regionDict[region].cells
        print "Operation:", regionDict[region].operation
        print "Result:", regionDict[region].answer
    
# This function has the user define where the regions are on the puzzle.         
def getRegions(puzzleSize):
    print "lets define the regions"
    regSquare = [['*'] * puzzleSize for i in range(puzzleSize)]
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
            
            
# This function calls all of the user prompting functions and returns the final
# region dictionary, after printing it    

def getUserInfo():               
    regSquare = getRegions()                
    regionDict = makeRegionList(regSquare)
    printRegionList(regionDict)
    return regionDict
    
    
# this function pulls the region definitions from text gotten from a file instead.  
# Much easier for debuging etc.  Returns a region dictionary

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
    
# Here is where the actual file operations are handled.
    
def getFileInfo(filename):
    fi = open(filename,'r')
    info = fi.read()
    info = info.split()
    puzzleSize = int(info[0])
    regSquare = info[1:puzzleSize + 1]
    info = info[puzzleSize + 1:]
    regionDict = fileRegionList(regSquare, info)
    #printRegionList(regionDict)
    return regionDict,puzzleSize
    
    
# this function ties everything together. Currently it pulls all of the region info
# from a file (test3.txt), makes a list of all possible squares, and then checks to 
# see if each square solves the puzzle.  It then prints all of the winning squares.
   
def solvePuzzle():
    regionDict, puzzleSize = getFileInfo('test3.txt')
    regionList = [regionDict[x] for x in regionDict]

    winSquares = makeSquareList(puzzleSize, regionList)

    print "the winning squares are:"  
    for i in winSquares:
        printSquare(i)

    return regionList

regionList = solvePuzzle()     
  
