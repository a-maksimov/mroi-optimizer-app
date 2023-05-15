import streamlit as st
from streamlit_option_menu import option_menu
from translations import _


def menu():
    """
    Creates horizontal options menu and manually adds the key 'menu' to st.sessions_state.
    :return: selected option
    """
    options = [_('About'), _('Specification'), _('Planning')]
    if 'menu_tracker' not in st.session_state:
        st.session_state['menu_tracker'] = 1

    selected = option_menu(
        menu_title=None,
        options=options,
        icons=['house', 'bar-chart-fill', 'graph-up'],
        menu_icon='cast',
        default_index=st.session_state['menu_tracker'],
        orientation='horizontal',
    )
    st.session_state['menu_tracker'] = options.index(selected)
    return selected
