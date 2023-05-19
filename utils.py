import re
from translations import _


def display_currency(value, currency='€'):
    if value >= 1e5:
        return f'{currency} {round(value / 1e6, 2)} {_("M")}'
    else:
        return f'{currency} {round(value, 2)}'


def display_volume(value):
    if value >= 1e5:
        return f'{round(value / 1e3)} {_("k")} {_("kg")}'
    else:
        return f'{round(value)} {_("kg")}'


def display_percent(old_value, new_value):
    return f'{round(((new_value - old_value) / old_value) * 100, 2)}%'


def validate_currency_input(input_text):
    # remove any non-numeric characters except decimal point
    cleaned_input = re.sub(r'[^0-9.]', '', input_text)
    # convert the input to float
    try:
        value = float(cleaned_input)
    except ValueError:
        return None

    return value
