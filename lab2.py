"""Написать программу, решающую задачу из 1 лабораторной работы (в соответствии со своим вариантом) со следующими изменениями:
1.	Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
2.	Распознавание и обработку делать  через регулярные выражения;
3.	В вариантах, где есть параметр (например К), допускается его заменить на любое число;
4.	Все остальные требования соответствуют варианту задания лабораторной работы №1.

Нечетные восьмиричные числа, не превышающие 409610, у которых вторая справа цифра равна 7.
Выводит на экран цифры числа, исключая семерки.
Вычисляется среднее число между минимальным и максимальным и выводится прописью.
"""

import re

digit_to_word = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре', '5': 'пять', '6': 'шесть',
                 '7': 'семь', '8': 'восемь', '9': 'девять'}
min_num = 0
max_num = 10000
num_filtered = []

with open("input.txt", "r", encoding="utf-8") as file:
    content = file.read()

    numbers = re.findall(r'-?\d+', content)

    if not numbers:
        print("\nВ файле input.txt нет чисел")
    else:
        for num in numbers:
            if re.match(r'^-?[0-7]*[1357]*7[0-7]$', num) and len(num) < 5:
                num_filtered.append(int(num))

if num_filtered:
    print("Список чисел, удовлетворяющих условию:")
    print(num_filtered)

    min_num, max_num = min(num_filtered), max(num_filtered)
    print("Цифры чисел, исключая семерки:")
    for num in num_filtered:
        num_remove_seven = re.sub(r'7', '', str(num))
        print(num_remove_seven)

    avg_num = (min_num + max_num) // 2
    avg_num_words = ' '.join([digit_to_word[digit] for digit in str(abs(avg_num))])
    print(f"Среднее число между минимальным ({min_num}) и максимальным ({max_num}): {avg_num_words}")
else:
    print("Нет чисел для обработки.")
