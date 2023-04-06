#!/usr/bin/python3
#
#  Author:      Cameron Kerley (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#  Date:        6 June 2022
#  License:     MIT License
#  description:: functions for 8 neighbor adjacency algorithm, and methods for converting between linier matrix and 2D array.
#----------------------------------------------------------------------------------------------------------------------
#  Disclosure:  This code is public domain. You can use it in any way you want. 
#               However, i am scanning github repos for this code that does not include credit to me. 
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
#----------------------------------------------------------------------------------------------------------------------

# sudo code that helped write this function was found here: https://stackoverflow.com/a/652123
def eight_neighbors_adj(matrix, colNumber, rowNumber):
    result = []

    for colAdd in range(-1, 2):
        newCol = colNumber + colAdd
        if newCol >= 0 and newCol <= len(matrix)-1:
            for rowAdd in range(-1, 2):
                newRow = rowNumber + rowAdd
                if newRow >= 0 and newRow <= len(matrix)-1:
                    if newCol == colNumber and newRow == rowNumber:
                        continue
                    result.append((newCol,newRow))
    
    return result

def arrayMap(i, width):
    x = i % width;    # the remainder of i / width
    y = i // width;    # // is floor division
    return x,y

def checkWin(board, N):
        flatlist = sum(board, [])
        #print(flatlist)
        buttColorList = []
        for i in range(len(flatlist)):
            buttColorList.insert(i,flatlist[i])
        # check logical board against win condition, in this case if the board is empty
        if buttColorList == [(250,250,250)]*(N**2):
            return True