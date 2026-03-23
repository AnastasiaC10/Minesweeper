'''
Minesweeper
1. Generate grids:
    grid = list of lists, all values set to '-'
    displayGrid = list of lists, all values set to '-'
    
    for i in range(mines): #put mines in
        x = rand(0, rows)
        y = rand(0, cols)
        grid[x][y] = 'M'
    
    iterate through outer list: #add num of mines touching square
        iterate through inner list:
            if any squares touching current square == 'M' && current square != 'M':
                current square == num. of squares touching it == 'M'
    
    set centre of displayGrid == centre of grid
        
2. Display displayGrid:
    print x coordinates over the top
    iterate through outer list:
        print y coordinate
        iterate through inner list:
            print item
        print new line
        
3. Take user input:
    ask for square coordinates to dig
    while grid[x][y] != 'M':
        increase score by 1
        displayGrid[x][y] == grid[x][y]
        reprint displayGrid
        ask for square coordinates to dig
    
4. Game end:
    [end of above while loop]
    save the score to a csv file
    analyse data
'''
import random #for generating the mines

#for analytics
import csv
import pandas as pd
import matplotlib.pyplot as plt

#Functions#        
def generateGrid(gridIn, mines): #generate the grid w/ mines
    cols = len(gridIn[0])
    rows = len(gridIn)
    
    #make new list so that function doesn't alter main list
    gridOut = [[0 for i in range(cols)] for j in range(rows)]
    for y in range(rows):
        for x in range(cols):
            gridOut[y][x] = gridIn[y][x]
    
    for i in range(mines): #generate mines
        #pick random coordinates for the mine
        x = random.randint(0, cols-1)
        y = random.randint(0, rows-1)
        while gridOut[y][x] == 'M': #make sure to get the right num of mines
            x = random.randint(0, cols-1)
            y = random.randint(0, rows-1)
        gridOut[y][x] = 'M'
        
    for y in range(rows): #fill in the rest of the squares
        for x in range(cols):
            if gridOut[y][x] != 'M':
                minesTouching = 0
                if y > 0 and gridOut[y-1][x] == 'M': #above
                    minesTouching += 1
                if y < rows-1 and gridOut[y+1][x] == 'M': #below
                    minesTouching += 1
                    
                if x > 0 and gridOut[y][x-1] == 'M': #left
                    minesTouching += 1
                if x < cols-1 and gridOut[y][x+1] == 'M': #right
                    minesTouching += 1
                    
                if y > 0 and x > 0 and gridOut[y-1][x-1] == 'M': #diagonally above left
                    minesTouching += 1
                if y > 0 and x < cols-1 and gridOut[y-1][x+1] == 'M': #diagonally above right
                    minesTouching += 1
                    
                if y < rows-1 and  x > 0 and gridOut[y+1][x-1] == 'M': #diagonally below left
                    minesTouching += 1
                if y < rows-1 and x < cols-1 and gridOut[y+1][x+1] == 'M': #diagonally below right
                    minesTouching += 1
                
                gridOut[y][x] = minesTouching
    
    return gridOut

def gridDisplay(gridIn): #show grid
    for i in range(len(gridIn[0])+1): #show x coords
        if i == 0:
            print(" ", end=" |")
        else:
            if i-1 < 10:
                print(i-1, end=" |")
            else:
                print(i-1, end="|") #for med/hard
    print()
    displayLength = (len(gridIn[0])+1)*3
    print("-" * displayLength)
        
    for y in range(len(gridIn)): #show grid content & y coords
        if y < 10:
            print(y, end=" |")
        else:
            print(y, end="|") #for med/hard
        for x in range(len(gridIn[y])):
            print(gridIn[y][x], end="  ")
        print()
        
def revealNonMinesTouching(x, y, gridIn, displayIn):
    rows = len(gridIn)
    cols = len(gridIn[0])
    
    #make new list so that function doesn't alter main list
    displayOut = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            displayOut[i][j] = displayIn[i][j]
            
    above = y-1
    below = y+1
    left = x-1
    right = x+1
    
    if y > 0: #above
        if gridIn[above][x] != 'M':
            displayOut[above][x] = gridIn[above][x]
            
        if x > 0 and gridIn[above][left] != 'M':
            displayOut[above][left] = gridIn[above][left]
        if x < cols-1 and gridIn[above][right] != 'M':
            displayOut[above][right] = gridIn[above][right]
            
    if y < rows-1: #below
        if gridIn[below][x] != 'M':
            displayOut[below][x] = gridIn[below][x]
            
        if x > 0 and gridIn[below][left] != 'M':
            displayOut[below][left] = gridIn[below][left]
        if x < cols-1 and gridIn[below][right] != 'M':
            displayOut[below][right] = gridIn[below][right]
            
    if x > 0 and gridIn[y][left] != 'M': #left
        displayOut[y][left] = gridIn[y][left]
    if x < cols-1 and gridIn[y][right] != 'M': #right
        displayOut[y][right] = gridIn[y][right]
        
    return displayOut
        
