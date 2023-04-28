import gettext


def _(message):
    return translation.gettext(message)


translation = gettext.translation('messages', localedir='locales', languages=['ru_RU'])


# update language
def set_language(language_code):
    global translation
    if language_code == 'ru_RU':
        translation = gettext.translation('messages', localedir='locales', languages=[language_code])
    else:
        translation = gettext.NullTranslations()
    # reload all translations
    translation.install()



