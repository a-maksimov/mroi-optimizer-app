import streamlit as st
from streamlit_option_menu import option_menu


def menu(language_code=None):
    from translations import _  # import inside the function to avoid circular import
    selected = option_menu(
        menu_title=None,
        options=[_('About'), _('Specification'), _('Planning')],
        icons=['house', 'bar-chart-fill', 'graph-up'],
        menu_icon='cast',
        default_index=1,
        orientation='horizontal',
        key=language_code  # unique key to avoid DuplicateWidgetID error
    )
    return selected
