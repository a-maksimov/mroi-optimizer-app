import streamlit as st
from streamlit_option_menu import option_menu
from translations import _


def menu():
    """ Creates horizontal options menu and manually adds the key 'menu_tracker' to st.sessions_state. """
    # create placeholder for options menu to be able to delete it later
    menu_placeholder = st.empty()
    options = [_('About'), _('Specification'), _('Planning'), _('Optimization')]
    # initialize menu tracker
    if 'menu_tracker' not in st.session_state:
        st.session_state['menu_tracker'] = 1
    # delete options menu because it glitches
    else:
        menu_placeholder.empty()

    with menu_placeholder:
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=['question-circle', 'bar-chart-fill', 'graph-up', 'sliders'],
            menu_icon='cast',
            default_index=st.session_state['menu_tracker'],
            orientation='horizontal',
        )
    st.session_state['menu_tracker'] = options.index(selected)
    return selected
