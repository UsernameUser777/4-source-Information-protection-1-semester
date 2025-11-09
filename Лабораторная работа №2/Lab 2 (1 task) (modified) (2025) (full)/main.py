import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import string

def simple_permutation_encrypt(text, key):
    """
    Шифрует текст с помощью шифра простой одинарной перестановки.

    Этот метод шифрования работает следующим образом:
    1.  Исходный текст разбивается на блоки фиксированной длины, равной длине ключа.
    2.  Если длина текста не делится нацело на длину ключа, текст дополняется
        пробелами до ближайшей длины, кратной длине ключа.
    3.  Каждый блок текста рассматривается как строка в виртуальной таблице,
        где количество столбцов равно длине ключа.
    4.  Ключ перестановки задает порядок, в котором символы внутри блока (в строке таблицы)
        переставляются. Ключ - это последовательность чисел, где каждое число указывает
        на новую позицию символа. Например, ключ "2417653" означает, что 1-й символ
        блока станет 2-м, 2-й символ станет 4-м, 3-й символ станет 1-м и т.д.
    5.  После перестановки символов в строке, все переставленные строки записываются
        подряд. Затем, зашифрованный текст формируется путем считывания символов
        по столбцам из этой виртуальной таблицы.

    :param text: Исходный текст для шифрования (str).
                 Пример: "Колосов".
    :param key: Ключ перестановки (str), например, "2417653".
                Длина ключа определяет ширину "виртуальной таблицы".
                Каждая цифра в ключе - это номер позиции (1-инддекс), куда перейдет
                символ из исходной позиции.
    :return: tuple:
             - encrypted_text (str): Зашифрованный текст.
             - encrypted_table (list of lists): Виртуальная таблица после перестановки
                                                символов в строках, но до финального
                                                считывания по столбцам.
    """
    # Преобразуем ключ в список индексов (0-based), чтобы использовать для индексации списков.
    # Например, ключ "2417653" становится [1, 3, 0, 6, 5, 4, 2] (1-2 -> 0-1, 4-1 -> 3-0 и т.д.)
    try:
        # Проверяем, что ключ состоит только из цифр
        if not key.isdigit():
            raise ValueError("Ключ должен содержать только цифры.")
        # Преобразуем строку в список целых чисел
        key_indices = [int(k) - 1 for k in key]
        # Проверяем, что ключ не пустой
        if len(key_indices) == 0:
            raise ValueError("Ключ не может быть пустым.")
        # Проверяем, что все индексы уникальны и не выходят за пределы [0, len(key)-1]
        if len(set(key_indices)) != len(key_indices) or any(k < 0 or k >= len(key_indices) for k in key_indices):
            raise ValueError("Ключ должен содержать только уникальные цифры от 1 до длины ключа.")
    except ValueError as e:
        # Если возникла ошибка при обработке ключа, поднимаем её дальше
        raise e

    n = len(key_indices) # n - ширина виртуальной таблицы, определяется длиной ключа

    # Дополняем текст пробелами до длины, кратной n (ширине таблицы).
    # Это гарантирует, что текст можно будет разбить на строки одинаковой длины.
    original_length = len(text)
    padding_needed = (n - (original_length % n)) % n
    padded_text = text + ' ' * padding_needed
    padded_length = len(padded_text)

    # Создаем виртуальную таблицу, разбивая дополненный текст на строки длины n.
    # Каждая строка таблицы будет подвергаться перестановке по ключу.
    table = []
    for i in range(0, padded_length, n):
        row = list(padded_text[i:i+n]) # Берем n символов и создаем из них список (строку)
        table.append(row)

    # Применяем перестановку к каждой строке таблицы в соответствии с ключом.
    # Новый символ на позиции new_pos берется из старой позиции j.
    encrypted_table = []
    for row in table:
        # Создаем новую строку той же длины
        encrypted_row = [''] * n
        # Проходим по индексам из ключа (new_pos) и заполняем новую строку
        # символами из старой строки (row) по правилу ключа (j -> new_pos)
        for j, new_pos in enumerate(key_indices):
            # j - старая позиция символа в строке
            # new_pos - новая позиция символа в строке после перестановки
            encrypted_row[new_pos] = row[j]
        encrypted_table.append(encrypted_row)

    # Формируем зашифрованный текст, считывая символы по столбцам из виртуальной таблицы.
    # Это стандартный способ формирования итогового шифротекста для этого типа перестановки.
    encrypted_chars = []
    for col_idx in range(n): # Проходим по всем столбцам (от 0 до n-1)
        for row in encrypted_table: # Проходим по всем строкам в таблице
            encrypted_chars.append(row[col_idx]) # Добавляем символ из текущего столбца

    # Возвращаем зашифрованный текст в виде строки и таблицу после перестановки строк
    return ''.join(encrypted_chars), encrypted_table

