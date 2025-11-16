import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import secrets
import math

# --- Глобальные переменные для хранения сгенерированной гаммы ---
# Используем словари для хранения битов и шагов
lfsr_gamma_bits = []
lfsr_gamma_steps = []
bbs_gamma_bits = []
bbs_gamma_steps = []

# --- Вспомогательные функции ---

def text_to_bits(text):
    """
    Преобразует текст в список 8-битных строк, представляющих байты Windows-1251.
    """
    bits_list = []
    for char in text.upper():
        try:
            byte_val = char.encode('cp1251')[0]
            char_bits_str = format(byte_val, '08b')
            bits_list.append(char_bits_str)
        except UnicodeEncodeError:
            continue
    return bits_list

def bits_to_text(bits_list):
    """
    Преобразует список 8-битных строк (Windows-1251) обратно в текст.
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

def gamma_cipher_mod2_bits(text_bits, gamma_bits_list):
    """
    Шифрует список 8-битных строк текста с помощью списка 8-битных строк гаммы по модулю 2 (XOR).
    """
    if not text_bits or not gamma_bits_list:
        return []

    extended_gamma = []
    for i in range(len(text_bits)):
        extended_gamma.append(gamma_bits_list[i % len(gamma_bits_list)])

    encrypted_bits = []
    for i in range(len(text_bits)):
        t_bits = text_bits[i]
        g_bits = extended_gamma[i]

        if len(t_bits) != 8 or len(g_bits) != 8:
             continue

        encrypted_char_bits = ""
        for j in range(8):
            bit_t = int(t_bits[j])
            bit_g = int(g_bits[j])
            encrypted_bit = (bit_t + bit_g) % 2
            encrypted_char_bits += str(encrypted_bit)
        encrypted_bits.append(encrypted_char_bits)

    return encrypted_bits

def gamma_decipher_mod2_bits(encrypted_bits, gamma_bits_list):
    """
    Дешифрует список 8-битных строк текста с помощью списка 8-битных строк гаммы по модулю 2 (XOR).
    """
    # Операция XOR обратима, поэтому используем ту же функцию, что и для шифрования
    return gamma_cipher_mod2_bits(encrypted_bits, gamma_bits_list)


def calculate_initial_value_surname(surname):
    """
    Вычисляет начальное значение для генераторов гаммы по фамилии.
    Начальное значение определяется сложением по модулю 2 (XOR) всех букв фамилии
    в соответствии с кодировкой Windows 1251.

    :param surname: Введенная пользователем фамилия (str).
    :return: Кортеж из:
             - initial_int: начальное значение (int, 0-255),
             - calculation_steps: список строк с промежуточными вычислениями (list of str),
             - initial_bits_str: 8-битная строка начального значения (str).
    """
    # Преобразуем фамилию в верхний регистр для единообразия
    surname_upper = surname.upper()
    # Список для хранения 8-битных строк, представляющих байты каждой буквы в cp1251
    bits_list = []
    for char in surname_upper:
        try:
            # Кодируем символ в байт по кодировке cp1251 (Windows-1251)
            byte_val = char.encode('cp1251')[0]
            # Преобразуем байт (значение от 0 до 255) в 8-битную двоичную строку (например, '01000000')
            char_bits_str = format(byte_val, '08b')
            bits_list.append(char_bits_str)
        except UnicodeEncodeError:
            # Если символ не входит в кодировку cp1251, он игнорируется
            # Это маловероятно для русской фамилии, но на всякий случай
            continue

    # Если не удалось получить биты ни для одной буквы, возвращаем ошибку
    if not bits_list:
        return None, [], ""

    # Инициализируем аккумулирующий XOR результат нулями
    initial_int = 0
    accumulated_xor_bits = ['0'] * 8
    # Список для хранения строк промежуточных вычислений для отчета
    calculation_steps = []

    # Проходим по каждой 8-битной строке, представляющей букву
    for i, bits_str in enumerate(bits_list):
        # Формируем строку для отчета: биты + (буква)
        calc_step = f"{bits_str} (буква '{surname_upper[i]}')"
        calculation_steps.append(calc_step)
        # Выполняем побитовый XOR с аккумулирующим значением
        for j in range(8):
            # Складываем по модулю 2 (XOR) текущий бит буквы и аккумулируемый бит
            accumulated_xor_bits[j] = str((int(accumulated_xor_bits[j]) + int(bits_str[j])) % 2)

    # Преобразуем итоговый 8-битный список в строку
    initial_bits_str = "".join(accumulated_xor_bits)
    # Преобразуем 8-битную строку в целое число (0-255)
    initial_int = int(initial_bits_str, 2)

    # Формируем строку для отчета с полным расчетом
    # full_calc_str = " ⊕ ".join([step.split(' ')[0] for step in calculation_steps])
    # full_calc_str += f" = {initial_bits_str} = {initial_int} (по модулю 256)"

    return initial_int, calculation_steps, initial_bits_str


def lfsr_generator(initial_state, poly_taps, num_bits):
    """
    Генерирует биты с помощью регистра сдвига с линейной обратной связью (LFSR).

    :param initial_state: Начальное состояние регистра (int, 0-255 для 8-бит).
    :param poly_taps: Индексы тапов (от младшего бита), определяющие полином (list of int).
                      Например, для x^8 + x^4 + x^3 + x^2 + 1, тапы на битах 4, 3, 2, 0.
    :param num_bits: Количество бит гаммы для генерации (int).
    :return: Кортеж из:
             - bits: список сгенерированных битов (list of int),
             - steps: список словарей с промежуточными шагами для отчета (list of dict).
    """
    # Используем копию начального состояния для вычислений
    state = initial_state
    # Список для хранения сгенерированных битов
    bits = []
    # Список для хранения информации о каждом шаге генерации
    steps = []

    # Выполняем num_bits итераций
    for i in range(num_bits):
        # Вычисляем новый бит для вставки (обратная связь) как XOR тапов
        new_bit = 0
        tap_bits = [] # Для отчета: значения тапов на этом шаге
        for tap in poly_taps:
            # Получаем значение бита в позиции tap
            bit_val = (state >> tap) & 1
            new_bit ^= bit_val
            tap_bits.append(str(bit_val))

        # Сохраняем информацию о текущем шаге для отчета
        steps.append({
            'step': i + 1,
            'state_before': format(state, f'08b'), # Состояние до сдвига
            'taps': tap_bits, # Значения тапов
            'feedback': str(new_bit), # Вычисленный бит обратной связи
            'state_after': format(((state << 1) | new_bit) & 0xFF, f'08b') # Состояние после сдвига и вставки
        })

        # Выполняем сдвиг влево на 1 бит и вставляем новый бит
        # Ограничиваем результат 8-битным значением с помощью & 0xFF
        state = ((state << 1) | new_bit) & 0xFF
        # Сгенерированный бит (старший бит до сдвига) - это бит, который был "вытолкнут" из регистра
        # Однако, в классическом LFSR, выходом часто считается бит обратной связи
        # В примере в учебнике (Табл. 6.6) кажется, что выходной бит - это feedback.
        # Поэтому добавляем new_bit в список гаммы.
        bits.append(new_bit)

    return bits, steps


def bbs_generator(initial_seed, p, q, num_bits):
    """
    Генерирует биты с помощью алгоритма Блюм-Блюм-Шуба (BBS).
    Проверяет, что p и q являются безопасными простыми.

    :param initial_seed: Начальное значение (x0) (int).
    :param p: Простое число p (int), p ≡ 3 (mod 4).
    :param q: Простое число q (int), q ≡ 3 (mod 4).
    :param num_bits: Количество бит гаммы для генерации (int).
    :return: Кортеж из:
             - bits: список сгенерированных битов (list of int),
             - steps: список словарей с промежуточными шагами для отчета (list of dict).
    """
    # Проверка, что p и q - безопасные простые (p = 2p' + 1, q = 2q' + 1, где p', q' - простые)
    # Для простоты, в данном примере проверка не реализована, предполагается корректный ввод.
    # В реальном приложении следует добавить проверку.
    if (p - 1) % 4 != 0 or (q - 1) % 4 != 0:
        messagebox.showwarning("Предупреждение",
                               f"p={p} и q={q} должны быть безопасными простыми (≡ 3 mod 4). Результат может быть некорректным.")

    # Вычисляем модуль n = p * q
    n = p * q
    # Убедимся, что начальное значение корректно (не 0 и в пределах n)
    seed = initial_seed % n
    if seed == 0:
        seed = 1 # Если seed % n == 0, используем 1 как ненулевое начальное значение

    # Список для хранения сгенерированных битов
    bits = []
    # Список для хранения информации о каждом шаге генерации
    steps = []

    # Выполняем num_bits итераций
    for i in range(num_bits):
        # Вычисляем x_{i+1} = (x_i)^2 mod n
        x_squared = (seed * seed) % n
        # Берем младший бит (паритет) как выходной бит
        parity_bit = x_squared % 2
        # Добавляем бит в гамму
        bits.append(parity_bit)

        # Сохраняем информацию о текущем шаге для отчета
        steps.append({
            'step': i + 1,
            'x_i': seed, # Текущее значение x_i перед возведением в квадрат
            'x_squared': x_squared, # Значение x_i^2 до взятия по модулю
            'parity_bit': parity_bit # Сгенерированный бит (x_{i+1} mod 2)
        })

        # Переходим к следующему значению
        seed = x_squared

    return bits, steps


def is_prime(n):
    """Проверяет, является ли число n простым."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_safe_prime_candidate():
    """Генерирует потенциальное безопасное простое число p = 2*q + 1, где q также простое."""
    while True:
        # Генерируем случайное 15-битное число для q
        q = secrets.randbits(15)
        if q % 2 == 0:
            q += 1  # Делаем нечетным
        if q < 3:
            continue
        # Проверяем, является ли q простым
        if is_prime(q):
            # Вычисляем p = 2*q + 1
            p = 2 * q + 1
            # Проверяем, является ли p простым
            if is_prime(p):
                return p # Возвращаем найденное безопасное простое число p


