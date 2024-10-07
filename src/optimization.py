from .utils import calculate_total_revenue_with_penalty

from scipy.optimize import minimize, differential_evolution
import numpy as np

def objective_with_penalty(
    cutoffs: np.ndarray,
    propensities: np.ndarray,
    predictions: np.ndarray,
    penalty_factor: float,
    revenue_func: callable,
    cost_func: callable
) -> float:
    '''
    Objective function to minimize for optimizing cutoffs.

    Args:
        cutoffs (np.ndarray): Array of cutoff values.
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        penalty_factor (float): Penalizing value for not exploring values.
        revenue_func (callable): Function to calculate revenue based on bin index.
        cost_func (callable): Function to calculate cost based on bin index.

    Returns:
        float: Negative total revenue (to be minimized).
    '''
    return -calculate_total_revenue_with_penalty(cutoffs, propensities, predictions, 
                                                 penalty_factor, revenue_func, cost_func)

def optimize_cutoffs_with_quantiles(
    n_bins: int,
    propensities: np.ndarray,
    predictions: np.ndarray,
    penalty_factor: float,
    revenue_func: callable,
    cost_func: callable
) -> np.ndarray:
    '''
    Optimize cutoffs using quantiles.

    Args:
        n_bins (int): Number of bins to optimize for.
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        penalty_factor (float): Penalizing value for not exploring values.
        revenue_func (callable): Function to calculate revenue based on bin index.
        cost_func (callable): Function to calculate cost based on bin index.

    Returns:
        np.ndarray: Sorted array of optimized cutoff values.
    '''
    initial_cutoffs = np.quantile(propensities, np.linspace(0, 1, n_bins + 1)[1:-1])
    bounds = [(0, 1) for _ in range(n_bins - 1)]
    result = minimize(
        objective_with_penalty,
        initial_cutoffs,
        args=(propensities, predictions, penalty_factor, revenue_func, cost_func),
        bounds=bounds,
        method='SLSQP',
        options={'disp': False}
    )
    return np.sort(result.x)

def optimize_cutoffs_with_global_search(
    n_bins: int,
    propensities: np.ndarray,
    predictions: np.ndarray,
    penalty_factor: float,
    revenue_func: callable,
    cost_func: callable
) -> np.ndarray:
    '''
    Optimize cutoffs using global search with differential evolution.

    Args:
        n_bins (int): Number of bins to optimize for.
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        penalty_factor (float): Penalizing value for not exploring values.
        revenue_func (callable): Function to calculate revenue based on bin index.
        cost_func (callable): Function to calculate cost based on bin index.

    Returns:
        np.ndarray: Sorted array of optimized cutoff values.
    '''
    bounds = [(0, 1) for _ in range(n_bins - 1)]
    result = differential_evolution(
        objective_with_penalty,
        bounds,
        args=(propensities, predictions, penalty_factor, revenue_func, cost_func),
        strategy='best1bin',
        disp=False
    )
    return np.sort(result.x)
