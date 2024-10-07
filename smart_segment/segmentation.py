from .optimization import (
    optimize_cutoffs_with_global_search,
    optimize_cutoffs_with_quantiles
)
from .utils import (
    merge_bins,
    default_cost_function,
    default_revenue_function,
    calculate_total_revenue_with_penalty
)
import numpy as np

def find_optimal_bins(
    propensities: np.ndarray,
    predictions: np.ndarray,
    n_bins: int = 10,
    cost_fn: callable = default_cost_function,
    revenue_fn: callable = default_revenue_function,
    penalty_factor: float = 0,
    min_samples: int = 10,
    global_search: bool = True
) -> tuple[int, np.ndarray, float]:
    '''
    Find the optimal number of bins and cutoffs based on propensities and predictions.

    Args:
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        n_bins (int): Number of bins to consider (default: 10).
        cost_fn (callable): Function to calculate cost based on bin index (default: default_cost_function).
        revenue_fn (callable): Function to calculate revenue based on bin index (default: default_revenue_function).
        penalty_factor (float): Penalizing value for not exploring values (default: 0).
        min_samples (int): Minimum samples required for a bin (default: 10).
        global_search (bool): Flag for using global search (default: True).

    Returns:
        tuple: A tuple containing the best number of bins, best cutoffs, and maximum revenue.
    '''

    if n_bins > len(propensities): return (0, None, -np.inf)

    # Optimize the cutoffs for the current number of bins
    if global_search:
        cutoffs = optimize_cutoffs_with_global_search(n_bins, propensities, predictions, penalty_factor, revenue_fn, cost_fn)
    else:
        cutoffs = optimize_cutoffs_with_quantiles(n_bins, propensities, predictions, penalty_factor, revenue_fn, cost_fn)

    # Merge bins that do not meet the minimum sample requirement
    merged_cutoffs = merge_bins(cutoffs, propensities, predictions, min_samples)

    # Calculate total revenue for this set of merged cutoffs
    revenue = calculate_total_revenue_with_penalty(merged_cutoffs, propensities, predictions, penalty_factor, revenue_fn, cost_fn)

    best_cutoffs = np.concatenate(([0], merged_cutoffs, [1]))  # Add 0 and 1

    return len(best_cutoffs)-1, best_cutoffs, revenue
