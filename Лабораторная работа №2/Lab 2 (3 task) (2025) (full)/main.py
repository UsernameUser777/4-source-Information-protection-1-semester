import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def route_table_permutation_encrypt(text, rows, cols, write_route, read_route):
    """
    Шифрует текст с помощью шифра табличной маршрутной перестановки.

    Этот метод шифрования работает следующим образом:
    1.  Создается виртуальная таблица заданного размера (rows x cols).
    2.  Исходный текст вписывается в эту таблицу по определенному *маршруту вписывания*.
        Это может быть, например, по строкам слева направо, "змейкой", по диагоналям и т.д.
    3.  Если текст короче размера таблицы (rows * cols), он дополняется пробелами.
    4.  Зашифрованный текст формируется путем выписывания символов из таблицы
        по другому, *маршруту выписывания*. Это также может быть, например, по столбцам,
        "змейкой", по диагоналям и т.д.
    5.  Ключом шифра являются размеры таблицы и два маршрута (вписывания и выписывания).

    :param text: Исходный текст для шифрования (str).
                 Пример: "Колосов Станислав".
    :param rows: Количество строк в виртуальной таблице (int).
                 Пример: 3.
    :param cols: Количество столбцов в виртуальной таблице (int).
                 Пример: 6.
    :param write_route: Маршрут вписывания (str), например, "змейка_сверху", "по_строкам".
                         Определяет, как символы из текста будут помещены в таблицу.
    :param read_route: Маршрут выписывания (str), например, "снизу_по_столбцам", "по_столбцам".
                        Определяет, как символы из заполненной таблицы будут объединены
                        в зашифрованное сообщение.
    :return: tuple:
             - encrypted_text (str): Зашифрованный текст.
             - table (list of lists): Виртуальная таблица после вписывания символов
                                      по маршруту write_route, но до выписывания.
    """
    # Рассчитываем общее количество ячеек в таблице
    total_cells = rows * cols

    # Дополняем текст пробелами до размера таблицы (total_cells).
    # Это гарантирует, что текст можно будет полностью разместить в таблице.
    padded_text = text.ljust(total_cells)

    # Создаем пустую виртуальную таблицу (список списков), заполненную пустыми строками
    table = [['' for _ in range(cols)] for _ in range(rows)]

    # --- Определяем последовательность координат (r, c) для вписывания ---
    # Эта последовательность зависит от выбранного маршрута вписывания.
    write_coords = []
    if write_route == "змейка_сверху":
        # Пример маршрута: строки поочередно, направление чередуется
        # r=0: c=0->cols-1 (слева направо)
        # r=1: c=cols-1->0 (справа налево)
        # r=2: c=0->cols-1 (слева направо) и т.д.
        for r in range(rows):
            if r % 2 == 0:  # Четная строка - слева направо
                for c in range(cols):
                    write_coords.append((r, c))
            else:  # Нечетная строка - справа налево
                for c in range(cols - 1, -1, -1):
                    write_coords.append((r, c))
    elif write_route == "по_строкам":
        # Простой маршрут: заполняем строку за строкой сверху вниз
        for r in range(rows):
            for c in range(cols):
                write_coords.append((r, c))
    # Можно добавить другие маршруты вписывания по аналогии
    else:
        # Если маршрут неизвестен, используем "по_строкам" как стандартный
        for r in range(rows):
            for c in range(cols):
                write_coords.append((r, c))

    # Заполняем таблицу по рассчитанному маршруту вписывания
    # Проходим по индексам символов в дополненном тексте и координатам в таблице
    for i, (r, c) in enumerate(write_coords):
        if i < len(padded_text):
            table[r][c] = padded_text[i]

    # --- Определяем последовательность координат (r, c) для выписывания ---
    # Эта последовательность зависит от выбранного маршрута выписывания.
    read_coords = []
    if read_route == "снизу_по_столбцам":
        # Пример маршрута: проходим по столбцам, но внутри столбца - снизу вверх
        for c in range(cols): # Проходим по всем столбцам (от 0 до cols-1)
            for r in range(rows - 1, -1, -1): # Проходим по строкам столбца (от rows-1 до 0)
                read_coords.append((r, c))
    elif read_route == "по_столбцам":
        # Простой маршрут: проходим по столбцам, внутри столбца - сверху вниз
        for c in range(cols): # Проходим по всем столбцам
            for r in range(rows): # Проходим по строкам столбца (от 0 до rows-1)
                read_coords.append((r, c))
    elif read_route == "по_диагонали":
        # Пример сложного маршрута: диагонали слева-сверх вниз-вправо
        # Сначала диагонали, начинающиеся в верхней строке (c=0, c=1, ...)
        for start_col in range(cols):
            r, c = 0, start_col # Начинаем с верхней строки, текущего столбца
            while r < rows and c < cols: # Пока не вышли за границы таблицы
                read_coords.append((r, c))
                r += 1 # Переходим на следующую строку
                c += 1 # Переходим на следующий столбец
        # Потом диагонали, начинающиеся в левом столбце (r=1, r=2, ...), кроме первой (уже прошли)
        for start_row in range(1, rows):
            r, c = start_row, 0 # Начинаем с текущей строки, левого столбца
            while r < rows and c < cols: # Пока не вышли за границы таблицы
                read_coords.append((r, c))
                r += 1 # Переходим на следующую строку
                c += 1 # Переходим на следующий столбец
    # Можно добавить другие маршруты выписывания по аналогии
    else:
        # Если маршрут неизвестен, используем "по_столбцам" как стандартный
        for c in range(cols):
            for r in range(rows):
                read_coords.append((r, c))

    # Формируем зашифрованный текст, считывая символы из таблицы по маршруту выписывания
    encrypted_chars = []
    for r, c in read_coords:
        encrypted_chars.append(table[r][c]) # Добавляем символ из текущей ячейки

    # Возвращаем зашифрованный текст в виде строки и таблицу после вписывания
    return ''.join(encrypted_chars), table

