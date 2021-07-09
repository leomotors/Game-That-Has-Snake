import pygame as pg
import numpy as np
from pyautogui import alert

pg.init()

FPS = 75

SCREENRES = (800, 600)
screen = pg.display.set_mode(SCREENRES)
pg.display.set_caption("Game that have Snake 1.0 Snapshot")

setfps = pg.time.Clock()


class Sprite:
    def __init__(self, x, y, v, direction):
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction

    def move(self):
        if self.direction == 0:
            self.x += self.v
        elif self.direction == 1:
            self.y -= self.v
        elif self.direction == 2:
            self.x -= self.v
        elif self.direction == 3:
            self.y += self.v
        else:
            assert "What the f**k"

        self.x = self.x % SCREENRES[0]
        self.y = self.y % SCREENRES[1]

    def show(self, screen):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, 10, 10))


class Apple(Sprite):
    def __init__(self):
        x = np.random.randint(0, SCREENRES[0])
        y = np.random.randint(0, SCREENRES[1])

        Sprite.__init__(self, x, y, 0, 0)

    def show(self, screen):
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, 8, 8))


head = Sprite(300, 300, 3, 0)
ap = Apple()

score = 0
while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            alert(text="Your final Score is {}".format(score),
                  title="Quit Game")
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                head.direction = 0
            elif event.key == pg.K_UP or event.key == pg.K_w:
                head.direction = 1
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                head.direction = 2
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                head.direction = 3

    if abs(head.x - ap.x) < 10 and abs(head.y - ap.y) < 10:
        ap = Apple()
        score += 1
        print("Score =", score)
        if np.random.randint(0, 100) < 5:
            alert(text="Never gonna give you up, Never gonna let you down",
                  title="Rick Astley Sanjou!")

    head.move()
    ap.show(screen)
    head.show(screen)

    pg.display.flip()
    setfps.tick(FPS)
