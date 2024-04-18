"""
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде
отчета по лабораторной работе.

8.	F(n<2)=1;F(n)=(-1)^n*(2F(n-1)+F(n-3))/(2n)!
"""

import timeit
import matplotlib.pyplot as plt


def recursive_F(n, val):
    if n < 2:
        return 1
    val *= -1

    return val * (2 * (recursive_F(n - 1, val) + recursive_F(n - 3, val))) / factorial(2*n)


def iterative_F(n, val):
    if n < 2:
        return 1

    prev2, prev1 = 1, 1
    current = 0
    val *= -1

    for i in range(2, n + 1):
        current = val * (2 * (prev1 + prev2)) / factorial(2*n)
        prev2, prev1 = prev1, current

    return current

def factorial(n):
    if n not in cache:
        cache[n] = n * factorial(n-1)
    return cache[n]

n = int(input("Введите натуральное число: "))
while not (0 < n < 50):
    print("Это число не является натуральным или превышает границу. Повторите ввод.")
    n = int(input("Введите натуральное число: "))

results_table = []
minus_one = int(input("Введите число -1 или 1 "))
while not (-1 == minus_one or minus_one == 1):
    print("Это число не является 1 или -1. Повторите ввод.")
    minus_one = int(input("Введите число -1 или 1 "))

cache = {0: 0, 1: 1}

for n in range(1, n + 1):
    recursive_time = timeit.timeit('recursive_F(n, minus_one)', globals=globals(), number=1)
    iterative_time = timeit.timeit('iterative_F(n, minus_one)', globals=globals(), number=1)

    results_table.append((n, recursive_time, iterative_time))

print("+-" + "-"*12 + "-+-" + "-"*12 + "-+-" + "-"*15 + "-+")
print("| {:^14} | {:^14} | {:^17} |".format("n", "Recursive", "Iterative"))
print("+-" + "-"*12 + "-+-" + "-"*12 + "-+-" + "-"*15 + "-+")
for row in results_table:
    print("| {:^14} | {:^14.6f} | {:^17.6f} |".format(row[0], row[1], row[2]))
print("+-" + "-"*13 + "-+-" + "-"*12 + "-+-" + "-"*15 + "-+")

plt.plot([row[0] for row in results_table], [row[1] for row in results_table], label='Рекурсивный метод')
plt.plot([row[0] for row in results_table], [row[2] for row in results_table], label='Итерационный метод')
plt.xlabel('n')
plt.ylabel('Время (сек.)')
plt.title('Сравнение время между Рекурсией и Итерационным методом')
plt.legend()
plt.show()
