import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import secrets # Для генерации криптографически стойких случайных чисел

# --- Конфигурация ---
# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
N = len(ALPHABET) # Размер алфавита, используемый как модуль N

# --- Вспомогательные функции ---
def text_to_numbers(text, alphabet):
    """
    Преобразует текст в список чисел, где каждая буква заменяется её индексом в алфавите.
    Используется для подготовки текста к числовому шифрованию.

    :param text: Исходный текст для преобразования (str).
    :param alphabet: Алфавит, используемый для сопоставления букв и чисел (str).
    :return: Список целых чисел, представляющих индексы букв в алфавите (list of int).
             Если символ не найден в алфавите, он пропускается.
    """
    numbers = []
    for char in text.upper():
        if char in alphabet:
            numbers.append(alphabet.index(char))
    return numbers

def numbers_to_text(numbers, alphabet):
    """
    Преобразует список чисел обратно в текст, используя заданный алфавит.
    Используется для восстановления текста из числового шифра.

    :param numbers: Список целых чисел, представляющих индексы букв в алфавите (list of int).
    :param alphabet: Алфавит, используемый для сопоставления чисел и букв (str).
    :return: Восстановленный текст (str).
             Если число выходит за пределы индексов алфавита, символ игнорируется.
    """
    text = ""
    for num in numbers:
        if 0 <= num < len(alphabet):
            text += alphabet[num]
    return text

def text_to_bits(text):
    """
    Преобразует текст в список 8-битных строк, представляющих байты Windows-1251.

    :param text: Исходный текст для преобразования (str).
    :return: Список 8-битных строк (list of str).
    """
    bits_list = []
    for char in text.upper():
        try:
            byte_val = char.encode('cp1251')[0]
            char_bits_str = format(byte_val, '08b')
            bits_list.append(char_bits_str)
        except UnicodeEncodeError:
            # Если символ не входит в cp1251, пропускаем
            continue
    return bits_list

def bits_to_text(bits_list):
    """
    Преобразует список 8-битных строк (Windows-1251) обратно в текст.

    :param bits_list: Список строк, каждая из которых представляет 8 бит (list of str).
    :return: Восстановленный текст (str).
    """
    text = ""
    for bits_str in bits_list:
        if len(bits_str) != 8:
            continue
        byte_val = int(bits_str, 2)
        try:
            char = bytes([byte_val]).decode('cp1251')
            text += char
        except UnicodeDecodeError:
            text += '?'
    return text

def generate_random_gamma_modN(length, alphabet_size):
    """
    Генерирует криптографически стойкую случайную гамму для шифрования по модулю N.
    Использует модуль secrets для обеспечения безопасности.

    :param length: Длина требуемой гаммы (int).
    :param alphabet_size: Размер алфавита (N) для ограничения значений гаммы (int).
    :return: Список случайных целых чисел в диапазоне [0, alphabet_size - 1] (list of int).
    """
    gamma = []
    for _ in range(length):
        # Генерируем криптографически безопасное случайное число
        gamma_val = secrets.randbelow(alphabet_size)
        gamma.append(gamma_val)
    return gamma

def generate_random_gamma_mod2(length):
    """
    Генерирует криптографически стойкую случайную битовую гамму для шифрования по модулю 2.
    Использует модуль secrets для обеспечения безопасности.

    :param length: Длина требуемой гаммы в битах (int).
    :return: Список 8-битных строк случайных битов (list of str).
    """
    gamma_bits = []
    for _ in range(length):
        # Генерируем криптографически безопасное 8-битное случайное число
        random_byte = secrets.randbits(8)
        gamma_bits.append(format(random_byte, '08b'))
    return gamma_bits

# --- Функции шифрования и дешифрования ---
def gamma_cipher_modN(text, gamma, alphabet):
    """
    Шифрует текст с помощью гаммирования по модулю N (длина алфавита).
    Реализует формулу CLi = (PLi + KGi) mod N.

    :param text: Исходный текст для шифрования (str).
    :param gamma: Гамма (ключ) - список чисел, используемых для шифрования (list of int).
    :param alphabet: Алфавит, используемый для шифрования (str).
    :return: Кортеж из зашифрованного текста (str) и списка чисел зашифрованного текста (list of int).
    """
    text_numbers = text_to_numbers(text, alphabet)
    if not text_numbers:
        return "", []

    # Циклически используем гамму
    extended_gamma = []
    for i in range(len(text_numbers)):
        extended_gamma.append(gamma[i % len(gamma)])

    # Выполняем операцию шифрования: (буква_текста + буква_гаммы) mod N
    encrypted_numbers = []
    for i in range(len(text_numbers)):
        encrypted_num = (text_numbers[i] + extended_gamma[i]) % len(alphabet)
        encrypted_numbers.append(encrypted_num)

    encrypted_text = numbers_to_text(encrypted_numbers, alphabet)
    return encrypted_text, encrypted_numbers

