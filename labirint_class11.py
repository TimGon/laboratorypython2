import random
import pygame

class Labyrinth:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.border = 5
        self.width_line = 40
        self.width_wall = 5
        self.color_bg = (255, 255, 255)
        self.color_wall = (0, 0, 0)
        self.color_player = (0, 0, 255)
        self.color_start = (0, 255, 0)
        self.color_finish = (255, 0, 0)
        self.trace = False
        self.color_trace = self.color_player
        self.width_window = ((self.width * 2 - 1) // 2 + 1) * self.width_line + ((self.width * 2 - 1) // 2) * self.width_wall + self.border * 2
        self.height_window = ((self.height * 2 - 1) // 2 + 1) * self.width_line + ((self.height * 2 - 1) // 2) * self.width_wall + self.border * 2
        self.score = 0
        self.matrix_base = []
        self.start = self.generate_start_point(self.width, self.height)
        self.finish = self.generate_finish_point(self.start, self.width, self.height)
        self.player = list(self.start)
        self.running = True

        pygame.init()
        self.window = pygame.display.set_mode((self.width_window, self.height_window))
        pygame.display.set_caption("Лабиринт")
        self.font = pygame.font.Font(None, 25)


    def generate_start_point(self, n, m):
        """Функция выбора точки начала лабиринта"""
        sides = [(0, random.randint(0, m - 1)),  # Top
                 (n - 1, random.randint(0, m - 1)),  # Bottom
                 (random.randint(0, n - 1), 0),  # Left
                 (random.randint(0, n - 1), m - 1)]  # Right

        return random.choice(sides)

    def generate_finish_point(self, start, n, m):
        """Выбор точки конца лабиринта"""
        return n - 1 - start[0], m - 1 - start[1]

    def transition_choice(self, x, y, rm):
        """Выбирает следующий ход в генерации лабиринта."""
        possible_moves = [
            (x - 1, y) if x > 0 and not rm[x - 1][y] else None,
            (x + 1, y) if x < len(rm) - 1 and not rm[x + 1][y] else None,
            (x, y - 1) if y > 0 and not rm[x][y - 1] else None,
            (x, y + 1) if y < len(rm[0]) - 1 and not rm[x][y + 1] else None,
        ]

        possible_moves = [move for move in possible_moves if move]  # Удаляем None

        if possible_moves:
            nx, ny = random.choice(possible_moves)
            tx = x * 2 + (1 if nx > x else -1 if nx < x else 0)
            ty = y * 2 + (1 if ny > y else -1 if ny < y else 0)
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1

    def create_labyrinth(self):
        """Генерация лабиринта"""
        rm = [] # матрица достижимости
        for i in range(self.width):  # создание и заполнение матрицы достижимости
            rm.append([])
            for j in range(self.height):
                rm[i].append(False)
        tm = []
        for i in range(self.width * 2 - 1):  # создание и заполнение матрицы переходов
           tm.append([])
           for j in range(self.height * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    tm[i].append(True)
                else:
                    tm[i].append(False)
        list_transition = [self.start]
        x, y = self.start
        rm[x][y] = True
        x, y, tx, ty = self.transition_choice(x, y, rm)
        for i in range(1, self.height * self.width):
            while not (x >= 0 and y >= 0):
                x, y = list_transition[-1]
                list_transition.pop()
                x, y, tx, ty = self.transition_choice(x, y, rm)
            rm[x][y] = True
            list_transition.append((x, y))
            tm[tx][ty] = True
            x, y, tx, ty = self.transition_choice(x, y, rm)

        return tm, self.start, self.finish  # возвращаем матрицу проходов и начальную с конечной точками

    def draw_labyrinth(self, matrix, start, finish, color_start=(0, 255, 0), color_finish=(255, 0, 0)):
        """Рисование лабиринта"""

        width = (len(matrix) // 2 + 1) * self.width_line + (len(matrix) // 2) * self.width_wall + self.border * 2
        height = (len(matrix[0]) // 2 + 1) * self.width_line + (len(matrix[0]) // 2) * self.width_wall + self.border * 2
        for i in range(width):
            for j in range(height):
                if i < self.border or width - i <= self.border or j < self.border or height - j <= self.border:  # отображение границ лабиринта
                    pygame.draw.line(self.window, self.color_wall, [i, j], [i, j], 1)
                else:
                    if (i - self.border) % (self.width_line + self.width_wall) <= self.width_line:
                        x = (i - self.border) // (self.width_line + self.width_wall) * 2
                    else:
                        x = (i - self.border) // (self.width_line + self.width_wall) * 2 + 1
                    if (j - self.border) % (self.width_line + self.width_wall) <= self.width_line:
                        y = (j - self.border) // (self.width_line + self.width_wall) * 2
                    else:
                        y = (j - self.border) // (self.width_line + self.width_wall) * 2 + 1
                    if matrix[x][y]:
                        pygame.draw.line(self.window, self.color_bg, [i, j], [i, j], 1)
                    else:
                        pygame.draw.line(self.window, self.color_wall, [i, j], [i, j], 1)
        pygame.draw.rect(self.window, color_start, (
            self.border + start[0] * (self.width_line + self.width_wall), self.border + start[1] * (self.width_line + self.width_wall), self.width_line,
            self.width_line))
        pygame.draw.rect(self.window, color_finish, (
            self.border + finish[0] * (self.width_line + self.width_wall), self.border + finish[1] * (self.width_line + self.width_wall),
            self.width_line,
            self.width_line))
    def delete_player(self):
        """Функция удаления игрока при движении и оставления следов"""
        if (self.player[0], self.player[1]) == self.start:
            pygame.draw.circle(self.window, self.color_start, (self.border + self.player[0] * (self.width_line + self.width_wall) + self.width_line // 2,
                                                     self.border + self.player[1] * (self.width_line + self.width_wall) + self.width_line // 2),
                               self.width_line // 2 - 3)
        else:
            pygame.draw.circle(self.window, self.color_bg, (self.border + self.player[0] * (self.width_line + self.width_wall) + self.width_line // 2,
                                                   self.border + self.player[1] * (self.width_line + self.width_wall) + self.width_line // 2),
                               self.width_line // 2 - 3)
        if self.trace:
            pygame.draw.circle(self.window, self.color_trace, (self.border + self.player[0] * (self.width_line + self.width_wall) + self.width_line // 2,
                                                     self.border + self.player[1] * (self.width_line + self.width_wall) + self.width_line // 2),
                               self.width_line // 3 - 3)


    def draw_player(self):
        """Отрисовка игрока на экране"""
        pygame.draw.circle(self.window, self.color_player, (self.border + self.player[0] * (self.width_line + self.width_wall) + self.width_line // 2,
                                                  self.border + self.player[1] * (self.width_line + self.width_wall) + self.width_line // 2),
                           self.width_line // 2 - 3)
    def new_game(self):
        pygame.draw.rect(self.window, (0, 0, 0), (0, self.height_window - 70, self.width_window, 70))
        matrix, start, finish = self.create_labyrinth()
        k = 0
        while matrix in self.matrix_base or start[0] == finish[0] or start[1] == finish[1]:
            matrix, start, finish = self.create_labyrinth()
            k += 1
            if k > 20:
                print('Не найдено лабиринтов без повторения')
                break
        self.matrix_base.append(matrix)
        self.player = list(start)
        self.draw_labyrinth(matrix, start, finish)
        self.draw_player()
    def setting_trace(self):
        """Изменение флага оставления следов"""
        if self.trace:
            self.trace = False
        else:
            self.trace = True

    def click_RIGHT(self, m):
        """Движение вправо"""
        if len(m) > self.player[0] * 2 + 2:
            if m[self.player[0] * 2 + 1][self.player[1] * 2]:
                self.player[0] += 1

    def click_LEFT(self, m):
        """Движение влево"""
        if -1 < self.player[0] * 2 - 2:
            if m[self.player[0] * 2 - 1][self.player[1] * 2]:
                self.player[0] -= 1

    def click_DOWN(self, m):
        """Движение вниз"""
        if len(m[0]) > self.player[1] * 2 + 2:
            if m[self.player[0] * 2][self.player[1] * 2 + 1]:
                self.player[1] += 1

    def click_UP(self, m):
        """Движение вверх"""
        if -1 < self.player[1] * 2 - 2:
            if m[self.player[0] * 2][self.player[1] * 2 - 1]:
                self.player[1] -= 1
    def game_interface(self):
        runing_interface = True
        while runing_interface:
            pygame.init()
            self.window.fill((1, 50, 32))
            title_text = self.font.render("Начать игру лабиринт?", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(width+210, height+100 ))
            self.window.blit(title_text, title_rect)

            # Кнопка "Начать"
            start_button_color = (0, 255, 0)  # Зеленый
            start_button_rect = pygame.Rect(width+100, height+150, width+200, 50)
            pygame.draw.rect(self.window, start_button_color, start_button_rect)
            start_text = self.font.render("Начать", True, (0, 0, 0))
            start_text_rect = start_text.get_rect(center=start_button_rect.center)
            self.window.blit(start_text, start_text_rect)

            # Кнопка "Выход"
            quit_button_color = (255, 0, 0)  # Красный
            quit_button_rect = pygame.Rect(width+100 , height+250, width+200 , 50)  # Расстояние
            pygame.draw.rect(self.window, quit_button_color, quit_button_rect)
            quit_text = self.font.render("Выход", True, (0, 0, 0))
            quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
            self.window.blit(quit_text, quit_text_rect)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing_interface = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        self.run()
                        runing_interface=False
                        self.running = True
                    elif quit_button_rect.collidepoint(event.pos):
                        runing_interface = False
                        pygame.quit()
    def run(self):
        matrix, start, finish = self.create_labyrinth()
        k = 0
        while matrix in self.matrix_base or start[0] == finish[0] or start[1] == finish[1]:
            k += 1
            if k > 20:
                print('Не найдено лабиринтов без повторения')
                break
            matrix, start, finish = self.create_labyrinth()
        self.matrix_base.append(matrix)
        self.player = list(start)
        self.draw_labyrinth(matrix, start, finish)
        while self.running:
            self.delete_player()
            if tuple(self.player) == self.finish:
                self.window.fill((0, 0, 0))
                pygame.draw.rect(self.window, (0, 0, 0), (0, self.height_window - 70, self.width_window, 70))
                matrix, start, finish = self.create_labyrinth()
                k = 0
                while matrix in self.matrix_base or start[0] == finish[0] or start[1] == finish[1]:
                    matrix, start, finish = self.create_labyrinth()
                    k += 1
                    if k > 20:
                        print("Количество", k)
                        print('Не найдено лабиринтов без повторения')
                        break
                self.matrix_base.append(matrix)
                self.player = list(start)
                self.draw_labyrinth(matrix,start,finish)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.click_RIGHT(matrix)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.click_LEFT(matrix)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.click_UP(matrix)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.click_DOWN(matrix)
                    if event.key == pygame.K_p:
                        pass
                    if event.key == pygame.K_q:
                        self.setting_trace()
                    if event.key == pygame.K_r:
                        self.new_game()
                    if event.key == pygame.K_e:
                        self.player[0] = self.start[0]
                        self.player[1] = self.start[1]
                    if (self.player[0], self.player[1]) == (self.finish[0], self.finish[1]):
                        font = pygame.font.Font(None, 74)
                        text = font.render("Вы победили!", True, (0, 255, 0))
                        text_rect = text.get_rect(center=(
                        self.window.get_width() // 2, self.window.get_height() // 2))
                        self.window.blit(text, text_rect)
                        pygame.display.update()
                        pygame.time.delay(1000)
                        self.game_interface()
                        self.runing = False
                        pygame.display.update()
            self.draw_player()
            pygame.display.update()

"""Переменные"""
width = 10
height = 10

game = Labyrinth(width, height)
game.game_interface()