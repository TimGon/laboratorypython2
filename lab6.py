"""
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального  решения.

Вариант 8. В парламентскую комиссию нужно выбрать К членов. Претендентов предоставили N партий. Вывести все возможные варианты комиссии (от каждой партии должно быть от 1 до 3 членов).
"""
"""Часть 1:
Алгоритмический вариант:
"""
import timeit
from itertools import combinations


def generate_combinations(parties, k, combination=[], all_combinations=[]):
    if len(combination) == k:
        all_combinations.append(combination)
        return

    for party in parties:
        for candidate in party:
            generate_combinations(parties, k, combination + [candidate], all_combinations)

    return all_combinations

def generate_combinations_python(parties, k):
    combinations_iter = combinations(parties, k)
    result = []
    for combination in combinations_iter:
        result.append(list(combination))
    return result
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

parties_age = [
    [("A1", 35), ("A2", 28), ("A3", 31)],
    [("B1", 29), ("B2", 32)],
    [("C1", 30), ("C2", 33), ("C3", 27), ("C4", 34)]
]

parties = [
    ["A1", "A2", "A3"],
    ["B1", "B2"],
    ["C1", "C2", "C3", "C4"]
]

k = int(input("Введите количество выбираемых кандидатов: "))

combinations_algorithmic = generate_combinations(parties, k)
print("Алгоритмический подход:\n", combinations_algorithmic)

combinations_functional = generate_combinations_python(parties, k)
print("С использованием функций Python:\n",)
for combination in combinations_functional:
    print(combination)

algorithmic_time = timeit.timeit('generate_combinations(parties, k)', globals=globals(), number=1)
print("Время алгоритма: ", algorithmic_time)

functional_time = timeit.timeit('generate_combinations_python(parties, k)', globals=globals(), number=1)
print("Время Функционального: ", functional_time)

min_age = int(input("Введите минимальный возраст кандидатов: "))
print("С ограничением на возраст кандидатов:")
combinations_with_age = generate_combinations_with_age_constraint(parties_age, k, min_age)
print(combinations_with_age)
"""
1 вариант - недорабочий
import timeit
import itertools

def generate_functional(N, K):
    combination = []
    for i in range(1, K + 1):
        for comb in itertools.combinations(range(N), i):
            if len(comb) <= K:
                combination.append(comb)
    return combination
def generate_combinations(parties, k, current_combination, all_combinations):
    if len(current_combination) == k:
        all_combinations.append(current_combination)
        return

    for i in range(len(parties)):
        party = parties[i]
        for j in range(1, K):
            new_combination = current_combination + party * j
            generate_combinations(parties[i+1:], k, new_combination, all_combinations)

def print_combinations(all_combinations):
    for combination in all_combinations:
        print(combination)

N = int(input("Введите количество партий: "))
parties = []
for i in range(N):
    party = [i+1]
    parties.append(party)

K = int(input("Введите количество членов в комиссии: "))

all_combinations = []
generate_combinations(parties, K, [], all_combinations)
print("Алгоритмический вывод комбинации: ")
print_combinations(all_combinations)

functional_comb = generate_functional(N, K)

print("Функциональный вывод комбинации: ")
for combin in functional_comb:
    print(combin)
algorithmic_time = timeit.timeit('generate_combinations(parties, K, [], all_combinations)', globals=globals(), number=1000)

print("Время алгоритма: ", algorithmic_time)
functional_time = timeit.timeit('generate_functional(N, K)', globals=globals(), number=1000)
print("Время Функционального: ", functional_time)

#2 часть


def generate_modernized_functional(N, K):
    combination = []
    for i in range(1, K + 1):
        for comb in itertools.combinations(range(N), i):
            if len(comb) <= K:
                combination.append(comb)
    return combination"""

"""
2 вариант.

import itertools
import timeit


def generate_combinations(K, N):
    Генерирует все возможные комбинации количества членов от партий с учётом ограничения.
    combinations = []
    for combination in itertools.product(range(1, 4), repeat=N):
        if sum(combination) == K and is_valid(combination):
            combinations.append(combination)
    return combinations


def is_valid(combination):
    Проверяет, является ли комбинация допустимой с учётом ограничения.
    # Проверяет, есть ли хотя бы один член от каждой партии
    if min(combination) < 1:
        return False

    # Проверяет, что общее количество членов от любых двух партий не превышает K/2
    for i in range(N):
        for j in range(i + 1, N):
            if combination[i] + combination[j] > K / 2:
                return False

    # Дополнительное ограничение: проверяет, что количество членов от любой партии не превышает K/2
    for member_count in combination:
        if member_count > K / 2:
            return False

    return True


# Основная программа

K = int(input("Введите количество выбираемых претендентов в парламентарий ",))  # количество членов в комиссии
N = int(input("Введите количество партий ",))  # количество партий

start_time = timeit.timeit()
combinations = generate_combinations(K, N)
end_time = timeit.timeit()

print("Изменённая программа с ограничениями и целевой функцией:")
print("Количество комбинаций:", len(combinations))
print("Время выполнения:", end_time - start_time)

# Проверяет, были ли найдены допустимые комбинации
if combinations:
    # Находит оптимальное решение с минимальным значением целевой функции
    optimal_solution = min(combinations, key=lambda x: x[1])
    print("Оптимальное решение:", optimal_solution[0])
    print("Значение целевой функции:", optimal_solution[1])
else:
    print("Допустимые комбинации не найдены.")"""
