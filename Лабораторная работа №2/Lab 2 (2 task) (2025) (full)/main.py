import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def block_permutation_encrypt(text, key):
    """
    Шифрует текст с помощью шифра блочной одинарной перестановки.

    Этот метод шифрования работает следующим образом:
    1.  Исходный текст разбивается на блоки фиксированной длины, равной длине ключа.
    2.  Если длина текста не делится нацело на длину ключа, текст дополняется
        пробелами до ближайшей длины, кратной длине ключа.
    3.  Каждый блок текста рассматривается отдельно.
    4.  Ключ перестановки задает порядок, в котором символы внутри *каждого* блока
        переставляются. Ключ - это последовательность чисел, где каждое число указывает
        на новую позицию символа в пределах этого *одного* блока.
        Например, ключ "2413" означает, что 1-й символ блока станет 2-м,
        2-й символ станет 4-м, 3-й символ станет 1-м, 4-й символ станет 3-м.
    5.  Перестановка применяется к символам *внутри* каждого блока независимо.
    6.  Зашифрованный текст формируется путем объединения всех переставленных блоков
        в исходном порядке.

    :param text: Исходный текст для шифрования (str).
                 Пример: "Колосов".
    :param key: Ключ перестановки (str), например, "2413".
                Длина ключа определяет размер блока.
                Каждая цифра в ключе - это номер позиции (1-индекс), куда перейдет
                символ из исходной позиции в пределах блока.
    :return: tuple:
             - encrypted_text (str): Зашифрованный текст.
             - encrypted_blocks (list of lists): Список блоков (в виде списков),
                                                каждый из которых уже подвергнут
                                                перестановке по ключу.
    """
    # Преобразуем ключ в список индексов (0-based), чтобы использовать для индексации списков.
    # Например, ключ "2413" становится [1, 3, 0, 2] (1-2 -> 0-1, 4-1 -> 3-0 и т.д.)
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

    n = len(key_indices) # n - размер блока, определяется длиной ключа

    # Дополняем текст пробелами до длины, кратной n (размеру блока).
    # Это гарантирует, что текст можно будет разбить на блоки одинаковой длины.
    original_length = len(text)
    padding_needed = (n - (original_length % n)) % n
    padded_text = text + ' ' * padding_needed
    padded_length = len(padded_text)

    # Разбиваем дополненный текст на блоки длины n.
    # Каждый блок будет подвергаться перестановке по ключу.
    blocks = []
    for i in range(0, padded_length, n):
        block = list(padded_text[i:i+n]) # Берем n символов и создаем из них список (блок)
        blocks.append(block)

    # Применяем перестановку к каждому блоку в соответствии с ключом.
    # Новый символ на позиции new_pos берется из старой позиции j.
    encrypted_blocks = []
    for block in blocks:
        # Создаем новый блок той же длины
        encrypted_block = [''] * n
        # Проходим по индексам из ключа (new_pos) и заполняем новый блок
        # символами из старого блока по правилу ключа (j -> new_pos)
        for j, new_pos in enumerate(key_indices):
            # j - старая позиция символа в блоке
            # new_pos - новая позиция символа в блоке после перестановки
            encrypted_block[new_pos] = block[j]
        encrypted_blocks.append(encrypted_block)

    # Формируем зашифрованный текст, объединяя все переставленные блоки.
    encrypted_chars = []
    for block in encrypted_blocks:
        encrypted_chars.extend(block) # Добавляем все символы из переставленного блока

    # Возвращаем зашифрованный текст в виде строки и список переставленных блоков
    return ''.join(encrypted_chars), encrypted_blocks

