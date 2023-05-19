from scipy.optimize import minimize
import numpy as np
from translations import _


def l_bfgs_b(dataframe):
    """
    L-BFGS-B doesn't include. So we add penalty to the objective instead.
    But because of this, we can't use `jac` option (gradient) anymore to speed up the optimization.
    However, the speed is good enough. Solves quicker than SLSQP.
    Gives lower optimized revenue than both NLopt and SLSQP
    :param dataframe:
    :return optimized dataframe:
    """

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
    x0 = np.array(dataframe[_('Simulated Spend')])

    # optimize with `L-BFGS-B` method
    res = minimize(fun=objective_penalty,
                   x0=x0,
                   method='L-BFGS-B',
                   bounds=bounds,
                   tol=1.0e-10,
                   options={'maxiter': 4000}
                   )

    # results
    optimised = {'solution': res.x, 'objective_value': -res.fun}

    # transform dataframe
    dataframe[_('Optimized Spend')] = optimised['solution']
    dataframe[_('Optimized Contribution')] = dataframe['Coefficient'] * np.power(dataframe[_('Optimized Spend')],
                                                                                 dataframe['Power'])
    dataframe[_('Optimized Revenue')] = dataframe[_('Multiplier')] * dataframe[_('Optimized Contribution')]

    return dataframe


def slsqp(dataframe):
    """
    Takes constraints, boundaries, gradient.
    Gives the same optimum as NLopt MMA, but it takes 2 mins to reach this result.
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
                   tol=1.0e-10,
                   options={'maxiter': 4000})

    # results
    optimised = {'solution': res.x, 'objective_value': -res.fun}

    # transform dataframe
    dataframe[_('Optimized Spend')] = optimised['solution']
    dataframe[_('Optimized Contribution')] = dataframe['Coefficient'] * np.power(dataframe[_('Optimized Spend')],
                                                                                 dataframe['Power'])
    dataframe[_('Optimized Revenue')] = dataframe[_('Multiplier')] * dataframe[_('Optimized Contribution')]

    return dataframe
