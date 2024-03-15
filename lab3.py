import random

"""
С клавиатуры вводится два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется 
случайным образом целыми числами в интервале [-10,10]. 

Для ИСТд-12 вид матрицы А
Е	В
D	С

Для простоты все индексы в подматрицах относительные. Библиотечными методами пользоваться нельзя.

Для тестирования использовать не случайное заполнение, а целенаправленное.
Формируется матрица F следующим образом: если в С количество простых чисел в нечетных столбцах в области 2 больше, 
чем количество нулевых  элементов в четных строках в области 3, то поменять в С симметрично области 1 и 3 местами, 
иначе С и В поменять местами несимметрично. При этом матрица А не меняется. 
После чего вычисляется выражение: ((К*A)*F– (K * AT) . 
Выводятся по мере формирования А, F и все матричные операции последовательно."""


# Функция для проверки числа на простоту
def is_prime(num):
    count = 0
    for k in range(2, num):
        if num % k == 0 or num % 2 == 0:
            count = count
        else:
            if num % 3 == 0 and num // 3 != 1:
                count = 0
            else:
                count += 1
                break
    return count


# Функция для проверки числа на 0
def is_zero(num):
    count = 0
    if num >= 1 or num < 0:
        return count
    else:
        count += 1
    return count


# Ввод переменной K с клавиатуры
K = int(input("Введите число K: "))

# Ввод размера матрицы с клавиатуры
while True:
    N = int(input("Введите размер/ранг матрицы (N): "))
    if N >= 6 and N % 2 == 0:
        break
    else:
        print(
            "Пожалуйста, введите размер/ранг матрицы (N) число больше/равно 6 и четное число для равных по размеру подматриц")

# Создаем матрицу A NxN и заполняем ее вручную
A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]

# Определяем области подматриц B, C, D, E
E = [row[:N // 2] for row in A[:N // 2]]
B = [row[N // 2:] for row in A[:N // 2]]
D = [row[:N // 2] for row in A[N // 2:]]
C = [row[N // 2:] for row in A[N // 2:]]

# В областе С нахождение количество простых чисел в нечетных столбцах
count_in_area_two = 0
for i in range(len(C) // 2 - (len(C) // 2), len(C) - (len(C) // 2)):
    for j in range(len(C) - (i + 1), len(C)):
        if j % 2 != 0:
            count_in_area_two += is_prime(C[i][j])
for i in range(len(C) // 2, len(C) - (len(C) // 2 - 1)):
    for j in range(i, len(C)):
        if j % 2 != 0:
            count_in_area_two += is_prime(C[i][j])
print("Количество в нечетных столбцах ", count_in_area_two)

# В областе С нахождение количество нулевых элементов в четных строках
count_in_zero_three = 0
for i in range(len(C) // 2 - 1, len(C)):
    for j in range(len(C) - (i + 1), len(C) // 2 + 1):
        if i % 2 == 0:
            count_in_zero_three += is_zero(C[i][j])
for i in range(len(C) // 2 + (len(C) // 2), len(C) - (len(C) // 2 - (len(C) // 2))):
    for j in range(1, i + 1):
        if i % 2 == 0:
            count_in_zero_three += is_zero(C[i][j])
print("Количество нулевых элементов в четных столбцах ", count_in_zero_three)

temp = C
matr_B = [row[:] for row in B]
matr_C = [row[:] for row in C]
if count_in_area_two > count_in_zero_three:
    temp_two = matr_C[:]
    for i in range(len(C)//2):
        matr_C[i], matr_C[len(C)//2 + (i-(len(C)//2+len(C)//2))] = (temp_two[len(C)//2 + (i-(len(C)//2+len(C)//2))],
                                                                    temp_two[i])
else:
    matr_C = matr_B
    matr_B = temp
F = [[matr_C[i % N//2][j % N//2] for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if 0 <= i < 3 and 0 <= j < 3:
            F[i][j] = E[i][j]
        elif 0 <= i < 3 and 3 <= j < 6:
            F[i][j] = matr_B[i][j - 3]
        elif 3 <= i < 6 and 0 <= j < 3:
            F[i][j] = D[i - 3][j]
        else:
            F[i][j] = matr_C[i - 3][j - 3]
# Вывод результатов
print("Матрица A:")
for row in A:
    print(row)

print("\nМатрица F:")
for row in F:
    print(row)

K_times_A = [[K * A[i][j] for j in range(N)] for i in range(N)]
print("Результат выражения K * A:")
for row in K_times_A:
    print(row)
K_times_AT = [[K * A[j][i] for j in range(N)] for i in range(N)]
print("Результат выражения K * A^T:")
for row in K_times_AT:
    print(row)
# Вычисление выражения ((K * A) * F) - (K * A^T)
result_matrix = [[((K * K_times_A[i][j]) * F[i][j]) - (K * K_times_AT[i][j]) for j in range(N)] for i in range(N)]
print("Результат выражения ((K * A) * F) - (K * A^T):")
for row in result_matrix:
    print(row)
