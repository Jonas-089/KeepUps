import pygame
import random

pygame.init()
myfont = pygame.font.SysFont("Futura", 15)
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("KeepUps")
clock = pygame.time.Clock()

# default: 1.5
gravity = 1.5
# to get higher difficulty lower difficulty variable; default: 4
difficulty = 4
# default: 13
player_vel = 13
keepUps = 0
highScore = 0


def draw(player, ball):
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), (ball.x, ball.y, ball.width, ball.height))
    pygame.draw.rect(window, (0, 0, 255), (player.x, player.y, player.width, player.height))
    keep_ups_display = myfont.render("Score: " + str(keepUps), 1, (0, 0, 0))
    high_score_display = myfont.render("HighScore: " + str(highScore), 1, (0, 0, 0))

    window.blit(keep_ups_display, (100, 100))
    window.blit(high_score_display, (100, 125))
    pygame.display.update()


class Ball:

    def __init__(self, x, y, width, height, ball_vel_x, ball_vel_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ball_vel_x = ball_vel_x
        self.ball_vel_y = ball_vel_y


class Player:

    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel


def hit(player, ball):
    if (player.x < ball.x + ball.width and player.x + player.width > ball.x) and ball.y >= player.y - player.height:
        return True

    return False


# Main Program

run = True
# default: 400, 200, 10, 10, 0, 7
play_ball = ball(400, 200, 10, 10, 0, 7)
# default: 350, 485, 100, 21
player1 = player(350, 485, 100, 21, player_vel)

while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player1.x -= player1.vel

    if keys[pygame.K_RIGHT]:
        player1.x += player1.vel

    # ball updating
    if play_ball.y <= player1.y:
        if hit(player1, play_ball):
            # bounce
            keepUps += 1
            play_ball.ball_vel_y = -play_ball.ball_vel_y
            play_ball.ball_vel_y -= gravity

            # ball direction changes depending on where it hits the player,
            # with a random offset to prevent easy endless highscores
            offset = random.randint(-1,1)
            play_ball.ball_vel_x = -(player1.x - play_ball.x + (player1.width / 2)) / difficulty + offset

    play_ball.ball_vel_y += gravity

    play_ball.y += play_ball.ball_vel_y
    play_ball.x += play_ball.ball_vel_x

    # boundary setting
    if play_ball.x + play_ball.width >= pygame.display.get_surface().get_width() or play_ball.x <= 0:
        play_ball.ball_vel_x = -play_ball.ball_vel_x

    # defines what happens when play_ball is not caught
    # highscore is reset and ball is respawned after reaching a certain depth
    if play_ball.y >= 2000:
        play_ball = ball(400, 200, 10, 10, 0, 7)

        if keepUps > highScore:
            highScore = keepUps

        keepUps = 0

    draw(player1, play_ball)

