import streamlit as st
import re
from translations import _


def display_currency(value, currency='€'):
    if value >= 1000000:
        return f'{currency} {round(value / 1e6, 2)} {_("M")}'
    elif 100000 <= value <= 999999:
        return f'{currency} {round(value / 1e3, 2)} {_("k")}'
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


def flip_checkbox_track(key):
    """ Callback function that is called on sidebar checkboxes change and tracks its values in between re-rendering """
    key_checkbox_track = key + '_track'
    # flip the checkbox tracked value
    st.session_state['tracking'][key_checkbox_track] = not st.session_state['tracking'][key_checkbox_track]


def create_checkbox(key):
    """ Create Percents checkbox """
    # initialize checkbox value tracking
    key_checkbox_track = key + '_track'
    if key_checkbox_track not in st.session_state['tracking']:
        st.session_state['tracking'][key_checkbox_track] = False

    # create percents checkbox
    st.checkbox(_('Percents'),
                value=st.session_state['tracking'][key_checkbox_track],
                key=key,
                on_change=flip_checkbox_track,
                args=(key,))


def parse_input(input_text):
    """ Parse and validate input text """
    # replacement of possible phrases to allowed
    possible_phrases_of_m = ['mln', 'mil', 'млн', 'млн.', 'м', 'М', 'kk']
    possible_phrases_of_k = ['тыс', 'тыс.', 'к', 'К']

    for char in possible_phrases_of_m:
        input_text = input_text.replace(char, 'm')

    for char in possible_phrases_of_k:
        input_text = input_text.replace(char, 'k')

    input_text = input_text.replace(" ", '')
    input_text = input_text.replace(',', '.')

    # allowed chars check
    allowed_phrases = set('0123456789mMKk.')
    if not set(input_text).issubset(allowed_phrases):
        st.error(_("Error: Invalid character."))
        return 0

    # extraction of number and suffix
    number = ''
    suffix = ''
    for char in input_text:
        if char.isdigit() or char == '.':
            number += char
        elif char.lower() == 'k' or char.lower() == 'm':
            suffix += char.lower()

    # check if number exist
    if not number:
        st.error(_('Error: Enter a number.'))
        return 0

    # float number transformation
    try:
        amount = float(number)
    except ValueError:
        st.error(_('Error: Invalid number.'))
        return 0

    # transformation suffix to multiplier
    multiplier = 1
    if 'k' in suffix:
        multiplier *= 1e3 ** suffix.count('k')
    if 'm' in suffix:
        multiplier *= 1e6 ** suffix.count('m')

    # calculation
    euro_amount = amount * multiplier

    return euro_amount
