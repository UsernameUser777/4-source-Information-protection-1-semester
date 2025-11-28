# Импортируем необходимые библиотеки для создания графического интерфейса
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu, StringVar
# Импортируем библиотеки для работы с числами и генерации случайных значений
import random
import math

# --- Константы ---
# Определяем русский алфавит (для кодирования по позиции)
# Включает все буквы от 'А' до 'Я', включая 'Ё'
RU_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# --- Вспомогательные математические функции для ElGamal ---

def gcd_extended(a, b):
    """
    Расширенный алгоритм Евклида.
    Находит наибольший общий делитель (gcd) чисел a и b,
    а также коэффициенты x и y такие, что a*x + b*y = gcd(a, b).
    Эта функция критически важна для вычисления мультипликативного обратного числа (s_inv),
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
    s_inv - это секретный ключ, такой что (s * s_inv) % m = 1.
    Это необходимо для вычисления s_inv в процессе дешифрования.

    :param e: Число, для которого ищется обратное (например, s).
    :param m: Модуль (например, p-1).
    :return: s_inv - секретный ключ (целое число) или None, если обратное не существует
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
    s_inv = x % m
    # Возвращаем вычисленное значение s_inv
    return s_inv

def is_prime(n):
    """
    Проверяет, является ли число n простым методом пробного деления.
    Используется для генерации простого числа p, которое является
    основой для создания ключей в ElGamal.

    :param n: Целое число для проверки.
    :return: True, если n простое, иначе False.
    """
    # Числа меньше 2 не являются простыми
    if n < 2:
        return False
    # 2 - простое число
    if n == 2:
        return True
    # Четные числа (кроме 2) не являются простыми
    if n % 2 == 0:
        return False
    # Проверяем делители до sqrt(n), так как если n составное,
    # то у него есть делитель, не превышающий sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2): # Проверяем только нечетные числа
        if n % i == 0:
            return False
    # Если не нашли делителей, n - простое
    return True

def generate_prime_candidate(length):
    """
    Генерирует случайное нечетное число заданной битовой длины.
    Используется как кандидат для простого числа в процессе генерации ключей.

    :param length: Битовая длина числа (например, 16 означает число от 32768 до 65535).
    :return: Случайное нечетное число с заданной битовой длиной.
    """
    # Генерируем случайное число с заданной битовой длиной
    p = random.getrandbits(length)
    # Устанавливаем младший бит, чтобы число было нечетным
    p |= 1
    # Устанавливаем старший бит, чтобы гарантировать, что длина числа равна length
    p |= (1 << length - 1)
    # Возвращаем сгенерированное число
    return p

def generate_prime_number(length=16): # Увеличена длина для лучшей "стойкости"
    """
    Генерирует простое число заданной битовой длины.
    Повторяет генерацию кандидата и проверку на простоту до тех пор,
    пока не будет найдено простое число.

    :param length: Битовая длина простого числа (по умолчанию 16 для простоты).
    :return: Сгенерированное простое число.
    """
    # Инициализируем переменную p составным числом, чтобы войти в цикл
    p = 4
    # Повторяем, пока не найдем простое число
    while not is_prime(p):
        # Генерируем нового кандидата
        p = generate_prime_candidate(length)
    # Возвращаем найденное простое число
    return p

def is_primitive_root(g, p):
    """
    Проверяет, является ли g первообразным корнем по модулю p.
    g является первообразным корнем, если его степени g^1, g^2, ..., g^(p-1) mod p
    генерируют все ненулевые остатки от 1 до p-1.
    Это важно для выбора безопасного g в ElGamal.

    :param g: Предполагаемый первообразный корень.
    :param p: Простое число.
    :return: True, если g - первообразный корень, иначе False.
    """
    # Если g и p не взаимно просты, g не может быть первообразным корнем
    if math.gcd(g, p) != 1:
        return False
    # Проверяем, что g^( (p-1)/q ) != 1 (mod p) для всех простых делителей q числа (p-1)
    phi = p - 1
    factors = set() # Используем множество для уникальных делителей
    n = phi
    # Найдем простые делители phi
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)

    # Проверяем условие для каждого уникального простого делителя
    for factor in factors:
        # Если g^(phi/factor) mod p равно 1, то g не первообразный корень
        if pow(g, phi // factor, p) == 1:
            return False
    # Если ни для одного делителя условие не нарушилось, g - первообразный корень
    return True

def find_primitive_root(p):
    """
    Находит первообразный корень по модулю p.
    Использует перебор, начиная с 2.
    Для простых чисел p, если g - первообразный корень, то g^k тоже может быть
    первообразным корнем при gcd(k, p-1) = 1. Простой перебор часто эффективен.

    :param p: Простое число.
    :return: Первообразный корень (целое число) или None, если не найден.
    """
    for g in range(2, p): # Пробуем g от 2 до p-1
        if is_primitive_root(g, p): # Проверяем, является ли g первообразным корнем
            return g
    return None # Не найден (маловероятно для простых p, но на всякий случай)

# --- Основные функции ElGamal ---

def generate_keys():
    """
    Генерирует пару открытого и закрытого ключей ElGamal.
    Выбирает простое p, первообразный корень g, случайный секретный ключ x,
    вычисляет открытый ключ y.

    :return: Кортеж ((p, g, y) - открытый ключ, x - закрытый ключ)
             или (None, None) при ошибке.
    """
    # Генерируем простое число p
    p = generate_prime_number(16) # Используем 16 бит для большей "стойкости"
    if not p:
        # print("Ошибка: Не удалось сгенерировать простое p.")
        return None, None

    # Находим первообразный корень g по модулю p
    g = find_primitive_root(p)
    if g is None:
        # print(f"Ошибка: Не удалось найти первообразный корень для p={p}.")
        return None, None

    # Выбираем случайный секретный ключ x: 1 < x < p-1
    x = random.randint(2, p - 2)

    # Вычисляем открытый ключ y = g^x mod p
    y = pow(g, x, p)

    # Формируем открытый и закрытый ключи
    public_key = (p, g, y)
    private_key = x
    # Возвращаем открытый и закрытый ключи
    return public_key, private_key

def encrypt_elgamal(numbers, public_key):
    """
    Шифрует список чисел (кодов символов), с помощью открытого ключа ElGamal.
    Для каждого числа генерируется *отдельное* случайное k.
    Это требование указано в задании: "Для алгоритма шифрования Эль-Гамаля
    случайные числа k для каждой буквы исходного сообщения должны быть разными."

    :param numbers: Список целых чисел (0-32 для русского алфавита).
    :param public_key: Кортеж (p, g, y).
    :return: Список кортежей [(c1_1, c2_1), (c1_2, c2_2), ...] - зашифрованные пары.
    """
    # Распаковываем открытый ключ
    p, g, y = public_key
    # Инициализируем список для хранения зашифрованных пар
    encrypted_pairs = []
    # Проходим по каждому числу (символу) в списке
    for num in numbers:
        # Проверяем, что число (символ) меньше p, иначе ElGamal не работает корректно
        if num >= p:
            # print(f"Ошибка: Значение символа {num} >= p ({p}). Выберите большее p.")
            return None

        # Генерируем *отдельное* случайное k для этой буквы: 1 < k < p-1
        k = random.randint(2, p - 2)

        # Вычисляем c1 = g^k mod p
        c1 = pow(g, k, p)

        # Вычисляем c2 = (m * y^k) mod p
        # Сначала вычисляем y^k mod p
        y_k = pow(y, k, p)
        # Затем вычисляем (m * y^k) mod p
        c2 = (num * y_k) % p

        # Добавляем зашифрованную пару (c1, c2) в результат
        encrypted_pairs.append((c1, c2))
    # Возвращаем список зашифрованных пар
    return encrypted_pairs

def decrypt_elgamal(encrypted_pairs, private_key, p):
    """
    Дешифрует список пар (c1, c2), с помощью закрытого ключа ElGamal.

    :param encrypted_pairs: Список кортежей [(c1_1, c2_1), (c1_2, c2_2), ...].
    :param private_key: Целое число x (секретный ключ).
    :param p: Простое число из открытого ключа.
    :return: Список дешифрованных целых чисел (исходные коды символов) или None при ошибке.
    """
    # Инициализируем список для хранения дешифрованных чисел
    decrypted_nums = []
    # Проходим по каждой зашифрованной паре (c1, c2)
    for c1, c2 in encrypted_pairs:
        # Вычисляем s = c1^x mod p
        s = pow(c1, private_key, p)

        # Вычисляем s_inv = s^(-1) mod p
        s_inv = mod_inverse(s, p)
        # Проверяем, удалось ли вычислить s_inv
        if s_inv is None:
            # print(f"Ошибка: Не удалось найти обратное для s={s} по модулю p={p}.")
            return None

        # Вычисляем m = (c2 * s_inv) mod p
        m = (c2 * s_inv) % p
        # Добавляем дешифрованное число в результат
        decrypted_nums.append(m)
    # Возвращаем список дешифрованных чисел
    return decrypted_nums

# --- Функции преобразования данных между текстом и числами ---
# Используются для подготовки текста к шифрованию и восстановления после дешифрования
# Согласно требованиям, используется кодирование по позиции в алфавите

def text_to_numbers(text, alphabet):
    """
    Преобразует текст в список чисел по позиции символа в алфавите (0-базированная).
    Буква 'А' -> 0, 'Б' -> 1, ..., 'Я' -> 32.

    :param text: Входной текст (строка).
    :param alphabet: Алфавит (строка).
    :return: Список целовыx чисел (коды символов).
    """
    # Инициализируем список для чисел
    numbers = []
    # Проходим по каждому символу в тексте
    for char in text.upper(): # Работаем с верхним регистром для согласованности
        # Проверяем, есть ли символ в алфавите
        if char in alphabet:
            # Находим индекс символа в алфавите и добавляем его в список
            numbers.append(alphabet.index(char))
        else:
            # Игнорируем неалфавитные символы (например, пробелы, знаки препинания)
            # Можно также реализовать обработку таких символов, если нужно
            pass
    # Возвращаем список чисел
    return numbers

def numbers_to_text(numbers, alphabet):
    """
    Преобразует список чисел обратно в текст по алфавиту.
    Число 0 -> 'А', 1 -> 'Б', ..., 32 -> 'Я'.

    :param numbers: Список целых чисел (0-32 для русского алфавита).
    :param alphabet: Алфавит (строка).
    :return: Восстановленный текст (строка).
    """
    # Инициализируем строку для текста
    text = ""
    # Проходим по каждому числу в списке
    for num in numbers:
        # Проверяем, находится ли число в допустимом диапазоне алфавита
        if 0 <= num < len(alphabet):
            # Находим символ в алфавите по индексу и добавляем к строке
            text += alphabet[num]
        else:
            # Обработка ошибки: число вне диапазона алфавита
            # Можно использовать символ-заполнитель или бросить исключение
            text += "?"
    # Возвращаем восстановленный текст
    return text

# --- Глобальные переменные для хранения ключей ---
# Эти переменные будут использоваться между функциями GUI
current_public_key = None
current_private_key = None

# --- Функции для обработки действий пользователя в GUI ---

def generate_keys_action():
    """
    Обработчик кнопки 'Сгенерировать ключи'.
    Вызывает функцию генерации ключей и отображает результаты в интерфейсе.
    """
    global current_public_key, current_private_key
    try:
        # Вызываем основную функцию генерации ключей
        pub_key, priv_key = generate_keys()
        # Проверяем, успешно ли сгенерированы ключи
        if pub_key is None or priv_key is None:
            # Если нет, показываем сообщение об ошибке
            messagebox.showerror("Ошибка", "Не удалось сгенерировать ключи. Попробуйте снова.")
            return

        # Сохраняем сгенерированные ключи в глобальные переменные
        current_public_key = pub_key
        current_private_key = priv_key

        # Очищаем поле вывода и записываем информацию о сгенерированных ключах
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Сгенерированные параметры ElGamal ---\n")
        output_text.insert(tk.END, f"Простое число p: {pub_key[0]}\n")
        output_text.insert(tk.END, f"Первообразный корень g: {pub_key[1]}\n")
        output_text.insert(tk.END, f"Открытый ключ y (g^x mod p): {pub_key[2]}\n")
        output_text.insert(tk.END, f"Секретный ключ x: {priv_key}\n")
        output_text.insert(tk.END, f"--- Ключи готовы к использованию ---\n\n")
    except Exception as e:
        # Обрабатываем любые непредвиденные ошибки
        messagebox.showerror("Ошибка", f"Произошла ошибка при генерации ключей: {e}")

def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать'.
    Получает текст из поля ввода, преобразует его в числа (по алфавиту),
    шифрует, и выводит результат в поле вывода.
    """
    global current_public_key
    # Проверяем, сгенерированы ли ключи
    if current_public_key is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем текст из многострочного поля ввода
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Предупреждение", "Введите текст для шифрования.")
        return

    try:
        # 1. Преобразуем текст в числа (коды символов по алфавиту)
        numbers = text_to_numbers(text, RU_ALPHABET)
        if not numbers:
             messagebox.showwarning("Предупреждение", "Введенный текст не содержит символов из русского алфавита.")
             return

        # 2. Шифруем числа, используя открытый ключ
        # Каждому символу соответствует *отдельное* случайное k
        encrypted_pairs = encrypt_elgamal(numbers, current_public_key)
        # Проверяем, успешно ли прошло шифрование (например, если символ > p)
        if encrypted_pairs is None:
            messagebox.showerror("Ошибка", f"Значение символа в тексте превышает допустимое p={current_public_key[0]}. Попробуйте снова.")
            return

        # 3. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат шифрования ElGamal ---\n")
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        output_text.insert(tk.END, f"Коды символов (по алфавиту): {numbers}\n")
        output_text.insert(tk.END, f"Открытый ключ (p, g, y): {current_public_key}\n")
        output_text.insert(tk.END, f"Секретный ключ x: {current_private_key}\n")
        output_text.insert(tk.END, f"Зашифрованные пары (c1, c2): {encrypted_pairs}\n")
        # Конвертируем пары в строку для удобства отображения
        encrypted_str = ', '.join([f'({c1},{c2})' for c1, c2 in encrypted_pairs])
        output_text.insert(tk.END, f"Зашифрованное сообщение (строка пар): {encrypted_str}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"p: {current_public_key[0]}, g: {current_public_key[1]}, y: {current_public_key[2]}\n")
        output_text.insert(tk.END, f"x: {current_private_key}\n")

    except Exception as e:
        # Обрабатываем любые ошибки, возникшие в процессе шифрования
        messagebox.showerror("Ошибка", f"Произошла ошибка при шифровании: {e}")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать'.
    Получает зашифрованные пары из поля ввода, дешифрует их,
    преобразует обратно в текст и выводит результат.
    """
    global current_private_key, current_public_key
    # Проверяем, сгенерированы ли ключи
    if current_private_key is None or current_public_key is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем строку зашифрованных пар из многострочного поля ввода
    encrypted_str = input_text.get("1.0", tk.END).strip()
    if not encrypted_str:
        messagebox.showwarning("Предупреждение", "Введите зашифрованные пары для дешифрования.")
        return

    try:
        # 1. Преобразуем строку пар в список кортежей
        # Ожидаем формат: (c1,c2), (c3,c4), ...
        # Используем регулярные выражения для извлечения чисел из скобок
        import re
        # Находим все последовательности (цифра, цифра) в строке
        pairs_str = re.findall(r'\((\d+),(\d+)\)', encrypted_str)
        if not pairs_str:
            raise ValueError("Неверный формат ввода пар. Используйте формат: (c1,c2), (c3,c4), ...")

        # Преобразуем найденные строки в кортежи целых чисел
        encrypted_pairs = [(int(c1), int(c2)) for c1, c2 in pairs_str]

        # 2. Дешифруем пары, используя закрытый ключ и p
        decrypted_numbers = decrypt_elgamal(encrypted_pairs, current_private_key, current_public_key[0])
        # Проверяем, успешно ли прошло дешифрование
        if decrypted_numbers is None:
            messagebox.showerror("Ошибка", "Ошибка при дешифровании. Проверьте введенные данные и ключи.")
            return

        # 3. Преобразуем дешифрованные числа обратно в текст
        decrypted_text = numbers_to_text(decrypted_numbers, RU_ALPHABET)

        # 4. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат дешифрования ElGamal ---\n")
        output_text.insert(tk.END, f"Зашифрованные пары (введите строку): {encrypted_str}\n")
        output_text.insert(tk.END, f"Зашифрованные пары (список): {encrypted_pairs}\n")
        output_text.insert(tk.END, f"Секретный ключ x: {current_private_key}\n")
        output_text.insert(tk.END, f"p: {current_public_key[0]}\n")
        output_text.insert(tk.END, f"Дешифрованные коды: {decrypted_numbers}\n")
        output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted_text}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"p: {current_public_key[0]}, g: {current_public_key[1]}, y: {current_public_key[2]}\n")
        output_text.insert(tk.END, f"x: {current_private_key}\n")

    except ValueError as ve:
        # Обрабатываем ошибку, если введенные данные не соответствуют формату пар
        messagebox.showerror("Ошибка", f"Неверный формат ввода: {ve}")
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
root.title("Лабораторная работа 4 - ElGamal (Модифицированный)")
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
input_label = ttk.Label(crypto_frame, text="Введите текст или пары:")
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
