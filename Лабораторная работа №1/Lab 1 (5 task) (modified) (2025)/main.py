# Программа для шифрования фамилии методом шифра Playfair
# Используется русский алфавит

# Запрашиваем у пользователя фамилию
surname = input("Введите вашу фамилию: ").strip()

# Запрашиваем у пользователя ключевое слово для формирования таблицы Playfair
keyword = input("Введите ключевое слово для шифра Playfair: ").strip()

# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# Функция для создания таблицы Playfair
def create_playfair_table(keyword, original_alphabet, rows=6, cols=6):
    """
    Создает таблицу 6x6 для шифра Playfair на основе ключевого слова.

    :param keyword: Ключевое слово (строка).
    :param original_alphabet: Оригинальный алфавит (строка).
    :param rows: Количество строк в таблице (int).
    :param cols: Количество столбцов в таблице (int).
    :return: Таблица Playfair (список списков).
    """
    # Приводим ключевое слово к верхнему регистру
    keyword_upper = keyword.upper()

    # Создаем список для хранения уникальных букв из ключа в порядке их появления
    unique_keyword_letters = []
    # Множество для быстрой проверки, была ли буква уже добавлена
    seen_letters = set()

    # Проходим по каждой букве в ключевом слове
    for char in keyword_upper:
        # Проверяем, является ли символ буквой из оригинального алфавита
        # и не встречалась ли она уже в ключе
        if char in original_alphabet and char not in seen_letters:
            # Добавляем букву в список уникальных букв ключа
            unique_keyword_letters.append(char)
            # Добавляем букву в множество просмотренных
            seen_letters.add(char)
        # Если символ не из алфавита или уже был добавлен, игнорируем его

    # Создаем алфавит для заполнения таблицы
    # Начинаем с уникальных букв из ключа
    table_alphabet = "".join(unique_keyword_letters)

    # Затем добавляем оставшиеся буквы из оригинального алфавита,
    # которые не вошли в ключ
    for char in original_alphabet:
        if char not in seen_letters:
            table_alphabet += char

    # Теперь заполняем таблицу размером rows x cols
    # Создаем пустую таблицу
    table = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Вычисляем индекс символа в строке table_alphabet
            index = i * cols + j

            # Проверяем, не вышли ли мы за пределы алфавита
            if index < len(table_alphabet):
                # Добавляем символ из алфавита в ячейку таблицы
                row.append(table_alphabet[index])
            else:
                # Если индекс выходит за пределы, добавляем фиктивный символ
                # или оставляем пустым. В примере из учебника (Таблица 3.7)
                # используются '-', '1', '2'. Добавим '1', '2', '3' и т.д.
                # если места в алфавите не хватает.
                # row.append('-')
                # row.append(str(index - len(table_alphabet))) # Не очень, так как могут быть отрицательные индексы
                row.append('-')  # Используем один фиктивный символ
        # Добавляем заполненную строку в таблицу
        table.append(row)

    # Возвращаем готовую таблицу
    return table


# Функция для получения координат символа в таблице Playfair
def get_coordinates_playfair(char, table):
    """
    Находит координаты (строка, столбец) символа в таблице Playfair.

    :param char: Символ для поиска (строка, длина 1).
    :param table: Таблица Playfair (список списков).
    :return: Кортеж (row, col) индексов (int, int) или (-1, -1), если символ не найден.
    """
    # Ищем символ в таблице
    for r in range(len(table)):
        for c in range(len(table[r])):
            if table[r][c] == char:
                return r, c
    # Если символ не найден, возвращаем (-1, -1)
    return -1, -1


# Функция для шифрования биграммы с помощью таблицы Playfair
def encrypt_bigram(bigram, table):
    """
    Шифрует биграмму (пару букв) по правилам шифра Playfair.

    :param bigram: Биграмма (строка длиной 2).
    :param table: Таблица Playfair (список списков).
    :return: Зашифрованная биграмма (строка длиной 2).
    """
    # Извлекаем две буквы биграммы
    char1, char2 = bigram[0], bigram[1]

    # Получаем координаты обеих букв в таблице
    row1, col1 = get_coordinates_playfair(char1, table)
    row2, col2 = get_coordinates_playfair(char2, table)

    # Проверяем, были ли найдены обе буквы
    if row1 == -1 or col1 == -1 or row2 == -1 or col2 == -1:
        # Если какая-то буква не найдена, возвращаем её как есть (или обрабатываем ошибку)
        # В данном случае, если биграмма содержит символ не из таблицы, результат может быть некорректным
        # print(f"Ошибка: один из символов биграммы '{bigram}' не найден в таблице.")
        return bigram  # Возвращаем как есть, хотя это не по правилам

    # Проверяем, находятся ли обе буквы в одной строке
    if row1 == row2:
        # Если да, заменяем на буквы, стоящие справа (с циклическим переходом)
        new_col1 = (col1 + 1) % len(table[0])  # % len(table[0]) обеспечивает цикличность
        new_col2 = (col2 + 1) % len(table[0])
        encrypted_char1 = table[row1][new_col1]
        encrypted_char2 = table[row2][new_col2]
    # Проверяем, находятся ли обе буквы в одном столбце
    elif col1 == col2:
        # Если да, заменяем на буквы, стоящие ниже (с циклическим переходом)
        new_row1 = (row1 + 1) % len(table)  # % len(table) обеспечивает цикличность
        new_row2 = (row2 + 1) % len(table)
        encrypted_char1 = table[new_row1][col1]
        encrypted_char2 = table[new_row2][col2]
    # Если буквы находятся в разных строках и разных столбцах
    else:
        # Заменяем на буквы, находящиеся в других углах прямоугольника, образованного этими двумя буквами
        # То есть, меняем столбцы букв
        encrypted_char1 = table[row1][col2]
        encrypted_char2 = table[row2][col1]

    # Возвращаем зашифрованную биграмму
    return encrypted_char1 + encrypted_char2


