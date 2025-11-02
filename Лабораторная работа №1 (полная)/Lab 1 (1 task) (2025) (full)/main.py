import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Функция для шифрования строки с помощью шифра Цезаря
def caesar_cipher(text, shift_value, alphabet):
    """
    Шифрует текст с помощью шифра Цезаря.

    :param text: Исходный текст для шифрования (строка).
    :param shift_value: Величина сдвига (целое число).
    :param alphabet: Алфавит, используемый для шифрования (строка).
    :return: Зашифрованный текст (строка).
    """
    # Преобразуем входной текст в верхний регистр для поиска в алфавите
    text_upper = text.upper()

    # Инициализируем строку для хранения результата
    result_text = ""

    # Проходим по каждой букве в верхнем регистре текста
    for i, char in enumerate(text_upper):
        # Проверяем, находится ли символ в алфавите
        if char in alphabet:
            # Находим индекс символа в алфавите
            old_index = alphabet.index(char)

            # Вычисляем новый индекс с учетом сдвига
            # Используем операцию % (остаток от деления), чтобы обеспечить цикличность
            new_index = (old_index + shift_value) % len(alphabet)

            # Находим букву в алфавите по новому индексу
            new_char_upper = alphabet[new_index]

            # Сохраняем исходный регистр символа из оригинального текста
            original_char = text[i]  # Берем символ из оригинального текста
            if original_char.islower():
                result_text += new_char_upper.lower()  # Если был нижний, добавляем нижний
            else:
                result_text += new_char_upper  # Если был верхний, добавляем верхний
        else:
            # Если символ не является буквой алфавита, оставляем его без изменений, включая регистр
            result_text += text[i]

    # Возвращаем зашифрованный текст
    return result_text

# Функция для дешифрования строки, зашифрованной шифром Цезаря
def caesar_decipher(text, shift_value, alphabet):
    """
    Дешифрует текст, зашифрованный с помощью шифра Цезаря.

    :param text: Текст для дешифрования (строка).
    :param shift_value: Величина сдвига, использованная при шифровании (целое число).
    :param alphabet: Алфавит, использованный при шифровании (строка).
    :return: Дешифрованный текст (строка).
    """
    # Преобразуем входной текст в верхний регистр для поиска в алфавите
    text_upper = text.upper()

    # Инициализируем строку для хранения результата
    result_text = ""

    # Проходим по каждой букве в зашифрованном тексте в верхнем регистре
    for i, char in enumerate(text_upper):
        # Проверяем, находится ли символ в алфавите
        if char in alphabet:
            # Находим индекс символа в алфавите
            old_index = alphabet.index(char)

            # Вычисляем индекс в исходном алфавите (сдвигаем влево)
            # Используем % len(alphabet), чтобы обеспечить цикличность
            new_index = (old_index - shift_value) % len(alphabet)

            # Находим букву в алфавите по вычисленному индексу
            new_char_upper = alphabet[new_index]

            # Сохраняем исходный регистр символа из зашифрованного текста
            original_char = text[i]  # Берем символ из оригинального зашифрованного текста
            if original_char.islower():
                result_text += new_char_upper.lower()  # Если был нижний, добавляем нижний
            else:
                result_text += new_char_upper  # Если был верхний, добавляем верхний
        else:
            # Если символ не является буквой алфавита, оставляем его без изменений, включая регистр
            result_text += text[i]

    # Возвращаем дешифрованный текст
    return result_text

def encrypt_action():
    """Обработчик кнопки 'Зашифровать'."""
    text = input_text.get()
    try:
        shift = int(shift_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END) # Очищаем окно вывода
        output_text.insert(tk.END, "Ошибка: Ключ должен быть целым числом.")
        return

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите текст для шифрования.")
        return

    encrypted = caesar_cipher(text, shift, alphabet)
    output_text.delete(1.0, tk.END) # Очищаем окно вывода
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (величина сдвига): {shift}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    """Обработчик кнопки 'Дешифровать'."""
    text = input_text.get()
    try:
        shift = int(shift_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Ключ должен быть целым числом.")
        return

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите текст для дешифрования.")
        return

    # Для дешифрования используем отрицательный сдвиг
    decrypted = caesar_decipher(text, shift, alphabet)
    output_text.delete(1.0, tk.END) # Очищаем окно вывода
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (величина сдвига): {shift}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted}\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифр Цезаря (Шифрование и Дешифрование)")
root.geometry("600x400") # Устанавливаем начальный размер окна

# --- Виджеты ---

# Ввод текста
input_label = ttk.Label(root, text="Введите текст:")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_text = ttk.Entry(root, width=50)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод ключа
shift_label = ttk.Label(root, text="Введите ключ (целое число):")
shift_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

shift_entry = ttk.Entry(root, width=20)
shift_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=4, column=1, padx=10, pady=5, sticky="e")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=70, height=15)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1) # Ряд с выводом растягивается
root.grid_columnconfigure(0, weight=1) # Колонка с вводом растягивается

# Запуск главного цикла
root.mainloop()
