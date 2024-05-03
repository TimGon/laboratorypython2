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
import random


def generate_combinations(parties, k, combination=[], all_combinations=[]):
    if len(combination) == k:
        all_combinations.append(combination)
        return

    for party in parties:
        for candidate in party:
            # print("Кандидат:",candidate)
            if candidate not in combination:
                # print("Проходит проверку", candidate)
                generate_combinations(parties, k, combination + [candidate], all_combinations)

    return all_combinations

def generate_combinations_python(parties, k):
    unique_parties = set([item for sublist in parties for item in sublist])
    result = list(combinations(unique_parties, k))
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
            if set(combination + valid_candidates[:j]) not in set(combination):
                result.extend(generate_combinations_with_age_constraint(parties, k - j, min_age,
                                                                        combination + valid_candidates[:j], index + 1))
    return result


def get_average_age(age):
    total_age = 0
    total_members = 0

    for party in age:
        for member in party:
            total_age += member[1]
            total_members += 1

    return float(total_age / total_members)

k = int(input("Введите количество выбираемых кандидатов: "))
n = int(input("Введите количество партий: "))

# Создание списка parties для хранения кандидатов каждой партии
parties = []
parties_age = []

if k > n:

    for i in range(n):
        num_candidates = random.randint(1, 3)
        candidates = [f"{chr(97 + i)}{j}" for j in range(1, num_candidates + 1)]
        parties.append(candidates)

    for _ in range(n):
        num_candidates = random.randint(1, 3)
        party = []
        for i in range(num_candidates):
            name = f"{chr(97 + i)}{random.randint(1, 100)}"
            age = random.randint(18, 35)
            candidate = (name, age)
            party.append(candidate)
        parties_age.append(party)

    print("Вывод списка партий", parties)
    print("Вывод список партий с возрастами: ", parties_age, '\n')
    count_candidate = set([item for sublist in parties for item in sublist])
    count_candidate_age = set([item for sublist in parties_age for item in sublist])

    if len(count_candidate) >= k:
        combinations_algorithmic = generate_combinations(parties, k)
        print("Алгоритмический подход:\n", combinations_algorithmic)

        combinations_functional = generate_combinations_python(parties, k)
        print("С использованием функций Python:\n", combinations_functional)

        algorithmic_time = timeit.timeit('generate_combinations(parties, k)', globals=globals(), number=1)
        print("Время алгоритма: ", algorithmic_time)

        functional_time = timeit.timeit('generate_combinations_python(parties, k)', globals=globals(), number=1)
        print("Время Функционального: ", functional_time)

        min_commision = min(combinations_functional)
        print("Оптимальное решение", min_commision)

        min_age = int(input("Введите минимальный возраст кандидатов: "))

        combinations_with_age = generate_combinations_with_age_constraint(parties_age, k, min_age)
            print("С ограничением на возраст кандидатов:\n", combinations_with_age)
        age_aver_parties = get_average_age(parties_age)
        # Выводим средний возраст партий
        print("Средний возраст:", age_aver_parties)
    else:
        print("Мест в парламенте оказалось много, а кандидатов от партий мало. Чтобы исправить это попробуйте ещё раз запустить программу.")
else:
    print("Нет подходящих кандидатов в парламент")
