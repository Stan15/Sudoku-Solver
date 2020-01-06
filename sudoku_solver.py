import copy, random, time

def boxCoords(row, col):
    boxRow = 3*(row//3)
    boxCol = 3*(col//3)
    return boxRow, boxCol

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
        if sudoku[i][col]!=0:
            invalid.append(sudoku[i][col])
        if sudoku[row][i]!=0:
            invalid.append(sudoku[row][i])

    boxRow, boxCol = boxCoords(row, col)
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if not(boxRow+i==row or boxCol+j==col):
                num=sudoku[boxRow+i][boxCol+j]
                if num!=0:
                    invalid.append(num)

    valid = list({1,2,3,4,5,6,7,8,9} - set(invalid))
    return valid

count=0
def solve(sudoku, steps=False, both=False):
    global count
    
    if both:
        steps=True

    sudokuSol=copy.deepcopy(sudoku)
    spaces=cellSpaces(sudokuSol)
    valid=[None]*(len(spaces))
    actions=[]

    
    def solveNext(): 
        global count
        row=spaces[count][0]               #the index of the current space to be filled
        col=spaces[count][1]

        valid[count]=validNums(sudokuSol, row, col)
        while valid[count]!=[]:
            numIndex=random.randint(0,len(valid[count])-1)
            finalNum=valid[count][numIndex]   #choose the numIndex-th valid number for the current cell
            sudokuSol[row][col]=finalNum
            spaces[count][2]=1        #change cell state to filled
            valid[count].pop(numIndex)        #remove that chosen number from the valid

            if count<len(spaces)-1:         #don't add to count if count is at its maximum value(if at the last space to be filled)
                count+=1
            if steps:
                actions.append(["+", row, col, finalNum])
            
            solveNext()

        if valid[count]==[] and spaces[-1][2]==0:      #if there is no other possible number for this cell and the last cellSpace is empty(sudoku is not already solved)
            count-=1
            sudokuSol[row][col]=0
            spaces[count][2]=0        #change cell state to unfilled
            
            if steps:
                actions.append(["-", row, col])
            

    solveNext()
    #when finished solving, do this.
    count=0
    
    if both:
        return sudokuSol, actions
    elif steps:
        return actions
    else:
        return sudokuSol
    

test=[[1, 0, 0, 0, 9, 2, 0, 0, 7],
     [4, 5, 0, 0, 0, 7, 1, 0, 0], 
     [2, 0, 0, 8, 0, 4, 0, 5, 0], 
     [0, 0, 4, 0, 3, 0, 0, 9, 0], 
     [0, 2, 0, 0, 0, 0, 0, 6, 0], 
     [0, 0, 0, 0, 2, 0, 0, 0, 0], 
     [0, 9, 0, 2, 0, 0, 0, 1, 8], 
     [5, 0, 0, 0, 0, 1, 3, 0, 9], 
     [8, 1, 6, 0, 0, 0, 5, 0, 0]]

#-----------------------Run time and step count---------------------------------
# start=time.time()
# sudokuSol, actions = solve(test, both=True)
# end=time.time()
# for i in sudokuSol:
#     print(i)
# print("solved in {} seconds. {} steps taken".format(end-start, len(actions)))
# -------------------------------------------------------------------------------

#----------------------------Average Time-----------------------------
# times=[]
# def runner():
#     start=time.time()
#     solve(test)
#     end=time.time()
#     times.append(end-start)

# for i in range(1000):
#     runner()

# print(times)
# print("Average time is: {} seconds".format(sum(times)/len(times)))
#----------------------------------------------------------------------