def simple_permutation_decrypt(ciphertext, key):
    """
    Дешифрует текст, зашифрованный шифром простой одинарной перестановки.

    Процесс дешифрования обратен шифрованию:
    1.  Определяется длина ключа n.
    2.  Зашифрованный текст разбивается на "столбцы" длиной len(ciphertext) / n.
    3.  Символы распределяются по этим "столбцам".
    4.  Затем "столбцы" переставляются *назад* в соответствии с обратным ключом.
        Обратный ключ - это такой ключ, который "отменяет" перестановку.
        Если в прямом ключе символ с позиции j шел на позицию new_pos (j -> new_pos),
        то в обратном ключе символ с позиции new_pos должен вернуться на позицию j (new_pos -> j).
        Иными словами, inverse_key[new_pos] = j.
    5.  После обратной перестановки столбцов, текст считывается по строкам,
        восстанавливая исходный порядок символов.

    :param ciphertext: Зашифрованный текст (str).
    :param key: Ключ перестановки, использованный при шифровании (str), например, "2417653".
    :return: str: Восстановленный (дешифрованный) текст.
    """
    # Преобразуем ключ в список индексов (0-based), как и в encrypt
    try:
        if not key.isdigit():
            raise ValueError("Ключ должен содержать только цифры.")
        key_indices = [int(k) - 1 for k in key]
        if len(key_indices) == 0:
            raise ValueError("Ключ не может быть пустым.")
        if len(set(key_indices)) != len(key_indices) or any(k < 0 or k >= len(key_indices) for k in key_indices):
            raise ValueError("Ключ должен содержать только уникальные цифры от 1 до длины ключа.")
    except ValueError as e:
        raise e

    n = len(key_indices)
    if n == 0:
        return ciphertext

    # Длина зашифрованного текста
    ct_len = len(ciphertext)
    # Количество "строк" в виртуальной таблице при считывании по столбцам
    num_rows = ct_len // n if n != 0 else 0

    # Создаем "столбцы" из зашифрованного текста
    # Сначала разбиваем текст на n частей (столбцов)
    columns = []
    for i in range(n):
        start_idx = i * num_rows
        end_idx = start_idx + num_rows
        col = list(ciphertext[start_idx:end_idx])
        columns.append(col)

    # Создаем обратный ключ
    # Если key_indices[j] = new_pos, то inverse_key[new_pos] = j
    inverse_key = [0] * n
    for j, new_pos in enumerate(key_indices):
        inverse_key[new_pos] = j

    # Создаем пустую таблицу для восстановления строк
    restored_table = [['' for _ in range(n)] for _ in range(num_rows)]

    # Распределяем столбцы по *оригинальным* позициям, определяемым обратным ключом
    for col_idx, col_data in enumerate(columns):
        original_pos = inverse_key[col_idx]
        for row_idx, char in enumerate(col_data):
            restored_table[row_idx][original_pos] = char

    # Формируем дешифрованный текст, считывая строки таблицы
    decrypted_chars = []
    for row in restored_table:
        decrypted_chars.extend(row)

    # Удаляем пробелы, которые были добавлены для выравнивания
    decrypted_text = ''.join(decrypted_chars)
    # Удаляем пробелы в конце, которые были добавлены при шифровании
    # original_len = len(text) передавалась бы как аргумент.
    # decrypted_text = decrypted_text[:original_len]
    # Вместо этого, удаляем пробелы в конце, полагая, что они были добавлены.
    return decrypted_text.rstrip(' ')

def generate_random_key(length):
    """
    Генерирует случайный ключ перестановки заданной длины.
    Ключ - это перестановка чисел от 1 до length.
    """
    if length <= 0:
        return ""
    numbers = list(range(1, length + 1))
    random.shuffle(numbers)
    return ''.join(map(str, numbers))

