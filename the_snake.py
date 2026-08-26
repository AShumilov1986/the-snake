from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка (для выхода из игры нажми клавишу ESC)')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Определяем базовый класс объектов."""

    def __init__(self, body_color=(255, 255, 255), position=None):
        self.position = position or SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""


class Apple(GameObject):
    """Опрекделяем класс яблока"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()  # в начале игры проверка не обязательна

    def _generate_random_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def randomize_position(self, snake_positions=None):
        """Генерируем координаты яблока и проверяем на совпадение со змейкой"""
        if snake_positions is None:
            self.position = self._generate_random_position()
            return
        while True:
            x, y = self._generate_random_position()
            if (x, y) not in snake_positions:
                self.position = (x, y)
                return

    def draw(self):
        """Отрисовываем Яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описываем змейку."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.direction = RIGHT
        self.reset()

    def get_head_position(self):
        """Определяем координаты головы змейки."""
        if not self.positions:  # Если список пуст
            return None         # Возвращаем None или какую-то заглушку
        return self.positions[0]

    def move(self):
        """Описание логики движения змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = ((head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Смена направления движения змейки от нажатия клавиш."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовываем змейку."""
        for position in self.positions[1:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """Сброс змейки на стартовую позицию."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Основная логика игры."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.move()
        snake.draw()
        apple.draw()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake_positions=snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            snake.direction = choice([UP, DOWN, LEFT, RIGHT])
            apple.randomize_position(snake_positions=snake.positions)
        pg.display.flip()


if __name__ == '__main__':
    main()
