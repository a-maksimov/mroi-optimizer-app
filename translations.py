import streamlit as st
import gettext

languages = {'Русский': 'ru_RU'}

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


# update language
def set_language():
    global translation
    if st.session_state['language'] == 'Русский':
        translation = gettext.translation('messages', localedir='locales', languages=[languages['Русский']])
    else:
        translation = gettext.NullTranslations()
    # reload all translations
    translation.install()


# messages.po -o messages.mo
