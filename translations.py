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


def translate_nest(value, get_original=False):
    """
    Recursively apply a function to all values in the nested collection
    """
    if isinstance(value, dict):
        return {translate_nest(k, get_original=get_original): translate_nest(v, get_original=get_original)
                for k, v in value.items()}
    elif isinstance(value, list):
        return [translate_nest(elem, get_original=get_original) for elem in value]
    else:
        return _(value, get_original=get_original)


# update language
def set_language():
    global translation
    # initiate or updated language switch counter
    st.session_state['language_switch_counter'] = st.session_state.get('language_switch_counter', 0) + 1
    if st.session_state['language_switch_counter'] % 2 == 0:
        translation = gettext.translation('messages', localedir='locales', languages=[languages['Русский']])
        # translate values in session state
        st.session_state = {key: translate_nest(value) for key, value in st.session_state.items()}
    else:
        # translate values in session state
        translation = gettext.NullTranslations()
        # translate values in session state
        st.session_state = {key: translate_nest(value, get_original=True) for key, value in st.session_state.items()}
    # reload all translations
    translation.install()

# messages.po -o messages.mo