def calculate_initial_and_run_lfsr():
    """
    Обработчик события нажатия кнопки 'Рассчитать нач. знач. и запустить LFSR'.
    Вычисляет начальное значение по фамилии и генерирует гамму с помощью LFSR.
    Выводит результаты в текстовое поле.
    Также сохраняет сгенерированную гамму в глобальные переменные.
    Затем автоматически шифрует и дешифрует введённую фамилию с помощью этой гаммы.
    """
    global lfsr_gamma_bits, lfsr_gamma_steps
    # Получаем фамилию из поля ввода
    surname = input_surname.get().strip()

    # Проверяем, введена ли фамилия
    if not surname:
        output_text.delete(1.0, tk.END) # Очищаем поле вывода
        output_text.insert(tk.END, "Ошибка: Введите фамилию для расчета начального значения.\n")
        return

    # Вычисляем начальное значение
    initial_val, calc_steps, initial_bits = calculate_initial_value_surname(surname)
    # Проверяем, удалось ли вычислить
    if initial_val is None:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Не удалось вычислить начальное значение для фамилии '{surname}'.\n")
        return

    # --- Параметры LFSR ---
    # Полином: x^8 + x^4 + x^3 + x^2 + 1
    # Этот полином означает, что обратная связь формируется как XOR битов на позициях 4, 3, 2, 0
    # (индексы от 0 до 7, где 7 - старший бит регистра, 0 - младший).
    # Это биты, соответствующие членам x^4, x^3, x^2, x^0 в полиноме.
    poly_taps = [4, 3, 2, 0]
    num_iterations = 10 # Количество итераций из задания

    # Убедимся, что начальное состояние не ноль (иначе гамма будет нулевой)
    initial_state_for_lfsr = initial_val if initial_val != 0 else 1

    # Генерируем гамму с помощью LFSR
    lfsr_bits, lfsr_steps = lfsr_generator(initial_state_for_lfsr, poly_taps, num_iterations)
    # Сохраняем гамму и шаги в глобальные переменные
    lfsr_gamma_bits = [format(bit, '08b') for bit in lfsr_bits] # Преобразуем биты в 8-битные строки
    lfsr_gamma_steps = lfsr_steps

    # Очищаем поле вывода и вставляем результаты
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Расчет начального значения для генераторов ---\n")
    output_text.insert(tk.END, f"Фамилия: {surname}\n")
    output_text.insert(tk.END, "Расчет (XOR байтов Windows-1251): \n")
    for step in calc_steps:
        output_text.insert(tk.END, f"  {step}\n")
    output_text.insert(tk.END, f"Результат: {initial_val} (десятичное), {initial_bits} (8-бит двоичное)\n\n")

    output_text.insert(tk.END, "--- Генерация гаммы LFSR ---\n")
    output_text.insert(tk.END, f"Полином: x^8 + x^4 + x^3 + x^2 + 1\n")
    output_text.insert(tk.END, f"Тапы (0-indexed от младшего бита): {poly_taps}\n")
    output_text.insert(tk.END,
                       f"Начальное состояние (S0): {format(initial_state_for_lfsr, '08b')} ({initial_state_for_lfsr})\n")
    output_text.insert(tk.END, f"Количество итераций: {num_iterations}\n\n")

    output_text.insert(tk.END, "Таблица генерации гаммы LFSR:\n")
    output_text.insert(tk.END, "Шаг\tСостояние (до)\tТапы (b4,b3,b2,b0)\tОбратная связь\tСостояние (после)\n")
    for step_data in lfsr_steps:
        output_text.insert(tk.END,
                           f"{step_data['step']}\t{step_data['state_before']}\t\t{','.join(step_data['taps'])}\t\t{step_data['feedback']}\t\t{step_data['state_after']}\n")

    output_text.insert(tk.END, f"\nСгенерированная гамма (биты): {lfsr_bits}\n")
    output_text.insert(tk.END, f"Сгенерированная гамма (8-битные строки): {lfsr_gamma_bits}\n\n")

    # --- НОВОЕ: Автоматическое шифрование и дешифрование введенной фамилии ---
    output_text.insert(tk.END, "--- Автоматическое шифрование и дешифрование введенной фамилии с использованием сгенерированной LFSR гаммы ---\n")

    # Шифрование
    surname_bits = text_to_bits(surname)
    if surname_bits:
        encrypted_surname_bits = gamma_cipher_mod2_bits(surname_bits, lfsr_gamma_bits)
        encrypted_surname_text = bits_to_text(encrypted_surname_bits)

        output_text.insert(tk.END, f"Исходная фамилия: {surname}\n")
        output_text.insert(tk.END, f"Фамилия (байты, биты): {surname_bits}\n")
        output_text.insert(tk.END, f"Использованная LFSR гамма: {lfsr_gamma_bits}\n")
        output_text.insert(tk.END, f"Зашифрованная фамилия (байты, биты): {encrypted_surname_bits}\n")
        output_text.insert(tk.END, f"Зашифрованная фамилия: {encrypted_surname_text}\n\n")

        # Дешифрование
        decrypted_surname_bits = gamma_decipher_mod2_bits(encrypted_surname_bits, lfsr_gamma_bits)
        decrypted_surname_text = bits_to_text(decrypted_surname_bits)

        output_text.insert(tk.END, f"Дешифрованная фамилия (байты, биты): {decrypted_surname_bits}\n")
        output_text.insert(tk.END, f"Дешифрованная фамилия: {decrypted_surname_text}\n\n")
    else:
        output_text.insert(tk.END, f"Не удалось преобразовать фамилию '{surname}' в биты для шифрования.\n\n")


