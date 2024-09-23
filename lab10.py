import tkinter as tk
import random
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Крестики-нолики")

        self.board = [['' for _ in range(3)] for _ in range(3)] # Игровое поле
        self.current_player = 'X' # Начало игры с крестиков
        self.game_over = False

        # Создание игрового поля
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20, padx=20)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.frame,
                    text="",
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j)

        # Кнопка "Новая игра"
        self.new_game_button = tk.Button(
            master,
            text="Новая игра",
            command=self.new_game
        )
        self.new_game_button.pack(pady=20, padx=20)

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return # Если игра окончена или клетка занята, игнорируем

        self.buttons[row][col].config(text=self.current_player)
        self.board[row][col] = self.current_player

        if self.check_win():
            self.game_over = True
            self.show_result(f"{self.current_player} победил!")
        elif self.check_draw():
            self.game_over = True
            self.show_result("Ничья!")
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.computer_move() # Ход компьютера

    def computer_move(self):
        if self.game_over:
            return

        # Простой алгоритм:
        # 1. Проверяем, есть ли возможность победить на следующем ходу.
        # 2. Проверяем, есть ли возможность заблокировать победу противника.
        # 3. Если нет возможности выиграть или заблокировать, делаем случайный ход.

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    if self.check_win():
                        self.buttons[i][j].config(text='O')
                        self.game_over = True
                        self.show_result("Компьютер победил!")
                        return
                    self.board[i][j] = ''  # Отменяем ход для проверки других вариантов

        # Проверяем, может ли игрок выиграть на следующем ходу
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'X'
                    if self.check_win():
                        self.buttons[i][j].config(text='O')
                        self.board[i][j] = 'O'
                        self.current_player = 'X'
                        return
                    self.board[i][j] = ''  # Отменяем ход для проверки других вариантов

        # Если ни игрок, ни компьютер не могут выиграть на следующем ходу,
        # делаем ход, гарантирующий ничью
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == '':
                self.buttons[row][col].config(text='O')
                self.board[row][col] = 'O'
                self.current_player = 'X'
                return
    def check_win(self):
        # Проверка строк
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != '':
                return True

        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '':
                return True

        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return True

        return False

    def check_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def show_result(self, message):
        tk.messagebox.showinfo("Результат", message)

    def new_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

# Запуск игры
root = tk.Tk()
game = TicTacToe(root)
root.geometry(f"+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 300) // 2}")
root.mainloop()