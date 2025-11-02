import tkinter as tk
from tkinter import ttk, scrolledtext

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def create_playfair_table(keyword, original_alphabet, rows=6, cols=6):
    """
    Создает таблицу 6x6 для шифра Playfair на основе ключевого слова.
    """
    keyword_upper = keyword.upper()
    unique_keyword_letters = []
    seen_letters = set()

    for char in keyword_upper:
        if char in original_alphabet and char not in seen_letters:
            unique_keyword_letters.append(char)
            seen_letters.add(char)

    table_alphabet = "".join(unique_keyword_letters)
    for char in original_alphabet:
        if char not in seen_letters:
            table_alphabet += char

    table = []
    for i in range(rows):
        row = []
        for j in range(cols):
            index = i * cols + j
            if index < len(table_alphabet):
                row.append(table_alphabet[index])
            else:
                row.append('-')
        table.append(row)

    return table

def get_coordinates_playfair(char, table):
    """
    Находит координаты (строка, столбец) символа в таблице Playfair.
    """
    for r in range(len(table)):
        for c in range(len(table[r])):
            if table[r][c] == char:
                return r, c
    return -1, -1

def process_bigram(bigram, table, mode='encrypt'):
    """
    Шифрует или дешифрует биграмму по правилам шифра Playfair.
    """
    if len(bigram) != 2:
        return bigram # Не обрабатываем неполную биграмму

    char1, char2 = bigram[0], bigram[1]
    row1, col1 = get_coordinates_playfair(char1, table)
    row2, col2 = get_coordinates_playfair(char2, table)

    if row1 == -1 or col1 == -1 or row2 == -1 or col2 == -1:
        # Символ не найден в таблице
        return bigram

    shift = 1 if mode == 'encrypt' else -1

    if row1 == row2:
        new_col1 = (col1 + shift) % len(table[0])
        new_col2 = (col2 + shift) % len(table[0])
        processed_char1 = table[row1][new_col1]
        processed_char2 = table[row2][new_col2]
    elif col1 == col2:
        new_row1 = (row1 + shift) % len(table)
        new_row2 = (row2 + shift) % len(table)
        processed_char1 = table[new_row1][col1]
        processed_char2 = table[new_row2][col2]
    else: # Разные строки и столбцы
        processed_char1 = table[row1][col2]
        processed_char2 = table[row2][col1]

    return processed_char1 + processed_char2

def prepare_text_for_playfair(text, filler_char='Я'):
    """
    Подготавливает текст для шифрования/дешифрования Playfair.
    """
    text_upper = text.upper()
    prepared_chars = []
    i = 0
    while i < len(text_upper):
        current_char = text_upper[i]
        prepared_chars.append(current_char)

        if i + 1 < len(text_upper):
            next_char = text_upper[i + 1]
            if current_char == next_char:
                prepared_chars.append(filler_char)
            i += 1
        else:
            i += 1

    prepared_string = "".join(prepared_chars)
    if len(prepared_string) % 2 != 0:
        prepared_string += filler_char

    bigrams = []
    for j in range(0, len(prepared_string), 2):
        bigram = prepared_string[j:j+2]
        bigrams.append(bigram)

    return bigrams

def playfair_cipher(text, keyword, original_alphabet, filler_char='Я'):
    """
    Шифрует текст с помощью шифра Playfair.
    """
    playfair_table = create_playfair_table(keyword, original_alphabet, 6, 6)
    bigrams = prepare_text_for_playfair(text, filler_char)
    encrypted_text = ""
    for bigram in bigrams:
        encrypted_bigram = process_bigram(bigram, playfair_table, mode='encrypt')
        encrypted_text += encrypted_bigram
    return encrypted_text, bigrams # Возвращаем также подготовленные биграммы для отладки

