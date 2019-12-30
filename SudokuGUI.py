import pygame, math, copy
from solve_sudoku import solve
from sudoku_maker import makeNew

sudokuQ=makeNew()

userSol=copy.deepcopy(sudokuQ)  #replace with newGame
autoSol=copy.deepcopy(sudokuQ)
sudokuAns = solve(sudokuQ)


pygame.init()
clock = pygame.time.Clock()

win_width, win_height = 650, 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Sudoku")

boardH, boardW = 500, 500

buttonWtoHatio= 379/190
buttonH=50
buttonW = int(buttonH*buttonWtoHatio)

peekOn = pygame.transform.scale(pygame.image.load("buttons/peek1.png"), (buttonW,buttonH))
peekOff = pygame.transform.scale(pygame.image.load("buttons/peek0.png"), (buttonW,buttonH))
solveOn = pygame.transform.scale(pygame.image.load("buttons/solve1.png"), (buttonW,buttonH))
solveOff = pygame.transform.scale(pygame.image.load("buttons/solve0.png"), (buttonW,buttonH)) 
newOn = pygame.transform.scale(pygame.image.load("buttons/new1.png"), (buttonW,buttonH))
newOff = pygame.transform.scale(pygame.image.load("buttons/new0.png"), (buttonW,buttonH)) 
buttons = {"new":[boardW+20, 20], "peek":[boardW+20, buttonH+80], "solve":[boardW+20, 2*buttonH+100]}    #x and y coords to place each button


gap=boardH/9

def grid():
    for i in range(10):
        if i in [0,3,6,9]:
            thick=3
        else:
            thick=1
        pygame.draw.line(win, (0,0,0), (int(i*gap), 0), (int(i*gap), boardH), thick)
        pygame.draw.line(win, (0,0,0), (0, int(i*gap)), (boardH, int(i*gap)), thick)

def newGame():
    global sudokuQ, userSol, autoSol, sudokuAns, selected, peeking, solving, temp
    sudokuQ=makeNew()
    userSol=copy.deepcopy(sudokuQ)
    autoSol=copy.deepcopy(sudokuQ)
    sudokuAns = solve(sudokuQ)
    

    selected=False
    peeking=False
    solving=[False, 0]  #first value is for the solve button, second is for making it only solve once
    temp=[]

def QuestionNums(sudoku):
    for i in range(len(sudoku)):   
        for j in range(len(sudoku)):
            if sudoku[i][j] != 0:   #displaying numbers from question
                permNumRender(sudoku[i][j], i, j)

