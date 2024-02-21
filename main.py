#Hiss and Nibble game code
import turtle
import time
import random

#window setup for game
win = turtle.Screen()
win.title("Hiss and Nibble")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0) #Turn off automatic screen updates

#create snake head (green)
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop" #Initial direction does not cause movement

#Create food for snake
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.penup()

#Create segements of snake body
segments = []
delay = 0.1
score = 0
high_score = 0
level = 1
time_limit = 6.0
starvation_timer = 5.0 

#Create scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)
scoreboard.write("Score: 0  High Score: 0  Level: 1", align="center",
                 font=("Courier", 20, "normal"))

#Defining head direction of snake to match movement
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

#Defining function to move snake
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

#Checks for collisions
def check_collision():
    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        return True

    for segment in segments[1:]:
        if head.distance(segment) < 20:
            return True

    return False

#Creating movement for segments of snake
def move_segments():
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

#Resets game when snake collides with itself/the wall
def reset_game():
    global score, delay, high_score, level, time_limit, starvation_timer
    time.sleep(1)
    head.goto(0, 0) #Moves snake back to center of window
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000) #Hides segments of snake if any
    segments.clear()
    score = 0
    delay = 0.1
    level = 1
    time_limit = max(3.0, time_limit - 0.5) 
    starvation_timer = 5.0
    scoreboard.clear()
    scoreboard.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center",
                     font=("Courier", 20, "normal"))

#Generates and places food at random locations
def spawn_food():
    global last_food_time
    while True:
        x = random.randint(-260, 260) #Randomises x-coordinate for food to spawn
        y = random.randint(-260, 260) #Randomises y-coordinate for food to spawn
        if (x, y) not in [(segment.xcor(), segment.ycor()) for segment in segments]:
            #Checks that random coordinates do not overlap with any snake segments
            food.goto(x, y)
            food.color(random.choice(["red", "yellow", "white"]))
            last_food_time = time.time()
            break

#Binds specific movement functions with wasd keys
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

last_food_time = time.time()
last_tail_removal_time = time.time()

while True:
    win.update()

    #Checks for collisions
    if check_collision():
        reset_game()
        last_food_time = time.time()
        last_tail_removal_time = time.time()

    #If the snake is moving and has not eaten in 6 seconds, remove snake segment
    if head.direction != "stop":
        if time.time() - last_food_time > 6:
            spawn_food()

            if len(segments) > 0:
                segments[-1].goto(1000, 1000)
                segments.pop() #Removes segment of snake
                last_tail_removal_time = time.time()

    #Checks if snake ate food and adds another segment to tail
    if head.distance(food) < 20:
        spawn_food()

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("green")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001

        score += 10 #Score increases by 10 for every consumption of food

        #Updates high score
        if score > high_score:
            high_score = score

        #New level is reached after every score of 100
        if score % 100 == 0:
            level += 1
            delay *= 0.8
            time_limit = max(3.0, time_limit - 0.5)

        scoreboard.clear()
        scoreboard.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center",
                         font=("Courier", 20, "normal"))

        #Tracks when food was last spawned
        last_food_time = time.time()
        starvation_timer = 5.0

    #If snake has not consumed food within time limit, segment is taken off tail
    if time.time() - last_food_time > time_limit:
        if time.time() - last_tail_removal_time > time_limit:
            if len(segments) > 0:
                segments[-1].goto(1000, 1000)
                segments.pop() #Segment of tail is popped
                last_tail_removal_time = time.time()

    #If snake has no more segments, starvation timer decreased and game is reset if timer reaches 0
    if len(segments) == 0:
        starvation_timer -= 0.1
        if starvation_timer <= 0:
            reset_game()

    #Moves snake segments
    move_segments()

    #Moves snake head
    move()

    #Controls speed of snake
    time.sleep(delay)

#Keeps window open, maintaining event loop
win.mainloop()
