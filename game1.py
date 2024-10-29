from tkinter import *
import time
import random
from PIL import Image, ImageTk

class Ball():
    def __init__(self, canvas, platform, image_path):
        self.canvas = canvas
        self.platform = platform
        self.image = Image.open(image_path)
        self.image = self.image.resize((15, 15), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.oval = canvas.create_image(200, 200, anchor=NW, image=self.photo)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -1
        self.touch_bottom = False

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        ball_width, ball_height = 15, 15

        if pos[1] <= 0:
            self.y = 3
        if pos[1] + ball_height >= 400:
            self.touch_bottom = True
        if self.touch_platform([pos[0], pos[1], pos[0] + ball_width, pos[1] + ball_height]):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[0] + ball_width >= 500:
            self.x = -3

class Platform():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def left(self, event):
        self.x = -2

    def right(self, event):
        self.x = 2

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= 500:
            self.x = 0


window = Tk()
window.title("игра")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)


canvas = Canvas(window, width=500, height=400)
canvas.pack()

background_image = Image.open("кк.jpg")
background_image = background_image.resize((500, 400), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(background_image)

canvas.create_image(0, 0, anchor=NW, image=bg_image)

canvas.create_text(250, 20, text="игра", font=("Arial", 24), fill="white")

platform = Platform(canvas, 'green')
ball = Ball(canvas, platform, 'ball.jpg')

while True:
    if ball.touch_bottom == False:
        ball.draw()
        platform.draw()
    else:
        break

    window.update()
    time.sleep(0.01)

window.mainloop()