def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать' для интерфейса tkinter.

    Функция извлекает текст и ключ из полей ввода, вызывает функцию шифрования,
    и выводит результат (исходный текст, ключ, таблицу, зашифрованный текст)
    в текстовое поле вывода. Обрабатывает возможные ошибки ввода.
    """
    # Получаем текст из поля ввода фамилии
    text = input_text.get()
    # Получаем ключ из поля ввода ключа
    key = key_entry.get()

    # Проверяем, введен ли текст
    if not text:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return # Выходим из функции

    # Проверяем, введен ли ключ
    if not key:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключ перестановки.\n")
        return

    try:
        # Вызываем функцию шифрования
        encrypted_text, table = simple_permutation_encrypt(text, key)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр простой одинарной перестановки (Шифрование) ---\n")
        # Вставляем исходное сообщение
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        # Вставляем ключ перестановки
        output_text.insert(tk.END, f"Ключ перестановки: {key}\n")
        # Вставляем таблицу после перестановки строк (для визуализации)
        output_text.insert(tk.END, f"Таблица (после перестановки строк): {table}\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с неправильным ключом
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать' для интерфейса tkinter.

    Функция извлекает зашифрованный текст и ключ из полей ввода, вызывает функцию дешифрования,
    и выводит результат (зашифрованный текст, ключ, восстановленное сообщение)
    в текстовое поле вывода. Обрабатывает возможные ошибки ввода.
    """
    # Получаем зашифрованный текст из поля ввода
    ciphertext = input_text.get()
    # Получаем ключ из поля ввода ключа
    key = key_entry.get()

    # Проверяем, введен ли зашифрованный текст
    if not ciphertext:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return # Выходим из функции

    # Проверяем, введен ли ключ
    if not key:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключ перестановки.\n")
        return

    try:
        # Вызываем функцию дешифрования
        decrypted_text = simple_permutation_decrypt(ciphertext, key)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр простой одинарной перестановки (Дешифрование) ---\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {ciphertext}\n")
        # Вставляем ключ перестановки
        output_text.insert(tk.END, f"Ключ перестановки: {key}\n")
        # Вставляем восстановленное сообщение
        output_text.insert(tk.END, f"Восстановленное сообщение: {decrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с неправильным ключом
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def generate_key_action():
    """
    Обработчик кнопки 'Сгенерировать ключ'.
    Генерирует случайный ключ на основе длины текста.
    """
    text = input_text.get()
    if not text:
        messagebox.showwarning("Предупреждение", "Сначала введите текст для шифрования.")
        return
    key_length = len(text)
    if key_length == 0:
        key_length = 4 # Установим минимальную длину 4, если текст пустой, но поле существует
    generated_key = generate_random_key(key_length)
    key_entry.delete(0, tk.END)
    key_entry.insert(0, generated_key)


# --- Создание графического интерфейса ---
# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Шифр простой одинарной перестановки (Модифицированный)")
# Устанавливаем начальный размер окна
root.geometry("900x700")

# --- Виджеты ---

# Фрейм для ввода текста
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
root.grid_columnconfigure(0, weight=1) # Делаем колонку 0 растягиваемой

# Метка для поля ввода фамилии
input_label = ttk.Label(input_frame, text="Введите текст (фамилию для первых двух шифров):")
input_label.grid(row=0, column=0, sticky="w")

# Поле ввода для фамилии
input_text = ttk.Entry(input_frame, width=60)
input_text.grid(row=1, column=0, sticky="ew", padx=(0, 10))
input_frame.grid_columnconfigure(0, weight=1) # Делаем колонку 0 внутри фрейма растягиваемой
input_text.insert(0, "Колосов")

# Фрейм для ввода ключа и кнопки генерации
key_frame = ttk.Frame(root)
key_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Метка для поля ввода ключа
key_label = ttk.Label(key_frame, text="Введите ключ перестановки (например, 2417653):")
key_label.grid(row=0, column=0, sticky="w")

# Поле ввода для ключа
key_entry = ttk.Entry(key_frame, width=30)
key_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
key_frame.grid_columnconfigure(0, weight=1)
key_entry.insert(0, "2417653")

# Кнопка генерации ключа
generate_key_button = ttk.Button(key_frame, text="Сгенерировать ключ", command=generate_key_action)
generate_key_button.grid(row=1, column=1, sticky="e")


# Кнопки для шифрования и дешифрования
button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

encrypt_button = ttk.Button(button_frame, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=0, column=0, padx=(0, 5))

decrypt_button = ttk.Button(button_frame, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=0, column=1, padx=(5, 0))

# Метка для поля вывода результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Текстовое поле с прокруткой для вывода результата
output_text = scrolledtext.ScrolledText(root, width=100, height=35)
output_text.grid(row=4, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
# Делаем так, чтобы строка 4 (где поле вывода) растягивалась при изменении размера окна
root.grid_rowconfigure(4, weight=1)

# Запуск главного цикла обработки событий tkinter
root.mainloop()
