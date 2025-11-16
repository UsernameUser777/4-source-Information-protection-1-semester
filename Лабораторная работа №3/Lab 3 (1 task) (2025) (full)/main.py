import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def text_to_numbers(text, alphabet):
    """
    Преобразует текст в список чисел, где каждая буква заменяется её индексом в алфавите.
    Используется для подготовки текста к числовому шифрованию.

    :param text: Исходный текст для преобразования (строка).
    :param alphabet: Алфавит, используемый для сопоставления букв и чисел (строка).
    :return: Список целых чисел, представляющих индексы букв в алфавите (list of int).
             Если символ не найден в алфавите, он пропускается.
    """
    # Преобразуем весь текст в верхний регистр, чтобы соответствовать алфавиту
    numbers = []
    for char in text.upper():
        # Проверяем, есть ли символ в заданном алфавите
        if char in alphabet:
            # Находим индекс символа в строке алфавита (например, 'А' -> 0, 'Б' -> 1)
            numbers.append(alphabet.index(char))
        # Если символ не найден в алфавите, он просто игнорируется в этом цикле
    return numbers

def numbers_to_text(numbers, alphabet):
    """
    Преобразует список чисел обратно в текст, используя заданный алфавит.
    Используется для восстановления текста из числового шифра.

    :param numbers: Список целых чисел, представляющих индексы букв в алфавите (list of int).
    :param alphabet: Алфавит, используемый для сопоставления чисел и букв (строка).
    :return: Восстановленный текст (строка).
             Если число выходит за пределы индексов алфавита, символ игнорируется.
    """
    # Инициализируем пустую строку для результата
    text = ""
    for num in numbers:
        # Проверяем, что индекс находится в пределах алфавита
        if 0 <= num < len(alphabet):
            # Добавляем соответствующую букву из алфавита к результирующей строке
            text += alphabet[num]
        # Если число вне диапазона, оно игнорируется
    return text

def gamma_cipher_modN(text, gamma, alphabet):
    """
    Шифрует текст с помощью гаммирования по модулю N (длина алфавита).
    Реализует формулу CLi = (PLi + KGi) mod N.

    :param text: Исходный текст для шифрования (строка).
    :param gamma: Гамма (ключ) - список чисел, используемых для шифрования (list of int).
    :param alphabet: Алфавит, используемый для шифрования (строка).
    :return: Кортеж из зашифрованного текста (str) и списка чисел зашифрованного текста (list of int).
    """
    # Преобразуем исходный текст в числовую форму
    text_numbers = text_to_numbers(text, alphabet)
    # Если текст не содержит букв из алфавита, возвращаем пустые значения
    if not text_numbers:
        return "", []

    # Циклически используем гамму. Если гамма короче текста, она повторяется.
    extended_gamma = []
    for i in range(len(text_numbers)):
        # Берём элемент гаммы по модулю длины гаммы, обеспечивая цикличность
        extended_gamma.append(gamma[i % len(gamma)])

    # Выполняем операцию шифрования: (буква_текста + буква_гаммы) mod N
    encrypted_numbers = []
    for i in range(len(text_numbers)):
        # Формула (5.1) из учебника: CLi = (PLi + KGi) mod N
        # PLi - i-й символ открытого текста (text_numbers[i])
        # KGi - i-й символ гаммы (extended_gamma[i])
        # N - длина алфавита (len(alphabet))
        encrypted_num = (text_numbers[i] + extended_gamma[i]) % len(alphabet)
        encrypted_numbers.append(encrypted_num)

    # Преобразуем зашифрованные числа обратно в текст
    encrypted_text = numbers_to_text(encrypted_numbers, alphabet)
    return encrypted_text, encrypted_numbers

