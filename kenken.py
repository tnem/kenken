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

# This function makes a list of all of the valid rows, e.g, all permutations of
# digits 1-4 (used once each).

def makeRowList():
    posOne = [1,2,3,4]
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
                rows += [[i,j,k,posFour[0]]]
    return rows
    
# This funtion tests if a list of rows is valid, e.g., if there are any repeated 
# digits in any of the columns.  It returns true if the list of rows is invalid 
# and false if the list is valid. (backwards, I know)

def invalidRows(rows):
    for i in range(len(rows[0])):
        col = [item[i] for item in rows]
        if len(col) != len(set(col)):
            return True
    return False
    
# this  function returns a list of all of the possible valid squares, e.g.,
# the combinations of 4 rows which have all 4 numbers in each column
    
def makeSquares():
    squares = []
    rows = makeRowList()
    for i in rows:
        secondRows = list(rows)
        secondRows.remove(i)
        for j in secondRows:
            if invalidRows([i,j]):
                continue
            thirdRows = list(secondRows)
            thirdRows.remove(j)
            for k in thirdRows:
                if invalidRows([i,j,k]):
                    continue
                fourthRows = list(thirdRows)
                fourthRows.remove(k)
                for l in fourthRows:
                    if invalidRows([i,j,k,l]):
                        continue
                    squares += [[i,j,k,l]]
    return squares

def plus(vals):
    return [sum(vals)]

def sub(vals):
    return [abs(vals[0] - vals[1])]

def mul(vals):
    return [prod(vals)]

def div(vals):
    return [vals[0] / float(vals[1]), vals[1] / float(vals[0])]

opSwitch = {'a' : plus,
            's' : sub,
            'm' : mul,
            'd' : div}

# Now we get to the part which deals with the regions.  This is a class for 
# defining each region, which includes the cells that are in the region, the operation
# and the target solution to the operation.    
                
class Region:
    def __init__(self, cells, operation, answer):
        self.cells = cells
        self.operation = opSwitch[operation]
        self.answer = answer
        
    def isValid(self, square):
        if self.answer in self.operation(extractVals(square, self.cells)):
            return True
        return False


# A simple funciton to print the square nicely.

def printSquare(square):
    print square
    for row in square:
        for cell in range(len(row)):
            row[cell] = str(row[cell]) 
        print ' '.join(row) 
        
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
            
            
# This function just returns a list of values at given coordinates in a square
    
def extractVals(square, cells):
    vals = []
    for cell in cells:
        #print cell, type(cell)
        #print square
        vals += [square[cell[0]][cell[1]]]
    return vals
    
# This function takes a dictionary of regions and a square and tests all of them to 
# see if that square is a valid solution.
  
def checkRegions(square, regionDict):
    for region in regionDict:
        if not regionDict[region].isValid(square):
            return False
    return True


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
    regSquare = info[0:4]
    info = info[4:]
    regionDict = fileRegionList(regSquare, info)
    #printRegionList(regionDict)
    return regionDict
    
    
# this function ties everything together. Currently it pulls all of the region info
# from a file (test3.txt), makes a list of all possible squares, and then checks to 
# see if each square solves the puzzle.  It then prints all of the winning squares.
   
#def solvePuzzle():
regionDict = getFileInfo('test3.txt')
squares = makeSquares()
winSquares = []
for square in squares:
    if checkRegions(square, regionDict):
        winSquares    += [square]
print "the winning squares are:"  
for i in winSquares:
    printSquare(i)

#easySquare = 
        
#solvePuzzle()     
  
