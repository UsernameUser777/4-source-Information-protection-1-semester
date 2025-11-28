# Импортируем необходимые библиотеки для создания графического интерфейса
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu, StringVar
# Импортируем библиотеки для работы с числами и генерации случайных значений
import random
import math

# --- Вспомогательные математические функции для Knapsack ---

def gcd_extended(a, b):
    """
    Расширенный алгоритм Евклида.
    Находит наибольший общий делитель (gcd) чисел a и b,
    а также коэффициенты x и y такие, что a*x + b*y = gcd(a, b).
    Эта функция критически важна для вычисления мультипликативного обратного числа (w_inv),
    которое используется в процессе дешифрования.

    :param a: Целое число.
    :param b: Целое число.
    :return: Кортеж (gcd, x, y), где gcd - наибольший общий делитель,
             а x, y - коэффициенты, удовлетворяющие уравнению a*x + b*y = gcd.
    """
    # Базовый случай рекурсии: если a равно 0, то gcd(a, b) = b, x = 0, y = 1
    if a == 0:
        return b, 0, 1
    # Рекурсивно вызываем функцию для (b % a, a)
    # gcd, x1, y1 - результаты рекурсивного вызова
    gcd, x1, y1 = gcd_extended(b % a, a)
    # Обновляем значения x и y на основе полученных x1, y1
    # x = y1 - (b // a) * x1
    # y = x1
    x = y1 - (b // a) * x1
    y = x1
    # Возвращаем найденные значения gcd, x, y
    return gcd, x, y

def mod_inverse(e, m):
    """
    Вычисляет мультипликативное обратное e по модулю m.
    Использует расширенный алгоритм Евклида.
    w_inv - это такое число, что (w * w_inv) % m = 1.
    Это необходимо для вычисления w_inv в процессе дешифрования.

    :param e: Число, для которого ищется обратное (например, w).
    :param m: Модуль (например, m).
    :return: w_inv - обратное число (целое число) или None, если обратное не существует
             (например, если e и m не взаимно просты).
    """
    # Вызываем расширенный алгоритм Евклида для e и m
    gcd, x, y = gcd_extended(e, m)
    # Проверяем, являются ли e и m взаимно простыми (gcd должен быть 1)
    if gcd != 1:
        # Если gcd != 1, обратное число не существует
        return None
    # x может быть отрицательным, приведем к положительному по модулю m
    # Это делается с помощью операции % m
    w_inv = x % m
    # Возвращаем вычисленное значение w_inv
    return w_inv

def generate_superincreasing_knapsack(size, max_element_base=200):
    """
    Генерирует супервозрастающий вектор (секретный ключ).
    Каждый элемент вектора больше суммы всех предыдущих.
    Это основа для создания закрытого ключа в криптосистеме рюкзака.

    :param size: Размер вектора (например, 8 для 8-битного блока).
    :param max_element_base: Базовое значение для увеличения диапазона генерации.
    :return: Список целых чисел - супервозрастающий вектор.
    """
    # Инициализируем пустой список для вектора и переменную для суммы
    knapsack = []
    total = 0
    # Генерируем 'size' элементов
    for _ in range(size):
        # Следующий элемент должен быть строго больше суммы всех предыдущих
        # Выбираем случайное значение в расширенном диапазоне для большей стойкости
        next_element = random.randint(total + 1, total + max_element_base)
        # Добавляем элемент в вектор
        knapsack.append(next_element)
        # Обновляем общую сумму
        total += next_element
    # Возвращаем сгенерированный супервозрастающий вектор
    return knapsack

# --- Основные функции для шифрования/дешифрования Knapsack ---

def generate_knapsack_keys():
    """
    Генерирует пару открытого и закрытого ключей для криптосистемы на основе задачи о рюкзаке.
    Генерирует супервозрастающий вектор w_secret (закрытый ключ),
    затем модуль m (больше суммы w_secret), и множитель w (взаимно простой с m).
    Открытый ключ - это 'обычный' вектор, вычисленный как (w_secret_i * w) mod m.

    :return: Кортеж (закрытый_ключ (супервозрастающий), открытый_ключ (обычный), m, w, w_inv)
             или (None, None, None, None, None) при ошибке.
    """
    # Определим размерность. Пусть будет 8, чтобы хватило на 8-битный блок.
    # Это позволяет кодировать один байт (8 бит) в одно число-сумму.
    size = 8
    # Генерируем супервозрастающий вектор с увеличенным диапазоном
    w_secret = generate_superincreasing_knapsack(size, max_element_base=200)
    # Вычисляем сумму элементов супервозрастающего вектора
    total_sum = sum(w_secret)

    # Выбираем m так, чтобы m > сумма, но с бóльшим запасом
    m = total_sum + random.randint(100, 500)

    # Выбираем w так, чтобы 1 < w < m и gcd(w, m) = 1 (w и m взаимно просты)
    w = random.randint(2, m - 2)
    # Цикл для поиска подходящего w
    while math.gcd(w, m) != 1: # Проверяем, что w и m взаимно просты
        w = random.randint(2, m - 2) # Пробуем другое w

    # Вычисляем w_inv - мультипликативное обратное к w по модулю m
    w_inv = mod_inverse(w, m)
    if w_inv is None:
        # print("Ошибка: Не удалось вычислить w_inv.")
        return None, None, None, None, None

    # Открытый ключ: w_i_public = (w_secret_i * w) mod m
    w_public = [(wi * w) % m for wi in w_secret]

    # Возвращаем закрытый ключ, открытый ключ и параметры
    return w_secret, w_public, m, w, w_inv

def encrypt_knapsack(message_bytes, public_key, m):
    """
    Шифрует список байтов (чисел 0-255), с помощью открытого ключа криптосистемы рюкзака.
    Каждый байт преобразуется в 8-битное двоичное представление,
    и шифруется как сумма (b0*w_public[0] + b1*w_public[1] + ... + b7*w_public[7]) mod m.

    :param message_bytes: Список целых чисел (0-255), представляющих байты сообщения.
    :param public_key: Открытый вектор (обычный) - список целых чисел.
    :param m: Модуль, используемый при генерации ключей.
    :return: Список зашифрованных чисел (шифротекст).
    """
    # Инициализируем список для хранения зашифрованных чисел
    encrypted_msg = []
    # Размер блока (длина ключа) должен быть 8 для 8-битных байтов
    block_size = len(public_key)

    # Проходим по каждому байту в сообщении
    for byte_val in message_bytes:
        # Преобразуем байт в список 8 битов (от младшего к старшему).
        # Например, байт 65 (01000001 в двоичном) -> [1, 0, 0, 0, 0, 0, 1, 0]
        # где b0 (бит 0) соответствует public_key[0], b1 (бит 1) - public_key[1], и т.д.
        # Это делается с помощью побитовых операций.
        bits = [(byte_val >> i) & 1 for i in range(8)] # b0, b1, ..., b7

        # Вычисляем сумму для этого байта: sum(b_i * w_public_i)
        encrypted_sum = 0
        for i in range(block_size):
            encrypted_sum += bits[i] * public_key[i]
        # Применяем модуль m к полученной сумме
        encrypted_sum_mod = encrypted_sum % m
        # Добавляем зашифрованное число в результат
        encrypted_msg.append(encrypted_sum_mod)

    # Возвращаем список зашифрованных чисел
    return encrypted_msg

def decrypt_knapsack(encrypted_message, secret_key, m, w_inv):
    """
    Дешифрует список чисел, с помощью закрытого ключа криптосистемы рюкзака.
    Для каждого зашифрованного числа:
    1. Вычисляет c' = (c * w_inv) mod m
    2. Решает задачу о рюкзаке для c' с супервозрастающим вектором secret_key
    3. Преобразует полученные 8 битов обратно в байт.

    :param encrypted_message: Список зашифрованных целых чисел.
    :param secret_key: Секретный супервозрастающий вектор.
    :param m: Модуль.
    :param w_inv: Мультипликативное обратное к w по модулю m.
    :return: Список дешифрованных целых чисел (байтов) или None при ошибке.
    """
    # Инициализируем список для хранения дешифрованных байтов
    decrypted_bytes = []
    # Проходим по каждому зашифрованному числу
    for c in encrypted_message:
        # Шаг 1: Вычисляем c' = (c * w_inv) mod m
        # Это "возвращает" число к виду, пригодному для решения задачи о рюкзаке
        # с супервозрастающим вектором.
        c_prime = (c * w_inv) % m

        # Шаг 2: Решить задачу о рюкзаке для c_prime с супервозрастающим вектором secret_key
        # Используем жадный алгоритм: начиная с наибольшего элемента, вычитаем его из c_prime,
        # если он помещается, и отмечаем соответствующий бит.
        bits = []
        # Проходим по вектору в обратном порядке (от наибольшего к наименьшему)
        for w_i in reversed(secret_key):
            if c_prime >= w_i:
                bits.append(1) # Бит установлен
                c_prime -= w_i # Вычитаем вес
            else:
                bits.append(0) # Бит не установлен

        # Результат bits сейчас в порядке [b7, b6, ..., b1, b0] (от старшего к младшему)
        # Нужно развернуть, чтобы получить [b0, b1, ..., b6, b7] для правильного восстановления байта
        bits.reverse()

        # Проверяем, что c_prime стало 0 (иначе ошибка)
        if c_prime != 0:
            # print(f"Ошибка дешифрования: c_prime не равен 0 после вычитания. c_prime = {c_prime}")
            return None # Ошибка при решении задачи о рюкзаке

        # Шаг 3: Преобразовать 8 битов в байт
        # Вычисляем байт как b0*2^0 + b1*2^1 + ... + b7*2^7
        byte_val = 0
        for i, bit in enumerate(bits):
            byte_val += bit * (2 ** i)
        # Добавляем восстановленный байт в результат
        decrypted_bytes.append(byte_val)

    # Возвращаем список дешифрованных байтов
    return decrypted_bytes

# --- Функции преобразования данных между текстом и байтами ---
# Используются для подготовки текста к шифрованию и восстановления после дешифрования
# Согласно требованиям, используется кодировка Windows-1251

def text_to_bytes_windows1251(text):
    """
    Преобразует текст в список байтов, закодированных в Windows-1251.
    Каждый байт представляется как целое число (0-255).
    Это требуется по условию задачи для второго способа шифрования.

    :param text: Входной текст (строка).
    :return: Список целых чисел (байты) или пустой список при ошибке.
    """
    try:
        # Кодируем строку в байты с помощью Windows-1251
        byte_list = text.encode('windows-1251')
        # Преобразуем байтовый объект в список целых чисел
        return list(byte_list)
    except UnicodeEncodeError as e:
        # print(f"Ошибка кодирования в Windows-1251: {e}")
        # Возвращаем пустой список в случае ошибки
        return []

def bytes_to_text_windows1251(byte_list):
    """
    Преобразует список байтов, закодированных в Windows-1251, обратно в текст.

    :param byte_list: Список целых чисел (байты, 0-255).
    :return: Восстановленный текст (строка) или пустая строка при ошибке.
    """
    try:
        # Преобразуем список байтов в байтовый объект
        byte_array = bytes(byte_list)
        # Декодируем байты в строку с помощью Windows-1251
        text = byte_array.decode('windows-1251')
        return text
    except UnicodeDecodeError as e:
        # print(f"Ошибка декодирования из Windows-1251: {e}")
        # Возвращаем пустую строку в случае ошибки
        return ""

# --- Глобальные переменные для хранения ключей ---
# Эти переменные будут использоваться между функциями GUI
current_secret_key = None
current_public_key = None
current_m = None
current_w = None
current_w_inv = None

# --- Функции для обработки действий пользователя в GUI ---

def generate_keys_action():
    """
    Обработчик кнопки 'Сгенерировать ключи'.
    Вызывает функцию генерации ключей и отображает результаты в интерфейсе.
    """
    global current_secret_key, current_public_key, current_m, current_w, current_w_inv
    try:
        # Вызываем основную функцию генерации ключей
        secret_k, public_k, m, w, w_inv_calc = generate_knapsack_keys()
        # Проверяем, успешно ли сгенерированы ключи
        if secret_k is None or public_k is None:
            # Если нет, показываем сообщение об ошибке
            messagebox.showerror("Ошибка", "Не удалось сгенерировать ключи. Попробуйте снова.")
            return

        # Сохраняем сгенерированные ключи и параметры в глобальные переменные
        current_secret_key = secret_k
        current_public_key = public_k
        current_m = m
        current_w = w
        current_w_inv = w_inv_calc

        # Очищаем поле вывода и записываем информацию о сгенерированных ключах
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Сгенерированные параметры Knapsack ---\n")
        output_text.insert(tk.END, f"Секретный супервозрастающий вектор (закрытый ключ): {secret_k}\n")
        output_text.insert(tk.END, f"Открытый вектор (открытый ключ): {public_k}\n")
        output_text.insert(tk.END, f"Модуль m: {m}\n")
        output_text.insert(tk.END, f"Множитель w (для генерации открытого ключа): {w}\n")
        output_text.insert(tk.END, f"Мультипликативное обратное w^(-1) mod m: {w_inv_calc}\n")
        output_text.insert(tk.END, f"--- Ключи готовы к использованию ---\n\n")
    except Exception as e:
        # Обрабатываем любые непредвиденные ошибки
        messagebox.showerror("Ошибка", f"Произошла ошибка при генерации ключей: {e}")

def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать'.
    Получает текст из поля ввода, преобразует его в байты (Windows-1251),
    шифрует, и выводит результат в поле вывода.
    """
    global current_public_key, current_m
    # Проверяем, сгенерированы ли ключи
    if current_public_key is None or current_m is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем текст из многострочного поля ввода
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Предупреждение", "Введите текст для шифрования.")
        return

    try:
        # 1. Преобразуем текст в байты (Windows-1251)
        byte_list = text_to_bytes_windows1251(text)
        if not byte_list:
             messagebox.showwarning("Предупреждение", "Ошибка при кодировании текста в Windows-1251.")
             return

        # 2. Шифруем байты, используя открытый ключ
        encrypted_numbers = encrypt_knapsack(byte_list, current_public_key, current_m)

        # 3. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат шифрования Knapsack ---\n")
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        output_text.insert(tk.END, f"Коды байтов (Windows-1251): {byte_list}\n")
        output_text.insert(tk.END, f"Открытый ключ (вектор): {current_public_key}\n")
        output_text.insert(tk.END, f"Модуль m: {current_m}\n")
        output_text.insert(tk.END, f"Множитель w: {current_w}\n")
        output_text.insert(tk.END, f"Зашифрованные числа: {encrypted_numbers}\n")
        # Конвертируем числа в строку для удобства отображения
        encrypted_str = ' '.join(map(str, encrypted_numbers))
        output_text.insert(tk.END, f"Зашифрованное сообщение (строка чисел): {encrypted_str}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"Секретный ключ (супервозв.): {current_secret_key}\n")
        output_text.insert(tk.END, f"m: {current_m}, w: {current_w}, w^(-1): {current_w_inv}\n")

    except Exception as e:
        # Обрабатываем любые ошибки, возникшие в процессе шифрования
        messagebox.showerror("Ошибка", f"Произошла ошибка при шифровании: {e}")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать'.
    Получает зашифрованные числа из поля ввода, дешифрует их,
    преобразует обратно в текст (Windows-1251) и выводит результат.
    """
    global current_secret_key, current_m, current_w_inv
    # Проверяем, сгенерированы ли ключи
    if current_secret_key is None or current_m is None or current_w_inv is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем строку зашифрованных чисел из многострочного поля ввода
    encrypted_str = input_text.get("1.0", tk.END).strip()
    if not encrypted_str:
        messagebox.showwarning("Предупреждение", "Введите зашифрованные числа для дешифрования.")
        return

    try:
        # 1. Преобразуем строку чисел, разделенных пробелами, в список целых чисел
        encrypted_numbers = list(map(int, encrypted_str.split()))

        # 2. Дешифруем числа, используя закрытый ключ и параметры
        decrypted_bytes = decrypt_knapsack(encrypted_numbers, current_secret_key, current_m, current_w_inv)
        # Проверяем, успешно ли прошло дешифрование
        if decrypted_bytes is None:
            messagebox.showerror("Ошибка", "Ошибка при дешифровании. Проверьте введенные данные и ключи.")
            return

        # 3. Преобразуем дешифрованные байты обратно в текст (Windows-1251)
        decrypted_text = bytes_to_text_windows1251(decrypted_bytes)

        # 4. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат дешифрования Knapsack ---\n")
        output_text.insert(tk.END, f"Зашифрованные числа (введите строку): {encrypted_str}\n")
        output_text.insert(tk.END, f"Зашифрованные числа (список): {encrypted_numbers}\n")
        output_text.insert(tk.END, f"Секретный ключ (супервозв.): {current_secret_key}\n")
        output_text.insert(tk.END, f"Модуль m: {current_m}\n")
        output_text.insert(tk.END, f"Мультипликативное обратное w^(-1): {current_w_inv}\n")
        output_text.insert(tk.END, f"Дешифрованные байты: {decrypted_bytes}\n")
        output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted_text}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"m: {current_m}, w: {current_w}, w^(-1): {current_w_inv}\n")

    except ValueError:
        # Обрабатываем ошибку, если введенные данные не являются числами
        messagebox.showerror("Ошибка", "Неверный формат ввода. Введите числа, разделенные пробелом.")
    except Exception as e:
        # Обрабатываем любые другие ошибки, возникшие в процессе дешифрования
        messagebox.showerror("Ошибка", f"Произошла ошибка при дешифровании: {e}")

