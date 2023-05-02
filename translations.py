import gettext
import streamlit as st

reverse_dict = {}


# function to translate strings overloaded for backwards translation
def _(message, get_original=False):
    global reverse_dict

    if get_original:
        return reverse_dict.get(message, message)

    translated_message = translation.gettext(message)
    reverse_dict[translated_message] = message
    return translated_message


translation = gettext.translation('messages', localedir='locales', languages=['ru_RU'])


# update language
def set_language():
    global translation
    if st.session_state['language'] == 'Русский':
        translation = gettext.translation('messages', localedir='locales', languages=['ru_RU'])
    else:
        translation = gettext.NullTranslations()
    # reload all translations
    translation.install()

# messages.po -o messages.mo
