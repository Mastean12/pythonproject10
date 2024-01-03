import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 15
SNAKE_SIZE = 20
FOOD_SIZE = 20
BIG_FOOD_SIZE = 50
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * SNAKE_SIZE)) % WIDTH), (cur[1] + (y * SNAKE_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for i, p in enumerate(self.positions):
            pygame.draw.rect(surface, self.color, (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE))
            if i == 0:
                pygame.draw.rect(surface, BLUE, (p[0] + SNAKE_SIZE // 2 - 5, p[1] + SNAKE_SIZE // 2 - 5, 10, 10))


# Food class
class Food:
    def __init__(self, big=False):
        self.position = (0, 0)
        self.color = RED
        self.size = BIG_FOOD_SIZE if big else FOOD_SIZE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH - self.size) // self.size) * self.size,
                         random.randint(0, (HEIGHT - self.size) // self.size) * self.size)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size))


# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()
    big_food = None

    score = 0
    highest_score = 0
    bonus_score = 20
    bonus_activated = False

    font = pygame.font.SysFont(None, 36)

    running = False
    paused = False
    game_over = False

    start_button = pygame.Rect(300, 200, 200, 50)
    new_game_button = pygame.Rect(300, 300, 200, 50)
    start_new_game = False

    food_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == pygame.K_SPACE:
                    if not running and not game_over:
                        running = True
                        start_new_game = False
                    elif game_over:
                        running = True
                        game_over = False
                        start_new_game = True
                        score = 0
                        food_counter = 0
                    else:
                        paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if not running and not game_over:
                        running = True
                        start_new_game = False
                    elif game_over:
                        running = True
                        game_over = False
                        start_new_game = True
                        score = 0
                        food_counter = 0
                    else:
                        paused = not paused

                elif new_game_button.collidepoint(event.pos):
                    if game_over:
                        running = True
                        game_over = False
                        start_new_game = True
                        score = 0
                        food_counter = 0

        if running and not paused:
            snake.update()
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food_counter += 1
                if food_counter >= 5:
                    big_food = Food(big=True)

                    food_counter = 0
                if score == bonus_score:
                    score += bonus_score
                    bonus_activated = True
                    bonus_score += 20
                if score > highest_score:
                    highest_score = score
                food.randomize_position()

            if bonus_activated and big_food.position[0] <= snake.get_head_position()[0] <= big_food.position[0] + BIG_FOOD_SIZE \
                    and big_food.position[1] <= snake.get_head_position()[1] <= big_food.position[1] + BIG_FOOD_SIZE:
                snake.length += 3
                bonus_activated = False

            if (
                snake.get_head_position()[0] < 0
                or snake.get_head_position()[0] >= WIDTH
                or snake.get_head_position()[1] < 0
                or snake.get_head_position()[1] >= HEIGHT
            ):
                game_over = True
                running = False

            surface.fill((0, 0, 0))
            snake.render(surface)
            food.render(surface)
            if big_food:
                big_food.render(surface)

            screen.blit(surface, (0, 0))
            score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
            highest_score_text = font.render("Highest Score: {}".format(highest_score), True, (255, 255, 255))
            screen.blit(score_text, (5, 5))
            screen.blit(highest_score_text, (5, 35))

        elif not running and not start_new_game:
            pygame.draw.rect(screen, (0, 0, 255), start_button)
            start_text = font.render("Start", True, (255, 255, 255))
            screen.blit(start_text, (start_button.x + 20, start_button.y + 15))

        elif not running and start_new_game:
            pygame.draw.rect(screen, (0, 0, 255), new_game_button)
            new_game_text = font.render("Start a New Game", True, (255, 255, 255))
            screen.blit(new_game_text, (new_game_button.x + 20, new_game_button.y + 15))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()


