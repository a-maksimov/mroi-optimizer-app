import streamlit as st
import read_data
from translations import _
import utils
from options_menu.optimization_tabs import tab_table, tab_plotting
from options_menu.planning import plan_input
import solvers


def handle_goal_input():
    """
    Callback for planned budget input text widget
    Validates input on the edit of field and if correct, saves new value to the session state
    """
    parsed_input_contribution = utils.parse_input(st.session_state['target_contribution'])

    if 'display_target_contribution' in st.session_state['tracking']:
        st.session_state['tracking']['display_target_contribution'] = parsed_input_contribution

    # reset optimization by deleting the optimized dataframe from session state
    if 'df_optimized' in st.session_state['tracking']:
        del st.session_state['tracking']['df_optimized']


def goal_input():
    """
    Input for target contribution for goal based optimization.
    """
    # 'display target contribution' is initialized in calculate_opt
    input_goal = st.session_state['tracking']['display_target_contribution']
    input_goal = '{:.2f}'.format(input_goal)

    st.text_input(f'{_("Enter target contribution")}, {_("kg")}',
                  value=input_goal,
                  key='target_contribution',
                  on_change=handle_goal_input)

    input_goal = float(input_goal)

    if input_goal > st.session_state['tracking']['display_target_contribution'] * 2:
        st.error(_('Error: Number too large.'))
        return 0

    return input_goal


def reset_optimization():
    """ Resets optimization """
    if 'df_optimized' in st.session_state['tracking']:
        del st.session_state['tracking']['df_optimized']
    if 'spend_optimized_track' in st.session_state['tracking']:
        st.session_state['tracking']['spend_optimized'] = False
    if 'goal_optimized_track' in st.session_state['tracking']:
        st.session_state['tracking']['goal_optimized'] = False


def optimize(dataframe, optimization_type, goal):
    """ Run Spend based optimization and save optimized dataframe to session state """
    # reset any optimization done before and set both optimization tracks to False
    reset_optimization()
    if optimization_type == 'spend':
        st.session_state['tracking']['spend_optimized_track'] = True
        st.session_state['tracking']['goal_optimized_track'] = False
    else:
        st.session_state['tracking']['spend_optimized_track'] = False
        st.session_state['tracking']['goal_optimized_track'] = True
    # store optimized dataframe and the result of optimization convergence (boolean)
    with st.spinner(f'{_("Optimizing")}...'):
        df_optimized, success = solvers.nlopt_ld_mma(dataframe, optimization_type, goal)
    st.session_state['tracking']['df_optimized'] = df_optimized
    st.session_state['tracking']['success'] = success


def optimize_button(dataframe, scenario, goal, key):
    """ Creates button that initializes the optimization """
    # disable if no granularity has been selected in the sidebar
    selection_dict = st.session_state['tracking']['selection_dict']
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    if scenario == _('Spend based optimization'):
        optimization_type = 'spend'
    else:
        optimization_type = 'goal'
    # initialize optimization on button click
    st.button(_('Optimize'),
              key=key,
              disabled=not any(value for key, value in selection_dict.items() if key in granularity_levels),
              on_click=optimize, args=(dataframe, optimization_type, goal))


def update_boundary(variable, slider_key, boundary):
    """
    Callback on change of upper/lower boundary slider.
    Saves the value of the boundary in between re-renders.
    """
    st.session_state['tracking']['slider_values'][variable][boundary] = st.session_state[slider_key]


# TODO: Show warning when boundaries set outside +/- 30% of current spends.
def create_slider(variable, label, key, boundary, value=0, min_value=0, max_value=50):
    """
    Create Lower bound and Upper bound sliders.
    On slider change the function update_boundary() is called.
    """
    return st.slider(label,
                     value=value,
                     key=key,
                     min_value=min_value,
                     max_value=max_value,
                     on_change=update_boundary,
                     args=(variable, key, boundary))


def select_scenario():
    """ Callback function for select optimization scenario """
    st.session_state['tracking']['select_scenario_track'] = st.session_state['select_scenario']


def render_select_scenario():
    # optimization scenario select UI
    # set the default value after re-render of widget
    # 'select_scenario' value changes after set_scenario() callback
    scenarios = [_('Spend based optimization'), _('Goal based optimization')]
    if 'select_scenario_track' not in st.session_state['tracking']:
        st.session_state['tracking']['select_scenario_track'] = scenarios[0]
    # set up the translation selection
    return st.selectbox(_('Select optimization scenario'),
                        index=scenarios.index(st.session_state['tracking']['select_scenario_track']),
                        options=scenarios,
                        key='select_scenario',
                        on_change=select_scenario)


def select_boundary_variable():
    """ Callback function for select variable for boundary setting """
    variable = st.session_state['select_boundary_variable']
    st.session_state['tracking']['select_boundary_variable_track'] = variable


def render_select_variable():
    # variable select for boundaries setting UI
    # disable if no granularity has been selected in the sidebar
    selection_dict = st.session_state['tracking']['selection_dict']
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    # check if user has selected any granularity in sidebar
    # iterate backwards through the granularity levels and use the first one that is not empty
    for level in reversed(granularity_levels):
        if selection_dict[level]:
            granularity_options = selection_dict[level]
            break
    # the else block will NOT be executed if the loop is stopped by a break statement
    else:
        granularity_options = []

    variables = [_('Total Spend')] + granularity_options

    for variable in variables:
        if variable not in st.session_state['tracking']['slider_values']:
            st.session_state['tracking']['slider_values'][variable] = {'lower': -20, 'upper': 20}

    if 'select_boundary_variable_track' not in st.session_state['tracking']:
        st.session_state['tracking']['select_boundary_variable_track'] = variables[0]
    # set up the translation selection
    return st.selectbox(_('Select variable for spend boundaries setting'),
                        index=variables.index(st.session_state['tracking']['select_boundary_variable_track']),
                        options=variables,
                        key='select_boundary_variable',
                        on_change=select_boundary_variable,
                        disabled=not any(value for key, value in selection_dict.items() if key in granularity_levels))


