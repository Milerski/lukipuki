import turtle
import sys
import subprocess
import time
import random
import tkinter
from tkinter import simpledialog
import json
import os
import urllib.request

APPLE_B64 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAuklEQVR4nGNgIBJ0uwr/73YV/k9IHROxBsKA0Vmj/0ZnjXAaTJSBMJct75BHMZgsA++I2BD0JjJgJNWgsJ3fGBgYGBhWuXMxqLw5gqEfq4Eww5QNjzAwMDAw3D1vg9NF6IZieBndMHQ2LvU4DcRlAD5DcRpIagRg04fVhdjCDF84IgOcyQbZAGINY2BgYGDBJ0mKQTBActYjyUBsCZUYgKyPti5Et40YQDCnkGIo0XkZGWBL7OSG9eAAACVcQ2N+TxIKAAAAAElFTkSuQmCC'
HEAD_B64 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAuUlEQVR4nNWUsRHCMAxFvzhKpjADUGUWFrGnCItkFqoMYE1BHyrnZFsi4uA4otLfevqyZQP/HrS1IYxhadc4sZlnChrIA1aBEnbC0OkP3E3owYLlyMiRVWdSazupgBJGBBABc5wq2BynVdOgncNPY+2/VClnVpxdbtcuqdXKmXJiOlqVNJBH+3rLOwKWAZVD6wl5IRVQ2+SFqQ5lFQ/Uen6dQw/01Vv+zW+jgXNinMdggt6OBdh0DABP0Qlcm5VhR7wAAAAASUVORK5CYII='
BODY_B64 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAjklEQVR4nM2UwRGAIAwExbESPlZoFVboJ63oK8iEHBwM43hPcqw5CC7L3xVahnjG267JIXAfLHggBryOwpCvALIw5A+1okoueT17dMEaf6t9PQfZNQROkXujWul+91JQd0wdAkf1HRAdequegLXnxIgaG+2CmUNV0dXI+OTpijPsjW797qWwUM83/X84XQ9Bqz4iC5gUkwAAAABJRU5ErkJggg=='

delay = 0.1
score = 0
high_score = 0
current_border = 120 # Počáteční zmenšená hranice

# Nastavení obrazovky
wn = turtle.Screen()
wn.title("Hra Had (Snake) - Vylepšená verze")
wn.bgcolor("#1a1a24")  # Moderní tmavé pozadí
wn.setup(width=900, height=600)  # Rozšíření pro postranní panel
wn.tracer(0) # Vypne aktualizace obrazovky pro plynulost

SERVER_URL = "http://127.0.0.1:5000/leaderboard"
server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")

# Automatické spuštění serveru
try:
    req = urllib.request.Request(SERVER_URL)
    urllib.request.urlopen(req, timeout=0.2)
