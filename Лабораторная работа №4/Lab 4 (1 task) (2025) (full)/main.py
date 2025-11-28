# Импортируем необходимые библиотеки для создания графического интерфейса
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
# Импортируем библиотеки для работы с числами и генерации случайных значений
import random
import math

# --- Константы ---
# Определяем русский алфавит (для кодирования по позиции)
# Включает все буквы от 'А' до 'Я', включая 'Ё'
RU_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# --- Вспомогательные математические функции для RSA ---

def gcd_extended(a, b):
    """
    Расширенный алгоритм Евклида.
    Находит наибольший общий делитель (gcd) чисел a и b,
    а также коэффициенты x и y такие, что a*x + b*y = gcd(a, b).
    Эта функция критически важна для вычисления мультипликативного обратного числа (d),
    которое используется в секретном ключе RSA.

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

def mod_inverse(e, phi):
    """
    Вычисляет мультипликативное обратное e по модулю phi.
    Использует расширенный алгоритм Евклида.
    d - это секретный ключ, такой что (e * d) % phi = 1.
    Это необходимо для вычисления секретного ключа d в RSA.

    :param e: Открытая экспонента (часть открытого ключа).
    :param phi: Значение функции Эйлера (p-1)*(q-1).
    :return: d - секретный ключ (целое число) или None, если обратное не существует
             (например, если e и phi не взаимно просты).
    """
    # Вызываем расширенный алгоритм Евклида для e и phi
    gcd, x, y = gcd_extended(e, phi)
    # Проверяем, являются ли e и phi взаимно простыми (gcd должен быть 1)
    if gcd != 1:
        # Если gcd != 1, обратное число не существует
        # print(f"Ошибка: e={e} и phi={phi} не взаимно просты, невозможно найти d.")
        return None
    # x может быть отрицательным, приведем к положительному по модулю phi
    # Это делается с помощью операции % phi
    d = x % phi
    # Возвращаем вычисленное значение d
    return d

def is_prime(n):
    """
    Проверяет, является ли число n простым методом пробного деления.
    Используется для генерации простых чисел p и q, которые являются
    основой для создания ключей в RSA.

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

    :param length: Битовая длина числа (например, 8 означает число от 128 до 255).
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

