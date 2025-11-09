import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import string

def double_permutation_encrypt(text, col_key_word, row_key_word):
    """
    Шифрует текст с помощью шифра двойной перестановки.

    Этот метод шифрования работает следующим образом:
    1.  Создается виртуальная таблица. Количество столбцов равно длине ключевого слова
        для перестановки столбцов (col_key_word). Количество строк рассчитывается
        исходя из длины текста и количества столбцов (округляется вверх).
    2.  Исходный текст вписывается в таблицу по строкам, слева направо, сверху вниз.
        Если текст короче размера таблицы (кол-во строк * кол-во столбцов), он дополняется пробелами.
    3.  Выполняется *первая* перестановка: столбцы таблицы переставляются по алфавиту
        символов в ключевом слове col_key_word. Порядок столбцов определяется
        позицией этих отсортированных символов в *исходном* ключевом слове.
        Например, для ключа "ДЯДИНА" (col_key_word):
        - Символы: Д, Я, Д, И, Н, А
        - Индексы: 0, 1, 2, 3, 4, 5
        - Сортировка по алфавиту: А(5), Д(0), Д(2), И(3), Н(4), Я(1)
        - Порядок столбцов для перестановки: 5, 0, 2, 3, 4, 1
        Таблица после этого шага будет иметь столбцы в новом порядке.
    4.  Выполняется *вторая* перестановка: строки таблицы (уже с переставленными столбцами)
        переставляются по алфавиту символов в ключевом слове для перестановки строк (row_key_word).
        Порядок строк определяется позицией этих отсортированных символов в *исходном* ключевом слове row_key_word.
        Например, для ключа "МОСКВА" (row_key_word):
        - Символы: М, О, С, К, В, А
        - Индексы: 0, 1, 2, 3, 4, 5
        - Сортировка по алфавиту: А(5), В(4), К(3), М(0), О(1), С(2)
        - Порядок строк для перестановки: 5, 4, 3, 0, 1, 2
    5.  Зашифрованный текст формируется путем считывания символов из финальной
        таблицы по строкам, слева направо, сверху вниз.

    :param text: Исходный текст для шифрования (str).
                 Пример: "Колосов Станислав".
    :param col_key_word: Ключевое слово для перестановки столбцов (str).
                         Пример: "ДЯДИНА".
    :param row_key_word: Ключевое слово для перестановки строк (str).
                         Пример: "МОСКВА".
    :return: tuple:
             - encrypted_text (str): Зашифрованный текст.
             - final_table (list of lists): Виртуальная таблица после обеих перестановок.
    """
    # Проверяем, что оба ключевых слова не пустые
    if not col_key_word or not row_key_word:
        # Если какой-либо ключ пустой, возвращаем исходный текст и пустую таблицу
        return text, []

    n_cols = len(col_key_word) # n_cols - количество столбцов в виртуальной таблице
    n_rows = len(row_key_word) # n_rows - количество строк в виртуальной таблице

    # Дополняем текст пробелами до размера таблицы (n_rows * n_cols).
    # Это гарантирует, что текст можно будет полностью разместить в таблице размером n_rows x n_cols.
    original_length = len(text)
    total_cells = n_rows * n_cols
    padded_text = text.ljust(total_cells)

    # Создаем виртуальную таблицу, заполняя её по строкам из дополненного текста
    table = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    index = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if index < len(padded_text):
                table[r][c] = padded_text[index]
                index += 1

    # --- Первая перестановка: столбцов ---
    # Определяем порядок столбцов для перестановки на основе col_key_word.
    # sorted(range(n_cols), key=lambda k: col_key_word[k]) возвращает список индексов
    # столбцов в порядке, в котором они должны быть переставлены.
    sorted_col_indices = sorted(range(n_cols), key=lambda k: col_key_word[k])

    # Создаем новую таблицу с переставленными столбцами
    table_after_col_perm = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    for new_col_idx, old_col_idx in enumerate(sorted_col_indices):
        # Копируем столбец old_col_idx из исходной таблицы в позицию new_col_idx новой таблицы
        for r in range(n_rows):
            table_after_col_perm[r][new_col_idx] = table[r][old_col_idx]

    # --- Вторая перестановка: строк ---
    # Определяем порядок строк для перестановки на основе row_key_word.
    # sorted(range(n_rows), key=lambda k: row_key_word[k]) возвращает список индексов
    # строк в порядке, в котором они должны быть переставлены.
    sorted_row_indices = sorted(range(n_rows), key=lambda k: row_key_word[k])

    # Создаем финальную таблицу с переставленными строками
    final_table = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    for new_row_idx, old_row_idx in enumerate(sorted_row_indices):
        # Копируем строку old_row_idx из таблицы после перестановки столбцов
        # в позицию new_row_idx финальной таблицы
        final_table[new_row_idx] = table_after_col_perm[old_row_idx][:] # [:] - копируем список

    # Формируем зашифрованный текст, считывая символы из финальной таблицы по строкам
    encrypted_chars = []
    for r in range(n_rows): # Проходим по строкам финальной таблицы
        for c in range(n_cols): # Проходим по столбцам строки
            encrypted_chars.append(final_table[r][c]) # Добавляем символ

    # Возвращаем зашифрованный текст в виде строки и финальную таблицу после обеих перестановок
    return ''.join(encrypted_chars), final_table

