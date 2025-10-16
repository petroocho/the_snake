from random import choice, randint

import pygame as pg

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

# Скорость по умолчанию.
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(
    'Змейка. Для выхода нажмите ESC. Изменить скорость - W/S.'
)

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс."""

    def __init__(self, body_color=None) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw_cell(self, position, fill_color, border_color=None):
        """Рисует объекты с переданными параметрами."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, fill_color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Базовый метод отрисовки.

        Должен быть переопределен в дочерних классах.
        """
        raise NotImplementedError('Метод draw() должен быть переопределён.')


class Apple(GameObject):
    """Отрисовка объектов в зависимости от цвета."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None):
        super().__init__(body_color)
        self.randomize_position(occupied_cells or [])

    def randomize_position(self, occupied_cells):
        """Рандомное появление на игровом поле (Apple, Stone, Booster)."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовка объектов на игровом поле."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Поведение змейки на игровом поле."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self, direction):
        """Обновление направления змейки после нажатия на кнопку."""
        self.direction = direction

    def move(self):
        """Метод движения змейки по игровому полю."""
        head_position_x, head_position_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = (
            (head_position_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Рисует голову стирает хвост."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сброс игры при столкновении змейки со своим телом."""
        self.last = None
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])

    def get_head_position(self):
        """Возвращает положение головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Управление змейкой с клавиатуры."""
    for event in pg.event.get():
        global SPEED
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_w:
                SPEED += 1
            elif event.key == pg.K_s:
                SPEED = max(5, SPEED - 1)


def main():
    """Вся логика игры."""
    # Инициализация pg:
    pg.init()
    # Создаем объекты классов на игровом поле.
    snake = Snake()
    occupied_cells = list(snake.positions)
    apple = Apple(APPLE_COLOR, occupied_cells)
    stone = Apple(STONE_COLOR, occupied_cells)
    booster = Apple(BOOSTER_COLOR, occupied_cells)

    def reset_game():
        snake.reset()
        occupied_cells = list(snake.positions)
        apple.randomize_position(occupied_cells)
        occupied_cells.append(apple.position)
        stone.randomize_position(occupied_cells)
        occupied_cells.append(stone.position)
        booster.randomize_position(occupied_cells)
        occupied_cells.append(booster.position)
        return occupied_cells
    occupied_cells = reset_game()

    # Цикл игры.
    while True:
        handle_keys(snake)
        snake.move()
        # Нарастание змейки при столкновении с яблочком.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_cells)
            occupied_cells.append(apple.position)
            if snake.length % 3 == 0:
                new_object = choice([stone, booster])
                if new_object == stone:
                    stone.randomize_position(occupied_cells)
                    occupied_cells.append(stone.position)
                    stone.draw()
                else:
                    booster.randomize_position(occupied_cells)
                    occupied_cells.append(booster.position)
                    booster.draw()

        elif snake.get_head_position() == booster.position:
            snake.length += 2
            booster.randomize_position(occupied_cells)
            occupied_cells.append(booster.position)

        # Если змейка коснулась своего тела игра сбрасывается
        elif (
            snake.get_head_position() in snake.positions[4:]
            or snake.get_head_position() == stone.position
        ):
            screen.fill(BOARD_BACKGROUND_COLOR)
            occupied_cells = reset_game()
            continue

        snake.draw()
        apple.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