def generate_prime_number(length=8):
    """
    Генерирует простое число заданной битовой длины.
    Повторяет генерацию кандидата и проверку на простоту до тех пор,
    пока не будет найдено простое число.

    :param length: Битовая длина простого числа (по умолчанию 8 для простоты).
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

# --- Основные функции RSA ---

def generate_keys():
    """
    Генерирует пару открытого и закрытого ключей RSA.
    Выбирает два случайных простых числа p и q,
    вычисляет n и phi(n), выбирает e, вычисляет d.

    :return: Кортеж ((e, n) - открытый ключ, (d, n) - закрытый ключ, p, q)
             или (None, None, None, None) при ошибке.
    """
    # Генерируем два разных простых числа p и q.
    # Для демонстрации используем небольшую битовую длину (8 бит).
    # В реальных системах используются намного большие числа (1024, 2048, 4096 бит).
    p = generate_prime_number(8)
    q = generate_prime_number(8)
    # Убедимся, что p != q, генерируя q заново при необходимости
    while p == q:
        q = generate_prime_number(8)

    # Вычисляем n = p * q. Это первая часть и открытого, и закрытого ключа.
    n = p * q

    # Вычисляем phi = (p - 1) * (q - 1). Это значение функции Эйлера.
    phi = (p - 1) * (q - 1)

    # Выберем e. Обычно используется 65537, но для простых чисел подойдет и 3, 17, 257.
    # e должно удовлетворять условиям: 1 < e < phi и gcd(e, phi) = 1 (взаимно просты)
    e = 3
    # Цикл для поиска подходящего e
    while True:
        if math.gcd(e, phi) == 1: # Проверяем, что e и phi взаимно просты
            break
        e += 2 # Пробуем следующее нечетное число
        if e >= phi: # На всякий случай, если e станет слишком большим
            # print("Ошибка: Не удалось подобрать e.")
            return None, None, None, None

    # Вычисляем d - мультипликативное обратное к e по модулю phi
    # d удовлетворяет уравнению (e * d) % phi = 1
    d = mod_inverse(e, phi)
    if d is None:
        # print("Ошибка: Не удалось вычислить d.")
        return None, None, None, None

    # Формируем открытый и закрытый ключи
    public_key = (e, n)
    private_key = (d, n)
    # Возвращаем также p и q для отладки/демонстрации
    return public_key, private_key, p, q

def encrypt_rsa(message, public_key):
    """
    Шифрует сообщение, представленное как список чисел (кодов символов),
    с помощью открытого ключа RSA.

    :param message: Список целых чисел, представляющих символы (например, по позиции в алфавите).
    :param public_key: Кортеж (e, n).
    :return: Список зашифрованных чисел (шифротекст) или None при ошибке.
    """
    # Распаковываем открытый ключ
    e, n = public_key
    # Инициализируем список для хранения зашифрованных чисел
    encrypted_msg = []
    # Проходим по каждому числу (символу) в сообщении
    for num in message:
        # Проверяем, что число (символ) меньше n, иначе RSA не работает корректно
        if num >= n:
            # print(f"Ошибка: Значение символа {num} >= n ({n}). Выберите большие p и q.")
            return None
        # Шифрование: c = m^e mod n
        # Используем встроенную функцию pow(base, exp, mod) для эффективного вычисления
        encrypted_num = pow(num, e, n)
        # Добавляем зашифрованное число в результат
        encrypted_msg.append(encrypted_num)
    # Возвращаем список зашифрованных чисел
    return encrypted_msg

def decrypt_rsa(encrypted_message, private_key):
    """
    Дешифрует сообщение, представленное как список зашифрованных чисел,
    с помощью закрытого ключа RSA.

    :param encrypted_message: Список зашифрованных целых чисел.
    :param private_key: Кортеж (d, n).
    :return: Список дешифрованных целых чисел (исходные коды символов).
    """
    # Распаковываем закрытый ключ
    d, n = private_key
    # Инициализируем список для хранения дешифрованных чисел
    decrypted_msg = []
    # Проходим по каждому зашифрованному числу
    for enc_num in encrypted_message:
        # Дешифрование: m = c^d mod n
        # Используем встроенную функцию pow(base, exp, mod) для эффективного вычисления
        decrypted_num = pow(enc_num, d, n)
        # Добавляем дешифрованное число в результат
        decrypted_msg.append(decrypted_num)
    # Возвращаем список дешифрованных чисел
    return decrypted_msg

# --- Функции преобразования данных между текстом и числами ---
# Используются для подготовки текста к шифрованию и восстановления после дешифрования

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
current_p = None
current_q = None

# --- Функции для обработки действий пользователя в GUI ---

def generate_keys_action():
    """
    Обработчик кнопки 'Сгенерировать ключи'.
    Вызывает функцию генерации ключей и отображает результаты в интерфейсе.
    """
    global current_public_key, current_private_key, current_p, current_q
    try:
        # Вызываем основную функцию генерации ключей
        pub_key, priv_key, p, q = generate_keys()
        # Проверяем, успешно ли сгенерированы ключи
        if pub_key is None or priv_key is None:
            # Если нет, показываем сообщение об ошибке
            messagebox.showerror("Ошибка", "Не удалось сгенерировать ключи. Попробуйте снова.")
            return

        # Сохраняем сгенерированные ключи и параметры в глобальные переменные
        current_public_key = pub_key
        current_private_key = priv_key
        current_p = p
        current_q = q

        # Очищаем поле вывода и записываем информацию о сгенерированных ключах
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Сгенерированные параметры RSA ---\n")
        output_text.insert(tk.END, f"p (первое простое число): {p}\n")
        output_text.insert(tk.END, f"q (второе простое число): {q}\n")
        output_text.insert(tk.END, f"n (p*q): {pub_key[1]}\n")
        output_text.insert(tk.END, f"phi(n) ((p-1)*(q-1)): {(p-1)*(q-1)}\n")
        output_text.insert(tk.END, f"Открытый ключ (e, n): {pub_key}\n")
        output_text.insert(tk.END, f"Закрытый ключ (d, n): ({priv_key[0]}, {priv_key[1]})\n")
        output_text.insert(tk.END, f"--- Ключи готовы к использованию ---\n\n")
    except Exception as e:
        # Обрабатываем любые непредвиденные ошибки
        messagebox.showerror("Ошибка", f"Произошла ошибка при генерации ключей: {e}")

def encrypt_action():
    """
    Обработчик кнопки 'Зашифровать'.
    Получает текст из поля ввода, преобразует его в числа, шифрует,
    и выводит результат в поле вывода.
    """
    global current_public_key
    # Проверяем, сгенерированы ли ключи
    if current_public_key is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем текст из поля ввода
    text = input_text.get().strip()
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
        encrypted_numbers = encrypt_rsa(numbers, current_public_key)
        # Проверяем, успешно ли прошло шифрование (например, если символ > n)
        if encrypted_numbers is None:
            messagebox.showerror("Ошибка", f"Значение символа в тексте превышает допустимое n={current_public_key[1]}. Попробуйте снова.")
            return

        # 3. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат шифрования RSA ---\n")
        output_text.insert(tk.END, f"Исходное сообщение: {text}\n")
        output_text.insert(tk.END, f"Коды символов (по алфавиту): {numbers}\n")
        output_text.insert(tk.END, f"Открытый ключ (e, n): {current_public_key}\n")
        output_text.insert(tk.END, f"Зашифрованные числа: {encrypted_numbers}\n")
        # Конвертируем числа в строку для удобства отображения
        encrypted_str = ' '.join(map(str, encrypted_numbers))
        output_text.insert(tk.END, f"Зашифрованное сообщение (строка чисел): {encrypted_str}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"p: {current_p}, q: {current_q}\n")
        output_text.insert(tk.END, f"n: {current_public_key[1]}, phi(n): {(current_p-1)*(current_q-1)}\n")
        output_text.insert(tk.END, f"e: {current_public_key[0]}\n")

    except Exception as e:
        # Обрабатываем любые ошибки, возникшие в процессе шифрования
        messagebox.showerror("Ошибка", f"Произошла ошибка при шифровании: {e}")

def decrypt_action():
    """
    Обработчик кнопки 'Дешифровать'.
    Получает зашифрованные числа из поля ввода, дешифрует их,
    преобразует обратно в текст и выводит результат.
    """
    global current_private_key
    # Проверяем, сгенерированы ли ключи
    if current_private_key is None:
        messagebox.showwarning("Предупреждение", "Сначала сгенерируйте ключи.")
        return

    # Получаем строку зашифрованных чисел из поля ввода
    encrypted_str = input_text.get().strip()
    if not encrypted_str:
        messagebox.showwarning("Предупреждение", "Введите зашифрованные числа для дешифрования.")
        return

    try:
        # 1. Преобразуем строку чисел, разделенных пробелами, в список целых чисел
        encrypted_numbers = list(map(int, encrypted_str.split()))

        # 2. Дешифруем числа, используя закрытый ключ
        decrypted_numbers = decrypt_rsa(encrypted_numbers, current_private_key)

        # 3. Преобразуем дешифрованные числа обратно в текст
        decrypted_text = numbers_to_text(decrypted_numbers, RU_ALPHABET)

        # 4. Формируем и выводим результат в поле вывода
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"--- Результат дешифрования RSA ---\n")
        output_text.insert(tk.END, f"Зашифрованные числа (введите строку): {encrypted_str}\n")
        output_text.insert(tk.END, f"Зашифрованные числа (список): {encrypted_numbers}\n")
        output_text.insert(tk.END, f"Закрытый ключ (d, n): {current_private_key}\n")
        output_text.insert(tk.END, f"Дешифрованные коды: {decrypted_numbers}\n")
        output_text.insert(tk.END, f"Дешифрованное сообщение: {decrypted_text}\n\n")
        output_text.insert(tk.END, f"--- Параметры ключей ---\n")
        output_text.insert(tk.END, f"p: {current_p}, q: {current_q}\n")
        output_text.insert(tk.END, f"n: {current_private_key[1]}, phi(n): {(current_p-1)*(current_q-1)}\n")
        output_text.insert(tk.END, f"d: {current_private_key[0]}\n")

    except ValueError:
        # Обрабатываем ошибку, если введенные данные не являются числами
        messagebox.showerror("Ошибка", "Неверный формат ввода. Введите числа, разделенные пробелом.")
    except Exception as e:
        # Обрабатываем любые другие ошибки, возникшие в процессе дешифрования
        messagebox.showerror("Ошибка", f"Произошла ошибка при дешифровании: {e}")


# --- Создание графического интерфейса ---
# Инициализируем главное окно приложения
root = tk.Tk()
root.title("Лабораторная работа 4 - RSA")
root.geometry("700x500") # Устанавливаем начальный размер окна

# --- Создание виджетов (элементов интерфейса) ---

# Метка и поле для ввода текста
input_label = ttk.Label(root, text="Введите текст (для шифрования) или числа (для дешифрования):")
input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

input_text = ttk.Entry(root, width=70)
input_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)

# Кнопки для взаимодействия с программой
generate_button = ttk.Button(root, text="Сгенерировать ключи", command=generate_keys_action)
generate_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

encrypt_button = ttk.Button(root, text="Зашифровать (Текст -> Числа)", command=encrypt_action)
encrypt_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

decrypt_button = ttk.Button(root, text="Дешифровать (Числа -> Текст)", command=decrypt_action)
decrypt_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Метка и поле для вывода результата
output_label = ttk.Label(root, text="Результат и информация о ключах:")
output_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.grid(row=5, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

# --- Настройка сетки ---
# Позволяет элементам интерфейса адаптироваться при изменении размера окна
root.grid_rowconfigure(5, weight=1) # Ряд с полем вывода растягивается по вертикали
root.grid_columnconfigure(0, weight=1) # Колонка с полями ввода и кнопками растягивается по горизонтали

# Запуск главного цикла обработки событий Tkinter
root.mainloop()