def gamma_decipher_modN(encrypted_text, gamma, alphabet):
    """
    Дешифрует текст, зашифрованный с помощью гаммирования по модулю N.
    Реализует формулу PLi = (CLi + N - KGi) mod N.

    :param encrypted_text: Текст для дешифрования (строка).
    :param gamma: Гамма (ключ), использованная при шифровании (list of int).
    :param alphabet: Алфавит, использованный при шифровании (строка).
    :return: Кортеж из дешифрованного текста (str) и списка чисел дешифрованного текста (list of int).
    """
    # Преобразуем зашифрованный текст в числовую форму
    encrypted_numbers = text_to_numbers(encrypted_text, alphabet)
    # Если текст не содержит букв из алфавита, возвращаем пустые значения
    if not encrypted_numbers:
        return "", []

    # Циклически используем гамму. Если гамма короче текста, она повторяется.
    extended_gamma = []
    for i in range(len(encrypted_numbers)):
        # Берём элемент гаммы по модулю длины гаммы, обеспечивая цикличность
        extended_gamma.append(gamma[i % len(gamma)])

    # Выполняем операцию дешифрования: (буква_шифра - буква_гаммы + N) mod N
    decrypted_numbers = []
    for i in range(len(encrypted_numbers)):
        # Формула (5.2) из учебника: PLi = (CLi + N - KGi) mod N
        # CLi - i-й символ зашифрованного текста (encrypted_numbers[i])
        # KGi - i-й символ гаммы (extended_gamma[i])
        # N - длина алфавита (len(alphabet))
        # Добавляем N перед вычитанием, чтобы избежать отрицательного результата до mod
        decrypted_num = (encrypted_numbers[i] - extended_gamma[i]) % len(alphabet)
        decrypted_numbers.append(decrypted_num)

    # Преобразуем дешифрованные числа обратно в текст
    decrypted_text = numbers_to_text(decrypted_numbers, alphabet)
    return decrypted_text, decrypted_numbers

def gamma_cipher_mod2(text, gamma_bits):
    """
    Шифрует текст с помощью гаммирования по модулю 2 (XOR).
    Каждый символ текста преобразуется в 8-битное представление Windows-1251,
    затем побитово XOR'ится с соответствующим 8-битным элементом гаммы.

    :param text: Исходный текст для шифрования (строка).
    :param gamma_bits: Гамма в битовом виде - список 8-битных строк (list of str, e.g., ['01000000', ...]).
    :return: Кортеж из списка битов зашифрованного текста (list of str) и списка битов исходного текста (list of str).
    """
    # Преобразуем каждый символ текста в его 8-битное представление Windows-1251
    text_bits = []
    for char in text.upper():
        try:
            # Кодируем символ в байт по кодировке cp1251 (Windows-1251)
            byte_val = char.encode('cp1251')[0]
            # Преобразуем байт (значение от 0 до 255) в 8-битную двоичную строку (например, '01000000')
            char_bits_str = format(byte_val, '08b')
            text_bits.append(char_bits_str)
        except UnicodeEncodeError:
            # Если символ не входит в кодировку cp1251, он игнорируется
            continue

    # Если текст не содержит символов из cp1251, возвращаем пустые списки
    if not text_bits:
        return [], []

    # Циклически используем гамму. Если гамма короче текста, она повторяется.
    extended_gamma_bits = []
    for i in range(len(text_bits)):
        # Берём элемент гаммы по модулю длины гаммы, обеспечивая цикличность
        extended_gamma_bits.append(gamma_bits[i % len(gamma_bits)])

    # Выполняем операцию XOR побитно для каждого символа
    encrypted_bits = []
    for i in range(len(text_bits)):
        # Получаем биты символа текста и соответствующего элемента гаммы
        t_bits = text_bits[i]
        g_bits = extended_gamma_bits[i]

        # Проверяем, что длина строк битов составляет 8 бит
        if len(t_bits) != 8 or len(g_bits) != 8:
             # В реальной реализации нужно бы обрабатывать ошибки длины
             continue

        # Выполняем XOR для каждой пары битов
        encrypted_char_bits = ""
        for j in range(8):
            # Преобразуем символы '0'/'1' в числа 0/1, выполняем XOR (mod 2), и обратно в строку
            bit_t = int(t_bits[j])
            bit_g = int(g_bits[j])
            encrypted_bit = (bit_t + bit_g) % 2  # XOR: 0+0=0, 0+1=1, 1+0=1, 1+1=0
            encrypted_char_bits += str(encrypted_bit)
        encrypted_bits.append(encrypted_char_bits)

    return encrypted_bits, text_bits

