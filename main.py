import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

# Nastavení obrazovky
wn = turtle.Screen()
wn.title("Hra Had (Snake)")
wn.bgcolor("navy")
wn.setup(width=600, height=600)
wn.tracer(0) # Vypne aktualizace obrazovky pro plynulost

# Vykreslení ohraničení herní plochy
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-290, 290)
border.pendown()
border.pensize(2)
for _ in range(4):
    border.forward(580)
    border.right(90)
border.hideturtle()

# Hlava hada
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Jídlo
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

# Text scóre
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Skóre: 0  Nejlepší: 0", align="center", font=("Courier", 24, "normal"))

# Funkce pohybu
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
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Klávesnice (W, A, S, D nebo šipky)
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Hlavní herní smyčka
while True:
    try:
        wn.update()
    except:
        # Hráč zavřel okno
        break

    # 1. Kontrola kolize se zdmi
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Smazat segmenty (odsunout mimo obrazovku)
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        
        # Reset skóre a rychlosti
        score = 0
        delay = 0.1
        pen.clear()
        pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Courier", 24, "normal"))

    # 2. Snězení jídla
    if head.distance(food) < 20:
        # Přesun generování mimo okraj
        x = random.randint(-13, 13) * 20
        y = random.randint(-13, 13) * 20
        food.goto(x, y)

        # Přidání dílku těla
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("lightgreen")
        new_segment.penup()
        segments.append(new_segment)

        # Zkrácení zpoždění = zvýšení rychlosti
        delay -= 0.002
        score += 10
        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Courier", 24, "normal"))

    # 3. Přeskládání dílků těla
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # 4. Pohyb nultého dílku na místo hlavy
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # 5. Kontrola kolize hlavy se svým tělem
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            
            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            pen.clear()
            pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)
