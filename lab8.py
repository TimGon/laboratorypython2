"""
8 лабораторная работа.
    Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
    В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
    Ввод данных из файла с контролем правильности ввода.
    Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми
    или пробелами.
    Для GUI использовать библиотеку tkinter.

Вариант 8
    Объекты – полукруги
    Функции:	проверка пересечения
    визуализация
    раскраска
    поворот вокруг центра окружности

"""

import tkinter as tk
import math
from tkinter import messagebox
from matplotlib.colors import is_color_like


class Semicircle:
    def __init__(self, canvas, x, y, radius, color, root, angle_entry, rotate_button, change_color_button):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.semicircle_id = None
        self.root = root
        self.angle_entry = angle_entry
        self.rotate_button = rotate_button
        self.change_color_button = change_color_button

    def create_semicircle(self):
        """Визуализация полукруга."""
        coords_str_x = x_entry.get()
        coords_str_y = y_entry.get()

        if coords_str_x.isdigit() and coords_str_y.isdigit():
            coord_int_x = int(coords_str_x)
            coord_int_y = int(coords_str_y)
            for other_semicircle in semicircles:
                if other_semicircle != self:
                    if coord_int_x == other_semicircle.x and coord_int_y == other_semicircle.y:
                        tk.messagebox.showwarning("Предупреждение", "Полукруг с такими координатами уже существует! \
                                Измените координаты.")
                        return
        if self.x and self.y:
            self.canvas.itemconfig(self.semicircle_id, fill=self.color)

            self.semicircle_id = self.canvas.create_arc(
                self.x - self.radius,
                self.y - self.radius,
                self.x + self.radius,
                self.y + self.radius,
                start=0,
                extent=180,
                fill=self.color,
                outline=self.color
            )
        else:
            tk.messagebox.showwarning("Предупреждение", "Неправильно введены координаты/радиус")

    def change_color(self, new_color):
        """Раскраска полукруга."""
        global selected_semicircle_id
        self.color = new_color
        if is_color_like(new_color):
            self.canvas.itemconfig(selected_semicircle_id, fill=self.color, outline=self.color)
        else:
            tk.messagebox.showwarning("Предупреждение", "Неправильно введен цвет!")

    def select_semicircle(self, event):
        global selected_semicircle_id
        item_id = self.canvas.find_closest(event.x, event.y)
        if self.canvas.type(item_id) == "arc":
            selected_semicircle_id = item_id
        else:
            selected_semicircle_id = None

        # Обновление кнопки "Повернуть"
        if selected_semicircle_id is not None:
            self.rotate_button.config(state="normal")
            self.change_color_button.config(state="normal")
        else:
            self.rotate_button.config(state="disabled")
            self.change_color_button.config(state="disabled")

    def rotate(self):
        """Поворот полукруга вокруг центра окружности."""
        angle_str = self.angle_entry.get()
        if not angle_str:
            tk.messagebox.showwarning("Ошибка", "Введите угол поворота!")
            return

        if angle_str.isdigit():
            angle = int(angle_str)

            # Ограничение угла
            if angle < 0:
                angle = 0
                tk.messagebox.showwarning("Предупреждение", "Угол установлен в 0 градусов.")
            elif angle > 360:
                angle = 360
                tk.messagebox.showwarning("Предупреждение", "Угол установлен в 360 градусов.")

            angle = math.radians(angle)
            # Получаем координаты центра полукруга
            center_x = self.x
            center_y = self.y

            # Получаем координаты точек полукруга
            points = self.canvas.coords(selected_semicircle_id)
            new_coords_x = None
            new_coords_y = None
            # Поворачиваем каждую точку полукруга
            rotated_points = []
            for i in range(0, len(points), 2):
                x = points[i]
                y = points[i + 1]
                # Вычисляем новые координаты точки
                new_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
                new_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
                new_coords_x = new_x
                new_coords_y = new_y
                rotated_points.extend([new_x, new_y])

            # Обновляем координаты полукруга на холсте
            self.canvas.coords(selected_semicircle_id, *rotated_points)

            self.check_intersection(new_coords_x, new_coords_y, self.radius)
        else:
            tk.messagebox.showwarning("Ошибка", "Некорректный угол поворота!")
            return

    def check_intersection(self, x, y, radius):
        """Проверка пересечения с другим полукругом."""
        distance_squared = (self.x - x) * 2 + (self.y - y) * 2
        if distance_squared < 0:  # Check for negative value
            tk.messagebox.showerror("Ошибка", "Недопустимые координаты!")
            return False
        distance = math.sqrt(distance_squared)
        if distance < self.radius + radius:
            # Меняем цвет полукруга
            # self.canvas.itemconfig(self.semicircle_id, fill="red")
            tk.messagebox.showinfo("Пересечение", "Найдено пересечение!")
            return True
        else:
            return False