def route_table_permutation_decrypt(ciphertext, rows, cols, write_route, read_route):
    """
    Дешифрует текст, зашифрованный шифром табличной маршрутной перестановки.

    Процесс дешифрования обратен шифрованию:
    1.  Создается пустая виртуальная таблица размером rows x cols.
    2.  Определяется *маршрут выписывания* (read_route), использованный при шифровании.
        По этому маршруту в таблицу записываются символы из зашифрованного текста.
    3.  Затем определяется *маршрут вписывания* (write_route), использованный при шифровании.
        По *обратному* этому маршруту символы из таблицы собираются в исходное сообщение.
        Обратный маршрут - это путь, по которому нужно "пройти" по таблице,
        чтобы извлечь символы в том порядке, в котором они были туда помещены изначально.

    :param ciphertext: Зашифрованный текст (str).
    :param rows: Количество строк в виртуальной таблице (int).
    :param cols: Количество столбцов в виртуальной таблице (int).
    :param write_route: Маршрут вписывания, использованный при шифровании (str).
    :param read_route: Маршрут выписывания, использованный при шифровании (str).
    :return: str: Восстановленный (дешифрованный) текст.
    """
    # Проверяем, совпадает ли длина зашифрованного текста с размером таблицы
    if len(ciphertext) != rows * cols:
        # Если не совпадает, это ошибка или некорректный ввод
        raise ValueError("Длина зашифрованного текста не соответствует размеру таблицы.")

    # Создаем пустую виртуальную таблицу (список списков), заполненную пустыми строками
    table = [['' for _ in range(cols)] for _ in range(rows)]

    # --- Определяем последовательность координат (r, c) для выписывания (как при шифровании) ---
    # Это маршрут, по которому мы будем *заполнять* таблицу из зашифрованного текста.
    read_coords = []
    if read_route == "снизу_по_столбцам":
        for c in range(cols):
            for r in range(rows - 1, -1, -1):
                read_coords.append((r, c))
    elif read_route == "по_столбцам":
        for c in range(cols):
            for r in range(rows):
                read_coords.append((r, c))
    elif read_route == "по_диагонали":
        for start_col in range(cols):
            r, c = 0, start_col
            while r < rows and c < cols:
                read_coords.append((r, c))
                r += 1
                c += 1
        for start_row in range(1, rows):
            r, c = start_row, 0
            while r < rows and c < cols:
                read_coords.append((r, c))
                r += 1
                c += 1
    else:
        for c in range(cols):
            for r in range(rows):
                read_coords.append((r, c))

    # Заполняем таблицу по маршруту выписывания из зашифрованного текста
    for i, (r, c) in enumerate(read_coords):
        if i < len(ciphertext):
            table[r][c] = ciphertext[i]

    # --- Определяем последовательность координат (r, c) для вписывания (как при шифровании) ---
    # Это маршрут, по которому мы будем *считывать* символы из таблицы,
    # чтобы восстановить исходный текст.
    write_coords = []
    if write_route == "змейка_сверху":
        for r in range(rows):
            if r % 2 == 0:
                for c in range(cols):
                    write_coords.append((r, c))
            else:
                for c in range(cols - 1, -1, -1):
                    write_coords.append((r, c))
    elif write_route == "по_строкам":
        for r in range(rows):
            for c in range(cols):
                write_coords.append((r, c))
    else:
        for r in range(rows):
            for c in range(cols):
                write_coords.append((r, c))

    # Считываем символы из таблицы по маршруту вписывания
    decrypted_chars = []
    for r, c in write_coords:
        decrypted_chars.append(table[r][c])

    # Восстановленный текст (включая добавленные пробелы)
    decrypted_text_with_padding = ''.join(decrypted_chars)
    # Удаляем пробелы в конце, которые были добавлены при шифровании
    return decrypted_text_with_padding.rstrip(' ')


