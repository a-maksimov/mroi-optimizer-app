from streamlit_option_menu import option_menu
from translations import _


def menu():
    selected = option_menu(
        menu_title=None,
        options=[_('About'), _('Specification'), _('Planning')],
        icons=['house', 'bar-chart-fill', 'graph-up'],
        menu_icon='cast',
        default_index=1,
        orientation='horizontal',
        key='menu'
    )
    return selected
