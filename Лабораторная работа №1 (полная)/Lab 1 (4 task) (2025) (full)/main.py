import tkinter as tk
from tkinter import ttk, scrolledtext

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def create_trisemus_table(keyword, original_alphabet, rows=6, cols=6):
    """
    Создает таблицу для шифра Трисемуса.
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

def get_coordinates_trisemus(char, table):
    """
    Находит координаты (строка, столбец) символа в таблице Трисемуса.
    """
    for r in range(len(table)):
        for c in range(len(table[r])):
            if table[r][c] == char:
                return r, c
    return -1, -1

def trisemus_cipher(text, keyword, original_alphabet, table_rows=6, table_cols=6):
    """
    Шифрует текст с помощью шифра Трисемуса.
    """
    text_upper = text.upper()
    trisemus_table = create_trisemus_table(keyword, original_alphabet, table_rows, table_cols)
    encrypted_text = ""

    for i, char in enumerate(text_upper):
        row, col = get_coordinates_trisemus(char, trisemus_table)

        if row != -1 and col != -1:
            # Определяем строку для шифрования текущего символа
            encryption_row_index = i % len(trisemus_table)
            # Берем символ из этой строки по столбцу исходного символа
            encrypted_char_upper = trisemus_table[encryption_row_index][col]

            # Сохраняем регистр
            original_char = text[i]
            if original_char.islower():
                encrypted_text += encrypted_char_upper.lower()
            else:
                encrypted_text += encrypted_char_upper
        else:
            # Символ не найден, пропускаем
            pass

    return encrypted_text

def trisemus_decipher(text, keyword, original_alphabet, table_rows=6, table_cols=6):
    """
    Дешифрует текст, зашифрованный с помощью шифра Трисемуса.
    """
    text_upper = text.upper()
    trisemus_table = create_trisemus_table(keyword, original_alphabet, table_rows, table_cols)
    decrypted_text = ""

    for i, char in enumerate(text_upper):
        # Для дешифрования нужно найти строку шифрования, использованную для текущего символа
        decryption_row_index = i % len(trisemus_table)
        # Теперь ищем координаты текущего символа шифротекста в ЭТОЙ строке
        # Мы ищем char в строке с индексом decryption_row_index
        row_to_search = trisemus_table[decryption_row_index]
        if char in row_to_search:
             col = row_to_search.index(char)
             # Находим символ в ПЕРВОЙ строке таблицы по найденному столбцу
             decrypted_char_upper = trisemus_table[0][col] # Первая строка

             # Сохраняем регистр
             original_char = text[i]
             if original_char.islower():
                 decrypted_text += decrypted_char_upper.lower()
             else:
                 decrypted_text += decrypted_char_upper
        else:
             # Символ шифротекста не найден в строке шифрования - ошибка или символ не из алфавита
             # Для символов, не входящих в таблицу, можно оставить как есть, но в текущей логике шифрования
             # такие символы не должны попасть в шифротекст.
             # Если символ не найден, пропускаем или добавляем как есть (в реальной задаче это ошибка)
             # print(f"Символ '{char}' из шифротекста не найден в строке шифрования {decryption_row_index}.")
             pass # Пропускаем, так как это ошибка в данных или логике

    return decrypted_text


def encrypt_action():
    text = input_text.get()
    keyword = keyword_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите текст для шифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово (лозунг).\n")
        return

    trisemus_table = create_trisemus_table(keyword, alphabet, 6, 6)
    encrypted = trisemus_cipher(text, keyword, alphabet, 6, 6)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (лозунг): {keyword}\n")
    output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
    output_text.insert(tk.END, "Таблица шифрозамен (таблица Трисемуса):\n")
    for row in trisemus_table:
        output_text.insert(tk.END, f"{row}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    text = input_text.get()
    keyword = keyword_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите текст для дешифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово (лозунг), использованное при шифровании.\n")
        return

    trisemus_table = create_trisemus_table(keyword, alphabet, 6, 6)
    decrypted = trisemus_decipher(text, keyword, alphabet, 6, 6)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (лозунг): {keyword}\n")
    output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
    output_text.insert(tk.END, "Таблица шифрозамен (таблица Трисемуса):\n")
    for row in trisemus_table:
        output_text.insert(tk.END, f"{row}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted}\n")

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифр Трисемуса (Шифрование и Дешифрование)")
root.geometry("800x600")

# --- Виджеты ---

# Ввод текста
input_label = ttk.Label(root, text="Введите текст:")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_text = ttk.Entry(root, width=70)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод ключа (лозунга)
keyword_label = ttk.Label(root, text="Введите ключевое слово (лозунг):")
keyword_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

keyword_entry = ttk.Entry(root, width=30)
keyword_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=4, column=1, padx=10, pady=5, sticky="e")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=90, height=30)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
