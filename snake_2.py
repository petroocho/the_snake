from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс объектов"""

    def __init__(self, body_color=None) -> None:
        """Базовые значения для родительского класса"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        # self.position = self.positions
        # self.body_color = None
        self.border_color = None

    def draw(self) -> None:
        """Отрисовка"""
        raise NotImplementedError


class Snake(GameObject):
    """Класс змейка"""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """Начальные значения змейки"""
        super().__init__(body_color)
        # self.body_color = SNAKE_COLOR
        self.border_color = BORDER_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.get_head_position(), (GRID_SIZE,
                                                           GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращение положения головы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """Движение змейки"""
        x, y = self.get_head_position()
        self.positions.insert(0, ((x + self.direction[0] * GRID_SIZE) %
                                 SCREEN_WIDTH,
                                 (y + self.direction[1] * GRID_SIZE) %
                                 SCREEN_HEIGHT))

        if len(self.position) > self.length:
            self.positions.pop()

    def reset(self) -> None:
        """Сброс змейки"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        ramdon_direction = ([RIGHT, LEFT, UP, DOWN])
        self.direction = choice(ramdon_direction)

    def snake_position(self) -> list(tuple[int, int]):
        """Позиция змейки"""
        return self.positions


class Apple(GameObject):
    """Класс яблоко"""

    def __init__(self, forbidden_position=None) -> None:  # ВЫДАЕТ ОШИБКУ В ТЕСТЕ ПРИ ДОБАВ ПАРАМЕТРА
        """Начальные значения объекта яблоко"""
        super().__init__()
        self.body_color = APPLE_COLOR
        #  forbidden_position = Snake.snake_position(self)
        self.position = self.randomize_position(forbidden_position)

    def randomize_position(self, forbidden_position) -> tuple[int, int]:
        """Случайное расположение объекта яблоко"""
        while True:
            self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                             (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
            if self.position not in forbidden_position:
                break
        return self.position

    def draw(self) -> None:
        """Отрисовка объекта яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная логика программы"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position(snake.positions)
            snake.length += 1

        if snake.get_head_position() in snake.position[1:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
