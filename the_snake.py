from random import randint

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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Определяем базовый класс объектов."""

    def __init__(self, body_color=(255, 255, 255), position=None):
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Прописываем класс Яблока."""

    def randomize_position(self):
        """Определяем координаты Яблока."""
        # Логика случайной позиции
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
        return (x, y)

    def __init__(self):
        start_position = self.randomize_position()
        super().__init__(body_color=APPLE_COLOR, position=start_position)

    def draw(self):
        """Отрисовываем Яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описываем змейку."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Определяем координаты головы змейки."""
        if not self.positions:  # Если список пуст
            return None         # Возвращаем None или какую-то заглушку
        return self.positions[0]

    def move(self):
        """Описание логики движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        head = self.get_head_position()
        new_head = ((head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                    (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
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
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def reset(self):
        """Сброс змейки на стартовую позицию."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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
    """Основная логика игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.move()
        snake.draw()
        apple.draw()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        pygame.display.flip()


if __name__ == '__main__':
    main()