# TODO: Add reset button and/or selects to fallback to Planned budget and/or Specification budget.
#  Now everything resets by user manipulations with sidebar
def opt_page(dataframe):
    """ Renders the Optimization page based on the Planning page """
    optimize_col, input_col, sliders_col, success_col = st.columns(4)

    with optimize_col:
        # display select optimization scenario
        scenario = render_select_scenario()
        optimize_button_placeholder = st.empty()

    with input_col:
        if scenario == _('Spend based optimization'):
            # display simulated budget input widget
            goal = plan_input()
        else:
            # display simulated budget input widget
            goal = goal_input()

        # display variable selection widget for setting boundaries
        selected_variable = render_select_variable()

    # create placeholder for messages
    with success_col:
        success_placeholder = st.empty()

    planned_budget = st.session_state['tracking']['display_planned_budget']

    with optimize_button_placeholder:
        # create optimize button
        optimize_button(dataframe, scenario, goal, key='optimization_button')

    with sliders_col:
        # get boundaries for selected variable
        lower_bound = st.session_state['tracking']['slider_values'][selected_variable]['lower']
        upper_bound = st.session_state['tracking']['slider_values'][selected_variable]['upper']

        # display boundary sliders
        create_slider(selected_variable,
                      label=f'{_("Allowed decrease in spends")} {_("for variable")} {selected_variable}, %',
                      value=lower_bound,
                      boundary='lower',
                      min_value=-50,
                      max_value=0,
                      key=selected_variable + '_lower_bound_slider')

        create_slider(selected_variable,
                      label=f'{_("Allowed increase in spends")} {_("for variable")} {selected_variable}, %',
                      value=upper_bound,
                      boundary='upper',
                      min_value=0,
                      max_value=50,
                      key=selected_variable + '_upper_bound_slider')

    # display simulated top metrics
    left_column, middle_column1, middle_column2, right_column = st.columns(4)

    # access simulated top metrics calculated and saved in the session state by simulated_top_metrics() function
    # call inside calculate_plan
    simulated_total_contribution = st.session_state['tracking']['simulated_contribution']
    simulated_total_revenue = st.session_state['tracking']['simulated_revenue']
    simulated_total_mroi = st.session_state['tracking']['simulated_mroi']

    # before optimization
    if 'df_optimized' not in st.session_state['tracking']:
        with left_column:
            st.metric(_('Simulated Budget'),
                      value=utils.display_currency(planned_budget))
        with middle_column1:
            st.metric(_('Simulated Contribution'),
                      value=utils.display_volume(simulated_total_contribution))
        with middle_column2:
            st.metric(_('Simulated Revenue'),
                      value=utils.display_currency(simulated_total_revenue))
        with right_column:
            st.metric('MROI',
                      value=f'{round(simulated_total_mroi, 2)}')
    # after optimization
    else:
        # send message on the optimization success or failure
        opt_string = st.session_state['tracking']['select_scenario_track']
        with success_placeholder:
            if st.session_state['tracking']['success']:
                st.success(f'{opt_string} {_("successfully converged.")}')
            else:
                st.error(f'{opt_string} {_("did not converge to the desired criteria.")}')
        # access optimized top metrics calculated and saved in the session state by optimized_top_metrics() function
        # call inside calculate_opt
        optimized_total_spend = st.session_state['tracking']['optimized_spend']
        optimized_total_contribution = st.session_state['tracking']['optimized_contribution']
        optimized_total_revenue = st.session_state['tracking']['optimized_revenue']
        optimized_total_mroi = st.session_state['tracking']['optimized_mroi']

        # display optimized top metrics
        with left_column:
            st.metric(_('Optimized Spend'),
                      value=utils.display_currency(optimized_total_spend),
                      delta=utils.display_percent(planned_budget, optimized_total_spend))
        with middle_column1:
            st.metric(_('Optimized Contribution'),
                      value=utils.display_volume(optimized_total_contribution),
                      delta=utils.display_percent(simulated_total_contribution, optimized_total_contribution))
        with middle_column2:
            st.metric(_('Optimized Revenue'),
                      value=utils.display_currency(optimized_total_revenue),
                      delta=utils.display_percent(simulated_total_revenue, optimized_total_revenue))
        with right_column:
            st.metric(f'{_("Optimized")} MROI',
                      value=f'{round(optimized_total_mroi, 2)}',
                      delta=utils.display_percent(simulated_total_mroi, optimized_total_mroi))

        # swap dataframe to optimized dataframe from session state for table and plotting
        dataframe = st.session_state['tracking']['df_optimized']

    # create a tab layout
    tabs = st.tabs([_('Plotting'), _('Table')])

    # define the content of the second tab: Plotting
    with tabs[0]:
        tab_plotting.opt_plotting_tab(dataframe)

    # define the content of the first tab: Table
    with tabs[1]:
        tab_table.opt_table_tab(dataframe)
