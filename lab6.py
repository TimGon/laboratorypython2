"""
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального  решения.

Вариант 8. В парламентскую комиссию нужно выбрать К членов. Претендентов предоставили N партий. Вывести все возможные варианты комиссии (от каждой партии должно быть от 1 до 3 членов).
"""

import timeit
from itertools import combinations

"""Часть 1:
Алгоритмический вариант:
"""
def generate_combinations(parties, k, combination=[], all_combinations=[]):
    if len(combination) == k:
        all_combinations.append(combination)
        return

    for party in parties:
        for candidate in party:
            if candidate not in combination:
                generate_combinations(parties, k, combination + [candidate], all_combinations)

    return all_combinations
"""
Функциональный вариант:
"""
def generate_combinations_python(parties, k):
    combinations_iter = combinations(parties, k)
    result = []
    for combination in combinations_iter:
        result.append(list(combination))
    return result
"""Часть 2:
Ограничение по возрасту:
"""
def generate_combinations_with_age_constraint(parties, k, min_age, combination=[], index=0):
    if k == 0:
        return combination  

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
