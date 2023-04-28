import gettext
import streamlit as st


def _(message):
    return translation.gettext(message)


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
