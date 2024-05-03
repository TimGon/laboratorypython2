"""Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.
Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле, одна кнопка.

Вариант 8. В парламентскую комиссию нужно выбрать К членов. Претендентов предоставили N партий. Вывести все возможные варианты комиссии (от каждой партии должно быть от 1 до 3 членов).
"""
import tkinter as tk
from tkinter import *
import random

def generate_combinations_with_age_constraint(parties, k, min_age, combination=[], index=0):
    if k == 0:
        return combination  # Возвращаем комбинацию вместо её вывода

    if index == len(parties):
        return []

    result = []
    for i in range(1, min(4, k + 1)):
        valid_candidates = [candidate for candidate in parties[index] if candidate[1] >= min_age]
        for j in range(1, min(len(valid_candidates), i) + 1):
            result.extend(generate_combinations_with_age_constraint(parties, k - j, min_age,
                                                                    combination + valid_candidates[:j], index + 1))
    return result


def get_average_age(age):
    total_age = 0
    total_members = 0

    for parties in age:
        party_age = 0
        party_members = 0
        for member in parties:
            party_age += member[1]
            party_members += 1
        party_average_age = float(party_age / party_members)
        total_age += party_average_age
        total_members += 1

    return float(total_age / total_members)


window = Tk()
window.title("Генерация комбинаций с возрастным ограничением")
window.geometry("500x450")
window.resizable(False, False)

k_label = Label(window, text="Введите количество выбираемых кандидатов:")
k_label.grid(row=0, column=0, padx=20, pady=20)
k_input = tk.Entry(window)
k_input.grid(row=0, column=1, padx=20, pady=20)
n_label = Label(window, text="Введите количество партий:")
n_label.grid(row=2, column=0, padx=20, pady=20)
n_input = tk.Entry(window)
n_input.grid(row=2, column=1, padx=20, pady=20)

min_age_label = Label(window, text="Введите минимальный возраст кандидатов:")
min_age_label.grid(row=1, column=0, padx=5, pady=5)
min_age_input = tk.Entry(window)
min_age_input.grid(row=1, column=1, padx=5, pady=5)

label_title = Label(window, text="Комбинации претендентов парламента:")
label_title.grid(row=4, column=0, padx=5, pady=5)

labelt_average_title = Label(window, text="Средний возраст:")
labelt_average_title.grid(row=6, column=0, padx=5, pady=5)

def generate_combinations():
    k = int(k_input.get())
    n = int(n_input.get())
    parties_age = []
    for _ in range(n):
        num_candidates = random.randint(1, 3)
        party = []
        for i in range(num_candidates):
            name = f"{chr(97 + i)}{random.randint(1, 100)}"
            age = random.randint(18, 35)
            candidate = (name, age)
            party.append(candidate)
        parties_age.append(party)

    print("Вывод список партий с возрастами: ", parties_age, '\n')
    min_age = int(min_age_input.get())

    combinations = generate_combinations_with_age_constraint(
        parties_age, k, min_age
    )

    result_text.delete(1.0, tk.END)

    for combination in combinations:
        result_text.insert(tk.END, f"{combination}\n")
    result_average.insert(tk.END, f"{get_average_age(parties_age):.2f}")

generate_button = tk.Button(window, text="Сгенерировать", command=generate_combinations)
generate_button.grid(row=3, column=1, padx=5, pady=5)

result_text = tk.Text(window, width=50, height=10, font="Courier 10 bold")
result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
result_average = tk.Text(window, width=10, height=2, font="Courier 10 bold")
result_average.grid(row=6, column=1, columnspan=1, padx=5, pady=5)
scrollbar = tk.Scrollbar(window, command=result_text.yview)
scrollbar.grid(row=5, column=2, sticky='nsew')
result_text.config(yscrollcommand=scrollbar.set)

window.geometry(f"+{(window.winfo_screenwidth() - 300) // 2}+{(window.winfo_screenheight() - 300) // 2}")
window.mainloop()
