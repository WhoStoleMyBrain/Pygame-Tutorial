import pygame
import os
pygame.font.init()
pygame.mixer.init()

# game surface / window is created at first
WIDTH, HEIGHT = 900, 500
BORDER_WIDTH, BORDER_HEIGHT = 10, HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect((WIDTH - BORDER_WIDTH) // 2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1  # Syntax for custom events: USEREVENT + X
RED_HIT = pygame.USEREVENT + 2

FPS = 60
VEL = 5

ROTATE_LEFT = 90
ROTATE_RIGHT = -90

RED_HEALTH = 10
YELLOW_HEALTH = 10

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ROTATE_LEFT)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ROTATE_RIGHT)


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), True, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # blit -> draw surface on screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + SPACESHIP_HEIGHT < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + SPACESHIP_WIDTH < HEIGHT:
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + SPACESHIP_HEIGHT < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + SPACESHIP_WIDTH < HEIGHT:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width()//2, HEIGHT // 2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    yellow = pygame.Rect(100, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    clock = pygame.time.Clock()
    yellow_bullets = []
    red_bullets = []
    red_health = RED_HEALTH
    yellow_health = YELLOW_HEALTH
    winner_text = ''
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height - BULLET_HEIGHT) // 2,
                                         BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height - BULLET_HEIGHT) // 2,
                                         BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


if __name__ == '__main__':
    main()
