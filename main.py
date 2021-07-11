import pygame as pg
import numpy as np
from pyautogui import alert
from utils.rickroll import SendToHeaven

# * CONFIG
TICK_RATE = 75
SCREENRES = (800, 600)
BORDER = 10
FONT_SIZE = 22
SCORE_OFFSET = (16, 12)
TIME_OFFSET = (16, SCORE_OFFSET[0] + FONT_SIZE + 6)

BACKGROUND_MUSIC = "Daydream café ~solo piano ver~"
BG_MUSIC_LENGTH = 144

# * SETUP
pg.init()
screen = pg.display.set_mode(SCREENRES)
pg.display.set_caption("Game that have Snake 1.0")
setfps = pg.time.Clock()

font = pg.font.Font("assets/fonts/Prompt-Regular.ttf", FONT_SIZE)


class Music:
    def __init__(self, song_name, song_length):
        try:
            self.music = pg.mixer.Sound(
                "assets/musics/{}.wav".format(song_name))
        except:
            self.music = None
            print("LOAD ERROR: Unable to Load Music")

        self.song_length = song_length
        self.playMusic()
        self.next_play = song_length

    def playMusic(self):
        if self.music is not None:
            self.music.play()

    def CheckEnd(self, tick_passed):
        if tick_passed / TICK_RATE >= self.next_play:
            self.playMusic()
            self.next_play += self.song_length


bg_music = Music(BACKGROUND_MUSIC, BG_MUSIC_LENGTH)
xp_fx = pg.mixer.Sound("assets/sounds/Minecraft XP Sound.wav")


def showScore(score):
    txtSprite = font.render("Current Score : " +
                            str(score), True, (255, 255, 255))
    screen.blit(txtSprite, SCORE_OFFSET)


def showTime(tick):
    txtSprite = font.render(
        "Time Passed : " + "{:.1f}".format(tick/TICK_RATE), True, (255, 255, 255))
    screen.blit(txtSprite, TIME_OFFSET)


class Sprite:
    def __init__(self, x, y, v, direction, size):
        self.x = x
        self.y = y
        self.v = v
        self.direction = direction
        self.size = size

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
            assert "Direction Error!"

        self.x = self.x % SCREENRES[0]
        self.y = self.y % SCREENRES[1]

    def show(self, screen):
        pg.draw.rect(screen, (255, 255, 255),
                     (self.x, self.y, self.size, self.size))


class Apple(Sprite):
    def __init__(self):
        x = np.random.randint(0, SCREENRES[0] - 2 * BORDER) + BORDER
        y = np.random.randint(0, SCREENRES[1] - 2 * BORDER) + BORDER

        Sprite.__init__(self, x, y, 0, 0, 5)

    def show(self, screen):
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, 8, 8))


class SnakeCell(Sprite):
    def __init__(self, x, y, v, direction, size, rank=0):
        Sprite.__init__(self, x, y, v, direction, size)
        self.rank = rank
        self.next = None
        self.order = []

    def changeDirection(self, direction):
        if self.direction == direction or (self.direction == 0 and direction == 2) or (self.direction == 1 and direction == 3) or (self.direction == 2 and direction == 0) or (self.direction == 3 and direction == 1):
            return
        self.direction = direction

        if self.next is not None:
            self.next.order.append([direction, self.size])

    def processOrder(self):
        lastorder = self.order[0]
        lastorder[1] -= self.v

        if lastorder[1] <= 0:
            self.changeDirection(lastorder[0])
            del self.order[0]

    def update(self, screen):
        self.move()
        self.show(screen)
        self.fixAlignment()

        if len(self.order) > 0:
            self.processOrder()

        if self.next is not None:
            self.next.update(screen)

    def grow(self):
        if self.next is not None:
            self.next.grow()
        else:
            if self.direction == 0:
                dx = -self.size
                dy = 0
            elif self.direction == 1:
                dx = 0
                dy = self.size
            elif self.direction == 2:
                dx = self.size
                dy = 0
            elif self.direction == 3:
                dx = 0
                dy = -self.size
            else:
                assert "Direction Error!"

            self.next = SnakeCell(self.x+dx, self.y+dy,
                                  self.v, self.direction, self.size)

    def checkCollision(self, tocheck=None):
        if tocheck is None:
            if self.next is None:
                return False
            return self.next.checkCollision(self)

        if abs(self.x - tocheck.x) < 5 and abs(self.y - tocheck.y) < 5:
            return True

        if self.next is not None:
            return self.next.checkCollision(tocheck)

        return False

    def fixAlignment(self):
        if self.next is not None:
            if self.direction == self.next.direction:
                if self.direction == 0 or self.direction == 2:
                    if abs(self.y - self.next.y) < self.size/2:
                        self.next.y = self.y
                if self.direction == 1 or self.direction == 3:
                    if abs(self.x - self.next.x) < self.size/2:
                        self.next.x = self.x


head = SnakeCell(300, 300, 2, 0, 10)
ap = Apple()

# * GAME LOOP
score = 0
tick_passed = 0
while True:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.mixer.stop()
            alert(text="Your final Score is {}\nTime used : {:.1f}".format(score, (tick_passed/TICK_RATE)),
                  title="Quit Game")
            pg.quit()
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                head.changeDirection(0)
            elif event.key == pg.K_UP or event.key == pg.K_w:
                head.changeDirection(1)
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                head.changeDirection(2)
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                head.changeDirection(3)

    if abs(head.x - ap.x) < 10 and abs(head.y - ap.y) < 10:
        ap = Apple()
        score += 1
        head.grow()
        xp_fx.play()

    ap.show(screen)
    head.update(screen)
    showScore(score)
    showTime(tick_passed)

    if head.checkCollision():
        SendToHeaven()
        pg.mixer.stop()
        alert(text="Your final Score is {}\nTime used : {:.1f}".format(
            score, (tick_passed/TICK_RATE)), title="Game Over!")
        pg.quit()
        break

    bg_music.CheckEnd(tick_passed)

    pg.display.flip()
    tick_passed += 1
    setfps.tick(TICK_RATE)