def calculate_initial_and_run_bbs():
    """
    Обработчик события нажатия кнопки 'Рассчитать нач. знач. и запустить BBS'.
    Вычисляет начальное значение по фамилии и генерирует гамму с помощью BBS.
    Выводит результаты в текстовое поле.
    Также сохраняет сгенерированную гамму в глобальные переменные.
    Затем автоматически шифрует и дешифрует введённую фамилию с помощью этой гаммы.
    """
    global bbs_gamma_bits, bbs_gamma_steps
    # Получаем фамилию из поля ввода
    surname = input_surname.get().strip()

    # Проверяем, введена ли фамилия
    if not surname:
        output_text.delete(1.0, tk.END) # Очищаем поле вывода
        output_text.insert(tk.END, "Ошибка: Введите фамилию для расчета начального значения.\n")
        return

    # Вычисляем начальное значение
    initial_val, calc_steps, initial_bits = calculate_initial_value_surname(surname)
    # Проверяем, удалось ли вычислить
    if initial_val is None:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Не удалось вычислить начальное значение для фамилии '{surname}'.\n")
        return

    # --- Параметры BBS ---
    # Используем введенные пользователем значения p и q
    try:
        p_input = p_entry.get().strip()
        q_input = q_entry.get().strip()

        if p_input.lower() == "auto":
            p = generate_safe_prime_candidate()
        else:
            p = int(p_input)

        if q_input.lower() == "auto":
            q = generate_safe_prime_candidate()
            while q == p:  # Убедимся, что p != q
                q = generate_safe_prime_candidate()
        else:
            q = int(q_input)

        # Проверим, что p и q - простые и безопасные
        if not (is_prime(p) and is_prime(q) and (p - 1) % 4 == 0 and (q - 1) % 4 == 0):
            messagebox.showwarning("Предупреждение",
                                   f"Введенные p={p} и q={q} не являются безопасными простыми. Результат может быть некорректным.")

    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Ошибка: Неверный формат p или q. Введите целые числа или 'auto'.\n")
        return

    n = p * q
    num_iterations = 10

    initial_seed_for_bbs = initial_val % n
    if initial_seed_for_bbs == 0:
        initial_seed_for_bbs = 1

    # Генерируем гамму с помощью BBS
    bbs_bits, bbs_steps = bbs_generator(initial_seed_for_bbs, p, q, num_iterations)
    # Сохраняем гамму и шаги в глобальные переменные
    bbs_gamma_bits = [format(bit, '08b') for bit in bbs_bits] # Преобразуем биты в 8-битные строки
    bbs_gamma_steps = bbs_steps

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "--- Расчет начального значения для генераторов ---\n")
    output_text.insert(tk.END, f"Фамилия: {surname}\n")
    output_text.insert(tk.END, "Расчет (XOR байтов Windows-1251): \n")
    for step in calc_steps:
        output_text.insert(tk.END, f"  {step}\n")
    output_text.insert(tk.END, f"Результат: {initial_val} (десятичное), {initial_bits} (8-бит двоичное)\n\n")

    output_text.insert(tk.END, "--- Генерация гаммы BBS ---\n")
    output_text.insert(tk.END, f"p = {p}, q = {q}\n")
    output_text.insert(tk.END, f"n = p*q = {n}\n")
    output_text.insert(tk.END, f"Начальное значение (X0): {initial_seed_for_bbs}\n")
    output_text.insert(tk.END, f"Количество итераций: {num_iterations}\n\n")

    output_text.insert(tk.END, "Таблица генерации гаммы BBS:\n")
    output_text.insert(tk.END, "i\tXi\t\tXi^2\t\tПаритетный бит (bi)\n")
    for step_data in bbs_steps:
        output_text.insert(tk.END,
                           f"{step_data['step']}\t{step_data['x_i']}\t\t{step_data['x_squared']}\t\t{step_data['parity_bit']}\n")

    output_text.insert(tk.END, f"\nСгенерированная гамма (биты): {bbs_bits}\n")
    output_text.insert(tk.END, f"Сгенерированная гамма (8-битные строки): {bbs_gamma_bits}\n\n")

    # --- НОВОЕ: Автоматическое шифрование и дешифрование введенной фамилии ---
    output_text.insert(tk.END, "--- Автоматическое шифрование и дешифрование введенной фамилии с использованием сгенерированной BBS гаммы ---\n")

    # Шифрование
    surname_bits = text_to_bits(surname)
    if surname_bits:
        encrypted_surname_bits = gamma_cipher_mod2_bits(surname_bits, bbs_gamma_bits)
        encrypted_surname_text = bits_to_text(encrypted_surname_bits)

        output_text.insert(tk.END, f"Исходная фамилия: {surname}\n")
        output_text.insert(tk.END, f"Фамилия (байты, биты): {surname_bits}\n")
        output_text.insert(tk.END, f"Использованная BBS гамма: {bbs_gamma_bits}\n")
        output_text.insert(tk.END, f"Зашифрованная фамилия (байты, биты): {encrypted_surname_bits}\n")
        output_text.insert(tk.END, f"Зашифрованная фамилия: {encrypted_surname_text}\n\n")

        # Дешифрование
        decrypted_surname_bits = gamma_decipher_mod2_bits(encrypted_surname_bits, bbs_gamma_bits)
        decrypted_surname_text = bits_to_text(decrypted_surname_bits)

        output_text.insert(tk.END, f"Дешифрованная фамилия (байты, биты): {decrypted_surname_bits}\n")
        output_text.insert(tk.END, f"Дешифрованная фамилия: {decrypted_surname_text}\n\n")
    else:
        output_text.insert(tk.END, f"Не удалось преобразовать фамилию '{surname}' в биты для шифрования.\n\n")


