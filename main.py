import turtle
import time
import random

win = turtle.Screen()
win.title("Hiss and Nibble")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []
delay = 0.1
score = 0
high_score = 0

scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)
scoreboard.write("Score: 0  High Score: 0", align="center",
                 font=("Courier", 24, "normal"))

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

def check_collision():
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        return True

    for segment in segments[1:]:
        if head.distance(segment) < 20:
            return True

    return False

def move_segments():
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

def reset_game():
    global score, delay, high_score
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    delay = 0.1
    scoreboard.clear()
    scoreboard.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                     font=("Courier", 24, "normal"))

win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

while True:
    win.update()

    if check_collision():
        reset_game()

    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001

        score += 10

        if score > high_score:
            high_score = score

        scoreboard.clear()
        scoreboard.write("Score: {}  High Score: {}".format(score, high_score), align="center",
                         font=("Courier", 24, "normal"))

    move_segments()

    move()

    time.sleep(delay)

win.mainloop()