def gamma_decipher_modN(encrypted_text, gamma, alphabet):
    """
    Дешифрует текст, зашифрованный с помощью гаммирования по модулю N.
    Реализует формулу PLi = (CLi + N - KGi) mod N.

    :param encrypted_text: Текст для дешифрования (str).
    :param gamma: Гамма (ключ), использованная при шифровании (list of int).
    :param alphabet: Алфавит, использованный при шифровании (str).
    :return: Кортеж из дешифрованного текста (str) и списка чисел дешифрованного текста (list of int).
    """
    encrypted_numbers = text_to_numbers(encrypted_text, alphabet)
    if not encrypted_numbers:
        return "", []

    # Циклически используем гамму
    extended_gamma = []
    for i in range(len(encrypted_numbers)):
        extended_gamma.append(gamma[i % len(gamma)])

    # Выполняем операцию дешифрования: (буква_шифра - буква_гаммы + N) mod N
    decrypted_numbers = []
    for i in range(len(encrypted_numbers)):
        decrypted_num = (encrypted_numbers[i] - extended_gamma[i]) % len(alphabet)
        decrypted_numbers.append(decrypted_num)

    decrypted_text = numbers_to_text(decrypted_numbers, alphabet)
    return decrypted_text, decrypted_numbers

def gamma_cipher_mod2(text, gamma_bits):
    """
    Шифрует текст с помощью гаммирования по модулю 2 (XOR).
    Каждый символ текста преобразуется в 8-битное представление Windows-1251,
    затем побитово XOR'ится с соответствующим 8-битным элементом гаммы.

    :param text: Исходный текст для шифрования (str).
    :param gamma_bits: Гамма в битовом виде - список 8-битных строк (list of str).
    :return: Кортеж из списка битов зашифрованного текста (list of str) и списка битов исходного текста (list of str).
    """
    text_bits = text_to_bits(text)

    if not text_bits:
        return [], []

    # Циклически используем гамму
    extended_gamma_bits = []
    for i in range(len(text_bits)):
        extended_gamma_bits.append(gamma_bits[i % len(gamma_bits)])

    # Выполняем операцию XOR побитно
    encrypted_bits = []
    for i in range(len(text_bits)):
        t_bits = text_bits[i]
        g_bits = extended_gamma_bits[i]

        if len(t_bits) != 8 or len(g_bits) != 8:
             continue

        encrypted_char_bits = ""
        for j in range(8):
            bit_t = int(t_bits[j])
            bit_g = int(g_bits[j])
            encrypted_bit = (bit_t + bit_g) % 2
            encrypted_char_bits += str(encrypted_bit)
        encrypted_bits.append(encrypted_char_bits)

    return encrypted_bits, text_bits

def gamma_decipher_mod2(encrypted_bits, gamma_bits):
    """
    Дешифрует текст, зашифрованный с помощью гаммирования по модулю 2 (XOR).
    Так как XOR обратим сам к себе, процесс идентичен шифрованию.

    :param encrypted_bits: Список 8-битных строк зашифрованного текста (list of str).
    :param gamma_bits: Гамма в битовом виде (список строк), использованная при шифровании (list of str).
    :return: Список битов дешифрованного текста (list of str).
    """
    if not encrypted_bits:
        return []

    # Циклически используем гамму
    extended_gamma_bits = []
    for i in range(len(encrypted_bits)):
        extended_gamma_bits.append(gamma_bits[i % len(gamma_bits)])

    # Выполняем операцию XOR побитно (идентична шифрованию)
    decrypted_bits = []
    for i in range(len(encrypted_bits)):
        e_bits = encrypted_bits[i]
        g_bits = extended_gamma_bits[i]

        if len(e_bits) != 8 or len(g_bits) != 8:
             continue

        decrypted_char_bits = ""
        for j in range(8):
            bit_e = int(e_bits[j])
            bit_g = int(g_bits[j])
            decrypted_bit = (bit_e + bit_g) % 2
            decrypted_char_bits += str(decrypted_bit)
        decrypted_bits.append(decrypted_char_bits)

    return decrypted_bits