def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать' для интерфейса tkinter.

    Функция извлекает текст, размеры таблицы и маршруты из полей ввода/выбора,
    вызывает функцию шифрования, и выводит результат (исходный текст, размеры,
    маршруты, таблицу, зашифрованный текст) в текстовое поле вывода.
    Обрабатывает возможные ошибки ввода (например, некорректные размеры).
    """
    # Получаем текст из поля ввода фамилии и имени
    text = input_text.get()
    try:
        # Получаем количество строк и столбцов из полей ввода
        # Пытаемся преобразовать в целое число
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
    except ValueError:
        # Если преобразование не удалось, очищаем вывод и показываем ошибку
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Количество строк и столбцов должно быть целым числом.\n")
        return # Выходим из функции

    # Получаем выбранные маршруты вписывания и выписывания из выпадающих списков
    write_route = write_route_combo.get()
    read_route = read_route_combo.get()

    # Проверяем, введен ли текст
    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию и имя для шифрования.\n")
        return

    # Проверяем, положительные ли размеры таблицы
    if rows <= 0 or cols <= 0:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Количество строк и столбцов должно быть положительным.\n")
        return

    try:
        # Вызываем функцию шифрования
        encrypted_text, table = route_table_permutation_encrypt(text, rows, cols, write_route, read_route)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр табличной маршрутной перестановки (Шифрование) ---\n")
        # Вставляем исходное сообщение
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        # Вставляем размер таблицы
        output_text.insert(tk.END, f"Размер таблицы: {rows} x {cols}\n")
        # Вставляем маршрут вписывания
        output_text.insert(tk.END, f"Маршрут вписывания: {write_route}\n")
        # Вставляем маршрут выписывания
        output_text.insert(tk.END, f"Маршрут выписывания: {read_route}\n")
        # Вставляем таблицу после вписывания (для визуализации)
        output_text.insert(tk.END, f"Таблица (после вписывания): {table}\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")
    except Exception as e: # Ловим любые другие ошибки
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать' для интерфейса tkinter.

    Функция извлекает зашифрованный текст, размеры таблицы и маршруты из полей ввода/выбора,
    вызывает функцию дешифрования, и выводит результат (зашифрованный текст, размеры,
    маршруты, восстановленное сообщение) в текстовое поле вывода.
    Обрабатывает возможные ошибки ввода.
    """
    # Получаем зашифрованный текст из поля ввода
    ciphertext = input_text.get()
    try:
        # Получаем количество строк и столбцов из полей ввода
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Количество строк и столбцов должно быть целым числом.\n")
        return

    # Получаем маршруты из выпадающих списков
    write_route = write_route_combo.get()
    read_route = read_route_combo.get()

    # Проверяем, введен ли зашифрованный текст
    if not ciphertext:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return

    if rows <= 0 or cols <= 0:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Количество строк и столбцов должно быть положительным.\n")
        return

    try:
        # Вызываем функцию дешифрования
        decrypted_text = route_table_permutation_decrypt(ciphertext, rows, cols, write_route, read_route)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр табличной маршрутной перестановки (Дешифрование) ---\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {ciphertext}\n")
        # Вставляем размер таблицы
        output_text.insert(tk.END, f"Размер таблицы: {rows} x {cols}\n")
        # Вставляем маршрут вписывания (использованный при шифровании)
        output_text.insert(tk.END, f"Маршрут вписывания (ключ): {write_route}\n")
        # Вставляем маршрут выписывания (использованный при шифровании)
        output_text.insert(tk.END, f"Маршрут выписывания (ключ): {read_route}\n")
        # Вставляем восстановленное сообщение
        output_text.insert(tk.END, f"Восстановленное сообщение: {decrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с некорректной длиной или маршрутом
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")


# --- Создание графического интерфейса ---
# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Шифр табличной маршрутной перестановки")
# Устанавливаем начальный размер окна
root.geometry("900x700")

# --- Виджеты ---

# Метка для поля ввода фамилии и имени
input_label = ttk.Label(root, text="Введите текст (фамилию и имя для остальных шифров):")
# Размещаем метку в сетке окна (строка 0, столбец 0)
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Поле ввода для фамилии и имени
input_text = ttk.Entry(root, width=60)
# Размещаем поле ввода (строка 1, столбец 0, растягиваем на 2 столбца)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
# Вставляем значение по умолчанию в поле ввода
input_text.insert(0, "Колосов Станислав")

# Фрейм для ввода размеров таблицы
size_frame = ttk.Frame(root)
# Размещаем фрейм (строка 2, столбец 0)
size_frame.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Метка и поле ввода для количества строк
rows_label = ttk.Label(size_frame, text="Количество строк:")
rows_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
rows_entry = ttk.Entry(size_frame, width=10)
rows_entry.grid(row=0, column=1, padx=(0, 10), sticky="w")
rows_entry.insert(0, "3") # Вставляем значение по умолчанию

# Метка и поле ввода для количества столбцов
cols_label = ttk.Label(size_frame, text="Количество столбцов:")
cols_label.grid(row=0, column=2, padx=(0, 5), sticky="w")
cols_entry = ttk.Entry(size_frame, width=10)
cols_entry.grid(row=0, column=3, sticky="w")
cols_entry.insert(0, "6") # Вставляем значение по умолчанию

# Фрейм для выбора маршрутов
route_frame = ttk.Frame(root)
# Размещаем фрейм (строка 3, столбец 0)
route_frame.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Метка и выпадающий список для маршрута вписывания
write_route_label = ttk.Label(route_frame, text="Маршрут вписывания:")
write_route_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
# Определяем доступные варианты маршрутов вписывания
write_route_options = ["по_строкам", "змейка_сверху"]
write_route_combo = ttk.Combobox(route_frame, values=write_route_options, state="readonly", width=15)
write_route_combo.grid(row=0, column=1, padx=(0, 10), sticky="w")
write_route_combo.set(write_route_options[1]) # Устанавливаем значение по умолчанию

# Метка и выпадающий список для маршрута выписывания
read_route_label = ttk.Label(route_frame, text="Маршрут выписывания:")
read_route_label.grid(row=0, column=2, padx=(0, 5), sticky="w")
# Определяем доступные варианты маршрутов выписывания
read_route_options = ["по_столбцам", "снизу_по_столбцам", "по_диагонали"]
read_route_combo = ttk.Combobox(route_frame, values=read_route_options, state="readonly", width=15)
read_route_combo.grid(row=0, column=3, sticky="w")
read_route_combo.set(read_route_options[1]) # Устанавливаем значение по умолчанию

# Кнопки для шифрования и дешифрования
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
# Размещаем кнопку (строка 4, столбец 0), прижимаем к востоку
encrypt_button.grid(row=4, column=0, padx=5, pady=10, sticky="e")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
# Размещаем кнопку (строка 4, столбец 1), прижимаем к востоку
decrypt_button.grid(row=4, column=1, padx=5, pady=10, sticky="e")

# Метка для поля вывода результата
output_label = ttk.Label(root, text="Результат:")
# Размещаем метку (строка 5, столбец 0)
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Текстовое поле с прокруткой для вывода результата
output_text = scrolledtext.ScrolledText(root, width=100, height=35)
# Размещаем поле вывода (строка 6, столбец 0, растягиваем на 2 столбца)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
# Делаем так, чтобы строка 6 (где поле вывода) растягивалась при изменении размера окна
root.grid_rowconfigure(6, weight=1)
# Делаем так, чтобы столбец 0 (где основные элементы) растягивался
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла обработки событий tkinter
root.mainloop()
