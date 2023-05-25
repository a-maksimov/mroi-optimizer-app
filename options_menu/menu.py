import streamlit as st
from streamlit_option_menu import option_menu
from translations import _


def create_menu(options, index=1, key='menu'):
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=['question-circle', 'bar-chart-fill', 'graph-up', 'sliders'],
        menu_icon='cast',
        default_index=index,
        orientation='horizontal',
        key=key
    )
    return selected


def menu():
    """ Creates horizontal menu. """
    options = [_('About'), _('Specification'), _('Planning'), _('Optimization')]
    # create placeholder for options menu to be able to delete it later
    menu_placeholder = st.empty()
    with menu_placeholder:
        selected = create_menu(options=options)
    # recreate options menu because of UI glitch
    # https://github.com/victoryhb/streamlit-option-menu/issues/27
    del st.session_state['menu']
    menu_placeholder.empty()

    selected = create_menu(options=options, index=options.index(selected), key='new_menu')

    return selected