def clear_input():
    """
    Очищает поле ввода.
    """
    input_text.delete(1.0, tk.END)

def copy_output():
    """
    Копирует содержимое поля вывода в буфер обмена.
    """
    content = output_text.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("Информация", "Результат скопирован в буфер обмена.")

# --- Создание графического интерфейса ---
# Инициализируем главное окно приложения
root = tk.Tk()
root.title("Лабораторная работа 4 - Knapsack (Модифицированный)")
root.geometry("800x600")

# --- Меню ---
# Создаем меню (на будущее, можно расширить)
menubar = Menu(root)
root.config(menu=menubar)

# --- Фреймы для структуры ---
# Основной фрейм, заполняющий всё окно
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Фрейм для генерации ключей
keys_frame = ttk.LabelFrame(main_frame, text="Ключи")
keys_frame.pack(fill=tk.X, padx=5, pady=5)

# Фрейм для шифрования/дешифрования
crypto_frame = ttk.LabelFrame(main_frame, text="Шифрование / Дешифрование")
crypto_frame.pack(fill=tk.X, padx=5, pady=5)

# Фрейм для вывода результатов
output_frame = ttk.LabelFrame(main_frame, text="Вывод")
output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# --- Виджеты ---

# Ключи
generate_button = ttk.Button(keys_frame, text="Сгенерировать ключи", command=generate_keys_action)
generate_button.pack(side=tk.LEFT, padx=5, pady=5)

