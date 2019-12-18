sudoku=[[1, 0, 0, 0, 9, 2, 0, 0, 7],
        [4, 5, 0, 0, 0, 7, 1, 0, 0],
        [2, 0, 0, 8, 0, 4, 0, 5, 0],
        [0, 0, 4, 0, 3, 0, 0, 9, 0],
        [0, 2, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 9, 0, 2, 0, 0, 0, 1, 8],
        [5, 0, 0, 0, 0, 1, 3, 0, 9],
        [8, 1, 6, 0, 0, 0, 5, 0, 0]]

if len(sudoku) != len(sudoku[1]):
    print("sudoku grid size error")
    

#---------------choosing the entry which is central to the square which the current entry is in------------
coords = [1, 4, 7]                                   #all permutations of coords make up all the square centers entries in the sudoku. ie(row 1 col 1, row 4 col 7, ...etc)


def squarecenter(i, j):      
    
    if (i in coords) and (j in coords):              #the current entry (is the square_center the current entry?)       
        square_centre = [i, j]
    elif (i-1 in coords) and (j in coords):          #top (is the square_center the entry to the top of the current entry?)
        square_centre = [i-1, j]
    elif (i-1 in coords) and (j-1 in coords):        #top left ^^
        square_centre = [i-1, j-1]
    elif (i-1 in coords) and (j+1 in coords):        #top right ^^
        square_centre = [i-1, j+1]
    elif (i in coords) and (j-1 in coords):          #left ^^
        square_centre = [i, j-1]
    elif (i in coords) and (j+1 in coords):          #right ^^
        square_centre = [i, j+1]
    elif (i+1 in coords) and (j in coords):          #bottom ^^
        square_centre = [i+1, j]
    elif (i+1 in coords) and (j-1 in coords):        ##bottom left ^^
        square_centre = [i+1, j-1]
    elif (i+1 in coords) and (j+1 in coords):        #bottom right ^^
        square_centre = [i+1, j+1]
    
    return square_centre
#-----------------------------------------------------------------------------------------------------------

#---------------------what numbers can not be selected for a given row and column?--------------------------
def valid_nums(row, col):
    invalid_numbers=[]
    #----number to be chosen cannot be the same as a number in the square---------
    i = squarecenter(row, col)
    j=i[1]          #index of square center 
    i=i[0]
    invalid_numbers.append(sudoku[i-1][j-1])
    invalid_numbers.append(sudoku[i-1][j])
    invalid_numbers.append(sudoku[i-1][j+1])
    invalid_numbers.append(sudoku[i][j-1])
    invalid_numbers.append(sudoku[i][j])
    invalid_numbers.append(sudoku[i][j+1])
    invalid_numbers.append(sudoku[i+1][j-1])
    invalid_numbers.append(sudoku[i+1][j])
    invalid_numbers.append(sudoku[i+1][j+1])

    #----number to be chosen cannot be the same as a number in its row or column---
    for k in range(len(sudoku)):
        invalid_numbers.append(sudoku[row][k]) 
        invalid_numbers.append(sudoku[k][col])

    #remove 0's and repeated numbers from invalid numbers
    invalid_numbers = list(filter(lambda a: a != 0, invalid_numbers))
    invalid_numbers = set(invalid_numbers)
    
    #numbers that CAN be chosen from
    valid_numbers = list({1, 2, 3, 4, 5, 6, 7, 8, 9} - invalid_numbers)

    return valid_numbers
    

#selecting all sudoku spaces to be filled
spaces=[]
for i in range(len(sudoku)):
    for j in range(len(sudoku)):
        if sudoku[i][j] == 0:
            spaces.append([i, j, 0]) # [row, col, state] 0 indicates it is unfilled, 1 indicates that it is filled.
print(spaces)

count=0    #
numberpool=[None]*(len(spaces))      #stores the possible numbers for each space, so its size is the number of spaces

def solve():
    global count, numberpool, spaces

    i=spaces[count][0]  #the index of the current space to be filled
    j=spaces[count][1]


    numberpool[count]=valid_nums(i, j)      #when filling a new space, the possible valid numbers to choose from are stored in the 2d array for each number that has to be chosen
    while len(numberpool[count])!=0 and spaces[len(spaces)-1][2]==0:        #while there are still possible numbers to choose from for the current space, and the very last space is unfilled, continue to execute   
        finalnum=numberpool[count][0]       #set finalnum to the first possible number
        print("row:{}, col:{}, num:{}".format(i, j, finalnum))
        sudoku[i][j]=finalnum
        spaces[count][2]=1                   #setting state to 1 (filled)
        numberpool[count].pop(numberpool[count].index(finalnum)) #removing tried numbers from the list of possible number
        if count<len(spaces)-1:             #to prevent overshooting after it reaches the size of the number of spaces
            count+=1
        solve()
        
    if len(numberpool[count])==0 and spaces[len(spaces)-1][2]==0:       #<--on fail, execute. go back to previous space when there are no other possible number to choose from in the current space and the very last space isn't filled.
        sudoku[i][j]=0                  #set the sudoku space back to 0 ("empty" or "blank") before backtracking
        spaces[count][2]=0              #set state to 0 (unfilled) before backtracking
        count-=1                        



solve()
print(sudoku)
    
            
# for i in range(len(sudoku)):
#     for j in range(len(sudoku)): #since square matrix, column size = row size