def double_permutation_decrypt(ciphertext, col_key_word, row_key_word):
    """
    Дешифрует текст, зашифрованный шифром двойной перестановки.

    Процесс дешифрования обратен шифрованию:
    1.  Определяется количество столбцов n_cols (длина col_key_word) и строк n_rows (длина row_key_word).
    2.  Проверяется, совпадает ли длина шифротекста с n_rows * n_cols.
    3.  Создается пустая виртуальная таблица размером n_rows x n_cols.
    4.  Зашифрованный текст записывается в таблицу в фиксированном порядке
        (например, по строкам), восстанавливая финальную таблицу после шифрования.
    5.  Выполняется *обратная* перестановка строк.
        Определяется порядок, в котором строки *были* переставлены при шифровании (sorted_row_indices).
        Создается *обратный* порядок: inverse_row_order[sorted_row_idx] = original_row_idx.
        Затем строки таблицы переставляются обратно по этому обратному порядку.
    6.  Выполняется *обратная* перестановка столбцов.
        Определяется порядок, в котором столбцы *были* переставлены при шифровании (sorted_col_indices).
        Создается *обратный* порядок: inverse_col_order[sorted_col_idx] = original_col_idx.
        Затем столбцы таблицы переставляются обратно по этому обратному порядку.
    7.  Восстановленный текст формируется путем считывания символов из таблицы
        по строкам, слева направо, сверху вниз.

    :param ciphertext: Зашифрованный текст (str).
    :param col_key_word: Ключевое слово для перестановки столбцов, использованное при шифровании (str).
    :param row_key_word: Ключевое слово для перестановки строк, использованное при шифровании (str).
    :return: str: Восстановленный (дешифрованный) текст.
    """
    # Проверяем, что оба ключевых слова не пустые
    if not col_key_word or not row_key_word:
        return ciphertext

    n_cols = len(col_key_word)
    n_rows = len(row_key_word)

    # Проверяем, совпадает ли длина шифротекста с размером таблицы
    if len(ciphertext) != n_rows * n_cols:
        raise ValueError("Длина зашифрованного текста не соответствует размеру таблицы (n_rows * n_cols).")

    # --- Восстанавливаем финальную таблицу из шифротекста (по строкам) ---
    table = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    index = 0
    for r in range(n_rows):
        for c in range(n_cols):
            table[r][c] = ciphertext[index]
            index += 1

    # --- Обратная перестановка строк ---
    # Определяем порядок, в котором строки были переставлены при шифровании
    sorted_row_indices = sorted(range(n_rows), key=lambda k: row_key_word[k])
    # Создаем обратный порядок: индекс в отсортированном списке -> индекс строки в таблице
    inverse_row_order = [0] * n_rows
    for i, original_row_idx in enumerate(sorted_row_indices):
        inverse_row_order[original_row_idx] = i

    # Создаем таблицу после обратной перестановки строк
    table_after_row_unperm = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    for new_row_idx, old_row_idx in enumerate(inverse_row_order):
        table_after_row_unperm[new_row_idx] = table[old_row_idx][:]

    # --- Обратная перестановка столбцов ---
    # Определяем порядок, в котором столбцы были переставлены при шифровании
    sorted_col_indices = sorted(range(n_cols), key=lambda k: col_key_word[k])
    # Создаем обратный порядок: индекс в отсортированном списке -> индекс столбца в таблице
    inverse_col_order = [0] * n_cols
    for i, original_col_idx in enumerate(sorted_col_indices):
        inverse_col_order[original_col_idx] = i

    # Создаем таблицу после обратной перестановки столбцов (исходная таблица до шифрования)
    original_table = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    for r in range(n_rows):
        for new_col_idx, old_col_idx in enumerate(inverse_col_order):
            original_table[r][new_col_idx] = table_after_row_unperm[r][old_col_idx]

    # --- Формируем восстановленный текст из исходной таблицы (по строкам) ---
    decrypted_chars = []
    for r in range(n_rows):
        for c in range(n_cols):
            decrypted_chars.append(original_table[r][c])

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

    Функция извлекает текст и два ключевых слова из полей ввода,
    вызывает функцию шифрования, и выводит результат (исходный текст,
    ключи, финальную таблицу, зашифрованный текст) в текстовое поле вывода.
    Обрабатывает возможные ошибки ввода.
    """
    # Получаем текст из поля ввода фамилии и имени
    text = input_text.get()
    # Получаем ключевые слова из полей ввода
    col_key_word = col_key_entry.get()
    row_key_word = row_key_entry.get()

    # Проверяем, введен ли текст
    if not text:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите фамилию и имя для шифрования.\n")
        return # Выходим из функции

    # Проверяем, введены ли оба ключевых слова
    if not col_key_word or not row_key_word:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите оба ключевых слова.\n")
        return

    try:
        # Вызываем функцию шифрования
        encrypted_text, table = double_permutation_encrypt(text, col_key_word, row_key_word)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр двойной перестановки (Шифрование) ---\n")
        # Вставляем исходное сообщение
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        # Вставляем ключ перестановки столбцов
        output_text.insert(tk.END, f"Ключ перестановки столбцов: {col_key_word}\n")
        # Вставляем ключ перестановки строк
        output_text.insert(tk.END, f"Ключ перестановки строк: {row_key_word}\n")
        # Вставляем финальную таблицу после обеих перестановок (для визуализации)
        output_text.insert(tk.END, f"Таблица (после двойной перестановки): {table}\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")
    except Exception as e: # Ловим любые другие ошибки
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать' для интерфейса tkinter.

    Функция извлекает зашифрованный текст и два ключевых слова из полей ввода,
    вызывает функцию дешифрования, и выводит результат (зашифрованный текст,
    ключи, восстановленное сообщение) в текстовое поле вывода.
    Обрабатывает возможные ошибки ввода.
    """
    # Получаем зашифрованный текст из поля ввода
    ciphertext = input_text.get()
    # Получаем ключевые слова из полей ввода
    col_key_word = col_key_entry.get()
    row_key_word = row_key_entry.get()

    # Проверяем, введен ли зашифрованный текст
    if not ciphertext:
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем сообщение об ошибке
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return # Выходим из функции

    # Проверяем, введены ли оба ключевых слова
    if not col_key_word or not row_key_word:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите оба ключевых слова.\n")
        return

    try:
        # Вызываем функцию дешифрования
        decrypted_text = double_permutation_decrypt(ciphertext, col_key_word, row_key_word)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр двойной перестановки (Дешифрование) ---\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {ciphertext}\n")
        # Вставляем ключ перестановки столбцов
        output_text.insert(tk.END, f"Ключ перестановки столбцов: {col_key_word}\n")
        # Вставляем ключ перестановки строк
        output_text.insert(tk.END, f"Ключ перестановки строк: {row_key_word}\n")
        # Вставляем восстановленное сообщение
        output_text.insert(tk.END, f"Восстановленное сообщение: {decrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с некорректной длиной
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def generate_col_key_action():
    """
    Обработчик кнопки 'Сгенерировать ключ (столбцы)'.
    Генерирует случайное ключевое слово для перестановки столбцов.
    """
    text = input_text.get()
    if not text:
        messagebox.showwarning("Предупреждение", "Сначала введите текст для шифрования.")
        return
    key_length = len(text)
    if key_length == 0:
        key_length = 6 # Установим минимальную длину 6, если текст пустой, но поле существует
    generated_key = generate_random_key_word(key_length)
    col_key_entry.delete(0, tk.END)
    col_key_entry.insert(0, generated_key)

def generate_row_key_action():
    """
    Обработчик кнопки 'Сгенерировать ключ (строки)'.
    Генерирует случайное ключевое слово для перестановки строк.
    """
    text = input_text.get()
    if not text:
        messagebox.showwarning("Предупреждение", "Сначала введите текст для шифрования.")
        return
    key_length = len(text)
    if key_length == 0:
        key_length = 6 # Установим минимальную длину 6, если текст пустой, но поле существует
    generated_key = generate_random_key_word(key_length)
    row_key_entry.delete(0, tk.END)
    row_key_entry.insert(0, generated_key)


# --- Создание графического интерфейса ---
# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Шифр двойной перестановки (Модифицированный)")
# Устанавливаем начальный размер окна
root.geometry("1000x800")

# --- Виджеты ---

# Фрейм для ввода текста
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
root.grid_columnconfigure(0, weight=1) # Делаем колонку 0 растягиваемой

# Метка для поля ввода фамилии и имени
input_label = ttk.Label(input_frame, text="Введите текст (фамилию и имя для остальных шифров):")
input_label.grid(row=0, column=0, sticky="w")

# Поле ввода для фамилии и имени
input_text = ttk.Entry(input_frame, width=70)
input_text.grid(row=1, column=0, sticky="ew", padx=(0, 10))
input_frame.grid_columnconfigure(0, weight=1) # Делаем колонку 0 внутри фрейма растягиваемой
input_text.insert(0, "Колосов Станислав")

# Фрейм для ввода ключевых слов
key_frame = ttk.Frame(root)
key_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Метка и поле ввода для ключа перестановки столбцов
col_key_label = ttk.Label(key_frame, text="Ключ перестановки столбцов (например, ДЯДИНА):")
col_key_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
col_key_entry = ttk.Entry(key_frame, width=30)
col_key_entry.grid(row=0, column=1, padx=(0, 10), sticky="w")
col_key_entry.insert(0, "ДЯДИНА") # Вставляем значение по умолчанию

# Кнопка генерации ключа столбцов
generate_col_key_button = ttk.Button(key_frame, text="Сгенерировать (столбцы)", command=generate_col_key_action)
generate_col_key_button.grid(row=0, column=2, padx=(0, 10), sticky="w")

# Метка и поле ввода для ключа перестановки строк
row_key_label = ttk.Label(key_frame, text="Ключ перестановки строк (например, МОСКВА):")
row_key_label.grid(row=1, column=0, padx=(0, 5), sticky="w")
row_key_entry = ttk.Entry(key_frame, width=30)
row_key_entry.grid(row=1, column=1, padx=(0, 10), sticky="w")
row_key_entry.insert(0, "МОСКВА") # Вставляем значение по умолчанию

# Кнопка генерации ключа строк
generate_row_key_button = ttk.Button(key_frame, text="Сгенерировать (строки)", command=generate_row_key_action)
generate_row_key_button.grid(row=1, column=2, padx=(0, 10), sticky="w")


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
output_text = scrolledtext.ScrolledText(root, width=110, height=40)
output_text.grid(row=4, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
# Делаем так, чтобы строка 4 (где поле вывода) растягивалась при изменении размера окна
root.grid_rowconfigure(4, weight=1)

# Запуск главного цикла обработки событий tkinter
root.mainloop()