def block_permutation_decrypt(ciphertext, key):
    """
    Дешифрует текст, зашифрованный шифром блочной одинарной перестановки.

    Процесс дешифрования обратен шифрованию:
    1.  Определяется длина ключа n (размер блока).
    2.  Зашифрованный текст разбивается на блоки длины n.
    3.  Для каждого блока применяется *обратная* перестановка.
        Обратный ключ - это такой ключ, который "отменяет" перестановку.
        Если в прямом ключе символ с позиции j шел на позицию new_pos (j -> new_pos),
        то в обратном ключе символ с позиции new_pos должен вернуться на позицию j (new_pos -> j).
        Иными словами, inverse_key[new_pos] = j.
    4.  После обратной перестановки каждого блока, все блоки объединяются,
        восстанавливая исходный порядок символов.
    5.  Удаляются пробелы, которые были добавлены при шифровании для выравнивания.

    :param ciphertext: Зашифрованный текст (str).
    :param key: Ключ перестановки, использованный при шифровании (str), например, "2413".
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
    # Проверяем, делится ли длина на размер блока
    if ct_len % n != 0:
        # Теоретически, если шифр верен, это условие не должно выполняться.
        # Но добавим проверку на всякий случай.
        raise ValueError("Длина зашифрованного текста не кратна размеру блока.")

    # Разбиваем зашифрованный текст на блоки
    encrypted_blocks = []
    for i in range(0, ct_len, n):
        block = list(ciphertext[i:i+n])
        encrypted_blocks.append(block)

    # Создаем обратный ключ
    # Если key_indices[j] = new_pos, то inverse_key[new_pos] = j
    inverse_key = [0] * n
    for j, new_pos in enumerate(key_indices):
        inverse_key[new_pos] = j

    # Применяем обратную перестановку к каждому блоку
    decrypted_blocks = []
    for encrypted_block in encrypted_blocks:
        # Создаем новый блок для восстановления
        decrypted_block = [''] * n
        # Проходим по индексам из обратного ключа
        for j, original_pos in enumerate(inverse_key):
            # Символ из позиции j в зашифрованном блоке
            # должен вернуться на позицию original_pos в исходном
            decrypted_block[original_pos] = encrypted_block[j]
        decrypted_blocks.append(decrypted_block)

    # Формируем дешифрованный текст, объединяя восстановленные блоки
    decrypted_chars = []
    for block in decrypted_blocks:
        decrypted_chars.extend(block)

    # Восстановленный текст (включая добавленные пробелы)
    decrypted_text_with_padding = ''.join(decrypted_chars)
    # Удаляем пробелы в конце, которые были добавлены при шифровании
    return decrypted_text_with_padding.rstrip(' ')


def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать' для интерфейса tkinter.

    Функция извлекает текст и ключ из полей ввода, вызывает функцию шифрования,
    и выводит результат (исходный текст, ключ, список блоков, зашифрованный текст)
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
        encrypted_text, blocks = block_permutation_encrypt(text, key)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр блочной одинарной перестановки (Шифрование) ---\n")
        # Вставляем исходное сообщение
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        # Вставляем ключ перестановки
        output_text.insert(tk.END, f"Ключ перестановки: {key}\n")
        # Вставляем список блоков после перестановки (для визуализации)
        output_text.insert(tk.END, f"Блоки (после перестановки): {blocks}\n")
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
        decrypted_text = block_permutation_decrypt(ciphertext, key)
        # Очищаем поле вывода
        output_text.delete(1.0, tk.END)
        # Вставляем заголовок
        output_text.insert(tk.END, f"--- Шифр блочной одинарной перестановки (Дешифрование) ---\n")
        # Вставляем зашифрованное сообщение
        output_text.insert(tk.END, f"Зашифрованное сообщение: {ciphertext}\n")
        # Вставляем ключ перестановки
        output_text.insert(tk.END, f"Ключ перестановки: {key}\n")
        # Вставляем восстановленное сообщение
        output_text.insert(tk.END, f"Восстановленное сообщение: {decrypted_text}\n\n")
    except ValueError as e: # Ловим ошибки, связанные с неправильным ключом
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: {e}\n")


# --- Создание графического интерфейса ---
# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Шифр блочной одинарной перестановки")
# Устанавливаем начальный размер окна
root.geometry("800x600")

# --- Виджеты ---

# Метка для поля ввода фамилии
input_label = ttk.Label(root, text="Введите текст (фамилию для первых двух шифров):")
# Размещаем метку в сетке окна (строка 0, столбец 0)
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w") # padx/pady - отступы, sticky - прижим к западу

# Поле ввода для фамилии
input_text = ttk.Entry(root, width=50)
# Размещаем поле ввода (строка 1, столбец 0, растягиваем на 2 столбца)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
# Вставляем значение по умолчанию в поле ввода
input_text.insert(0, "Колосов")

# Метка для поля ввода ключа
key_label = ttk.Label(root, text="Введите ключ перестановки (например, 2413):")
# Размещаем метку (строка 2, столбец 0)
key_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Поле ввода для ключа
key_entry = ttk.Entry(root, width=20)
# Размещаем поле ввода (строка 3, столбец 0)
key_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")
# Вставляем значение по умолчанию в поле ввода ключа
key_entry.insert(0, "2413")

# Кнопки для шифрования и дешифрования
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
# Размещаем кнопку (строка 3, столбец 1), прижимаем к востоку
encrypt_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
# Размещаем кнопку (строка 4, столбец 1), прижимаем к востоку
decrypt_button.grid(row=4, column=1, padx=5, pady=5, sticky="e")

# Метка для поля вывода результата
output_label = ttk.Label(root, text="Результат:")
# Размещаем метку (строка 5, столбец 0)
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Текстовое поле с прокруткой для вывода результата
output_text = scrolledtext.ScrolledText(root, width=90, height=30)
# Размещаем поле вывода (строка 6, столбец 0, растягиваем на 2 столбца)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
# Делаем так, чтобы строка 6 (где поле вывода) растягивалась при изменении размера окна
root.grid_rowconfigure(6, weight=1)
# Делаем так, чтобы столбец 0 (где основные элементы) растягивался
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла обработки событий tkinter
root.mainloop()
