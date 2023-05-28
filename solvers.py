from scipy.optimize import minimize
import nlopt
import numpy as np
from translations import _


def slsqp(dataframe, goal, optimization_type='spend'):
    """
    Takes constraints, boundaries, gradient.
    Gives the same optimum as NLopt MMA, but may take longer to reach this result
    Accepts constraint, boundaries, gradient
    :param dataframe: input dataframe
    :param goal: contribution for goal based optimization
    :param optimization_type: either 'spend' or 'goal'
    :return: optimized dataframe
    """
    # create a list of tuples for the bounds
    bounds = [(lb, ub) for lb, ub in zip(dataframe[_('Lower Spend Bound')].tolist(),
                                         dataframe[_('Upper Spend Bound')].tolist())]

    # objective function
    def objective(x):
        return -np.sum(dataframe['Coefficient'] * np.power(x, dataframe['Power']))

    # here inequality means it has to be non-negative
    budget = dataframe[_('Simulated Spend')].sum()

    def constraint(x):
        if optimization_type == 'spend':
            constraint = budget - sum(x)
        else:
            contribution = -np.sum(dataframe[_('Coefficient')] * np.power(x, dataframe['Power']))
            constraint = contribution - goal
        return constraint

    # gradient of objective function
    def gradient(x):
        return -dataframe['Coefficient'] * dataframe['Power'] * np.power(x, dataframe['Power'] - 1)

    # initial guess
    x0 = np.array(dataframe[_('Simulated Spend')])

    # settings
    constraints = {'type': 'ineq', 'fun': constraint}

    # optimize with `SLSQP` method
    res = minimize(fun=objective,
                   x0=x0,
                   method='SLSQP',
                   jac=gradient,
                   bounds=bounds,
                   constraints=constraints,
                   options={'maxiter': 20000})

    # results
    optimised = {'solution': res.x, 'objective_value': -res.fun}

    # transform dataframe
    dataframe[_('Optimized Spend')] = optimised['solution']
    dataframe[_('Optimized Contribution')] = dataframe['Coefficient'] * np.power(dataframe[_('Optimized Spend')],
                                                                                 dataframe['Power'])
    dataframe[_('Optimized Revenue')] = dataframe[_('Multiplier')] * dataframe[_('Optimized Contribution')]

    return dataframe, res.success


def nlopt_ld_mma(dataframe, optimization_type='spend', goal=None):
    """
    Takes constraint, boundaries, gradient
    :param dataframe: input dataframe
    :param goal: contribution for goal based optimization
    :param optimization_type: either 'spend' or 'goal'
    :return: optimized dataframe
    """
    # define objective function
    def eval_f(x, grad):
        objective = -np.sum(dataframe[_('Coefficient')] * np.power(x, dataframe['Power']))
        if grad.size > 0:
            grad[:] = -dataframe[_('Coefficient')] * dataframe['Power'] * np.power(x, dataframe['Power'] - 1)
        return objective

    # define constraint
    budget = dataframe[_('Simulated Spend')].sum()

    def eval_g(x, grad):
        # spend based optimization
        if optimization_type == 'spend':
            constraint = np.sum(x) - budget
        # goal based optimization
        else:
            contribution = np.sum(dataframe[_('Coefficient')] * np.power(x, dataframe['Power']))
            constraint = contribution - goal
        grad[:] = 1
        return constraint

    # options
    local_opts = {'algorithm': 'NLOPT_LD_MMA', 'xtol_rel': 1.0e-10}
    opts = {'algorithm': 'NLOPT_LD_MMA', 'xtol_rel': 1.0e-10, 'maxeval': 20000, 'local_opts': local_opts}

    # initialize optimizer
    res = nlopt.opt(nlopt.LD_MMA, len(dataframe[_('Simulated Spend')]))

    # define boundaries
    res.set_lower_bounds(dataframe[_('Lower Spend Bound')])
    res.set_upper_bounds(dataframe[_('Upper Spend Bound')])

    res.set_min_objective(eval_f)
    res.add_inequality_constraint(eval_g)

    res.set_maxeval(opts['maxeval'])
    res.set_xtol_rel(opts['xtol_rel'])

    x0 = np.array(dataframe[_('Simulated Spend')])

    x = res.optimize(x0)

    optimised = {'solution': x, 'objective_value': -res.last_optimum_value()}

    dataframe[_('Optimized Spend')] = optimised['solution']
    dataframe[_('Optimized Contribution')] = dataframe[_('Coefficient')] * np.power(dataframe[_('Optimized Spend')],
                                                                                    dataframe['Power'])
    dataframe[_('Optimized Revenue')] = dataframe['Multiplier'] * dataframe[_('Optimized Contribution')]

    return dataframe, res.last_optimize_result() > 0


solvers_dict = {
    'NLOP_LD_MMA': nlopt_ld_mma,
    'SLSQP': slsqp,
}