# Создание основного окна
root = tk.Tk()
root.title("Полукруги")

# Создание холста
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(pady=10)

# Список полукругов
semicircles = []

# Выбранный полукруг для поворота или изменения цвета
selected_semicircle_id = None

# Фрейм для ввода данных
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Элементы ввода данных
x_label = tk.Label(input_frame, text="X:")
x_label.pack(side=tk.LEFT)
x_entry = tk.Entry(input_frame)
x_entry.pack(side=tk.LEFT)

y_label = tk.Label(input_frame, text="Y:")
y_label.pack(side=tk.LEFT)
y_entry = tk.Entry(input_frame)
y_entry.pack(side=tk.LEFT)

radius_label = tk.Label(input_frame, text="Радиус:")
radius_label.pack(side=tk.LEFT)
radius_entry = tk.Entry(input_frame)
radius_entry.pack(side=tk.LEFT)

color_label = tk.Label(input_frame, text="Цвет:")
color_label.pack(side=tk.LEFT)
color_entry = tk.Entry(input_frame)
color_entry.pack(side=tk.LEFT)

angle_label = tk.Label(input_frame, text="Угол:")
angle_label.pack(side=tk.LEFT)
angle_entry = tk.Entry(input_frame)
angle_entry.pack(side=tk.LEFT)


def update_button_state():
    x_str = x_entry.get()
    y_str = y_entry.get()
    radius_str = radius_entry.get()
    color_str = color_entry.get()

    if x_str.isdigit() and y_str.isdigit() and radius_str.isdigit() and color_str:
        create_button.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL)
    else:
        create_button.config(state=tk.DISABLED)
        save_button.config(state=tk.DISABLED)

# Функция для загрузки данных из файла
def load_data(filename):
    """Загрузка данных из файла."""
    with open(filename, "r") as file:
        for line in file:
            x, y, radius, color = line.strip().split(",")
            semicircles.append(
                Semicircle(canvas, int(x), int(y), int(radius), color, root, angle_entry, rotate_button,
                           change_color_button))
            semicircles[-1].create_semicircle()

# Функция для сохранения данных в файл
def save_data():
    """Сохранение данных в файл."""
    filename = "semicircles.txt"
    with open(filename, "w") as file:
        for semicircle in semicircles:
            file.write(f"{semicircle.x},{semicircle.y},{semicircle.radius},{semicircle.color}\n")

# Кнопки
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

create_button = tk.Button(button_frame, text="Создать",
                          command=lambda: Semicircle(canvas, int(x_entry.get()), int(y_entry.get()),
                                                     int(radius_entry.get()), color_entry.get(), root, angle_entry,
                                                     rotate_button, change_color_button).create_semicircle(),
                          state=tk.DISABLED)
create_button.pack(side=tk.LEFT, padx=5)

change_color_button = tk.Button(button_frame, text="Изменить цвет", command=lambda: semicircles[-1].change_color(
    color_entry.get()) if semicircles else None, state="disabled")
change_color_button.pack(side=tk.LEFT, padx=5)

rotate_button = tk.Button(button_frame, text="Повернуть",
                          command=lambda: semicircles[-1].rotate() if semicircles else None, state="disabled")
rotate_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Сохранить", command=save_data, state=tk.DISABLED)
save_button.pack(side=tk.LEFT, padx=5)

# Привязываем обработчик клика к холсту
canvas.bind("<Button-1>", lambda event: semicircles[-1].select_semicircle(event) if semicircles else None)

x_entry.bind("<KeyRelease>", lambda event: update_button_state())
y_entry.bind("<KeyRelease>", lambda event: update_button_state())
radius_entry.bind("<KeyRelease>", lambda event: update_button_state())
color_entry.bind("<KeyRelease>", lambda event: update_button_state())

load_data("semicircles.txt")

root.geometry(f"+{(root.winfo_screenwidth() - 300) // 2}+{(root.winfo_screenheight() - 300) // 2}")
root.mainloop()