def revealSquares(x, y, gridIn, displayIn):
    rows = len(gridIn)
    cols = len(gridIn[0])
    
    #make new list so that function doesn't alter main list
    displayOut = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            displayOut[i][j] = displayIn[i][j]

    displayOut[y][x] = gridIn[y][x]
    displayOut = revealNonMinesTouching(x, y, gridIn, displayOut)
    
    loop = True
    while loop:
        displayOut2 = [[0 for i in range(cols)] for j in range(rows)] #working copy of displayOut
        for i in range(rows):
            for j in range(cols):
                displayOut2[i][j] = displayOut[i][j]
                
        loop = False #if all zeroes have been checked, stop
        for i in range(rows):
            for j in range(cols):
                if displayOut2[i][j] == 0:
                    displayOut2 = revealNonMinesTouching(j, i, gridIn, displayOut2)
                    squaresTouching = []
                    squaresTouchingCheck = []
                    if i>0: #go over again if already checked squares are now zeroes
                        squaresTouching.append(displayOut2[i-1][j]) #above
                        squaresTouchingCheck.append(displayOut[i-1][j]) 
                        if j>0:
                            squaresTouching.append(displayOut2[i-1][j-1]) #diagonal left
                            squaresTouchingCheck.append(displayOut[i-1][j-1]) 
                        if j<cols-1:
                            squaresTouching.append(displayOut2[i-1][j+1]) #diagonal right
                            squaresTouchingCheck.append(displayOut[i-1][j+1])
                    if j>0:
                        squaresTouching.append(displayOut2[i][j-1]) #left
                        squaresTouchingCheck.append(displayOut[i][j-1])
                        
                    for k in range(len(squaresTouching)):
                        if squaresTouching[k] == 0 and squaresTouching[k] != squaresTouchingCheck[k]: #0 & not previously 0
                            loop = True
        for i in range(rows): #update displayOut again
            for j in range(cols):
                displayOut[i][j] = displayOut2[i][j]
        
    return displayOut