# --- Обработчики событий GUI ---
def encrypt_modN_action():
    """
    Обработчик события нажатия кнопки 'Зашифровать (Mod N)'.
    Получает введённые пользователем фамилию и гамму, выполняет шифрование,
    и выводит результаты в текстовое поле.
    """
    text = input_text.get().upper()
    gamma_input = gamma_entry_modN.get().strip()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return

    # Обработка гаммы: ввод пользователя или генерация
    gamma = []
    if gamma_input.lower() == "auto":
        # Генерация случайной гаммы
        gamma = generate_random_gamma_modN(len(text), N)
        gamma_str = str(gamma)
    else:
        try:
            gamma = [int(x.strip()) for x in gamma_input.split(',')]
            if not all(0 <= g < N for g in gamma):
                raise ValueError(f"Значения гаммы должны быть от 0 до {N-1}.")
            gamma_str = str(gamma)
        except ValueError as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
            return

    encrypted_text, encrypted_nums = gamma_cipher_modN(text, gamma, ALPHABET)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Шифрование по модулю N ---\n")
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Алфавит: {ALPHABET}\n")
    output_text.insert(tk.END, f"N (мощность алфавита): {N}\n")
    output_text.insert(tk.END, f"Гамма (использованная): {gamma_str}\n")
    output_text.insert(tk.END, f"Исходное сообщение (числа): {text_to_numbers(text, ALPHABET)}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (числа): {encrypted_nums}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {encrypted_text}\n\n")

def decrypt_modN_action():
    """
    Обработчик события нажатия кнопки 'Дешифровать (Mod N)'.
    Получает введённые пользователем зашифрованный текст и гамму, выполняет дешифрование,
    и выводит результаты в текстовое поле.
    """
    text = input_text.get().upper()
    gamma_input = gamma_entry_modN.get().strip()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение для дешифрования.\n")
        return
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (через запятую) или 'auto' для автогенерации.\n")
        return

    # Обработка гаммы: ввод пользователя или генерация (для тестирования)
    gamma = []
    if gamma_input.lower() == "auto":
        # Для демонстрации, генерируем гамму той же длины, что и текст
        gamma = generate_random_gamma_modN(len(text), N)
        gamma_str = str(gamma) + " (сгенерирована для теста)"
    else:
        try:
            gamma = [int(x.strip()) for x in gamma_input.split(',')]
            if not all(0 <= g < N for g in gamma):
                raise ValueError(f"Значения гаммы должны быть от 0 до {N-1}.")
            gamma_str = str(gamma)
        except ValueError as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
            return

    decrypted_text, decrypted_nums = gamma_decipher_modN(text, gamma, ALPHABET)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Дешифрование по модулю N ---\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение: {text}\n")
    output_text.insert(tk.END, f"Алфавит: {ALPHABET}\n")
    output_text.insert(tk.END, f"N (мощность алфавита): {N}\n")
    output_text.insert(tk.END, f"Гамма (использованная): {gamma_str}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (числа): {text_to_numbers(text, ALPHABET)}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (числа): {decrypted_nums}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted_text}\n\n")

def encrypt_mod2_action():
    """
    Обработчик события нажатия кнопки 'Зашифровать (Mod 2)'.
    Получает введённые пользователем фамилию и битовую гамму, выполняет шифрование,
    и выводит результаты в текстовое поле.
    """
    text = input_text.get().upper()
    gamma_input = gamma_entry_mod2.get().strip()

    if not text:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите фамилию для шифрования.\n")
        return

    # Обработка гаммы: ввод пользователя или генерация
    gamma_bits = []
    if gamma_input.lower() == "auto":
        # Генерация случайной битовой гаммы
        gamma_bits = generate_random_gamma_mod2(len(text))
        gamma_bits_str = str(gamma_bits)
    else:
        try:
            gamma_bits = [x.strip() for x in gamma_input.split(',')]
            if not all(len(g) == 8 and all(c in '01' for c in g) for g in gamma_bits):
                raise ValueError("Каждое значение гаммы должно быть 8-битной строкой (только 0 и 1).")
            gamma_bits_str = str(gamma_bits)
        except ValueError as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Ошибка: Неверный формат гаммы. {e}\n")
            return

    encrypted_bits, original_bits = gamma_cipher_mod2(text, gamma_bits)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Шифрование по модулю 2 ---\n")
    output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
    output_text.insert(tk.END, f"Исходное сообщение (байты Windows-1251, биты): {original_bits}\n")
    output_text.insert(tk.END, f"Гамма (биты, использованная): {gamma_bits_str}\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (байты, биты): {encrypted_bits}\n")
    output_text.insert(tk.END, "\n")

