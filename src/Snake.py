import codey, event, time, random

# Snake points
snake = []
# Snake head X position
x = 8
# Snake head Y position
y = 4
# Target X position
tX = 0
# Target Y position
tY = 0
# Snake move direction (0-3)
direction = 1
# Game over flag
gameOver = 0
# Turn flag
turn = 0
# Snake speed
speed = 1

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
    global direction, turn
    # If the turn is not completed yet
    if turn != 0:
        # Ignore
        return
    # Start turn
    turn = 1
    # Change direction
    if direction == 3:
        direction = 0
    else:
        direction += 1

# On B button pressed
@event.button_b_pressed
def on_button_b_pressed():
    global direction, turn
    # If the turn is not completed yet
    if turn != 0:
        # Ignore
        return
    # Start turn
    turn = 1
    # Change direction
    if direction == 0:
        direction = 3
    else:
        direction -= 1
    
# On C button pressed
@event.button_c_pressed
def on_button_c_pressed():
    global gameOver
    # Stop or restart the game with gameOver flag
    if (gameOver == 0):
        gameOver = 1
    else:
        gameOver = 0

# Main game loop
def start_game():
    global snake, x, y, tY, tX, direction, gameOver, turn, speed
    # Reset all variables
    snake.clear()
    x = 8
    y = 4
    tX = 0
    tY = 0
    direction = 1
    gameOver = 0
    turn = 0
    speed = 1
    # Add 3 points to snake
    addPoint(x-2,y)
    addPoint(x-1,y)
    addPoint(x,y)
    # Set random target
    setRandomTarget()
    # Save initial snake length
    initialLen = len(snake)
    # Repeat until gameOver flag is not 0
    while (gameOver == 0):
        # Complete turn
        turn = 0
        # Update the screen
        codey.display.show_image(getImage())
        # Set new snake head position according to the direction
        if (direction == 0):
            y -= 1
        if (direction == 1):
            x += 1
        if (direction == 2):
            y += 1
        if (direction == 3):
            x -= 1
        # Check if snake runs over the border or hits itself
        if (x < 0 or x > 15 or y < 0 or y > 7 or (x,y) in snake):
            # Game over
            gameOver = 1
        else:
            # Move the snake head to the defined position
            addPoint(x,y)
            # Check if the target is reached
            if tX == x and tY == y:
                # Play sound
                codey.speaker.play_melody('step_1.wav', True)
                # Increase the speed
                if speed < 20:
                    speed += 1
                # Set new random target
                setRandomTarget()
            else:
                # Target not reached yet - remove the last point from the snake
                removePoint()
        time.sleep(.5-speed/50)
    # Loop ended - play "Game over" melody
    playGameOver()
    # Show the score
    codey.display.show(len(snake)-initialLen)

# Set new random target
def setRandomTarget():
    global snake, gameOver, tY, tX
    # Generate list of available display points
    points = []
    for x in range(16):
        for y in range(8):
            if (x,y) not in snake:
                points.append((x,y))
    # More than 2 empty points available?
    if len(points) < 3:
        gameOver = 1
        return
    # Take random point from the list
    ind = random.randint(0, len(points)-1)
    elm = points[ind]
    # Set target position
    tX = elm[0]
    tY = elm[1]

# Add new point to the snake
def addPoint(x, y):
    global snake
    snake.append((x,y))

# Remove last point from the snake
def removePoint():
    global snake
    del snake[0]

# Generate image out of the snake and target
def getImage():
    global snake, tY, tX
    # Resulting image string
    result = ""
    # Generate empty display matrix (16x8)
    matrix = [["0" for y in range(8)] for x in range(16)]
    # Transfer snake points into the matrix
    for elm in snake:
        x = elm[0]
        y = elm[1]
        matrix[x][y] = "1"
    # Transfer target point into the matrix
    matrix[tX][tY] = "1"
    # For each column
    for x in range(16):
        col = 0
        # Calculate binary representation of the column
        for y in range(8):
            if (matrix[x][y] == "1"):
                col += 2**y
        # Convert binary number into hexadecimal number and add it to the resulting line
        result += bin2hex(col)
    return result

# Convert binary number into hexadecimal
def bin2hex(a):
    c = hex(a)[2:]
    if (len(c) == 1):
        c = "0" + c
    return c

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
    