def game(simulate, cols, rows):
    score = 0
    gridUncovered = 0
    win = False
    
    #Grid Generation
    grid = [[0 for i in range(cols)] for j in range(rows)] #make lists
    displayGrid = [['-' for i in range(cols)] for j in range(rows)]

    numMines = (cols*rows)//5 #generate mines
    grid = generateGrid(grid, numMines)

    #reveal a ring around the centre of displayGrid
    centreRow = rows//2
    revealCol = cols//2
    if grid[centreRow][revealCol] == 'M':
        for i in range(len(grid[centreRow])):
            if grid[centreRow][i] != 'M':
                revealCol = i
                break    
    displayGrid = revealSquares(revealCol, centreRow, grid, displayGrid)
    
    
    #gridDisplay(grid) #testing
    
    print(f"\nThere are {numMines} mines. Remove all squares around them.") #start game
    gridDisplay(displayGrid)

    blankCounter = 0 #so that you can win
    
    if not simulate:
        dig = input("Select a square (x,y): ") #first input
        x, y = dig.split(",")
        x, y = int(x), int(y)
    else:
        x = random.randint(0, cols-1) #Áine strategy
        y = random.randint(0, rows-1)
        print(f"Square selected: {x}, {y}")

    while grid[y][x] != 'M': #main game
        blankCounter = 0 #so that the blanks can be recounted each loop
        
        while displayGrid[y][x] == grid[y][x]: #make sure they can't just dig the same square over and over
            print("That square is already revealed!")
            if not simulate:
                dig = input("Select a new square (x,y): ")
                x, y = dig.split(",")
                x, y = int(x), int(y)
            else:
                x = random.randint(0, cols-1)
                y = random.randint(0, rows-1)
                print(f"Square selected: {x}, {y}")
        
        score += 1
        
        displayGrid = revealSquares(x, y, grid, displayGrid)
        print()
        if not simulate: #save time when simulating
            gridDisplay(displayGrid)
        
        #count blanks
        for i in range(rows):
            for j in range(cols):
                if displayGrid[j][i] == '-':
                    blankCounter+=1
        
        print(f"Blanks: {blankCounter}	| Mines: {numMines}")
        if blankCounter > numMines:
            if not simulate:
                dig = input("Select a square (x,y): ")
                x, y = dig.split(",")
                x, y = int(x), int(y)
            else:
                x = random.randint(0, cols-1)
                y = random.randint(0, rows-1)
                print(f"Square selected: {x}, {y}")
        else:
            break

    #End
    for i in range(len(displayGrid)):
        for j in range(len(displayGrid[i])):
            if displayGrid[i][j] == grid[i][j]:
                gridUncovered += 1
    gridUncovered /= (cols*rows)
    gridUncovered *= 100
    grindUncovered = round(gridUncovered, 2)

    #Display score, etc.
    if blankCounter != numMines:
        print("\nYou selected a mine!")
    else:
        print("You found all mines!")
        win = True
    gridDisplay(grid)
    print(f"Percentage grid uncovered: {gridUncovered}%")
    print(f"Score: {score}")

    #save current score, etc.
    new_row = [difficulty, score, gridUncovered, win]

    if not simulate:
        with open("scores.csv", "a", newline="") as file:
            #not putting this on a new line for some reason???
            writer = csv.writer(file)
            writer.writerow(new_row)
    else:
        with open("simulatedScores.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
            
    
#Main Code#
#Menu Stuff#
#Simulate/play
simulate = input("Simulate or play? (s/p) ")
simulate = simulate.upper()

while simulate != "S" and simulate != "P":
    print("Invalid answer.")
    simulate = input("Simulate or play? (s/p) ")
    simulate = simulate.upper()

if simulate == "S":
    simulate = True
else:
    simulate = False
    
print()

#Difficulty Selection
difficulty = input("Select difficulty: \nEasy \nMedium \nHard \n")
difficulty = difficulty.upper()

while difficulty != "TEST" and difficulty != "EASY" and difficulty != "MEDIUM" and difficulty != "HARD": #avoid later errors
    print("\nInvalid answer.")
    difficulty = input("Select difficulty: \nEasy \nMedium \nHard \n")
    difficulty = difficulty.upper()

if difficulty == "TEST":
    cols = 5
    rows = 5
elif difficulty == "EASY":
    cols = 10
    rows = 10
elif difficulty == "MEDIUM":
    cols = 15
    rows = 15
else: #hard
    cols = 20
    rows = 20
    
print()

#Num Games
numGames = input("How many games would you like to play? ")

while not numGames.isdigit():
    print("Invalid answer.")
    numGames = input("How many games would you like to play? ")
    
numGames = int(numGames)
    
print()

#Game#        
for i in range(numGames):
    print(f"Game {i+1}")
    game(simulate, cols,  rows)
    
#Analysis#
if not simulate:
    score_df = pd.read_csv("scores.csv")
else:
    score_df = pd.read_csv("simulatedScores.csv")
score_df = score_df[['difficulty','score','percentageUncovered','win']]

easyData = score_df[(score_df['difficulty'] == 'EASY')]
medData = score_df[(score_df['difficulty'] == 'MEDIUM')]
hardData = score_df[(score_df['difficulty'] == 'HARD')]

winData = score_df[(score_df['win'] == True)]
loseData = score_df[(score_df['win'] == False)]

#easy data
easyScores = easyData['score'].unique().tolist()
easyUncovered = easyData.groupby('score')['percentageUncovered'].mean().tolist()

easyGames = len(easyData['win'].tolist())
easyWins = len(easyData[(easyData['win'] == True)]['win'].tolist())
easyLosses = len(easyData[(easyData['win'] == False)]['win'].tolist())
pctEasyWins = round((easyWins/easyGames)*100, 2)

#medium data
medUncovered = medData.groupby('score')['percentageUncovered'].mean().tolist()
medScores = medData['score'].unique().tolist()

medGames = len(medData['win'].tolist())
medWins = len(medData[(medData['win'] == True)]['win'].tolist())
medLosses = len(medData[(medData['win'] == False)]['win'].tolist())
pctMedWins = round((medWins/medGames)*100, 2)

#hard data
hardScores = hardData['score'].unique().tolist()
hardUncovered = hardData.groupby('score')['percentageUncovered'].mean().tolist()

hardGames = len(hardData['win'].tolist())
hardWins = len(hardData[(hardData['win'] == True)]['win'].tolist())
hardLosses = len(hardData[(hardData['win'] == False)]['win'].tolist())
pctHardWins = round((hardWins/hardGames)*100, 2)

#pie graph easy wins v losses
plt.pie([easyWins, easyLosses], labels=["Wins", "Losses"], autopct='%1.1f%%')
plt.title("Easy Wins and Losses")
plt.show()

#pie graph med wins v losses
plt.pie([medWins, medLosses], labels=["Wins", "Losses"], autopct='%1.1f%%')
plt.title("Medium Wins and Losses")
plt.show()

#pie graph hard wins v losses
plt.pie([hardWins, hardLosses], labels=["Wins", "Losses"], autopct='%1.1f%%')
plt.title("Hard Wins and Losses")
plt.show()

#score vs percent uncovered graph
plt.scatter(easyScores, easyUncovered, color="red")
plt.scatter(medScores, medUncovered, color="orange")
plt.scatter(hardScores, hardUncovered, color="yellow")
plt.legend(['Easy', 'Medium', 'Hard'])
plt.ylabel("Percentage Grid Uncovered")
plt.xlabel("Score")
plt.title("Percentage Grid Uncovered vs Scores")
plt.show()

#wins graph
plt.bar(['Easy', 'Medium', 'Hard'], [pctEasyWins, pctMedWins, pctHardWins], color=['red', 'orange', 'yellow'])
plt.xlabel("Difficulty")
plt.ylabel("% of Wins")
plt.title("% of Wins by Difficulty")
plt.show()

#graph percentage uncovered wins vs losses, & percentage wins vs percentage losses by difficulty