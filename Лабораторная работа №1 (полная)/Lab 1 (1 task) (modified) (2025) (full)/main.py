import tkinter as tk
from tkinter import ttk, scrolledtext

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def caesar_cipher(text, shift_value, alphabet):
    """
    Шифрует текст с помощью шифра Цезаря.
    """
    text_upper = text.upper()
    encrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in alphabet:
            old_index = alphabet.index(char)
            new_index = (old_index + shift_value) % len(alphabet)
            new_char_upper = alphabet[new_index]

            original_char = text[i]
            if original_char.islower():
                encrypted_text += new_char_upper.lower()
            else:
                encrypted_text += new_char_upper
        else:
            encrypted_text += char

    return encrypted_text

def caesar_decipher(text, shift_value, alphabet):
    """
    Дешифрует текст, зашифрованный с помощью шифра Цезаря.
    """
    text_upper = text.upper()
    decrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in alphabet:
            old_index = alphabet.index(char)
            # Сдвигаем влево: вычитаем сдвиг
            # Используем % len(alphabet) для цикличности.
            # Python корректно обрабатывает отрицательные результаты %,
            # но для ясности можно использовать (old_index - shift_value % len(alphabet) + len(alphabet)) % len(alphabet)
            # Однако (old_index - shift_value) % len(alphabet) даст тот же результат в Python.
            new_index = (old_index - shift_value) % len(alphabet)
            new_char_upper = alphabet[new_index]

            original_char = text[i]
            if original_char.islower():
                decrypted_text += new_char_upper.lower()
            else:
                decrypted_text += new_char_upper
        else:
            decrypted_text += char

    return decrypted_text

def encrypt_action():
    """Обработчик кнопки 'Зашифровать'."""
    text = surname_entry.get()
    try:
        shift = int(shift_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Ключ должен быть целым числом.\n")
        return

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return

    encrypted = caesar_cipher(text, shift, alphabet)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (величина сдвига): {shift}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    """Обработчик кнопки 'Дешифровать'."""
    text = surname_entry.get()
    try:
        shift = int(shift_entry.get())
    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Ключ должен быть целым числом.\n")
        return

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для дешифрования.\n")
        return

    decrypted = caesar_decipher(text, shift, alphabet)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (величина сдвига): {shift}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted}\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифр Цезаря (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("650x450")

# --- Виджеты ---

# Ввод фамилии
surname_label = ttk.Label(root, text="Введите фамилию:")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=50)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод ключа (сдвига)
shift_label = ttk.Label(root, text="Введите величину сдвига (ключ):")
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

output_text = scrolledtext.ScrolledText(root, width=75, height=20)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
