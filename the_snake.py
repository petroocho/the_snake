from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (255, 255, 255)

# Цвет бустера
BOOSTER_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
# SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс"""

    def __init__(self, color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = BOARD_BACKGROUND_COLOR

    def randomize_position(self):
        """Рандомное появление на игровом поле
        дочерних классов (Apple, Stone, Booster)
        """
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (position_x, position_y)
        # while True:
        #     position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        #     position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        #     object_position = (position_x, position_y)
        #     if object_position not in snake_position:
        #         self.position = object_position
        #         break

    def draw(self):
        """Отрисовка камнtq на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Отрисовка яблочка"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
    # def randomize_position(self):
    #     position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
    #     position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    #     self.position = (position_x, position_y)

    # def draw(self):
    #     """Метод отрисовывает яблочко на игровом поле"""
    #     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
    #     pygame.draw.rect(screen, self.body_color, rect)
    #     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Отрисовка камней"""

    def __init__(self):
        self.type = 'stone'
        super().__init__()
        self.body_color = STONE_COLOR
        self.randomize_position()


class Booster(GameObject):
    """Отрисовка бустеров"""

    def __init__(self):
        self.type = 'booster'
        super().__init__()
        self.body_color = BOOSTER_COLOR
        self.randomize_position()


class Snake(GameObject):
    """Поведение змейки на игровом поле"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (1, 0)
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления змейки после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки по игровому полю"""
        head_position_x, head_position_y = Snake.get_head_position(self)
        dx, dy = self.direction
        new_head_position = (
            (head_position_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.last = self.positions[-1]
        self.positions = [new_head_position] + self.positions  # [:self.length - 1]

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает положение змейки на игровом поле"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """Сброс игры при столкновении змейки со своим телом"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = (1, 0)

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]


def handle_keys(game_object):
    """Управление змейкой с клавиатуры"""
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


def main():
    """Вся логика игры"""
    # Инициализация PyGame:
    pygame.init()
    # Создаем объекты классов на игровом поле.
    objects = []
    objects_spawn = 0
    apple = Apple()
    snake = Snake()
    apple.randomize_position()

    # Цикл игры.
    while True:
        SPEED = 5 + len(snake.positions) // 5  # Увеличение скорости змейки.

        if len(snake.positions) // 3 > objects_spawn:
            new_object = choice([Stone(), Booster()])
            new_object.randomize_position()
            while new_object.position in snake.position:
                new_object.randomize_position()
            objects.append(new_object)
            objects_spawn += 1

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Нарастание змейки при столкновении с яблочком.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        while apple.position in snake.position:
            del apple
            apple = Apple()
            apple.randomize_position()

        # Если змейка коснулась своего тела игра сбрасывается
        if snake.get_head_position() in snake.positions[1:]:
            pygame.time.delay(600)
            snake.reset()
            objects.clear()
            apple.randomize_position()
            objects_spawn = 0

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        for object in objects:
            object.draw()
            if snake.get_head_position() == object.position:
                if object.type == 'stone':
                    pygame.time.delay(600)
                    snake.reset()
                    objects.clear()
                    apple.randomize_position()
                    objects_spawn = 0
                if object.type == 'booster':
                    snake.length += 2
                    objects.remove(object)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
