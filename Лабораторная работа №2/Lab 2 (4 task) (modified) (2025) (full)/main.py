import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import string

def vertical_permutation_encrypt(text, key_word):
    """
    Шифрует текст с помощью шифра вертикальной перестановки.

    Этот метод шифрования работает следующим образом:
    1.  Создается виртуальная таблица. Количество столбцов равно длине ключевого слова.
    2.  Исходный текст вписывается в таблицу по строкам, слева направо, сверху вниз.
        Если текст короче размера таблицы (кол-во строк * кол-во столбцов), он дополняется пробелами.
    3.  Ключевое слово определяет порядок *столбцов* для финального считывания.
        Символы в ключевом слове сортируются по алфавиту. Порядок столбцов определяется
        позицией этих отсортированных символов в исходном ключевом слове.
        Например, ключ "ДЯДИНА":
        - Символы: Д, Я, Д, И, Н, А
        - Индексы: 0, 1, 2, 3, 4, 5
        - Сортировка по алфавиту: А(5), Д(0), Д(2), И(3), Н(4), Я(1)
        - Порядок столбцов для считывания: 5, 0, 2, 3, 4, 1
    4.  Зашифрованный текст формируется путем считывания символов из таблицы
        по *столбцам* в порядке, определенном ключевым словом. Сначала считывается
        первый столбец в порядке (например, столбец 5), затем второй (столбец 0) и т.д.

    :param text: Исходный текст для шифрования (str).
                 Пример: "Колосов Станислав".
    :param key_word: Ключевое слово (str), например, "ДЯДИНА".
                     Определяет количество столбцов и порядок их считывания.
    :return: tuple:
             - encrypted_text (str): Зашифрованный текст.
             - table (list of lists): Виртуальная таблица после вписывания
                                      символов по строкам, но до перестановки
                                      (считывания) столбцов.
    """
    # Проверяем, что ключевое слово не пустое
    if not key_word:
        # Если ключ пустой, возвращаем исходный текст и пустую таблицу
        return text, []

    n = len(key_word) # n - количество столбцов в виртуальной таблице
    original_length = len(text)

    # Создаем виртуальную таблицу, заполняя её по строкам
    # Количество строк зависит от длины текста и количества столбцов.
    table = []
    current_index = 0
    while current_index < original_length:
        row = []
        for j in range(n): # Проходим по количеству столбцов
            if current_index < original_length:
                # Если в тексте ещё есть символы, добавляем их в строку
                row.append(text[current_index])
                current_index += 1
            else:
                # Если текст закончился, заполняем пробелами
                row.append(' ')
        table.append(row)

    # Определяем порядок столбцов для считывания на основе ключевого слова.
    # Сортируем индексы по алфавиту символов ключевого слова.
    # sorted(range(n), key=lambda k: key_word[k]) возвращает список индексов
    # столбцов в порядке, в котором они должны быть считаны.
    # Например, для "ДЯДИНА" -> [5, 0, 2, 3, 4, 1]
    sorted_indices = sorted(range(n), key=lambda k: key_word[k])

    # Формируем зашифрованный текст, считывая символы из таблицы по столбцам
    # в порядке, определенном отсортированными индексами.
    encrypted_chars = []
    for col_idx in sorted_indices: # Проходим по индексам столбцов в нужном порядке
        for row in table: # Проходим по всем строкам таблицы
            encrypted_chars.append(row[col_idx]) # Добавляем символ из текущего столбца

    # Возвращаем зашифрованный текст в виде строки и таблицу после вписывания
    return ''.join(encrypted_chars), table