# Шифрование/Дешифрование
input_label = ttk.Label(crypto_frame, text="Введите текст или числа:")
input_label.pack(anchor="w", padx=5, pady=2)

# Многострочное поле ввода
input_text = tk.Text(crypto_frame, height=3, width=70)
input_text.pack(fill=tk.X, padx=5, pady=2, expand=True)

# Фрейм для кнопок в разделе шифрования
button_frame = ttk.Frame(crypto_frame)
button_frame.pack(fill=tk.X, padx=5, pady=5)

encrypt_button = ttk.Button(button_frame, text="Зашифровать", command=encrypt_action)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = ttk.Button(button_frame, text="Дешифровать", command=decrypt_action)
decrypt_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(button_frame, text="Очистить ввод", command=clear_input)
clear_button.pack(side=tk.LEFT, padx=5)

# Вывод
# Многострочное поле вывода с прокруткой
output_text = scrolledtext.ScrolledText(output_frame, width=80, height=20)
output_text.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

copy_button = ttk.Button(output_frame, text="Копировать результат", command=copy_output)
copy_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# --- Настройка сетки ---
# Позволяет элементам интерфейса адаптироваться при изменении размера окна
main_frame.grid_rowconfigure(2, weight=1) # output_frame растягивается по вертикали
main_frame.grid_columnconfigure(0, weight=1) # Колонка растягивается по горизонтали

# Запуск главного цикла обработки событий Tkinter
root.mainloop()
