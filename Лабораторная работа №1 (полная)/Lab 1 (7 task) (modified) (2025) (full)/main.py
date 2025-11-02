import tkinter as tk
from tkinter import ttk, scrolledtext

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
# Мощность алфавита N
N = len(alphabet)

def vigenere_cipher(text, key, alphabet):
    """
    Шифрует текст с помощью шифра Виженера.
    """
    text_upper = text.upper()
    key_upper = key.upper()
    encrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in alphabet:
            plaintext_char_index = alphabet.index(char)
            key_char_index = alphabet.index(key_upper[i % len(key_upper)])
            # C_i = (P_i + K_i) mod N
            encrypted_char_index = (plaintext_char_index + key_char_index) % N
            encrypted_char_upper = alphabet[encrypted_char_index]

            # Сохраняем регистр
            original_char = text[i]
            if original_char.islower():
                encrypted_text += encrypted_char_upper.lower()
            else:
                encrypted_text += encrypted_char_upper
        else:
            encrypted_text += char

    return encrypted_text

def vigenere_decipher(text, key, alphabet):
    """
    Дешифрует текст, зашифрованный с помощью шифра Виженера.
    """
    text_upper = text.upper()
    key_upper = key.upper()
    decrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in alphabet:
            encrypted_char_index = alphabet.index(char)
            key_char_index = alphabet.index(key_upper[i % len(key_upper)])
            # P_i = (C_i - K_i + N) mod N
            decrypted_char_index = (encrypted_char_index - key_char_index + len(alphabet)) % len(alphabet)
            decrypted_char_upper = alphabet[decrypted_char_index]

            # Сохраняем регистр
            original_char = text[i]
            if original_char.islower():
                decrypted_text += decrypted_char_upper.lower()
            else:
                decrypted_text += decrypted_char_upper
        else:
            decrypted_text += char

    return decrypted_text


def encrypt_action():
    text = surname_entry.get()
    key = key_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return
    if not key:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово.\n")
        return

    # Проверим, все ли символы ключа находятся в алфавите
    for char in key:
        if char.upper() not in alphabet:
             output_text.delete(1.0, tk.END)
             output_text.insert(tk.END, f"Ошибка: Ключ '{key}' содержит символы, отсутствующие в алфавите '{alphabet}'.\n")
             return

    encrypted = vigenere_cipher(text, key, alphabet)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ: {key}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Мощность алфавита (N): {N}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    text = surname_entry.get()
    key = key_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для дешифрования.\n")
        return
    if not key:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово, использованное при шифровании.\n")
        return

    # Проверим, все ли символы ключа находятся в алфавите
    for char in key:
        if char.upper() not in alphabet:
             output_text.delete(1.0, tk.END)
             output_text.insert(tk.END, f"Ошибка: Ключ '{key}' содержит символы, отсутствующие в алфавите '{alphabet}'.\n")
             return

    decrypted = vigenere_decipher(text, key, alphabet)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ: {key}\n")
    output_text.insert(tk.END, f"Алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Мощность алфавита (N): {N}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted}\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Шифр Виженера (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("800x550")

# --- Виджеты ---

# Ввод фамилии
surname_label = ttk.Label(root, text="Введите фамилию:")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=70)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод ключа
key_label = ttk.Label(root, text="Введите ключевое слово:")
key_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

key_entry = ttk.Entry(root, width=30)
key_entry.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Кнопки
encrypt_button = ttk.Button(root, text="Зашифровать", command=encrypt_action)
encrypt_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

decrypt_button = ttk.Button(root, text="Дешифровать", command=decrypt_action)
decrypt_button.grid(row=4, column=1, padx=10, pady=5, sticky="e")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=90, height=25)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
