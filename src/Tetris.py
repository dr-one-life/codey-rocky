import codey, event, time, random

# Points of the figure
fig = []
# Points of the base
base = []
# Points of borders
border = []
# Left border X
borderL = 2
# Right border X
borderR = 13
# Figure type (1-8)
figType = 1
# Figure X position
x = 7
# Figure Y position
y = 1
# Game over flag
gameOver = 0
# Current score
score = 0

# On Codey start
@event.start
def on_start():
    # Restart the game each time the gameOver flag set to 0
    while(1==1):
        if (gameOver == 0):
            start_game()

# On A button pressed
@event.button_a_pressed
def on_button_a_pressed():
    # Move figure to the left
    moveFig(-1)

# On B button pressed
@event.button_b_pressed
def on_button_b_pressed():
    # Move figure to the right
    moveFig(1)

# On C button pressed
@event.button_c_pressed
def on_button_c_pressed():
    global gameOver
    # Rotate figure or reset the gameOver flag if not 0
    if (gameOver == 0):
        rotateFigR()
    else:
        gameOver = 0

# On Codey tilted left
@event.tilted_left
def on_tilted_left():
    # Rotate figure left
    rotateFigL()
	
# On Codey tilted right
@event.tilted_right
def on_tilted_right():
    # Rotate figure right
    rotateFigR()

# Main game loop
def start_game():
    global gameOver, score
    # Reset all variables
    resetGame()
    # Set new figure
    setNextFig()
    # Repeat until gameOver flag is not 0
    while (gameOver == 0):
        # Try to to move the figure dowm
        # If base/bottom is reached
        if moveFigDown() == 0:
            # Add figure to the base
            addToBase()
            # Try to set next figure
            # If no more space availbale
            if setNextFig() == 0:
                # Game over
                playGameOver()
                gameOver = 1
                codey.display.show(score)
                return
        time.sleep(0.5)

# Reset all variables
def resetGame():
    global fig, base, figType, x, y, gameOver, score, border, borderL, borderR
    fig.clear()
    base.clear()
    # Create border points
    border = [ (borderL, y) for y in range(8) ]
    border.extend([ (borderR, y) for y in range(8) ])

    figType = 1
    x = 7
    y = 1
    gameOver = 0
    score = 0

# Try to place the specified figure at the specified position
def placeFigAt(fType, fX, fY):
    global fig
    # Make a copy of the figure for rollback case
    saveFig = fig.copy()
    # Remove all figure points
    fig.clear()
    # Add new figure points according to the figure type
    if (fType == 1):
        fig.append((fX, fY));
        fig.append((fX-1, fY));
        fig.append((fX, fY+1));
    if (fType == 2):
        fig.append((fX, fY));
        fig.append((fX-1, fY));
        fig.append((fX, fY-1));
    if (fType == 3):
        fig.append((fX, fY));
        fig.append((fX+1, fY));
        fig.append((fX, fY-1));
    if (fType == 4):
        fig.append((fX, fY));
        fig.append((fX+1, fY));
        fig.append((fX, fY+1));
    if (fType == 5):
        fig.append((fX, fY));
        fig.append((fX, fY+1));
    if (fType == 6):
        fig.append((fX, fY));
        fig.append((fX+1, fY));
    if (fType == 7):
        fig.append((fX, fY));
        fig.append((fX+1, fY));
        fig.append((fX, fY+1));
        fig.append((fX+1, fY+1));
    if (fType == 8):
        fig.append((fX, fY));
    # Check if new figure can be placed at the specified position
    if checkFig() == 0:
        # If not, rollback
        fig = saveFig
        return 0
    else:
        # If yes, update the screen
        codey.display.show_image(getImage())
        return 1

# Check if there are collisions between the figure and the base / the borders
def checkFig():
    global fig, base, border
    # Check for collisions between the figure and the base
    if len(base) > 0 and len(fig) > 0 and isIntersection(fig, base) > 0:
        return 0
    # Check for collisions between the figure and the borders
    if len(border) > 0 and len(fig) > 0 and isIntersection(fig, border) > 0:
        return 0
    # Check if the figure is outside of the display
    for elm in fig:
        if elm[0] < 0 or elm[0] > 15 or elm[1] > 7:
            return 0
    return 1

# Add figure to the base
def addToBase():
    global fig, base
    # Copy all figure points to the base
    for elm in fig:
        base.append(elm)
    # Remove figure
    fig.clear()
    # Check if full lines can be removed from the base (twice)
    checkLines()
    checkLines()


