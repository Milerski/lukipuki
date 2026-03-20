import turtle
import time
import random
import tkinter

APPLE_B64 = "R0lGODdhGQAZAIcAAPHGxu23tuiwr+SgoOCbnYCZa32bX3abXt2KidiKfdeLjXKTT3SLR16CMdp1atpvbdBxdtNlaLhtbZtzP1t+OVp7PFR2NVRrPjpqD0JnEDxnCUNmHjtiCMZUWtFQUKxXQbZOVbtKTrs/RaZFPINVWJNRVI9MT3VKTYVHNHA8PGpDRV9eNk5dEFZSJ1VJCzteEztaEC9VCDRTETNOEWRGS1hAQVo9LFRARDNDBi0/Gc47OsYtMsUrL8IsM6wsLr4lKrggJ7IdKa4lLawcJIg3OaogJnM1LHAxKm4gHZYcInweGnMdE2U2N2E3N1gtJ2AqK2EmJVkoKmAeD1sgGV8cHVYgIlUdFFkcHUo7QUY5QEg4PUwzND01Ozk0OTEvMygwKEsqLUonKEEkHTEtNSUkLSEmJEAfEywdJCsdFB8iKR8gKyAcKx8bIxsfKBkeKRgcJxsbJhgbIxYcJhQcJUUaCiAaIxoaJBoZJRoZJBoZIxkaIxkZJBkZIxgaJBgaIxgZJBgZIxcaIxcaIhcZJRcZJBcZIxcZIhYaIxYaIhYZJBYZIxYZIhUZJBUZIxUZIrMRGqUTGJ8THJ8SHJ8TF5oTG5MXGqkMFp4KE6UCDKgADZYME5UHEY4IEYcUHIsMFokFDXcECYMDCX8DCXoCCIwBCIMAAoEAAHsBBXwAAHcAAGsUFlITE08WF08GB2QDBGEEBVUEBHMBBW8AAmkBA2ABA1kAAUsSE0cPDzwVCkINEEEKDEMCAj0BAjoBATkRDxkYIzYIBzIGBTgAASwAABgYJBgYIxgYIhcYJBcYIxcYIhcXIxYYJBYYIxYYIhUYJBUYIxUYIhQYIhQYIBYXIxYXIhUXJBUXIhUXIRQXJBQXIhMXIxYWIhYWIRUWIxUWIhQWIxQWIhMWIhUVIhMTJBEXIhEVIREVHxIUIhIUIBEUIA0VHxITIBATHw4THhISIAwSHQsSHAoSHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAGQAZAEAI/wALISN0LJEiZo2WNWKmiNFCZ4qWPXvmaBkyhcgcLYomR4KOCAAQFJlEqhKLGBsqWFhwwd0eR4qQLVJE7Y0KVbJCnfp0SRKpVK+gMLkCRtsvZAcPIRt0SNFMRYWiSo16rFCiRYmsRnWqqBm0RXjetaFRosQIEyewrPlWqNq4boUiJltkzU0JS5mEUAIlxQyaFiNAdKLValWNbMUUJSJ2zOkiR4LStemiZQuYMGHOMGNWzBGjgwuXHWN4DFmjmXd+bRPHrdifiKUVlXbErNAyZov0wKPhYAePCBB6WPrkQkMGDhkafDmHaHMjP+pI/OgQQIQpJFboTGlRoICBFU60mP8jFBE3HnUqkpwK5SlJJCEOEAgIUUoVEyhdyvFppChZTEV7pMNFE7oIw8suu/QiTC62VFEHYosY4sgxxzSCDDGMEWOIIoQUM00zyADSWDMUImNiRIwhMxpuisDEYSGG8LehaIocxJBMzGQUkR3bwEOOGmSooU070hzSCCKIOAUTQwg5kkc8WEjgARCPZHJJJ0SsIAMMM+RQhjiLsLhMH+9k8cAPEQgwAAEhDGEEBi/AsAEFC6ThTUSKNBJHPDd4oEMABECCyixIIIGDBQUcsAADXqzzx2Z5NjNHCY8EAUEkoByBixk2LGGEE7gMc0sN4fwRpkLKyGECJJhswskoSqCSMMEHCRCgySxUXLFFOMTwx4wjfbDDBRGziMJJEpIMoYACPpTiSgpPPEEGOIBAddEyf6AzRgqw1FKLK7HI8korVUTBShRsTFPMIgvhuMhA5oxRQxi+ABMMMLewIkYd2ADS7iIWvZsMQswEcg071sABxx7ZYENMMfzV+GuOzJRWTDLJmHgtwKWZaEwxxRiDTDHIBAQAOw=="
HEAD_B64 = "R0lGODdhFAAUAIcAAJb7TIb6RoP7Ro/vR4jvR4fsRIXtQnz5PX/1QHvzQXPxQHbuP2fsPIDrQ4LpQ3fpPm/nOW7hP2TlOmDfNF/eNFrfOnfaPWzYNmDdPl/XM17bOVzUNFbcNFbXMlbUOFTPK1PbNlHcN0/aME3cMVLXM0nVK1DPNFHONEfRLVrLM1jKLk3KL0zMMUbGMEHCK0bBL0HBKT/JKjnGJT7FKm6xOEW/LUC9LD22KT22ID6qIjq6Jju1JzquJzLCIDe/JS+9HDW6Hi23Giu3GjSzISyzFyuyGzCvHimtGyauFSuqGiWwFyKqFyKnFTCTGSyjGC6dHymkGiqbHSilGSekGSWlFiWkFySgFlmNOVaIN1KINVSGNFGGNVCHKkuENEiFL0ODMUKFJCOiFiOfFiGeFh6cEyCZFBuZERuXEReYECGVFRmSEBWTDxKRDB2KEyCFFhiLDg+KDEiBND58Lz57MTx6Lzx4LTx3Kzl6Lzh4Ljd3LzN4KzV2LTJ1JjN0LDFzKy5xKy5xHjlsICtuKCptIidoIx6AFA+CCA56CRp5EBF3CxBzDBBxCxFvDA5rDA9qCiRoICRnICFnICNjISFkFx5jHgpnCAhmCCxeGiNbISZYFhpdGhlYGRpUExdbDhVVFxJUDDhSLTRSLSBNExdPEBxFFh1AIhRRGBNMDg9MCxVLDxNJGBE+FQ47FAw7CBU1DRkwDx0fJh0fJRwfJRwfJBsfJRofJBofIxweJRweJBseJRseJBwdJBsdJRsdJBoeJRoeJBoeIxkeJBodJRodJBodIxscJRscJBocJRocJBsbJRsbJBsbIxobJRobJBsYJxsXJxsXJRoXJBwVJxsVJxoWJBsUJxsTJxoTJhsSJhsRJxoRJhoQJhYTIxkSJRkRJRkQJRkQJBgQJQMYAgAZAA4RBwoRBxgPJBcPJBcOJBYPIxYOJBYOIxUOJBUOIxUNIxMNIhQMIxMMIxIMIhEMIgcMBBELIhEKIQMJAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAFAAUAEAI/wCTMTPmS5auX7loyYp1K5dDYbJ4NVt2qx0dDkbepCJ16UmhTK5O7UCjRJK3XLHsXTlABUGHMoaQ6EjwgYkIACUoadPVSxslM41ewKhyRoolHh5qiPHQhpWzYcOkqXISIYqEQOS4ACrXakwYNhO6xIuFDFqpQXE2eSKEZ84VOX729FllJxS3XbLmYYGwRgwnV5capAHJCQMAHKaq8bqFbg8DB4jIdKJ37x69T0VOFJDwx9wtXOvuoLBiYIOPMZbKMJlxY9GJIJuu9ULGi1s8cPLgdZv2bd08dtvayUNHrViyZseghYOHzVq4de7suTu3Lt2zddyEKeuVTdOPFEWW/M1AQcIChxAgYrRZUaddrlvn+sRQw8iGjyMtGlnIsMQEgSZOLfZOHBSYYYY4+LyigBDjJFiBCkRsgk0vsOgVAAtGzLAADfjgQ8MGcCRiBQp5qIMLL9OoksMAjgwxSYcddvLDFEMssMU8svziDSQ9uKCBAGCI8sAIo6CSBhRSyCCIObrIUg8WFzTCghuHsHFIJTs8oUgSDgDhiTW86MINKF5AosUXmKjyiB5Z2BEJHlvwUUo0xjTTTELAzDLLL8HoosssuPxSiyy2ENMMMgEBADs="
BODY_B64 = "R0lGODdhFAAUAIcAAD2wMS+oJTKkKjCjJyqjITKiKCqdIiqdIS2cJCqbIimbIiWbHSaaHyeXICuWJC2VJSaVHyaTHyWTHiWTHSCTGyiRIimQISWRHiSPHiOPHSGSGiKPHB+RGR2QGB2PGByPFyqLIiOMHR+OGh+NGx+NGh+LGSOKHSCJGx+IGB6NGB6KGB6JGh6IFx2NGByLFx2JGRuJFxuJFh2IGRyIGBuIFxiIEx2HGR2HGB2HFx6GGRuHFxiHFBiGFB2EFxuEFhuCFxeDExeCFBWDExiBFBaBEheAExh/FBWBEhR/ERN/ERl9FBh8Exd6EhR7EhN7ERF7DhJ6EBF6DxZ3ExR3ERJ4EA12DBZ1EhFuEW1FJG1DJg1yDQtuCmdAJGg/JGc/I2M9ImE8ImE8IWQ7ImI7IWE7IWA+H189H14+IWA8I2A8IWA6IGA6H2E5H186IF45H143H108JFw6H1o5H1w4Hls3Hlk3HVc6IFY3HFI3IUk9Hk03Ilo2HVk2HVo1Hlk1HFg2HFc2HVYzHFUzHFQzHFI0HE0yHFIxGUg0JUg1GkwxHE4vGUowGkU+G0A7Gzs7Gj44GUA3GD82Gz42HUA1GkA0GD40FzU0FEIzGEEyGkUxJEIxJUIwJUIwI0EvJD8vJDowFDgvFTUvFzQvFDMwFD8uIz0tIj4sIjwsIjwsITssIjssITosIzotFTctFDYsEzQsEzMtEzMsEi0uEScsDTsrIjoqIDkqIDgrIDgpITcpIDcoIDgpHzcpHzgqEzgrEjopETcoHzQqJjYpHzYoHzUoHzIpEDYnHzUnHjQmHjMmHzQmHTMmHTUnEDInDzEkHTAkHDEjHSsnDisjIikjIiwmDRkbIhkbIRoaIRkaIRoZIRkZIRkZIBkYIRkYIBgbIRgaIRgaIBcaIRgZIRgZIBcZIBgYIRYYIRUYIhUYIRQYIRMYIhMYIRYXIRUXIRUXIBQXIRMXIRMXIBIXIRIXIBQWIRQWHxMWIRMWIBMVIBIWIRIWIBIVIBEWIBEVIBAVIAAAACwAAAAAFAAUAEAI/wCxidt2Ldu2bdywYTv4TZs2bNq4lSunTZ8qPrFYcNDRIkWRDD540JjFxhY8iP4OnSEEqA6XNnsEffHzB42dMrvkKXxnTM6iVqKKjYpmiRqsSK8S4dEV79s3eLf2SApRxUMUKBSIYHhBxREdZ/CqjasX7JAuTclyeTqVChWpYbg21ZKGTpy4fKnUPHqR5MkRIEgCCBBigZUiZ+/GYeNXSowlFwA0bBhQgAYRBUyYhSHF79rTU2l+WTGRY8KSHEZK9JAyydCwc9fGiXOXr907ePbg8ZvHz546fvjymYNIrpu7ffTuvbt9jx49eO+Sv2OnjZy1fpmwxCHjhk+WQH3WeMDhYuiOGVP5BNoDNsgVCARKtEyRoKLCgyug4Gjat+3uMjCNNLFCAgZAcMIWLgTxQyiGPLNOONjIkwogzSxBQAxNzNCAAzYscMMob5xyEjbzEDOGLEIwsEMEIshwAAlO4NCMG53ocw048tgyRy8owDDEBxdo0EENHYzASBfDvOOZPqvoAQgmiORBiS+QfJLHJZUUIgc06WAzzjzBcJLMMbzQogwqwqiCDDK05LLLNOg4JM41dF6j0J3e2GmNndg0FBAAOw=="

delay = 0.1
score = 0
high_score = 0
current_border = 120 # Počáteční zmenšená hranice

# Nastavení obrazovky
wn = turtle.Screen()
wn.title("Hra Had (Snake) - Vylepšená verze")
wn.bgcolor("#1a1a24")  # Moderní tmavé pozadí
wn.setup(width=600, height=600)
wn.tracer(0) # Vypne aktualizace obrazovky pro plynulost

# Registrace nových textur z base64
apple_img = tkinter.PhotoImage(data=APPLE_B64)
head_img = tkinter.PhotoImage(data=HEAD_B64)
body_img = tkinter.PhotoImage(data=BODY_B64)

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
        pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Verdana", 20, "bold"))

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
        
        # Zvětšení dynamického ohraničení
        if current_border < 280:
            current_border += 10
            draw_border(current_border)
        
        pen.clear()
        pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Verdana", 20, "bold"))

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
            pen.write(f"Skóre: {score}  Nejlepší: {high_score}", align="center", font=("Verdana", 20, "bold"))

    time.sleep(delay)