def gamma_decipher_mod2(encrypted_bits, gamma_bits):
    """
    Дешифрует текст, зашифрованный с помощью гаммирования по модулю 2 (XOR).
    Так как XOR обратим сам к себе, процесс идентичен шифрованию.

    :param encrypted_bits: Список 8-битных строк зашифрованного текста (list of str).
    :param gamma_bits: Гамма в битовом виде (список строк), использованная при шифровании (list of str).
    :return: Список битов дешифрованного текста (list of str).
    """
    # Если зашифрованный текст пуст, возвращаем пустой список
    if not encrypted_bits:
        return []

    # Циклически используем гамму. Если гамма короче текста, она повторяется.
    extended_gamma_bits = []
    for i in range(len(encrypted_bits)):
        # Берём элемент гаммы по модулю длины гаммы, обеспечивая цикличность
        extended_gamma_bits.append(gamma_bits[i % len(gamma_bits)])

    # Выполняем операцию XOR побитно (идентична шифрованию)
    decrypted_bits = []
    for i in range(len(encrypted_bits)):
        # Получаем биты символа шифра и соответствующего элемента гаммы
        e_bits = encrypted_bits[i]
        g_bits = extended_gamma_bits[i]

        # Проверяем, что длина строк битов составляет 8 бит
        if len(e_bits) != 8 or len(g_bits) != 8:
             # В реальной реализации нужно бы обрабатывать ошибки длины
             continue

        # Выполняем XOR для каждой пары битов
        decrypted_char_bits = ""
        for j in range(8):
            # Преобразуем символы '0'/'1' в числа 0/1, выполняем XOR (mod 2), и обратно в строку
            bit_e = int(e_bits[j])
            bit_g = int(g_bits[j])
            decrypted_bit = (bit_e + bit_g) % 2  # XOR: 0+0=0, 0+1=1, 1+0=1, 1+1=0
            decrypted_char_bits += str(decrypted_bit)
        decrypted_bits.append(decrypted_char_bits)

    return decrypted_bits

def bits_to_text(bits_list):
    """
    Преобразует список 8-битных строк (Windows-1251) обратно в текст.

    :param bits_list: Список строк, каждая из которых представляет 8 бит (list of str).
    :return: Восстановленный текст (str).
    """
    # Инициализируем пустую строку для результата
    text = ""
    for bits_str in bits_list:
        # Проверяем, что строка содержит ровно 8 бит
        if len(bits_str) != 8:
            # Игнорируем строки неправильной длины
            continue
        # Преобразуем 8-битную строку в целое число (например, '01000000' -> 64)
        byte_val = int(bits_str, 2)
        # Преобразуем целое число (байт) обратно в символ по кодировке cp1251 (Windows-1251)
        try:
            char = bytes([byte_val]).decode('cp1251')
            text += char
        except UnicodeDecodeError:
            # Если байт не соответствует символу в cp1251, добавляем символ-заменитель
            text += '?'
    return text


def encrypt_modN_action():
    """
    Обработчик события нажатия кнопки 'Зашифровать (Mod N)'.
    Получает введённые пользователем фамилию и гамму, выполняет шифрование,
    и выводит результаты в текстовое поле.
    """
    # Получаем текст из поля ввода и преобразуем в верхний регистр
    text = input_text.get().upper()
    # Получаем строку с гаммой из поля ввода и убираем лишние пробелы
    gamma_input = gamma_entry_modN.get().strip()

    # Проверяем, введён ли текст
    if not text:
        output_text.delete(1.0, tk.END) # Очищаем поле вывода
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return
    # Проверяем, введена ли гамма
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (через запятую).\n")
        return

    # Пытаемся преобразовать строку гаммы в список целых чисел
    try:
        gamma = [int(x.strip()) for x in gamma_input.split(',')]
        # Проверяем, что все числа гаммы находятся в допустимом диапазоне [0, N-1]
        if not all(0 <= g < len(alphabet) for g in gamma):
            raise ValueError("Значения гаммы должны быть от 0 до {}.".format(len(alphabet)-1))
    except ValueError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
        return

    # Вызываем функцию шифрования
    encrypted_text, encrypted_nums = gamma_cipher_modN(text, gamma, alphabet)

    # Очищаем поле вывода и вставляем результаты шифрования
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Шифрование по модулю N ---\n")
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"N (мощность алфавита): {len(alphabet)}\n")
    output_text.insert(tk.END, f"Гамма (числа): {gamma}\n")
    output_text.insert(tk.END, f"Исходное сообщение (числа): {text_to_numbers(text, alphabet)}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (числа): {encrypted_nums}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")

