from datetime import datetime


def validate_date(date_str):
    '''Функция валидации даты'''
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        return None