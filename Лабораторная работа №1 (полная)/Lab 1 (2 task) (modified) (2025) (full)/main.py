import tkinter as tk
from tkinter import ttk, scrolledtext

# Определяем русский алфавит
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def generate_cipher_alphabet(keyword, original_alphabet):
    """
    Создает алфавит замены для лозунгового шифра.
    """
    keyword_upper = keyword.upper()
    unique_keyword_letters = []
    seen_letters = set()

    for char in keyword_upper:
        if char in original_alphabet and char not in seen_letters:
            unique_keyword_letters.append(char)
            seen_letters.add(char)

    cipher_alphabet = "".join(unique_keyword_letters)
    for char in original_alphabet:
        if char not in seen_letters:
            cipher_alphabet += char

    return cipher_alphabet

def slogan_cipher(text, keyword, original_alphabet):
    """
    Шифрует текст с помощью лозунгового шифра.
    """
    cipher_alphabet = generate_cipher_alphabet(keyword, original_alphabet)
    text_upper = text.upper()
    encrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in original_alphabet:
            index_in_original = original_alphabet.index(char)
            encrypted_char_upper = cipher_alphabet[index_in_original]
            original_char = text[i]
            if original_char.islower():
                encrypted_text += encrypted_char_upper.lower()
            else:
                encrypted_text += encrypted_char_upper
        else:
            encrypted_text += text[i] # Оставляем неалфавитные символы как есть

    return encrypted_text

def slogan_decipher(text, keyword, original_alphabet):
    """
    Дешифрует текст, зашифрованный с помощью лозунгового шифра.
    """
    cipher_alphabet = generate_cipher_alphabet(keyword, original_alphabet)
    text_upper = text.upper()
    decrypted_text = ""

    for i, char in enumerate(text_upper):
        if char in original_alphabet: # Проверяем, есть ли символ в ОРИГИНАЛЬНОМ алфавите
            # Находим индекс символа шифротекста в АЛФАВИТЕ ЗАМЕНЫ
            if char in cipher_alphabet: # Убедимся, что символ есть в cipher_alphabet
                 index_in_cipher = cipher_alphabet.index(char)
                 # Находим соответствующий символ в ОРИГИНАЛЬНОМ алфавите
                 decrypted_char_upper = original_alphabet[index_in_cipher]
                 # Сохраняем регистр
                 original_char = text[i]
                 if original_char.islower():
                     decrypted_text += decrypted_char_upper.lower()
                 else:
                     decrypted_text += decrypted_char_upper
            else:
                 # Если символ шифротекста не найден в алфавите замены
                 decrypted_text += text[i] # Оставляем как есть (на всякий случай)
        else:
            decrypted_text += text[i] # Оставляем неалфавитные символы как есть

    return decrypted_text

def encrypt_action():
    text = surname_entry.get()
    keyword = keyword_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово (лозунг).\n")
        return

    cipher_alphabet_used = generate_cipher_alphabet(keyword, alphabet)
    encrypted = slogan_cipher(text, keyword, alphabet)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (лозунг): {keyword}\n")
    output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Алфавит замены (таблица шифрозамен): {cipher_alphabet_used}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted}\n")

def decrypt_action():
    text = surname_entry.get()
    keyword = keyword_entry.get()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для дешифрования.\n")
        return
    if not keyword:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите ключевое слово (лозунг), использованное при шифровании.\n")
        return

    cipher_alphabet_used = generate_cipher_alphabet(keyword, alphabet)
    decrypted = slogan_decipher(text, keyword, alphabet)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Ключ (лозунг): {keyword}\n")
    output_text.insert(tk.END, f"Оригинальный алфавит: {alphabet}\n")
    output_text.insert(tk.END, f"Алфавит замены (таблица шифрозамен): {cipher_alphabet_used}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted}\n")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Лозунговый Шифр (Шифрование и Дешифрование) - Модифицированное задание")
root.geometry("750x550")

# --- Виджеты ---

# Ввод фамилии
surname_label = ttk.Label(root, text="Введите фамилию:")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

surname_entry = ttk.Entry(root, width=60)
surname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

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

output_text = scrolledtext.ScrolledText(root, width=85, height=25)
output_text.grid(row=6, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
