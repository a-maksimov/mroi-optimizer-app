import streamlit as st
from streamlit_option_menu import option_menu
from translations import _


def menu():
    """ Creates horizontal options menu and manually adds the key 'menu_tracker' to st.sessions_state. """
    options = [_('About'), _('Specification'), _('Planning'), _('Optimization')]
    if 'menu_tracker' not in st.session_state:
        st.session_state['menu_tracker'] = 1

    selected = option_menu(
        menu_title=None,
        options=options,
        icons=['question-circle', 'bar-chart-fill', 'graph-up', 'sliders'],
        menu_icon='cast',
        default_index=1,
        orientation='horizontal',
    )
    st.session_state['menu_tracker'] = options.index(selected)
    return selected
