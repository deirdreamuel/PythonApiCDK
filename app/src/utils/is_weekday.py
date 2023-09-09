from datetime import date


def is_weekday(date: date):
    return date.weekday() < 5