# Check if full lines can be removed from the base
def checkLines():
    global base, score, borderL, borderR
    # For each row starting from the bottom
    for y in range(7, -1, -1):
        # Generate a sample full line
        line = [ (x, y) for x in range(borderL+1, borderR) ]
        # Check for full intersection with the base
        if isIntersection(line, base) == len(line):
            # Line found
            score += 1
            codey.speaker.play_melody('gotcha.wav', True)
            # Move all upper lines one line down
            for u in range(y, -1, -1):
                # Consider the borders
                for x in range(borderL+1, borderR):
                    # Remove existing points from the current line
                    if (x, u) in base:
                        base.remove((x, u))
                    # Copy all point from the previous (upper) line
                    if (x, u-1) in base:
                        base.append((x, u))

# Set next figure
def setNextFig():
    global figType, x, y
    # Set figure start position
    x = 7
    y = 0
    # Select next figure type randomly
    figType = random.randint(1, 8)
    # Try to place the new figure and the specified position
    return placeFigAt(figType, x, y)

# Rotate figure to the right
def rotateFigR():
    global figType, x, y
    # Save current figure type for rollback case
    saveFigType = figType
    # Switch to the next figure type
    if (figType == 1):
        figType = 2
    elif (figType == 2):
        figType = 3
    elif (figType == 3):
        figType = 4
    elif (figType == 4):
        figType = 1
    elif (figType == 5):
        figType = 6
    elif (figType == 6):
        figType = 5
    # Try to place new figure at the same position
    if placeFigAt(figType, x, y) == 0:
        # Rollback if failed
        figType = saveFigType

# Rotate figure to the right
def rotateFigL():
    global figType, x, y
    # Save current figure type for rollback case
    saveFigType = figType
    # Switch to the next figure type
    if (figType == 1):
        figType = 4
    elif (figType == 2):
        figType = 1
    elif (figType == 3):
        figType = 2
    elif (figType == 4):
        figType = 3
    elif (figType == 5):
        figType = 6
    elif (figType == 6):
        figType = 5
    # Try to place new figure at the same position
    if placeFigAt(figType, x, y) == 0:
        # Rollback if failed
        figType = saveFigType

# Move figure to the left or to the right
def moveFig(dX):
    global figType, x, y
    # Save old X position for rollback case
    saveX = x
    # Change position
    x += dX
    # Try to place the figure at the new position
    if placeFigAt(figType, x, y) == 0:
        # Rollback if failed
        x = saveX

# Move figure one line down
def moveFigDown():
    global figType, x, y
    # Save old Y position for rollback case
    saveY = y
    # Change position
    y += 1
    # Try to place the figure at the new position
    if placeFigAt(figType, x, y) == 0:
        # Rollback if failed
        y = saveY
        return 0
    else:
        # Success
        return 1

# Generate image out of the figure, base and borders
def getImage():
    global fig, base, border
    # Resulting image string
    result = ""
    # Generate empty display matrix (16x8)
    matrix = [["0" for y in range(8)] for x in range(16)]
    # Transfer figure points into the matrix
    for elm in fig:
        x = elm[0]
        y = elm[1]
        if y >= 0:
            matrix[x][y] = "1"
    # Transfer base points into the matrix
    for elm in base:
        x = elm[0]
        y = elm[1]
        if y >= 0:
            matrix[x][y] = "1"
    # Transfer borders points into the matrix
    for elm in border:
        x = elm[0]
        y = elm[1]
        matrix[x][y] = "1"
    # For each column
    for x in range(16):
        col = 0
        # Calculate binary representation of the column
        for y in range(8):
            if (matrix[x][y] == "1"):
                col += 2**(7-y)
        # Convert binary number into hexadecimal number and add it to the resulting line
        result += bin2hex(col)
    return result

# Convert binary number into hexadecimal
def bin2hex(a):
    c = hex(a)[2:]
    if (len(c) == 1):
        c = "0" + c
    return str(c)

# Get number of common points in two lists
def isIntersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return len(lst3)

# Play random "Game over" melody
def playGameOver():
    snd = random.randint(0, 3)
    if snd == 0:
        codey.speaker.play_melody('wrong.wav', True)
    if snd == 1:
        codey.speaker.play_melody('explosion.wav', True)
    if snd == 2:
        codey.speaker.play_melody('start.wav', True)
    if snd == 3:
        codey.speaker.play_tone(330, 0.2)
        codey.speaker.play_tone(311, 0.2)
        codey.speaker.play_tone(294, 0.2)
        codey.speaker.play_tone(277, 0.2)
        codey.speaker.play_tone(262, 1)
    