def decrypt_modN_action():
    """
    Обработчик события нажатия кнопки 'Дешифровать (Mod N)'.
    Получает введённые пользователем зашифрованный текст и гамму, выполняет дешифрование,
    и выводит результаты в текстовое поле.
    """
    # Получаем текст из поля ввода и преобразуем в верхний регистр
    text = input_text.get().upper()
    # Получаем строку с гаммой из поля ввода и убираем лишние пробелы
    gamma_input = gamma_entry_modN.get().strip()

    # Проверяем, введён ли текст
    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return
    # Проверяем, введена ли гамма
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (через запятую).\n")
        return

    # Пытаемся преобразовать строку гаммы в список целых чисел
    try:
        gamma = [int(x.strip()) for x in gamma_input.split(',')]
        # Проверяем, что все числа гаммы находятся в допустимом диапазоне [0, N-1]
        if not all(0 <= g < len(alphabet) for g in gamma):
            raise ValueError("Значения гаммы должны быть от 0 до {}.".format(len(alphabet)-1))
    except ValueError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
        return

    # Вызываем функцию дешифрования
    decrypted_text, decrypted_nums = gamma_decipher_modN(text, gamma, alphabet)

    # Очищаем поле вывода и вставляем результаты дешифрования
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Дешифрование по модулю N ---\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"N (мощность алфавита): {len(alphabet)}\n")
    output_text.insert(tk.END, f"Гамма (числа): {gamma}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (числа): {text_to_numbers(text, alphabet)}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (числа): {decrypted_nums}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted_text}\n\n")

def encrypt_mod2_action():
    """
    Обработчик события нажатия кнопки 'Зашифровать (Mod 2)'.
    Получает введённые пользователем фамилию и битовую гамму, выполняет шифрование,
    и выводит результаты в текстовое поле.
    """
    # Получаем текст из поля ввода и преобразуем в верхний регистр
    text = input_text.get().upper()
    # Получаем строку с битовой гаммой из поля ввода и убираем лишние пробелы
    gamma_input = gamma_entry_mod2.get().strip()

    # Проверяем, введён ли текст
    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return
    # Проверяем, введена ли гамма
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (битовые строки через запятую, 8 бит каждая).\n")
        return

    # Пытаемся преобразовать строку гаммы в список 8-битных строк
    try:
        gamma_bits = [x.strip() for x in gamma_input.split(',')]
        # Проверяем, что каждая строка гаммы содержит ровно 8 бит и только символы '0' и '1'
        if not all(len(g) == 8 and all(c in '01' for c in g) for g in gamma_bits):
            raise ValueError("Каждое значение гаммы должно быть 8-битной строкой (только 0 и 1).")
    except ValueError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
        return

    # Вызываем функцию шифрования по модулю 2
    encrypted_bits, original_bits = gamma_cipher_mod2(text, gamma_bits)

    # Очищаем поле вывода и вставляем результаты шифрования
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Шифрование по модулю 2 ---\n")
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Исходное сообщение (байты Windows-1251, биты): {original_bits}\n")
    output_text.insert(tk.END, f"Гамма (биты): {gamma_bits}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (байты, биты): {encrypted_bits}\n")
    output_text.insert(tk.END, "\n")

