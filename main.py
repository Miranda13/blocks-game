import pygame
import sys
import random
import time

pygame.init()

# Configuración de la pantalla
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Eliminación de Bloques")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Jugador
player_width = 50
player_height = 20
player_x = (width - player_width) // 2
player_y = height - 2 * player_height

player_speed_x = 5
player_speed_y = 5

block_width = 50
block_height = 20
block_radius = 15
block_speed = 5
blocks = []

score = 0

def generate_blocks():
    blocks.clear()
    for i in range(5):
        block_x = random.randint(0, width - block_width)
        block_y = random.randint(50, 200)
        blocks.append([block_x, block_y])

generate_blocks()

clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, white, [x, y, player_width, player_height])

def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, red, block + [block_width, block_height])

def draw_round_blocks():
    for block in blocks:
        pygame.draw.circle(screen, red, (block[0] + block_width // 2, block[1] + block_height // 2), block_radius)

def show_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntuación: {score}", True, white)
    screen.blit(score_text, (10, 10))

def game():
    global player_x, player_y, score

    rectangular_blocks = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    rectangular_blocks = not rectangular_blocks
                    generate_blocks()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed_x
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed_x
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed_y
        if keys[pygame.K_DOWN] and player_y < height - player_height:
            player_y += player_speed_y

        for block in blocks:
            if (
                player_x < block[0] + block_width
                and player_x + player_width > block[0]
                and player_y < block[1] + block_height
                and player_y + player_height > block[1]
            ):
                blocks.remove(block)
                penalty = int(pygame.time.get_ticks() / 1000)
                score += max(0, 10 - penalty)

        screen.fill(black)
        draw_player(player_x, player_y)

        if rectangular_blocks:
            draw_blocks()
        else:
            draw_round_blocks()

        show_score()
        pygame.display.flip()

        if not blocks:
            print("¡Felicidades! Has eliminado todos los bloques.")
            time.sleep(1)
            pygame.quit()
            sys.exit()

        clock.tick(60)

game()
