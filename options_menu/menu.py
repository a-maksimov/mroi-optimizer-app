from streamlit_option_menu import option_menu
from translations import _


def menu():
    """ Creates horizontal options menu and adds the key 'menu_tracker' to st.sessions_state. """
    # create placeholder for options menu to be able to delete it later
    options = [_('About'), _('Specification'), _('Planning'), _('Optimization')]
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=['question-circle', 'bar-chart-fill', 'graph-up', 'sliders'],
        menu_icon='cast',
        default_index=1,
        orientation='horizontal'
    )
    return selected
