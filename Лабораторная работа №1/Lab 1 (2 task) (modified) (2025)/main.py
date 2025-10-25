# Программа для шифрования фамилии методом лозунгового шифра
# Используется русский алфавит

# Запрашиваем у пользователя фамилию
surname = input("Введите вашу фамилию: ").strip()

# Запрашиваем у пользователя ключевое слово (лозунг) для формирования алфавита замены
keyword = input("Введите ключевое слово (лозунг) для лозунгового шифра: ").strip()

# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# Функция для создания нового алфавита замены на основе ключевого слова
def generate_cipher_alphabet(keyword, original_alphabet):
    """
    Создает алфавит замены для лозунгового шифра.

    :param keyword: Ключевое слово (лозунг) (строка).
    :param original_alphabet: Оригинальный алфавит (строка).
    :return: Новый алфавит замены (строка).
    """
    # Приводим ключевое слово к верхнему регистру
    keyword_upper = keyword.upper()

    # Создаем список для хранения уникальных букв из ключа в порядке их появления
    # Используем список, чтобы сохранить порядок
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

    # Создаем алфавит замены
    # Начинаем с уникальных букв из ключа
    cipher_alphabet = "".join(unique_keyword_letters)

    # Затем добавляем оставшиеся буквы из оригинального алфавита,
    # которые не вошли в ключ
    for char in original_alphabet:
        if char not in seen_letters:
            cipher_alphabet += char

    # Возвращаем получившийся алфавит замены
    return cipher_alphabet


# Функция для шифрования строки с помощью лозунгового шифра
def slogan_cipher(text, keyword, original_alphabet):
    """
    Шифрует текст с помощью лозунгового шифра.

    :param text: Исходный текст для шифрования (строка).
    :param keyword: Ключевое слово (лозунг) (строка).
    :param original_alphabet: Оригинальный алфавит (строка).
    :return: Зашифрованный текст (строка).
    """
    # Генерируем алфавит замены на основе ключевого слова
    cipher_alphabet = generate_cipher_alphabet(keyword, original_alphabet)

    # Преобразуем входной текст в верхний регистр
    text_upper = text.upper()

    # Инициализируем строку для хранения результата
    encrypted_text = ""

    # Проходим по каждой букве в тексте
    for char in text_upper:
        # Проверяем, находится ли символ в оригинальном алфавите
        if char in original_alphabet:
            # Находим индекс символа в оригинальном алфавите
            index_in_original = original_alphabet.index(char)

            # Находим соответствующую букву в алфавите замены по этому индексу
            encrypted_char = cipher_alphabet[index_in_original]

            # Добавляем зашифрованную букву к результату
            encrypted_text += encrypted_char
        else:
            # Если символ не является буквой алфавита (например, пробел или знак препинания),
            # оставляем его без изменений
            encrypted_text += char

    # Возвращаем зашифрованный текст
    return encrypted_text


# Вызываем функцию шифрования с нашими параметрами
encrypted_surname = slogan_cipher(surname, keyword, alphabet)

# Генерируем алфавит замены для вывода
cipher_alphabet_output = generate_cipher_alphabet(keyword, alphabet)

# Выводим результаты
print(f"Исходное сообщение: {surname}")
print(f"Ключ (лозунг): {keyword}")
print(f"Оригинальный алфавит: {alphabet}")
print(f"Алфавит замены (таблица шифрозамен): {cipher_alphabet_output}")
print(f"Зашифрованное сообщение: {encrypted_surname}")
