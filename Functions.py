def check(num):
    """Функция проверяющая хранится ли
    в переменной num числовое целочисленное значение.
    Если в переменной храниться целочисленное, не отрицательное
    значение, то функция возвращает True. Иначе функиция возвращает False"""
    try:
        if isinstance(int(num), int) is True:
            return True
        return None
    except ValueError:
        return False