"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words_str = ["разработка", "администрирование", "protocol", "standard"]
words_byte = []

print("Байтовое представление:")

# Преобразование в байтовое представление.
[words_byte.append(word.encode()) for word in words_str]

print(*words_byte, sep="\n")
print()

print("Строковое представление:")

# Обратное преобразование в строковое представление.
print(*[word.decode() for word in words_byte], sep="\n")
