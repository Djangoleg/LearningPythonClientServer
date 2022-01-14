"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""
class_word = b"class"
function_word = b"function"
method_word = b"method"

words = [class_word, function_word, method_word]

for word in words:
    print(type(word))
    print(word)
    print(len(word))