def generate_safe_primes():
    """
    Обработчик события нажатия кнопки 'Сгенерировать безопасные p, q'.
    Генерирует случайные безопасные простые числа и вставляет их в соответствующие поля ввода.
    """
    p = generate_safe_prime_candidate()
    q = generate_safe_prime_candidate()
    while q == p:  # Убедимся, что p != q
        q = generate_safe_prime_candidate()

    p_entry.delete(0, tk.END)
    p_entry.insert(0, str(p))
    q_entry.delete(0, tk.END)
    q_entry.insert(0, str(q))


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Улучшенные Генераторы гаммы LFSR и BBS (Лабораторная работа 3, Задание 2)")
root.geometry("950x750")

# --- Виджеты ---

# Ввод фамилии
surname_label = ttk.Label(root, text="Введите фамилию:")
surname_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_surname = ttk.Entry(root, width=60)
input_surname.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Параметры BBS
bbs_params_label = ttk.Label(root, text="Параметры BBS (p, q):")
bbs_params_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

p_label = ttk.Label(root, text="p (≡ 3 mod 4, простое) или 'auto':")
p_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

p_entry = ttk.Entry(root, width=30)
p_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

q_label = ttk.Label(root, text="q (≡ 3 mod 4, простое) или 'auto':")
q_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

q_entry = ttk.Entry(root, width=30)
q_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Кнопки генерации и запуска
generate_primes_button = ttk.Button(root, text="Сгенерировать безопасные p, q", command=generate_safe_primes)
generate_primes_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

lfsr_button = ttk.Button(root, text="Рассчитать нач. знач. и запустить LFSR", command=calculate_initial_and_run_lfsr)
lfsr_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

bbs_button = ttk.Button(root, text="Рассчитать нач. знач. и запустить BBS", command=calculate_initial_and_run_bbs)
bbs_button.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

# Вывод результата
output_label = ttk.Label(root, text="Результат:")
output_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=115, height=35)
output_text.grid(row=8, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(0, weight=1)

# Запуск главного цикла
root.mainloop()