def decrypt_mod2_action():
    """
    Обработчик события нажатия кнопки 'Дешифровать (Mod 2)'.
    Получает введённые пользователем зашифрованные биты и битовую гамму, выполняет дешифрование,
    и выводит результаты в текстовое поле.
    """
    # Получаем строку с зашифрованными битами из поля ввода и убираем лишние пробелы
    encrypted_input = input_text.get().strip()
    # Получаем строку с битовой гаммой из поля ввода и убираем лишние пробелы
    gamma_input = gamma_entry_mod2.get().strip()

    # Проверяем, введены ли биты зашифрованного сообщения
    if not encrypted_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение (биты) для дешифрования.\n")
        return
    # Проверяем, введена ли гамма
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (битовые строки через запятую, 8 бит каждая).\n")
        return

    # Пытаемся преобразовать строки в списки 8-битных строк
    try:
        encrypted_bits = [x.strip() for x in encrypted_input.split(',')]
        gamma_bits = [x.strip() for x in gamma_input.split(',')]
        # Проверяем, что каждая строка зашифрованного текста содержит ровно 8 бит и только символы '0' и '1'
        if not all(len(e) == 8 and all(c in '01' for c in e) for e in encrypted_bits):
            raise ValueError("Каждое значение зашифрованного сообщения должно быть 8-битной строкой (только 0 и 1).")
        # Проверяем, что каждая строка гаммы содержит ровно 8 бит и только символы '0' и '1'
        if not all(len(g) == 8 and all(c in '01' for c in g) for g in gamma_bits):
            raise ValueError("Каждое значение гаммы должно быть 8-битной строкой (только 0 и 1).")
    except ValueError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат ввода. {e}\n")
        return

    # Вызываем функцию дешифрования по модулю 2
    decrypted_bits = gamma_decipher_mod2(encrypted_bits, gamma_bits)
    # Преобразуем полученные биты обратно в текст
    decrypted_text = bits_to_text(decrypted_bits)

    # Очищаем поле вывода и вставляем результаты дешифрования
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Дешифрование по модулю 2 ---\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (байты, биты): {encrypted_bits}\n")
    output_text.insert(tk.END, f"Гамма (биты): {gamma_bits}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (байты, биты): {decrypted_bits}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (символы): {decrypted_text}\n\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифры гаммирования (Лабораторная работа 3, Задание 1)")
root.geometry("800x600") # Устанавливаем начальный размер окна

# --- Виджеты ---

# Ввод текста (фамилии)
input_label = ttk.Label(root, text="Введите фамилию (или биты для Mod2):")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_text = ttk.Entry(root, width=50)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод гаммы для Mod N
gamma_label_modN = ttk.Label(root, text="Введите гамму (Mod N, числа через запятую):")
gamma_label_modN.grid(row=2, column=0, padx=10, pady=5, sticky="w")

gamma_entry_modN = ttk.Entry(root, width=50)
gamma_entry_modN.grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод гаммы для Mod 2
gamma_label_mod2 = ttk.Label(root, text="Введите гамму (Mod 2, 8-битные строки через запятую):")
gamma_label_mod2.grid(row=4, column=0, padx=10, pady=5, sticky="w")

gamma_entry_mod2 = ttk.Entry(root, width=50)
gamma_entry_mod2.grid(row=5, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Кнопки для Mod N
encrypt_button_modN = ttk.Button(root, text="Зашифровать (Mod N)", command=encrypt_modN_action)
encrypt_button_modN.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

decrypt_button_modN = ttk.Button(root, text="Дешифровать (Mod N)", command=decrypt_modN_action)
decrypt_button_modN.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

# Кнопки для Mod 2
encrypt_button_mod2 = ttk.Button(root, text="Зашифровать (Mod 2)", command=encrypt_mod2_action)
encrypt_button_mod2.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

decrypt_button_mod2 = ttk.Button(root, text="Дешифровать (Mod 2)", command=decrypt_mod2_action)
decrypt_button_mod2.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=90, height=25)
output_text.grid(row=9, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(9, weight=1) # Ряд с выводом растягивается
root.grid_columnconfigure(0, weight=1) # Колонка с вводом растягивается

# Запуск главного цикла
root.mainloop()