def vertical_permutation_decrypt(ciphertext, key_word):
    """
    Дешифрует текст, зашифрованный шифром вертикальной перестановки.

    Процесс дешифрования обратен шифрованию:
    1.  Определяется количество столбцов n (длина ключевого слова).
    2.  Рассчитывается количество строк num_rows (длина шифротекста / n).
    3.  Создается пустая виртуальная таблица размером num_rows x n.
    4.  Определяется порядок столбцов для *записи* в таблицу.
        Это *обратный* порядок считывания, использованный при шифровании.
        Если при шифровании столбцы читались в порядке sorted_indices,
        то при дешифровании они заполняются в *исходном* алфавитном порядке
        символов ключа. То есть, первый столбец в отсортированном списке
        заполняется первым, и т.д.
        Индекс столбца для записи определяется как inverse_order[sorted_pos] = original_col_index.
    5.  Зашифрованный текст разбивается на n частей (по одной для каждого столбца).
    6.  Каждая часть записывается в соответствующий столбец таблицы,
        определенный inverse_order.
    7.  Восстановленный текст формируется путем считывания символов из таблицы
        по строкам, слева направо, сверху вниз.

    :param ciphertext: Зашифрованный текст (str).
    :param key_word: Ключевое слово, использованное при шифровании (str).
    :return: str: Восстановленный (дешифрованный) текст.
    """
    # Проверяем, что ключевое слово не пустое
    if not key_word:
        return ciphertext

    n = len(key_word) # n - количество столбцов в виртуальной таблице

    # Проверяем, делится ли длина шифротекста на количество столбцов
    if len(ciphertext) % n != 0:
        raise ValueError("Длина зашифрованного текста не кратна длине ключа.")
    num_rows = len(ciphertext) // n

    # Создаем пустую виртуальную таблицу
    table = [['' for _ in range(n)] for _ in range(num_rows)]

    # Определяем порядок столбцов, в котором они были *считаны* при шифровании
    sorted_indices = sorted(range(n), key=lambda k: key_word[k])

    # Создаем обратный порядок: индекс в отсортированном списке -> индекс столбца в таблице
    # inverse_order[i] = j означает, что i-й столбец в порядке чтения (sorted_indices[i])
    # соответствует j-му столбцу в таблице (с индексом j).
    inverse_order = [0] * n
    for i, col_idx in enumerate(sorted_indices):
        inverse_order[i] = col_idx

    # Разбиваем шифротекст на столбцы
    # Длина каждого столбца равна num_rows
    for i in range(n): # i - индекс столбца в порядке чтения (от 0 до n-1)
        start_idx = i * num_rows
        end_idx = start_idx + num_rows
        col_data = ciphertext[start_idx:end_idx]
        # Записываем данные в столбец с индексом inverse_order[i] в таблице
        table_col_idx = inverse_order[i]
        for row_idx, char in enumerate(col_data):
            table[row_idx][table_col_idx] = char

    # Формируем дешифрованный текст, считывая таблицу по строкам
    decrypted_chars = []
    for row in table:
        decrypted_chars.extend(row)

    # Восстановленный текст (включая добавленные пробелы)
    decrypted_text_with_padding = ''.join(decrypted_chars)
    # Удаляем пробелы в конце, которые были добавлены при шифровании
    return decrypted_text_with_padding.rstrip(' ')

def generate_random_key_word(length):
    """
    Генерирует случайное ключевое слово заданной длины.
    """
    if length <= 0:
        return ""
    # Используем латинские буквы для простоты генерации
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))