# Функция для подготовки текста к шифрованию Playfair
def prepare_text_for_playfair(text, filler_char='Я'):
    """
    Подготавливает текст для шифрования Playfair: разбивает на биграммы,
    вставляя filler_char между одинаковыми буквами и при необходимости добавляя в конец.

    :param text: Исходный текст (строка).
    :param filler_char: Символ для вставки между одинаковыми буквами (строка, длина 1).
    :return: Подготовленный текст, разбитый на биграммы (список строк длиной 2).
    """
    # Приводим к верхнему регистру
    text_upper = text.upper()

    # Создаем список для хранения подготовленных символов
    prepared_chars = []

    # Проходим по символам текста
    i = 0
    while i < len(text_upper):
        current_char = text_upper[i]
        # Добавляем текущий символ
        prepared_chars.append(current_char)

        # Проверяем, есть ли следующий символ
        if i + 1 < len(text_upper):
            next_char = text_upper[i + 1]
            # Если текущий символ и следующий совпадают, вставляем filler_char
            if current_char == next_char:
                prepared_chars.append(filler_char)
                # Переходим к следующему символу, не пропуская текущий
                i += 1  # i указывает на следующий символ, который нужно обработать
            else:
                # Если символы не совпадают, просто переходим к следующему
                i += 1
        else:
            # Если это последний символ, выходим из цикла
            i += 1

    # Преобразуем список символов в строку
    prepared_string = "".join(prepared_chars)

    # Проверяем, является ли длина строки четной
    if len(prepared_string) % 2 != 0:
        # Если нечетная, добавляем filler_char в конец
        prepared_string += filler_char

    # Разбиваем строку на биграммы (группы по 2 символа)
    bigrams = []
    for j in range(0, len(prepared_string), 2):
        bigram = prepared_string[j:j + 2]
        bigrams.append(bigram)

    # Возвращаем список биграмм
    return bigrams


# Функция для шифрования строки с помощью шифра Playfair
def playfair_cipher(text, keyword, original_alphabet, filler_char='Я'):
    """
    Шифрует текст с помощью шифра Playfair.

    :param text: Исходный текст для шифрования (строка).
    :param keyword: Ключевое слово для формирования таблицы (строка).
    :param original_alphabet: Оригинальный алфавит (строка).
    :param filler_char: Символ для вставки между одинаковыми буквами и при нечетной длине (строка).
    :return: Зашифрованный текст (строка).
    """
    # Создаем таблицу Playfair
    playfair_table = create_playfair_table(keyword, original_alphabet, 6, 6)

    # Подготавливаем текст: разбиваем на биграммы
    bigrams = prepare_text_for_playfair(text, filler_char)

    # Инициализируем строку для хранения результата
    encrypted_text = ""

    # Проходим по каждой биграмме
    for bigram in bigrams:
        # Шифруем биграмму
        encrypted_bigram = encrypt_bigram(bigram, playfair_table)
        # Добавляем зашифрованную биграмму к результату
        encrypted_text += encrypted_bigram

    # Возвращаем зашифрованный текст
    return encrypted_text


# Вызываем функцию шифрования с нашими параметрами
# Используем таблицу 6x6, так как русский алфавит (33) + 3 символа = 36
encrypted_surname = playfair_cipher(surname, keyword, alphabet, 'Я')

# Создаем таблицу для вывода
playfair_table = create_playfair_table(keyword, alphabet, 6, 6)

# Выводим результаты
print(f"Исходное сообщение: {surname}")
print(f"Ключ: {keyword}")
print("Таблица шифрозамен (таблица Playfair):")
for row in playfair_table:
    print(row)
print(f"Зашифрованное сообщение: {encrypted_surname}")
