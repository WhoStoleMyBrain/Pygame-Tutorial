import pygame
import os

from settings import Settings

pygame.font.init()
pygame.mixer.init()

game_settings = Settings()

pygame.display.set_caption(game_settings.TITLE)


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    # WIN.fill(WHITE)
    game_settings.WIN.blit(game_settings.SPACE, (0, 0))
    pygame.draw.rect(game_settings.WIN, game_settings.BLACK, game_settings.BORDER)
    red_health_text = game_settings.HEALTH_FONT.render("Health:" + str(red_health), True, game_settings.WHITE)
    yellow_health_text = game_settings.HEALTH_FONT.render("Health:" + str(yellow_health), True, game_settings.WHITE)
    game_settings.WIN.blit(red_health_text, (game_settings.WIDTH - red_health_text.get_width() - 10, 10))
    game_settings.WIN.blit(yellow_health_text, (10, 10))
    game_settings.WIN.blit(game_settings.YELLOW_SPACESHIP, (yellow.x, yellow.y))  # blit -> draw surface on screen
    game_settings.WIN.blit(game_settings.RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(game_settings.WIN, game_settings.RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(game_settings.WIN, game_settings.YELLOW, bullet)
    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - game_settings.VEL > 0:
        yellow.x -= game_settings.VEL
    if keys_pressed[pygame.K_d] and yellow.x + game_settings.VEL + game_settings.SPACESHIP_HEIGHT < \
            game_settings.BORDER.x:
        yellow.x += game_settings.VEL
    if keys_pressed[pygame.K_w] and yellow.y - game_settings.VEL > 0:
        yellow.y -= game_settings.VEL
    if keys_pressed[pygame.K_s] and yellow.y + game_settings.VEL + game_settings.SPACESHIP_WIDTH < game_settings.HEIGHT:
        yellow.y += game_settings.VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - game_settings.VEL > game_settings.BORDER.x:
        red.x -= game_settings.VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + game_settings.VEL + game_settings.SPACESHIP_HEIGHT < \
            game_settings.WIDTH:
        red.x += game_settings.VEL
    if keys_pressed[pygame.K_UP] and red.y - game_settings.VEL > 0:
        red.y -= game_settings.VEL
    if keys_pressed[pygame.K_DOWN] and red.y + game_settings.VEL + game_settings.SPACESHIP_WIDTH < game_settings.HEIGHT:
        red.y += game_settings.VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += game_settings.BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(game_settings.RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > game_settings.WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= game_settings.BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(game_settings.YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = game_settings.WINNER_FONT.render(text, True, game_settings.WHITE)
    game_settings.WIN.blit(draw_text, (game_settings.WIDTH // 2 - draw_text.get_width() // 2,
                                       game_settings.HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, game_settings.SPACESHIP_HEIGHT, game_settings.SPACESHIP_WIDTH)
    yellow = pygame.Rect(100, 300, game_settings.SPACESHIP_HEIGHT, game_settings.SPACESHIP_WIDTH)
    clock = pygame.time.Clock()
    yellow_bullets = []
    red_bullets = []
    red_health = game_settings.RED_HEALTH
    yellow_health = game_settings.YELLOW_HEALTH
    winner_text = ''
    run = True
    while run:
        clock.tick(game_settings.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < game_settings.MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y +
                                         (yellow.height - game_settings.BULLET_HEIGHT) // 2,
                                         game_settings.BULLET_WIDTH, game_settings.BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    game_settings.BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < game_settings.MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height - game_settings.BULLET_HEIGHT) // 2,
                                         game_settings.BULLET_WIDTH, game_settings.BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    game_settings.BULLET_FIRE_SOUND.play()

            if event.type == game_settings.RED_HIT:
                red_health -= 1
                game_settings.BULLET_HIT_SOUND.play()

            if event.type == game_settings.YELLOW_HIT:
                yellow_health -= 1
                game_settings.BULLET_HIT_SOUND.play()

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
