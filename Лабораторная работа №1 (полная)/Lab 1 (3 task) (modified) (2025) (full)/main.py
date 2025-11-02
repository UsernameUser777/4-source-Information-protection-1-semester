import tkinter as tk
from tkinter import ttk, scrolledtext

# --- Параметры полибианского квадрата ---
square_size = 6 # 6x6 квадрат

# Алфавит для квадрата 6x6 (36 символов), объединяя 'Ё' с 'Е' и 'Й' с 'И'
alphabet_for_square_6x6 = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ01234" # 31 + 5 = 36 символов

# Создаем квадрат (список списков) размером square_size x square_size
polybius_square = []
for i in range(square_size):
    row = []
    for j in range(square_size):
        index = i * square_size + j
        if index < len(alphabet_for_square_6x6):
            row.append(alphabet_for_square_6x6[index])
        else:
            row.append('') # Заглушка, не должна использоваться при длине 36
    polybius_square.append(row)

def get_coordinates(char, square, alphabet):
    """
    Находит координаты (строка, столбец) символа в полибианском квадрате.
    Обрабатывает объединение 'Ё' с 'Е' и 'Й' с 'И'.
    """
    processed_char = char.upper() # Приводим к верхнему регистру для поиска
    if processed_char == 'Ё':
        processed_char = 'Е'
    elif processed_char == 'Й':
        processed_char = 'И'

    for r in range(len(square)):
        for c in range(len(square[r])):
            if square[r][c] == processed_char:
                return r, c
    return -1, -1

def polybius_cipher(text, square):
    """
    Шифрует текст с помощью полибианского квадрата.
    Возвращает строку координат.
    """
    encrypted_coords = ""
    for char in text:
        row, col = get_coordinates(char, square, alphabet_for_square_6x6)
        if row != -1 and col != -1:
            # Преобразуем индексы (0-based) в номера (1-based) и добавляем к результату
            coord_str = str(row + 1) + str(col + 1)
            encrypted_coords += coord_str
        # else: # Символ не найден, пропускаем
        #     pass # Пропускаем символ, не добавляя ничего к результату
    return encrypted_coords

def polybius_decipher(coords, square):
    """
    Дешифрует строку координат с помощью полибианского квадрата.
    Возвращает исходный текст.
    """
    if len(coords) % 2 != 0:
        raise ValueError("Длина строки координат должна быть чётной.")

    deciphered_text = ""
    # Разбиваем строку координат на пары
    for i in range(0, len(coords), 2):
        coord_pair = coords[i:i+2]
        try:
            row_num = int(coord_pair[0])
            col_num = int(coord_pair[1])
        except ValueError:
            raise ValueError(f"Неверный формат координаты: '{coord_pair}'. Ожидаются цифры.")

        # Проверяем диапазон (1-based)
        if not (1 <= row_num <= square_size) or not (1 <= col_num <= square_size):
            raise ValueError(f"Координата ({row_num}, {col_num}) выходит за пределы квадрата {square_size}x{square_size}.")

        # Получаем символ по индексам (0-based)
        char = square[row_num - 1][col_num - 1]
        deciphered_text += char

    return deciphered_text

def encrypt_action():
    text = surname_entry.get()
    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return

    try:
        encrypted_coords = polybius_cipher(text, polybius_square)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        output_text.insert(tk.END, f"Размер квадрата: {square_size}x{square_size}\n")
        output_text.insert(tk.END, f"Алфавит (и символы) для заполнения квадрата: {alphabet_for_square_6x6}\n")
        output_text.insert(tk.END, "Полибианский квадрат:\n")
        for row in polybius_square:
            output_text.insert(tk.END, f"{row}\n")
        output_text.insert(tk.END, f"Зашифрованное сообщение (координаты): {encrypted_coords}\n")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка при шифровании: {e}\n")

def decrypt_action():
    coords = surname_entry.get()
    if not coords:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите координаты для дешифрования.\n")
        return

    try:
        # Проверяем, содержит ли строка только цифры
        if not coords.isdigit():
             raise ValueError("Строка координат должна содержать только цифры.")

        deciphered_text = polybius_decipher(coords, polybius_square)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Зашифрованное сообщение (координаты): {coords}\n")
        output_text.insert(tk.END, f"Размер квадрата: {square_size}x{square_size}\n")
        output_text.insert(tk.END, f"Алфавит (и символы) для заполнения квадрата: {alphabet_for_square_6x6}\n")
        output_text.insert(tk.END, "Полибианский квадрат:\n")
        for row in polybius_square:
            output_text.insert(tk.END, f"{row}\n")
        output_text.insert(tk.END, f"Дешифрованное сообщение: {deciphered_text}\n")
    except ValueError as ve:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка при дешифровании: {ve}\n")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Неизвестная ошибка при дешифровании: {e}\n")

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Полибианский Квадрат (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("800x600")

# --- Виджеты ---

# Ввод фамилии (для шифрования) или координат (для дешифрования)
surname_label = ttk.Label(root, text="Введите фамилию для шифрования или координаты для дешифрования (чётное количество цифр):")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=70)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=2, column=1, padx=10, pady=5, sticky="e")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=90, height=30)
output_text.grid(row=4, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
