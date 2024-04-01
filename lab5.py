"""
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде
отчета по лабораторной работе.

8.	F(n<2)=1;F(n)=(-1)^n*(2F(n-1)+F(n-3))(при n четном),F(n)= 5F(n-1)/(2n)!- F(n-3)(при n нечетном)
"""
import cProfile
import timeit
import matplotlib.pyplot as plt


def recursive_F(n):
    if n < 2:
        return 1
    return (pow(-1, n)) * ((2 * recursive_F(n - 1) + recursive_F(n - 3)) / (2 * factorial(n)))


def iterative_F(n):
    if n < 2:
        return 1
    dp = [0 for i in range(n + 1)]
    dp[0], dp[1] = 1, 1
    for i in range(2, n + 1, 1):
        dp[i] = pow(-1, i) * (2 * dp[i - 1] + dp[i - 3]) / factorial(n)

    return dp[n]


def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, 2*n + 1, 2):
        result *= i

    return result

n = int(input("Введите натуральное число: "))
while not (0 < n < 50):
    print("Это число не является натуральным или превышает границу. Повторите ввод.")
    n = int(input("Введите натуральное число: "))

results_table = []

cProfile.runctx('''
for n in range(1, n + 1):
    recursive_time = timeit.timeit('recursive_F(n)', globals=globals(), number=10) * 10
    iterative_time = timeit.timeit('iterative_F(n)', globals=globals(), number=10) * 10

    results_table.append((n, recursive_time, iterative_time))
''', globals=globals(), locals=locals(), sort='cumulative')

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
