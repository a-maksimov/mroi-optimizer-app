import streamlit as st
import pandas as pd
import gettext

languages = {'Русский': 'ru_RU', 'English': 'en_US'}

translation = gettext.translation('messages', localedir='locales', languages=[languages['Русский']])

reverse_dict = {}


# function to translate strings
def _(message, get_original=False):
    global reverse_dict

    # reverse translation
    if get_original:
        return reverse_dict.get(message, message)

    # get translated string
    translated_message = translation.gettext(message)

    # create dictionary for reverse translation
    if translated_message not in reverse_dict:
        reverse_dict[translated_message] = message

    return translated_message


def translate_table(dataframe, get_original=False):
    """ Translate columns and values in text columns of a dataframe"""
    # select string columns
    string_dtypes = dataframe.head(1).convert_dtypes().select_dtypes('string')
    # translate values of string columns for filtering and display
    dataframe[string_dtypes.columns] = dataframe[string_dtypes.columns].applymap(lambda value: _(value, get_original=get_original))

    # translate columns names for filtering and display
    columns_translate = {column: _(column, get_original=get_original) for column in dataframe.columns}
    return dataframe.rename(columns=columns_translate)


def translate_nest(value, get_original=False):
    """ Recursively apply a translation function to all values in the nested collection """
    if isinstance(value, dict):
        return {k: translate_nest(v, get_original=get_original)
                for k, v in value.items()}
    elif isinstance(value, pd.DataFrame):
        return translate_table(value, get_original=get_original)
    elif isinstance(value, list):
        return [translate_nest(elem, get_original=get_original) for elem in value]
    elif isinstance(value, str):
        return _(value, get_original=get_original)
    else:
        return value


# update language
def set_language():
    global translation
    # initialize language tracking
    # set default value to False and switch between True and False
    st.session_state['language_switch'] = not st.session_state.get('language_switch')
    # if switched back to Russian
    if not st.session_state['language_switch']:
        translation = gettext.translation('messages', localedir='locales', languages=[languages['Русский']])
        # translate values in session state
        st.session_state = {key: translate_nest(value) for key, value in st.session_state.items()}
    # if switched to English
    else:
        # translate values in session state
        translation = gettext.NullTranslations()
        # translate values in session state
        st.session_state = {key: translate_nest(value, get_original=True) for key, value in st.session_state.items()}
    # reload all translations
    translation.install()

# msgfmt messages.po -o messages.mo
