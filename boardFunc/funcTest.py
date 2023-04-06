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
    # with the colNumber and rowNumber, we can find the 8 neighbors without a for loop
    upperbound = len(matrix) - 1
    lowerbound = 0
    # check if the rowNumber is not the upperbound
    if rowNumber != upperbound:
        # if the rowNumber is not the upperbound, then we can add the rowNumber + 1 to the result
        result.append((colNumber, rowNumber + 1))
        # check if the colNumber is not the upperbound
        if colNumber != upperbound:
            # if the colNumber is not the upperbound, then we can add the colNumber + 1 to the result
            result.append((colNumber + 1, rowNumber + 1))
        # check if the colNumber is not the lowerbound
        if colNumber != lowerbound:
            # if the colNumber is not the lowerbound, then we can add the colNumber - 1 to the result
            result.append((colNumber - 1, rowNumber + 1))
    # check if the rowNumber is not the lowerbound
    if rowNumber != lowerbound:
        # if the rowNumber is not the lowerbound, then we can add the rowNumber - 1 to the result
        result.append((colNumber, rowNumber - 1))
        # check if the colNumber is not the upperbound
        if colNumber != upperbound:
            # if the colNumber is not the upperbound, then we can add the colNumber + 1 to the result
            result.append((colNumber + 1, rowNumber - 1))
        # check if the colNumber is not the lowerbound
        if colNumber != lowerbound:
            # if the colNumber is not the lowerbound, then we can add the colNumber - 1 to the result
            result.append((colNumber - 1, rowNumber - 1))
            # check if the colNumber is not the upperbound
    if colNumber != upperbound:
        # if the colNumber is not the upperbound, then we can add the colNumber + 1 to the result
        result.append((colNumber + 1, rowNumber))   
    # check if the colNumber is not the lowerbound
    if colNumber != lowerbound:
        # if the colNumber is not the lowerbound, then we can add the colNumber - 1 to the result
        result.append((colNumber - 1, rowNumber))
    return result

def arrayMap(i, width):
    x = i % width;    # the remainder of i / width
    y = i // width;    # // is floor division
    return x,y

def checkWin(board, N,offcolor=(250,250,250)):
        flatlist = sum(board, [])
        #print(flatlist)
        buttColorList = []
        for i in range(len(flatlist)):
            buttColorList.insert(i,flatlist[i])
        # check logical board against win condition, in this case if the board is empty
        if buttColorList == [offcolor]*(N**2):
            return True