except:
    subprocess.Popen([sys.executable, server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.5)

# Přihlášení hráče
player_name = "Host"
player_password = ""

def ask_player_name():
    global player_name, player_password
    
    def on_login(event=None):
        global player_name, player_password
        val = entry.get()
        pwd = entry_pwd.get()
        if val.strip() == "" or pwd.strip() == "":
            lbl_error.config(text="Zadej jméno a heslo!", fg="red")
            return
            
        pn = val.strip()
        
        try:
            data = json.dumps({"name": pn, "password": pwd}).encode('utf-8')
            req = urllib.request.Request(SERVER_URL.replace("/leaderboard", "/login"), data=data, headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req, timeout=1)
            res_data = json.loads(response.read().decode('utf-8'))
            if not res_data.get("success"):
                lbl_error.config(text=res_data.get("error", "Chyba přihlášení!"), fg="red")
                return
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode('utf-8'))
                lbl_error.config(text=err_data.get("error", "Chyba přihlášení!"), fg="red")
            except:
                lbl_error.config(text="Chyba přihlášení!", fg="red")
            return
        except Exception as e:
            pass # Lokální hraní
            
        player_name = pn
        player_password = pwd
        login_win.destroy()

    def on_register(event=None):
        val = entry.get()
        pwd = entry_pwd.get()
        if val.strip() == "" or pwd.strip() == "":
            lbl_error.config(text="Zadej jméno a heslo!", fg="red")
            return
            
        pn = val.strip()
        try:
            data = json.dumps({"name": pn, "password": pwd}).encode('utf-8')
            req = urllib.request.Request(SERVER_URL.replace("/leaderboard", "/register"), data=data, headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req, timeout=1)
            res_data = json.loads(response.read().decode('utf-8'))
            if not res_data.get("success"):
                lbl_error.config(text=res_data.get("error", "Chyba registrace!"), fg="red")
                return
            lbl_error.config(text="Úspěšně registrováno! Nyní se přihlas.", fg="#00ff00")
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode('utf-8'))
                lbl_error.config(text=err_data.get("error", "Chyba registrace!"), fg="red")
            except:
                lbl_error.config(text="Chyba registrace!", fg="red")
            return
        except Exception as e:
            lbl_error.config(text="Server offline! Nelze registrovat.", fg="red")

    root = wn.getcanvas().winfo_toplevel()
    login_win = tkinter.Toplevel(root)
    login_win.title("Přihlášení - Luki Puki Snake")
    login_win.geometry("400x400")
    login_win.configure(bg="#1a1a24")
    login_win.transient(root)
    login_win.grab_set()

    lbl = tkinter.Label(login_win, text="🐍 LUKI PUKI SNAKE 🐍", bg="#1a1a24", fg="#00ff00", font=("Verdana", 18, "bold"))
    lbl.pack(pady=10)

    lbl_sub = tkinter.Label(login_win, text="Přezdívka (pro světovou tabulku):", bg="#1a1a24", fg="white", font=("Verdana", 10))
    lbl_sub.pack()
    entry = tkinter.Entry(login_win, font=("Verdana", 14), bg="#2a2a35", fg="white", insertbackground="white", justify="center")
    entry.pack(pady=5)
    
    lbl_pwd = tkinter.Label(login_win, text="Heslo:", bg="#1a1a24", fg="white", font=("Verdana", 10))
    lbl_pwd.pack()
    entry_pwd = tkinter.Entry(login_win, font=("Verdana", 14), bg="#2a2a35", fg="white", insertbackground="white", justify="center", show="*")
    entry_pwd.pack(pady=5)
    entry.focus()

    lbl_error = tkinter.Label(login_win, text="", bg="#1a1a24", fg="red", font=("Verdana", 10, "bold"))
    lbl_error.pack()

    # Frame for buttons
    btn_frame = tkinter.Frame(login_win, bg="#1a1a24")
    btn_frame.pack(pady=10)

    btn_login = tkinter.Button(btn_frame, text="PŘIHLÁSIT", command=on_login, bg="#00ff00", fg="black", font=("Verdana", 10, "bold"), width=12)
    btn_login.grid(row=0, column=0, padx=5)
    
    btn_register = tkinter.Button(btn_frame, text="REGISTROVAT", command=on_register, bg="#00aaff", fg="black", font=("Verdana", 10, "bold"), width=12)
    btn_register.grid(row=0, column=1, padx=5)
    
    lbl_contact = tkinter.Label(login_win, text="Kontakt na autora: lukasscrpitcz@gmail.com", bg="#1a1a24", fg="#aaaaaa", font=("Verdana", 8))
    lbl_contact.pack(side="bottom", pady=5)
    
    login_win.bind("<Return>", on_login)
    root.wait_window(login_win)

ask_player_name()

# Načtení lokální tabulky
leaderboard_file = "leaderboard.json"
if os.path.exists(leaderboard_file):
    try:
        with open(leaderboard_file, "r") as f:
            leaderboard = json.load(f)
    except:
        leaderboard = {}
else:
    leaderboard = {}

high_score = leaderboard.get(player_name, 0)

def upload_score(player, score):
    try:
        data = json.dumps({"name": player, "password": player_password, "score": score}).encode('utf-8')
        req = urllib.request.Request(SERVER_URL, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=1)
    except:
        pass

def fetch_leaderboard():
    try:
        req = urllib.request.Request(SERVER_URL)
        response = urllib.request.urlopen(req, timeout=1)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except:
        return None

# Počáteční synchronizace
if high_score > 0:
    upload_score(player_name, high_score)

# Registrace nových textur z base64
root = wn.getcanvas().winfo_toplevel()
apple_img = tkinter.PhotoImage(master=root, data=APPLE_B64)
head_img = tkinter.PhotoImage(master=root, data=HEAD_B64)
body_img = tkinter.PhotoImage(master=root, data=BODY_B64)

