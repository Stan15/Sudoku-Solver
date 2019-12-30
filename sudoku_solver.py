import copy, random, time

def boxCenter(row, col):
    coords=[1,4,7]  #all permutations of this is are all the center cells of the 9 boxes in the grid
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if ((row+i) in coords) and ((col+j) in coords): #making a 3x3 cell square around the current row,col. only one cell in this square is a center cell.
                return [row+i, col+j]

def cellSpaces(sudoku):
    cells=[]
    for i in range(len(sudoku)):
        for j in range(len(sudoku)):
            if sudoku[i][j] == 0:
                cells.append([i, j, 0]) #zero is the state of the cell, empty.
    return cells

def validNums(sudoku, row, col):
    invalid=[]
    for i in range(len(sudoku)):
        for j in range(len(sudoku)):
            invalid.append(sudoku[row][j])
            invalid.append(sudoku[i][col])

    centerRow, centerCol = boxCenter(row, col)
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            invalid.append(sudoku[centerRow+i][centerCol+j])

    invalid = list(filter(lambda a: a != 0, invalid))   #filter empty spaces
    invalid = set(invalid)
    valid = list({1,2,3,4,5,6,7,8,9} - invalid)

    return valid

count=0
def solve(sudoku, steps=False, both=False):
    global count
    
    if both:
        steps=True

    sudokuSol=copy.deepcopy(sudoku)
    spaces=cellSpaces(sudokuSol)
    numberpool=[None]*(len(spaces))
    actions=[]

    
    def solveNext(): 
        global count
        row=spaces[count][0]                                                      #the index of the current space to be filled
        col=spaces[count][1]

        numberpool[count]=validNums(sudokuSol, row, col)
        while numberpool[count]!=[] and spaces[-1][2]==0:
            numIndex=random.randint(0,len(numberpool[count])-1)
            finalNum=numberpool[count][numIndex]   #choose the numIndex-th valid number for the current cell
            sudokuSol[row][col]=finalNum
            spaces[count][2]=1        #change cell state to filled
            numberpool[count].pop(numIndex)        #remove that chosen number from the numberpool

            if count<len(spaces)-1:         #don't add to count if count is at its maximum value(if at the last space to be filled)
                count+=1
            if steps:
                actions.append(["+", row, col, finalNum])
            
            solveNext()

        if numberpool[count]==[] and spaces[-1][2]==0:      #if there is no other possible number for this cell and the last cellSpace is empty(sudoku is not already solved)
            count-=1
            row=spaces[count][0]
            col=spaces[count][1]
            sudokuSol[row][col]=0
            spaces[count][2]=0        #change cell state to unfilled
            
            if steps:
                actions.append(["-", row, col])
            

    solveNext()
    #when finished solving, do these.
    actions.append("finished")
    count=0
    
    if both:
        return sudokuSol, actions
    elif steps:
        return actions
    else:
        return sudokuSol
    

# autoSol=[[1, 0, 0, 0, 9, 2, 0, 0, 7],
#          [4, 5, 0, 0, 0, 7, 1, 0, 0], 
#          [2, 0, 0, 8, 0, 4, 0, 5, 0], 
#          [0, 0, 4, 0, 3, 0, 0, 9, 0], 
#          [0, 2, 0, 0, 0, 0, 0, 6, 0], 
#          [0, 0, 0, 0, 2, 0, 0, 0, 0], 
#          [0, 9, 0, 2, 0, 0, 0, 1, 8], 
#          [5, 0, 0, 0, 0, 1, 3, 0, 9], 
#          [8, 1, 6, 0, 0, 0, 5, 0, 0]]

# start=time.time()
# sudokuSol, actions = solve(autoSol, both=True)
# end=time.time()
# for i in sudokuSol:
#     print(i)
# print("solved in {} seconds. {} steps taken".format(end-start, len(actions)))