def playfair_decipher(text, keyword, original_alphabet, filler_char='Я'):
    """
    Дешифрует текст, зашифрованный с помощью шифра Playfair.
    Возвращаемый текст будет включать вставленные filler_char.
    """
    playfair_table = create_playfair_table(keyword, original_alphabet, 6, 6)
    # Для дешифрования текст должен быть разбит на биграммы так же, как и при шифровании
    # Т.е. он должен быть длиной, кратной 2, и не содержать пар одинаковых символов (до шифрования)
    # Предполагаем, что входной 'text' - это корректный шифротекст (чётная длина, только символы из таблицы)
    # Разобьём его на биграммы
    cipher_bigrams = []
    for j in range(0, len(text), 2):
        bigram = text[j:j+2]
        if len(bigram) == 2: # Убедимся, что биграмма полная
             cipher_bigrams.append(bigram)

    deciphered_text = ""
    for bigram in cipher_bigrams:
        deciphered_bigram = process_bigram(bigram, playfair_table, mode='decrypt')
        deciphered_text += deciphered_bigram

    # Возвращаем дешифрованный текст (включая вставленные filler_char)
    # Пользователь должен вручную удалить лишние filler_char ('Я'), если они были вставлены.
    return deciphered_text


def encrypt_action():
    text = surname_entry.get()
    keyword = keyword_entry.get()
    filler = filler_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово.\n")
        return
    if len(filler) != 1 or filler not in alphabet:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Заполнитель должен быть одной буквой из алфавита.\n")
        return

    playfair_table = create_playfair_table(keyword, alphabet, 6, 6)
    encrypted, prep_bigrams = playfair_cipher(text, keyword, alphabet, filler)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ: {keyword}\n")
    output_text.insert(tk.END, f"Заполнитель: {filler}\n")
    output_text.insert(tk.END, "Таблица шифрозамен (таблица Playfair):\n")
    for row in playfair_table:
        output_text.insert(tk.END, f"{row}\n")
    output_text.insert(tk.END, f"Подготовленные биграммы (для шифрования): {prep_bigrams}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    text = surname_entry.get()
    keyword = keyword_entry.get()
    filler = filler_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для дешифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово, использованное при шифровании.\n")
        return
    if len(filler) != 1 or filler not in alphabet:
         output_text.delete(1.0, tk.END)
         output_text.insert(tk.END, "Ошибка: Заполнитель должен быть одной буквой из алфавита.\n")
         return
    # Проверим, что длина шифротекста чётная
    if len(text) % 2 != 0:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Длина шифротекста должна быть чётной. Текущая длина: {len(text)}.\n")
        return

    playfair_table = create_playfair_table(keyword, alphabet, 6, 6)
    # Проверим, все ли символы шифротекста находятся в таблице
    all_chars_in_table = True
    flat_table = [char for row in playfair_table for char in row]
    for char in text:
        if char not in flat_table:
            all_chars_in_table = False
            break
    if not all_chars_in_table:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Шифротекст содержит символы, отсутствующие в таблице Playfair.\n")
        return

    deciphered = playfair_decipher(text, keyword, alphabet, filler)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ: {keyword}\n")
    output_text.insert(tk.END, f"Заполнитель (использованный при шифровании): {filler}\n")
    output_text.insert(tk.END, "Таблица шифрозамен (таблица Playfair):\n")
    for row in playfair_table:
        output_text.insert(tk.END, f"{row}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (включая заполнители): {deciphered}\n")
    output_text.insert(tk.END, f"Примечание: Результат может содержать вставленные заполнители ('{filler}').\n")
    output_text.insert(tk.END, f"Их нужно вручную удалить для получения осмысленного текста.\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифр Playfair (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("850x650")

# --- Виджеты ---

# Ввод фамилии
surname_label = ttk.Label(root, text="Введите фамилию:")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=70)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод ключа
keyword_label = ttk.Label(root, text="Введите ключевое слово:")
keyword_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

keyword_entry = ttk.Entry(root, width=30)
keyword_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Ввод заполнителя
filler_label = ttk.Label(root, text="Введите символ-заполнитель (по умолчанию 'Я'):")
filler_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

filler_entry = ttk.Entry(root, width=5)
filler_entry.insert(0, "Я") # Значение по умолчанию
filler_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=100, height=35)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
