from scipy.optimize import minimize
# import nlopt
import numpy as np
from translations import _


def l_bfgs_b(dataframe):
    """
    L-BFGS-B doesn't include constraints. So we add penalty to the objective instead.
    But because of this, we can't use `jac` option (gradient) anymore to speed up the optimization.
    However, the speed is good enough. Solves quicker than SLSQP.
    Gives lower optimized revenue than both NLopt and SLSQP
    :param dataframe:
    :return optimized dataframe:
    """
    dataframe = dataframe.fillna(0)

    # create a list of tuples for the bounds
    bounds = [(lb, ub) for lb, ub in zip(dataframe[_('Lower Spend Bound')].tolist(),
                                         dataframe[_('Upper Spend Bound')].tolist())]

    # objective function with penalty
    budget = dataframe[_('Simulated Spend')].sum()

    def objective_penalty(x):
        # calculate penalty
        penalty = np.square(np.maximum(0, np.sum(x) - budget))
        penalty = np.square(penalty)  # amplify penalty
        return -np.sum(dataframe['Coefficient'] * np.power(x, dataframe['Power'])) + penalty

    # initial guess
    x0 = np.zeros_like(dataframe[_('Simulated Spend')])

    options = {'maxls': 20, 'iprint': -1, 'gtol': 1e-05, 'eps': 1e-08, 'maxiter': 20000, 'ftol': 2.220446049250313e-09,
               'maxcor': 10, 'maxfun': 20000}

    # optimize with `L-BFGS-B` method
    res = minimize(fun=objective_penalty,
                   x0=x0,
                   method='L-BFGS-B',
                   bounds=bounds,
                   options=options
                   )

    # results
    optimised = {'solution': res.x, 'objective_value': -res.fun}

    # transform dataframe
    dataframe[_('Optimized Spend')] = optimised['solution']
    dataframe[_('Optimized Contribution')] = dataframe['Coefficient'] * np.power(dataframe[_('Optimized Spend')],
                                                                                 dataframe['Power'])
    dataframe[_('Optimized Revenue')] = dataframe[_('Multiplier')] * dataframe[_('Optimized Contribution')]

    return dataframe, res.success


def slsqp(dataframe):
    """
    Takes constraints, boundaries, gradient.
    Gives the same optimum as NLopt MMA, but it takes 2 mins to reach this result
    :param dataframe:
    :return dataframe:
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
        return budget - sum(x)

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


def nlopt_ld_mma(dataframe):
    """
    Takes constraint, boundaries, gradient
    :param dataframe:
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
        constraint = np.sum(x) - budget
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
    'L-BFGS-B': l_bfgs_b
}