wn.register_shape("apple_tex", turtle.Shape("image", apple_img))
wn.register_shape("head_tex", turtle.Shape("image", head_img))
wn.register_shape("body_tex", turtle.Shape("image", body_img))

# Vykreslení ohraničení herní plochy
border = turtle.Turtle()
border.speed(0)
border.color("#3a3a4c")
border.pensize(4)
border.hideturtle()

def draw_border(size):
    border.clear()
    border.penup()
    border.goto(-size, size)
    border.pendown()
    for _ in range(4):
        border.forward(size * 2)
        border.right(90)

draw_border(current_border)

# Hlava hada
head = turtle.Turtle()
head.speed(0)
head.shape("head_tex")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Jídlo
food = turtle.Turtle()
food.speed(0)
food.shape("apple_tex")
food.penup()
food.goto(0,100)

segments = []

# Text scóre
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Hráč: {player_name} | Skóre: {score} | Nejlepší: {high_score}", align="center", font=("Verdana", 14, "bold"))

leaderboard_pen = turtle.Turtle()
leaderboard_pen.speed(0)
leaderboard_pen.color("yellow")
leaderboard_pen.penup()
leaderboard_pen.hideturtle()
leaderboard_pen.goto(300, 150)

def update_sidebar_leaderboard():
    leaderboard_pen.clear()
    lb_data = fetch_leaderboard()
    if lb_data is None:
        leaderboard_pen.write("Server\nnedostupný", align="left", font=("Verdana", 10, "bold"))
    elif not lb_data:
        leaderboard_pen.write("Světová tabulka:\nZatím prázdná!", align="left", font=("Verdana", 10, "bold"))
    else:
        sorted_lb = sorted(lb_data.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "SVĚTOVÁ TABULKA\n\n"
        for i, (p, s) in enumerate(sorted_lb):
            short_p = p[:12] + ".." if len(p) > 12 else p
            text += f"{i+1}. {short_p} - {s}\n"
        leaderboard_pen.write(text, align="left", font=("Verdana", 10, "bold"))

# První načtení postranního panelu
update_sidebar_leaderboard()

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
    if head.xcor()>current_border or head.xcor()<-current_border or head.ycor()>current_border or head.ycor()<-current_border:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Smazat segmenty (odsunout mimo obrazovku)
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        
        # Reset skóre a ohraničení
        score = 0
        current_border = 120
        draw_border(current_border)
        delay = 0.1
        pen.clear()
        pen.write(f"Hráč: {player_name} | Skóre: {score} | Nejlepší: {high_score}", align="center", font=("Verdana", 14, "bold"))
        
        # Aktualizace tabulky po smrti
        update_sidebar_leaderboard()

    # 2. Snězení jídla
    if head.distance(food) < 20:
        # Přesun generování mimo okraj podle aktuálního ohraničení
        max_grid = (current_border - 20) // 20
        # Ošetření, aby nedošlo k případné chybě při příliš malém prostoru
        max_grid = max(1, max_grid)
        x = random.randint(-max_grid, max_grid) * 20
        y = random.randint(-max_grid, max_grid) * 20
        food.goto(x, y)

        # Přidání dílku těla
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("body_tex")
        new_segment.penup()
        segments.append(new_segment)

        # Zkrácení zpoždění = zvýšení rychlosti
        delay -= 0.002
        score += 10
        if score > high_score:
            high_score = score
            leaderboard[player_name] = high_score
            with open(leaderboard_file, "w") as f:
                json.dump(leaderboard, f)
            upload_score(player_name, high_score)
        
        # Zvětšení dynamického ohraničení
        if current_border < 280:
            current_border += 10
            draw_border(current_border)
        
        pen.clear()
        pen.write(f"Hráč: {player_name} | Skóre: {score} | Nejlepší: {high_score}", align="center", font=("Verdana", 14, "bold"))

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
            pen.write(f"Hráč: {player_name} | Skóre: {score} | Nejlepší: {high_score}", align="center", font=("Verdana", 14, "bold"))
            
            # Aktualizace tabulky po smrti
            update_sidebar_leaderboard()

    time.sleep(delay)
