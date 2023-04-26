from streamlit_option_menu import option_menu


def menu():
    selected = option_menu(
        menu_title=None,  # required
        options=['О приложении', 'Спецификация', 'Планирование'],  # required
        icons=['house', 'bar-chart-fill', 'graph-up'],  # optional
        menu_icon='cast',  # optional
        default_index=1,  # optional
        orientation='horizontal'
    )
    return selected