def permNumRender(num, row, col):
    x=(col*gap)+(gap//2)
    y=(row*gap)+(gap//2)
    FONT = pygame.font.SysFont('freesansbold.ttf',50)
    text=FONT.render(str(num), 1, (0,0,0))
    win.blit(text, (int(x-8),int(y-14)))

def tempNumRender(num, row, col):
    x=(col*gap)+(gap//2)
    y=(row*gap)+(gap//2)
    FONT = pygame.font.SysFont('freesansbold.ttf',30)
    text=FONT.render(str(num), 1, (100,100,100))
    win.blit(text, (x+10,y+5))

def permInput(boardRow, boardCol):
    if selected:            
        for i in temp:
            if i[0]==boardRow and i[1]==boardCol:
                userSol[boardRow][boardCol]=i[2]
                temp.pop(temp.index(i))

def tempInput(num, boardRow, boardCol):
    if selected and userSol[boardRow][boardCol] == 0:
        for i in temp:
            if i[0]==boardRow and i[1]==boardCol:
                temp.pop(temp.index(i)) #remove previous temporary entry to current cell
        temp.append([boardRow, boardCol, num])

def tempDelete(boardRow, boardCol):
    for i in temp:
        if i[0]==boardRow and i[1]==boardCol:
            temp.pop(temp.index(i))

def peek():
    for i in temp:
        row=i[0]
        col=i[1]
        if i[2] == sudokuAns[row][col]:
            pygame.draw.rect(win, (0,255,0), [col*gap, row*gap, gap, gap], 4)
        else:
            pygame.draw.rect(win, (255,0,0), [col*gap, row*gap, gap, gap], 4)

def select(Row, Col):
    pygame.draw.rect(win, (0,0,255), [Col*gap, Row*gap, gap, gap], 4)

def selLeft(Row, Col):
    global boardRow, boardCol
    if Row==0 and Col==0:
        pass
    elif Col==0:
        boardRow-=1
        boardCol=8
    else:
        boardCol-=1

def selRight(Row, Col):
    global boardRow, boardCol
    if Col==8 and Row==8:
        pass
    elif Col==8:
        boardRow=boardRow+1
        boardCol=0
    else:
        boardCol=boardCol+1
def selUp(Row, Col):
    global boardRow, boardCol
    if Row>0:
        boardRow-=1

def selDown(Row, Col):
    global boardRow, boardCol
    if Row<8:
        boardRow+=1

def solveBoard():
    global temp
    if solving[1]==0:
        solving[1]=1        #to make it solve only once until solving[1] is set back to 0
        temp=[]
        QuestionNums(autoSol)
        pygame.display.update()

        actions=solve(autoSol, steps=True)
        actionsLen=len(actions)
        actionIndex=0
        for i in actions:
            #-------------quit---------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            #--------------------------------
            actionIndex+=1
            if i == "finished":
                return
            elif i[0] == "+":
                row=i[1]
                col=i[2]
                num=i[3]
                win.fill((255,255,255))
                grid()
                autoSol[row][col]=num
                QuestionNums(autoSol)
                pygame.draw.rect(win, (0,255,0), [col*gap, row*gap, gap, gap], 4)
                #--------progress----------
                FONT = pygame.font.SysFont('freesansbold.ttf',50)
                text=FONT.render(str(round(((actionIndex/actionsLen)*100),1))+"%", 1, (0,0,0))
                win.blit(text, ((win_width-100),(win_height-100)))
                #--------------------------
                pygame.display.update()
            elif i[0] == "-":
                row=i[1]
                col=i[2]
                win.fill((255,255,255))
                grid()
                pygame.draw.rect(win, (255,0,0), [col*gap, row*gap, gap, gap], 4)
                QuestionNums(autoSol)

                autoSol[row][col]=0
                #--------progress----------
                FONT = pygame.font.SysFont('freesansbold.ttf',50)
                text=FONT.render(str(round(((actionIndex/actionsLen)*100),1))+"%", 1, (0,0,0))
                win.blit(text, ((win_width-100),(win_height-100)))
                #--------------------------
                pygame.display.update()
    
    finished(autoSol)

def finished(sudoku):
    finished=True
    for i in range(len(sudoku)):   
        for j in range(len(sudoku)):
            if sudoku[i][j] == 0:
                finished=False

    if finished:
        spaces=0
        correct=0
        wrong=[]
        for i in range(len(sudoku)):   
            for j in range(len(sudoku)):
                if sudokuQ[i][j]==0:
                    spaces+=1
                    if sudoku[i][j]==sudokuAns[i][j]:
                        correct+=1
                    else:
                        wrong.append(i,j)
                        

        if correct==spaces:
            pygame.draw.rect(win, (0,255,0), [0, 0, 500, 500], 4)
            
            FONT = pygame.font.SysFont('freesansbold.ttf',50)
            text=FONT.render("YOU WIN", 1, (0,170,0))
            win.blit(text, ((500//2)-75,(500//2)-15))
        else:
            pygame.draw.rect(win, (255,0,0), [0, 0, 500, 500], 4)
            for i in wrong:
                row=i[0]
                col=i[1]
                pygame.draw.rect(win, (170,0,0), [col*gap, row*gap, gap, gap], 4)
            
            FONT = pygame.font.SysFont('freesansbold.ttf',50)
            text=FONT.render("YOU LOSE", 1, (255,0,0))
            win.blit(text, ((500//2)-85,(500//2)-15))





selected=False
peeking=False
solving=[False, 0]  #first value is for the solve button, second is for making it only solve once
new=False
temp=[]

def redrawWindow():
    global peeking, new
    grid()

    if not(solving[0]) and solving[1]==0:
        QuestionNums(userSol)
    else:
        QuestionNums(autoSol)

    for i in temp:          #drawing temporary numbers
        row=i[0]
        col=i[1]
        num=i[2]
        tempNumRender(num, row, col)

    if selected and solving[1]==0:
        select(boardRow, boardCol)
    
    peekX, peekY = buttons["peek"][0], buttons["peek"][1]
    if peeking:
        if solving[1]==0:     #cant peek if sudoku board is solved. sudokuboard is solved if solving[1]==1
            peek()
        win.blit(peekOn, (peekX, peekY))
    else:
        win.blit(peekOff, (peekX, peekY))

    newX, newY = buttons["new"][0], buttons["new"][1]
    if new:
        new=False
        newGame()
        win.blit(newOn, (newX, newY))
    else:
        win.blit(newOff, (newX, newY))

    solveX, solveY = buttons["solve"][0], buttons["solve"][1]
    if solving[0]:
        win.blit(solveOn, (solveX, solveY))
        solving[0]=False
        if solving[1]==0:
            solveBoard()
        win.blit(solveOn, (solveX, solveY))
    else:
        win.blit(solveOff, (solveX, solveY))

    if solving[1]==0:
        finished(userSol)
    elif solving[1]==1:
        finished(autoSol)
    
    pygame.display.update()

run = True
while run:
    clock.tick(60)
    win.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            curX, curY = pygame.mouse.get_pos()
            boardCol=math.floor(curX/gap)   #selected sudoku cell column
            boardRow=math.floor(curY/gap)   #selected sudoku cell row
            if curX<=boardW and curY<=boardH:
                selected=True 
            else:
                selected=False

            peekX, peekY = buttons["peek"][0], buttons["peek"][1]
            if curX >=(peekX) and curX<=(peekX+buttonW):
                if curY >=(peekY) and curY<=(peekY+buttonH):
                    peeking=True
            
            solveX, solveY = buttons["solve"][0], buttons["solve"][1]
            if curX >=(solveX) and curX<=(solveX+buttonW):
                if curY >=(solveY) and curY<=(solveY+buttonH):
                    solving[0]=True
            
            newX, newY = buttons["new"][0], buttons["new"][1]
            if curX >=(newX) and curX<=(newX+buttonW):
                if curY >=(newY) and curY<=(newY+buttonH):
                    new=True


        if event.type == pygame.MOUSEBUTTONUP:

            peekX, peekY = buttons["peek"][0], buttons["peek"][1]
            if curX >=(peekX) and curX<=(peekX+buttonW):
                if curY >=(peekY) and curY<=(peekY+buttonH):
                    peeking=False

        if event.type == pygame.KEYDOWN:
            if selected:
                if event.key == pygame.K_LEFT:
                    selLeft(boardRow, boardCol)
                elif event.key == pygame.K_RIGHT:
                    selRight(boardRow, boardCol)
                elif event.key == pygame.K_UP:
                    selUp(boardRow, boardCol)
                elif event.key == pygame.K_DOWN:
                    selDown(boardRow, boardCol)
                elif event.key == pygame.K_TAB:
                    selRight(boardRow, boardCol)

    keys = pygame.key.get_pressed()
    if selected:
        if keys[pygame.K_1]:
            tempInput(1, boardRow, boardCol)
        elif keys[pygame.K_2]:
            tempInput(2, boardRow, boardCol)
        elif keys[pygame.K_3]:
            tempInput(3, boardRow, boardCol)
        elif keys[pygame.K_4]:
            tempInput(4, boardRow, boardCol)
        elif keys[pygame.K_5]:
            tempInput(5, boardRow, boardCol)
        elif keys[pygame.K_6]:
            tempInput(6, boardRow, boardCol)
        elif keys[pygame.K_7]:
            tempInput(7, boardRow, boardCol)
        elif keys[pygame.K_8]:
            tempInput(8, boardRow, boardCol)
        elif keys[pygame.K_9]:
            tempInput(9, boardRow, boardCol)
        elif keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]:
            tempDelete(boardRow, boardCol)
        elif  keys[pygame.K_RETURN]:
            permInput(boardRow, boardCol)

    redrawWindow()
