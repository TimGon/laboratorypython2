"""
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно (значение, время).
Определить (смоделировать) границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме в виде
отчета по лабораторной работе.

8.	F(n<2)=1;F(n)=(-1)^n*(2F(n-1)+F(n-3))(при n четном),F(n)= 5F(n-1)/(2n)!- F(n-3)(при n нечетном)
"""
import time
import matplotlib.pyplot as plt


def factorial_double(k):
    result = 2
    for j in range(2, 2*k + 1):
        result *= j
    return result


def recursive_F(n):
    if n < 2:
        return 1
    if n % 2 == 0:
        return -1 ** n * (2 * recursive_F(n - 1) + recursive_F(n - 3))
    else:
        return 5 * recursive_F(n - 1) / factorial_double(n) - recursive_F(n - 3)


while True:
    n = int(input("Введите натуральное число: "))
    if n > 0 and n < 50:
        break
    else:
        print("Это число не является натуральным/превышает границу. Повторите ввод.")

start_time = time.time()
dp = [0 for i in range(n + 1)]
dp[0] = 1
dp[1] = 1

for i in range(2, n + 1, 1):
    if i % 2 == 0:
        dp[i] = (-1) ** i * (2 * dp[i - 1] + dp[i - 3])
        print(f"dp{i} при четном:", dp[i])
    else:
        dp[i] = 5 * dp[i - 1] / factorial_double(n) - dp[i - 3]
        print(f"dp{i} при нечетном:", dp[i])
iterative_time = time.time() - start_time
result_iterative = dp[n]

start_time = time.time()
result_recursive = recursive_F(n)
recursive_time = time.time() - start_time

print(f"Рекурсивный результат для F({n}): {result_recursive}, время выполнения: {recursive_time} секунд")
print(f"Итеративный результат для F({n}): {result_iterative}, время выполнения: {iterative_time} секунд")

plt.figure(figsize=(10, 6))
plt.plot(n, recursive_time, label='Рекурсивный метод', marker='o')
plt.plot(n, iterative_time, label='Итеративный метод', marker='x')
plt.xlabel('Значение n')
plt.ylabel('Время выполнения (секунды)')
plt.title('Сравнение времени выполнения методов')
plt.legend()
plt.grid()
plt.show()
