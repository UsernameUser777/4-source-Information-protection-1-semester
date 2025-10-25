# Программа для шифрования фамилии методом системы омофонов
# Используется русский алфавит
# Для каждой буквы алфавита определяется по два омофона (шифрозамены)
# Шифрование: каждая буква исходного сообщения заменяется на один из её омофонов (например, первый, второй, поочередно или случайно)

# Запрашиваем у пользователя фамилию
surname = input("Введите вашу фамилию: ").strip()

# Определяем русский алфавит
# Включает все буквы от 'А' до 'Я', включая 'Ё'
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# Функция для создания таблицы омофонов
def create_omophonic_table(original_alphabet, num_homophones_per_letter=2):
    """
    Создает таблицу омофонов, где каждой букве алфавита соответствует список из num_homophones_per_letter шифрозамен.

    :param original_alphabet: Оригинальный алфавит (строка).
    :param num_homophones_per_letter: Количество омофонов для каждой буквы (int).
    :return: Таблица омофонов (словарь, где ключ - буква, значение - список омофонов).
    """
    # Импортируем модуль random для случайного выбора омофона
    import random

    # Инициализируем словарь для хранения таблицы омофонов
    homophonic_table = {}

    # Общий список возможных символов для омофонов
    # Можно использовать числа, буквы другого алфавита, специальные символы
    # В учебнике (стр. 40) в Таблице 3.8 используются числа (например, 311, 128, 175... для 'А')
    # Для простоты будем использовать числа от 100 до 999
    # Генерируем список всех возможных омофонов
    # Всего букв в алфавите * num_homophones_per_letter
    total_omophones_needed = len(original_alphabet) * num_homophones_per_letter

    # Проверяем, достаточно ли уникальных чисел
    # У нас 900 чисел от 100 до 999, для 33 букв * 2 = 66 омофонов - более чем достаточно
    all_possible_omophones = list(range(100, 1000))

    # Перемешиваем список, чтобы получить "случайные" омофоны
    random.shuffle(all_possible_omophones)

    # Выбираем нужное количество уникальных омофонов
    selected_omophones = all_possible_omophones[:total_omophones_needed]

    # Распределяем выбранные омофоны по буквам алфавита
    index = 0
    for letter in original_alphabet:
        # Создаем список омофонов для текущей буквы
        letter_omophones = []
        for _ in range(num_homophones_per_letter):
            # Добавляем очередной омофон из перемешанного списка
            letter_omophones.append(selected_omophones[index])
            index += 1
        # Сохраняем список омофонов для буквы в словаре
        homophonic_table[letter] = letter_omophones

    # Возвращаем готовую таблицу омофонов
    return homophonic_table


# Функция для шифрования строки с помощью системы омофонов
def omophonic_cipher(text, homophonic_table, use_random=False):
    """
    Шифрует текст с помощью системы омофонов.

    :param text: Исходный текст для шифрования (строка).
    :param homophonic_table: Таблица омофонов (словарь).
    :param use_random: Использовать ли случайный выбор омофона (bool).
                       Если False, чередует первый и второй омофон.
    :return: Зашифрованный текст (строка, омофоны, разделенные пробелом).
    """
    # Импортируем модуль random, если будем использовать случайный выбор
    import random

    # Преобразуем входной текст в верхний регистр
    text_upper = text.upper()

    # Инициализируем строку для хранения результата
    encrypted_text_parts = []

    # Счетчик для чередования омофонов, если use_random=False
    cycle_counter = 0

    # Проходим по каждой букве в тексте
    for char in text_upper:
        # Проверяем, находится ли символ в таблице омофонов
        if char in homophonic_table:
            # Получаем список омофонов для текущей буквы
            available_omophones = homophonic_table[char]

            # Выбираем омофон
            selected_omoph = None
            if use_random:
                # Если use_random=True, выбираем случайный омофон из доступных
                selected_omoph = random.choice(available_omophones)
            else:
                # Если use_random=False, чередуем омофоны (0, 1, 0, 1, ...)
                # Используем остаток от деления счетчика на количество омофонов (2)
                selected_omoph = available_omophones[cycle_counter % len(available_omophones)]
                # Увеличиваем счетчик для следующей буквы
                cycle_counter += 1

            # Добавляем выбранный омофон к результату
            encrypted_text_parts.append(str(selected_omoph))
        else:
            # Если символ не найден в таблице (например, пробел или знак препинания),
            # его можно пропустить или обработать особым образом.
            # В данном случае, мы просто пропускаем его.
            # print(f"Символ '{char}' не найден в таблице омофонов и будет пропущен.")
            pass  # Пропускаем символ

    # Соединяем все омофоны в одну строку, разделяя пробелом
    # Это делает шифрограмму более читаемой
    encrypted_text = " ".join(encrypted_text_parts)

    # Возвращаем зашифрованный текст
    return encrypted_text


# Создаем таблицу омофонов (по 2 на букву)
homophonic_table = create_omophonic_table(alphabet, 2)

# Запрашиваем у пользователя, использовать ли случайный выбор омофона
use_random_input = input("Использовать случайный выбор омофона? (y/n): ").lower().strip()
use_random = use_random_input == 'y'

# Вызываем функцию шифрования с нашими параметрами
encrypted_surname = omophonic_cipher(surname, homophonic_table, use_random)

# Выводим результаты
print(f"Исходное сообщение: {surname}")
print(f"Оригинальный алфавит: {alphabet}")
print("Таблица шифрозамен (омофонов):")
for letter, omophones in homophonic_table.items():
    print(f"  '{letter}': {omophones}")
print(f"Зашифрованное сообщение (омофоны, разделенные пробелами): {encrypted_surname}")
