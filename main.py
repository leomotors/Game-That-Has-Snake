import pygame as pg
import math

pg.init()

FPS = 75

screen = pg.display.set_mode((800, 600))
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
            self.y += self.v
        elif self.direction == 2:
            self.x -= self.v
        elif self.direction == 3:
            self.y -= self.v
        else:
            assert "What the f**k"

    def show(self, screen):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, 10, 10))


head = Sprite(300, 300, 3, 0)

while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                head.direction = 0
            elif event.key == pg.K_UP:
                head.direction = 1
            elif event.key == pg.K_LEFT:
                head.direction = 2
            elif event.key == pg.K_DOWN:
                head.direction = 3

    head.move()
    head.show(screen)
    pg.display.flip()
    setfps.tick(FPS)
