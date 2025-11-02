import tkinter as tk
from tkinter import ttk, scrolledtext
import random

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def create_omophonic_table(original_alphabet, num_homophones_per_letter=2):
    """
    Создает таблицу омофонов, где каждой букве алфавита соответствует список из num_homophones_per_letter шифрозамен.
    """
    homophonic_table = {}
    total_omophones_needed = len(original_alphabet) * num_homophones_per_letter
    all_possible_omophones = list(range(100, 1000))
    random.shuffle(all_possible_omophones)
    selected_omophones = all_possible_omophones[:total_omophones_needed]

    index = 0
    for letter in original_alphabet:
        letter_omophones = []
        for _ in range(num_homophones_per_letter):
            letter_omophones.append(selected_omophones[index])
            index += 1
        homophonic_table[letter] = letter_omophones

    return homophonic_table

def omophonic_cipher(text, homophonic_table, use_random=False):
    """
    Шифрует текст с помощью системы омофонов.
    """
    text_upper = text.upper()
    encrypted_text_parts = []
    cycle_counter = 0

    for char in text_upper:
        if char in homophonic_table:
            available_omophones = homophonic_table[char]
            selected_omoph = None
            if use_random:
                selected_omoph = random.choice(available_omophones)
            else:
                selected_omoph = available_omophones[cycle_counter % len(available_omophones)]
                cycle_counter += 1
            encrypted_text_parts.append(str(selected_omoph))
        # else: # Символ не найден, пропускаем
        #     pass

    encrypted_text = " ".join(encrypted_text_parts)
    return encrypted_text

def omophonic_decipher(encrypted_text, homophonic_table):
    """
    Дешифрует текст, зашифрованный с помощью системы омофонов.
    """
    # Разбиваем строку шифротекста по пробелам
    omophones_list = encrypted_text.split()

    deciphered_text = ""
    # Создаём обратный словарь: омофон -> буква
    # Это ускоряет поиск
    reverse_table = {}
    for letter, omophones in homophonic_table.items():
        for omophone in omophones:
            reverse_table[omophone] = letter

    for omophone_str in omophones_list:
        try:
            # Пытаемся преобразовать строку в число
            omophone_int = int(omophone_str)
        except ValueError:
            raise ValueError(f"Неверный формат омофона: '{omophone_str}'. Ожидаются числа, разделённые пробелами.")

        # Ищем букву, соответствующую омофону
        if omophone_int in reverse_table:
            deciphered_text += reverse_table[omophone_int]
        else:
            raise ValueError(f"Омофон '{omophone_int}' не найден в текущей таблице омофонов.")

    return deciphered_text

# --- Глобальная переменная для хранения текущей таблицы ---
current_homophonic_table = create_omophonic_table(alphabet, 2)

def encrypt_action():
    global current_homophonic_table
    text = surname_entry.get()
    use_random = random_var.get() # Получаем значение из Checkbutton

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return

    try:
        encrypted = omophonic_cipher(text, current_homophonic_table, use_random=use_random)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        output_text.insert(tk.END, f"Используется случайный выбор омофонов: {use_random}\n")
        output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
        output_text.insert(tk.END, "Таблица шифрозамен (омофонов):\n")
        for letter, omophones in current_homophonic_table.items():
            output_text.insert(tk.END, f"  '{letter}': {omophones}\n")
        output_text.insert(tk.END, f"Зашифрованное сообщение (омофоны, разделённые пробелами): {encrypted}\n")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка при шифровании: {e}\n")

def decrypt_action():
    global current_homophonic_table
    encrypted_text = surname_entry.get()

    if not encrypted_text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите омофоны для дешифрования.\n")
        return

    try:
        # Проверим, что строка содержит числа, разделённые пробелами
        # Это делается внутри omophonic_decipher, но можно добавить проверку здесь
        deciphered = omophonic_decipher(encrypted_text, current_homophonic_table)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Зашифрованное сообщение (омофоны): {encrypted_text}\n")
        output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
        output_text.insert(tk.END, "Таблица шифрозамен (омофонов):\n")
        for letter, omophones in current_homophonic_table.items():
            output_text.insert(tk.END, f"  '{letter}': {omophones}\n")
        output_text.insert(tk.END, f"Дешифрованное сообщение: {deciphered}\n")
    except ValueError as ve:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка при дешифровании: {ve}\n")
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Неизвестная ошибка при дешифровании: {e}\n")

def generate_new_table():
    global current_homophonic_table
    current_homophonic_table = create_omophonic_table(alphabet, 2)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Сгенерирована новая таблица омофонов:\n")
    for letter, omophones in current_homophonic_table.items():
        output_text.insert(tk.END, f"  '{letter}': {omophones}\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Система Омофонов (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("900x700")

# --- Виджеты ---

# Ввод фамилии (для шифрования) или омофонов (для дешифрования)
surname_label = ttk.Label(root, text="Введите фамилию для шифрования или омофоны для дешифрования (разделённые пробелом):")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=80)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Флажок для случайного выбора омофонов
random_var = tk.BooleanVar()
random_check = ttk.Checkbutton(root, text="Использовать случайный выбор омофонов (при шифровании)", variable=random_var)
random_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

generate_button = ttk.Button(root, text="Сгенерировать новую таблицу", command=generate_new_table)
generate_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

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
