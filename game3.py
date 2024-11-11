import cv2
import random
import numpy as np

class Ball():
    def __init__(self, canvas, platform, radius=5, color=(0, 0, 255)):
        self.canvas = canvas
        self.platform = platform
        self.radius = radius
        self.color = color
        self.x = random.choice([-3, -2, -1, 1, 2, 3])
        self.y = -1
        self.touch_bottom = False
        self.position = [200 + 19, 200]

    def touch_platform(self, ball_pos):
        platform_pos = self.platform.get_position()
        if (ball_pos[0] + self.radius * 2 >= platform_pos[0] and
            ball_pos[0] <= platform_pos[2] and
            ball_pos[1] + self.radius * 2 >= platform_pos[1] and
            ball_pos[1] <= platform_pos[1] + self.platform.height):
            return True
        return False

    def draw(self):
        self.position[0] += self.x
        self.position[1] += self.y

        if self.position[1] <= 0:
            self.y = 3
        if self.position[1] + self.radius * 2 >= 400:
            self.touch_bottom = True
        if self.touch_platform([self.position[0], self.position[1], self.position[0] + self.radius * 2, self.position[1] + self.radius * 2]):
            self.y = -3
        if self.position[0] <= 0:
            self.x = 3
        if self.position[0] + self.radius * 2 >= 500:
            self.x = -3

    def get_position(self):
        return self.position


class Platform():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.x = 230 + 19
        self.y = 300
        self.width = 100
        self.height = 10

    def left(self):
        self.x -= 5

    def right(self):
        self.x += 5

    def draw(self):
        if self.x < 0:
            self.x = 0
        if self.x + self.width > 500:
            self.x = 500 - self.width

    def get_position(self):
        return [self.x, self.y, self.x + self.width, self.y + self.height]


class Block():
    def __init__(self, x, y, width, height, color):
        self.x = x + 19
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True

    def draw(self, frame):
        if self.visible:
            cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), self.color, -1)

    def check_collision(self, ball_pos):
        if self.visible:
            block_rect = [self.x, self.y, self.x + self.width, self.y + self.height]
            if (ball_pos[0] >= block_rect[0] and ball_pos[0] <= block_rect[2]) and \
               (ball_pos[1] >= block_rect[1] and ball_pos[1] <= block_rect[3]):
                self.visible = False
                return True
        return False


window_width, window_height = 500, 400
background = np.zeros((window_height, window_width, 3), dtype=np.uint8)

bg_image = cv2.imread("kk.jpg")
bg_image = cv2.resize(bg_image, (window_width, window_height))

platform = Platform(background, 'green')
ball = Ball(background, platform)

blocks = []
block_width = 80
block_height = 20
block_color = (255, 255, 0)
horizontal_gap = 10
vertical_gap = 5

rows = 5
cols = window_width // (block_width + horizontal_gap)

for row in range(rows):
    for col in range(cols):
        x = col * (block_width + horizontal_gap)
        y = row * (block_height + vertical_gap) + 50
        blocks.append(Block(x, y, block_width, block_height, block_color))

while True:
    frame = bg_image.copy()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Game", (150, 40), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    for block in blocks:
        block.draw(frame)

    cv2.rectangle(frame, (platform.x, platform.y), (platform.x + platform.width, platform.y + platform.height), (0, 255, 0), -1)

    ball_pos = ball.get_position()
    if 0 <= ball_pos[0] < window_width - ball.radius * 2 and 0 <= ball_pos[1] < window_height - ball.radius * 2:
        cv2.circle(frame, (ball_pos[0] + ball.radius, ball_pos[1] + ball.radius), ball.radius, ball.color, -1)

    for block in blocks:
        if block.check_collision([ball_pos[0], ball_pos[1], ball_pos[0] + ball.radius * 2, ball_pos[1] + ball.radius * 2]):
            ball.y = -ball.y

    ball.draw()

    cv2.imshow("Game", frame)

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        platform.left()
    elif key == ord('d'):
        platform.right()

    platform.draw()

    if ball.touch_bottom:
        print("Game Over!")
        break

cv2.destroyAllWindows()