def decrypt_mod2_action():
    """
    Обработчик события нажатия кнопки 'Дешифровать (Mod 2)'.
    Получает введённые пользователем зашифрованные биты и битовую гамму, выполняет дешифрование,
    и выводит результаты в текстовое поле.
    """
    encrypted_input = input_text.get().strip()
    gamma_input = gamma_entry_mod2.get().strip()

    if not encrypted_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите зашифрованное сообщение (биты) для дешифрования.\n")
        return
    if not gamma_input:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Ошибка: Введите гамму (битовые строки через запятую, 8 бит каждая) или 'auto'.\n")
        return

    try:
        encrypted_bits = [x.strip() for x in encrypted_input.split(',')]
        gamma_bits = []
        if gamma_input.lower() == "auto":
            # Для демонстрации, генерируем гамму той же длины, что и зашифрованный текст
            gamma_bits = generate_random_gamma_mod2(len(encrypted_bits))
            gamma_bits_str = str(gamma_bits) + " (сгенерирована для теста)"
        else:
            gamma_bits = [x.strip() for x in gamma_input.split(',')]
            if not all(len(e) == 8 and all(c in '01' for c in e) for e in encrypted_bits):
                raise ValueError("Каждое значение зашифрованного сообщения должно быть 8-битной строкой (только 0 и 1).")
            if not all(len(g) == 8 and all(c in '01' for c in g) for g in gamma_bits):
                raise ValueError("Каждое значение гаммы должно быть 8-битной строкой (только 0 и 1).")
            gamma_bits_str = str(gamma_bits)
    except ValueError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат ввода. {e}\n")
        return

    decrypted_bits = gamma_decipher_mod2(encrypted_bits, gamma_bits)
    decrypted_text = bits_to_text(decrypted_bits)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Дешифрование по модулю 2 ---\n")
    output_text.insert(tk.END, f"Зашифрованное сообщение (байты, биты): {encrypted_bits}\n")
    output_text.insert(tk.END, f"Гамма (биты, использованная): {gamma_bits_str}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (байты, биты): {decrypted_bits}\n")
    output_text.insert(tk.END, f"Дешифрованное сообщение (символы): {decrypted_text}\n\n")

def generate_gamma_modN():
    """
    Обработчик события нажатия кнопки 'Сгенерировать гамму (Mod N)'.
    Генерирует случайную гамму и вставляет её в соответствующее поле ввода.
    """
    text = input_text.get().upper()
    if not text:
        messagebox.showwarning("Предупреждение", "Введите текст, чтобы определить длину гаммы.")
        return
    gamma = generate_random_gamma_modN(len(text), N)
    gamma_entry_modN.delete(0, tk.END)
    gamma_entry_modN.insert(0, ','.join(map(str, gamma)))

def generate_gamma_mod2():
    """
    Обработчик события нажатия кнопки 'Сгенерировать гамму (Mod 2)'.
    Генерирует случайную битовую гамму и вставляет её в соответствующее поле ввода.
    """
    text = input_text.get().upper()
    if not text:
        messagebox.showwarning("Предупреждение", "Введите текст, чтобы определить длину гаммы.")
        return
    gamma_bits = generate_random_gamma_mod2(len(text))
    gamma_entry_mod2.delete(0, tk.END)
    gamma_entry_mod2.insert(0, ','.join(gamma_bits))

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Улучшенные Шифры гаммирования (Лабораторная работа 3, Задание 1)")
root.geometry("900x700")

# --- Виджеты ---

# Ввод текста (фамилии)
input_label = ttk.Label(root, text="Введите фамилию (или биты для Mod2):")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_text = ttk.Entry(root, width=60)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Ввод гаммы для Mod N
gamma_label_modN = ttk.Label(root, text="Введите гамму (Mod N, числа через запятую) или 'auto':")
gamma_label_modN.grid(row=2, column=0, padx=10, pady=5, sticky="w")

gamma_entry_modN = ttk.Entry(root, width=60)
gamma_entry_modN.grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Кнопки генерации и шифрования/дешифрования для Mod N
generate_button_modN = ttk.Button(root, text="Сгенерировать гамму (Mod N)", command=generate_gamma_modN)
generate_button_modN.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

encrypt_button_modN = ttk.Button(root, text="Зашифровать (Mod N)", command=encrypt_modN_action)
encrypt_button_modN.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

decrypt_button_modN = ttk.Button(root, text="Дешифровать (Mod N)", command=decrypt_modN_action)
decrypt_button_modN.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# Ввод гаммы для Mod 2
gamma_label_mod2 = ttk.Label(root, text="Введите гамму (Mod 2, 8-битные строки через запятую) или 'auto':")
gamma_label_mod2.grid(row=6, column=0, padx=10, pady=5, sticky="w")

gamma_entry_mod2 = ttk.Entry(root, width=60)
gamma_entry_mod2.grid(row=7, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Кнопки генерации и шифрования/дешифрования для Mod 2
generate_button_mod2 = ttk.Button(root, text="Сгенерировать гамму (Mod 2)", command=generate_gamma_mod2)
generate_button_mod2.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

encrypt_button_mod2 = ttk.Button(root, text="Зашифровать (Mod 2)", command=encrypt_mod2_action)
encrypt_button_mod2.grid(row=9, column=0, padx=10, pady=5, sticky="ew")

decrypt_button_mod2 = ttk.Button(root, text="Дешифровать (Mod 2)", command=decrypt_mod2_action)
decrypt_button_mod2.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=110, height=25)
output_text.grid(row=11, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(11, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