def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать' для интерфейса tkinter.

    Функция извлекает текст и ключевое слово из полей ввода, вызывает функцию шифрования,
    и выводит результат (исходный текст, ключ, таблицу, порядок столбцов, зашифрованный текст)
    в текстовое поле вывода. Обрабатывает возможные ошибки ввода.
    """
    # Получаем текст из поля ввода фамилии и имени
    text = input_text.get()
    # Получаем ключевое слово из поля ввода
    key_word = key_entry.get()

    # Проверяем, введен ли текст
    if not text:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите фамилию и имя для шифрования.\n")
        return # Выходим из функции

    # Проверяем, введено ли ключевое слово
    if not key_word:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово.\n")
        return

    try:
        # Вызываем функцию шифрования
        encrypted_text, table = vertical_permutation_encrypt(text, key_word)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр вертикальной перестановки (Шифрование) ---\n")
        # Вставляем исходное сообщение
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        # Вставляем ключевое слово
        output_text.insert(tk.END, f"Ключевое слово: {key_word}\n")
        # Вставляем таблицу после вписывания (до перестановки столбцов)
        output_text.insert(tk.END, f"Таблица (до перестановки столбцов): {table}\n")
        # Вставляем порядок столбцов, определенный ключом
        # Используем ту же логику, что и в функции шифрования
        sorted_indices = sorted(range(len(key_word)), key=lambda k: key_word[k])
        output_text.insert(tk.END, f"Порядок столбцов (по ключу): {sorted_indices}\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")
    except Exception as e: # Ловим любые другие ошибки
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать' для интерфейса tkinter.

    Функция извлекает зашифрованный текст и ключевое слово из полей ввода,
    вызывает функцию дешифрования, и выводит результат (зашифрованный текст,
    ключ, восстановленное сообщение) в текстовое поле вывода.
    Обрабатывает возможные ошибки ввода.
    """
    # Получаем зашифрованный текст из поля ввода
    ciphertext = input_text.get()
    # Получаем ключевое слово из поля ввода
    key_word = key_entry.get()

    # Проверяем, введен ли зашифрованный текст
    if not ciphertext:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return # Выходим из функции

    # Проверяем, введено ли ключевое слово
    if not key_word:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово.\n")
        return

    try:
        # Вызываем функцию дешифрования
        decrypted_text = vertical_permutation_decrypt(ciphertext, key_word)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр вертикальной перестановки (Дешифрование) ---\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {ciphertext}\n")
        # Вставляем ключевое слово
        output_text.insert(tk.END, f"Ключевое слово: {key_word}\n")
        # Вставляем восстановленное сообщение
        output_text.insert(tk.END, f"Восстановленное сообщение: {decrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с некорректной длиной
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def generate_key_action():
    """
    Обработчик кнопки 'Сгенерировать ключ'.
    Генерирует случайное ключевое слово на основе длины текста.
    """
    text = input_text.get()
    if not text:
        messagebox.showwarning("Предупреждение", "Сначала введите текст для шифрования.")
        return
    key_length = len(text)
    if key_length == 0:
        key_length = 6 # Установим минимальную длину 6, если текст пустой, но поле существует
    generated_key = generate_random_key_word(key_length)
    key_entry.delete(0, tk.END)
    key_entry.insert(0, generated_key)


# --- Создание графического интерфейса ---
# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Шифр вертикальной перестановки (Модифицированный)")
# Устанавливаем начальный размер окна
root.geometry("900x700")

# --- Виджеты ---

# Фрейм для ввода текста
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
root.grid_columnconfigure(0, weight=1) # Делаем колонку 0 растягиваемой

# Метка для поля ввода фамилии и имени
input_label = ttk.Label(input_frame, text="Введите текст (фамилию и имя для остальных шифров):")
input_label.grid(row=0, column=0, sticky="w")

# Поле ввода для фамилии и имени
input_text = ttk.Entry(input_frame, width=60)
input_text.grid(row=1, column=0, sticky="ew", padx=(0, 10))
input_frame.grid_columnconfigure(0, weight=1) # Делаем колонку 0 внутри фрейма растягиваемой
input_text.insert(0, "Колосов Станислав")

# Фрейм для ввода ключа и кнопки генерации
key_frame = ttk.Frame(root)
key_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Метка для поля ввода ключевого слова
key_label = ttk.Label(key_frame, text="Введите ключевое слово (например, ДЯДИНА):")
key_label.grid(row=0, column=0, sticky="w")

# Поле ввода для ключевого слова
key_entry = ttk.Entry(key_frame, width=30)
key_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
key_frame.grid_columnconfigure(0, weight=1)
key_entry.insert(0, "ДЯДИНА")

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
