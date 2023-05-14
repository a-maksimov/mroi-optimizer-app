import streamlit as st
from streamlit_option_menu import option_menu
from translations import _


def menu():
    """
    Creates horizontal options menu and manually adds the key 'menu' to to st.sessions_state.
    :return: selected option
    """
    options = [_('About'), _('Specification'), _('Planning')]
    if 'menu' in st.session_state:
        default = options.index(_(st.session_state['menu']))
    else:
        default = 1
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=['house', 'bar-chart-fill', 'graph-up'],
        menu_icon='cast',
        default_index=default,
        orientation='horizontal'
    )
    st.session_state['menu'] = selected
    return selected
