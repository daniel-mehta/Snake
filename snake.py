import pygame
import random

# Initialize pygame
pygame.init()

# Color Definitions
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Display Settings
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400
BORDER = 5
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Snake Game')

# Game Settings
CLOCK = pygame.time.Clock()
SNAKE_BLOCK = 10
SNAKE_SPEED = 10

# Fonts
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)

def generate_food():
    """Generate a random food position."""
    return (
        round(random.randrange(BORDER, DISPLAY_WIDTH - BORDER - SNAKE_BLOCK) / 10.0) * 10.0,
        round(random.randrange(BORDER, DISPLAY_HEIGHT - BORDER - SNAKE_BLOCK) / 10.0) * 10.0
    )

def display_score(score):
    value = SCORE_FONT.render("Your Score: " + str(score), True, YELLOW)
    DISPLAY.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(DISPLAY, BLACK, [x[0], x[1], snake_block, snake_block])

def display_message(msg, color):
    mesg = FONT_STYLE.render(msg, True, color)
    DISPLAY.blit(mesg, [DISPLAY_WIDTH / 6, DISPLAY_HEIGHT / 3])

def game_loop():
    game_over = False
    game_close = False

    x = DISPLAY_WIDTH / 2
    y = DISPLAY_HEIGHT / 2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx, foody = generate_food()
    speed = SNAKE_SPEED

    while not game_over:
        while game_close:
            DISPLAY.fill(BLUE)
            display_message("You Lost! Press C-Play Again or Q-Quit", RED)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    x_change, y_change = {
                        pygame.K_LEFT: (-SNAKE_BLOCK, 0),
                        pygame.K_RIGHT: (SNAKE_BLOCK, 0),
                        pygame.K_UP: (0, -SNAKE_BLOCK),
                        pygame.K_DOWN: (0, SNAKE_BLOCK)
                    }[event.key]

        x += x_change
        y += y_change
        DISPLAY.fill(BLUE)

        # Draw boundary
        pygame.draw.rect(DISPLAY, RED, [0, 0, DISPLAY_WIDTH, BORDER])
        pygame.draw.rect(DISPLAY, RED, [0, DISPLAY_HEIGHT - BORDER, DISPLAY_WIDTH, BORDER])
        pygame.draw.rect(DISPLAY, RED, [0, 0, BORDER, DISPLAY_HEIGHT])
        pygame.draw.rect(DISPLAY, RED, [DISPLAY_WIDTH - BORDER, 0, BORDER, DISPLAY_HEIGHT])

        pygame.draw.rect(DISPLAY, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(snake_length - 1)
        pygame.display.update()

        if x == foodx and y == foody:
            foodx, foody = generate_food()
            snake_length += 1
            speed += 0.5  # Increase speed

        CLOCK.tick(speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()
