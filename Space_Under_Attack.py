import pygame
import random
import math
from pygame import mixer

# Background sound
# mixer.music.load("")
# mixer.music.play(-1)


# initialize the pygame
pygame.init()

scn = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Under Attack")
icon = pygame.image.load("solar-system.png")
pygame.display.set_icon(icon)
# background image
background = pygame.image.load("background.png")

# Scores
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
over_font = pygame.font.Font("freesansbold.ttf", 70)
text_x = 10
text_y = 10


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    scn.blit(score, (x, y))


# spaceship
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 500
playerChangeX = 0
playerChangeY = 0

# enemy
cnt_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
for i in range(cnt_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyChangeX.append(0.2)
    enemyChangeY.append(40)

# Bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletchangeX = 0
bulletchangeY = 0.8
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    scn.blit(bulletimg, (x + 16, y + 10))


def player(x, y):
    scn.blit(playerImg, (x, y))


def enemy(x, y, i):
    scn.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))

    if distance < 27:
        return True

    return False


# Game Over text
def game_over_text(x, y):
    over_text = font.render("GAME OVER !!", True, (255, 255, 255))
    scn.blit(over_text, (x, y))


# Game loop
running = True
while running:
    scn.fill((0, 0, 0))
    # Background image
    scn.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # to check whether keystroke is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerChangeX = -0.3
            if event.key == pygame.K_RIGHT:
                playerChangeX = 0.3
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("bullet_sound.wav")
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChangeX = 0

    # setting up boundaries for space-ship
    if playerX + playerChangeX <= 0:
        playerChangeX = 0
    elif playerX + playerChangeX >= 736:
        playerChangeX = 0

    # setting up movements of enemy
    for i in range(cnt_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(cnt_of_enemies):
                enemyY[j] = 2000
            game_over_text(300, 250)
            break
        if enemyX[i] + enemyChangeX[i] <= 0:
            enemyChangeX[i] = 0.2
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] + enemyChangeX[i] >= 736:
            enemyChangeX[i] = -0.2
            enemyY[i] += enemyChangeY[i]

        enemyX[i] += enemyChangeX[i]
        # Collision Concept
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Explosion sound
            # explosion_sound = mixer.Sound("")
            # explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 737)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletchangeY

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    playerX += playerChangeX
    player(playerX, playerY)
    show_score(text_x, text_y)
    pygame.display.update()
