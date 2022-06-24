def neighbors(matrix, rowNumber, colNumber):
    result = []
    # search the grid by the cords given 
    for rowAdd in range(-1, 2):
        newRow = rowNumber + rowAdd
        if newRow >= 0 and newRow <= len(matrix)-1:
            for colAdd in range(-1, 2):
                newCol = colNumber + colAdd
                if newCol >= 0 and newCol <= len(matrix)-1:
                    if newCol == colNumber and newRow == rowNumber:
                        continue
                    result.append((newRow,newCol))
    
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