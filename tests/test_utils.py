import numpy as np

from smart_segment.utils import (
    default_revenue_function,
    default_cost_function,
    calculate_total_revenue_with_penalty,
    merge_bins,
)

# Sample data for testing
cutoffs = np.array([0.2, 0.4, 0.6])
propensities = np.array([0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
predictions = np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 1])

def test_default_revenue_function():
    assert default_revenue_function(0) == 1, "Revenue function for bin index 0 should return 1"
    assert default_revenue_function(2) == 9, "Revenue function for bin index 2 should return 9"

def test_default_cost_function():
    assert default_cost_function(0) == 1, "Cost function for bin index 0 should return 1"
    assert default_cost_function(3) == 8, "Cost function for bin index 3 should return 8"

def test_calculate_total_revenue_with_penalty():
    total_revenue = calculate_total_revenue_with_penalty(cutoffs, propensities, predictions,
                                                         penalty_factor=1,
                                                         cost_func=lambda ix: 2*ix,
                                                         revenue_func=lambda ix: 10**ix)

    assert isinstance(total_revenue, float), "Total revenue should be a float"
    assert total_revenue >= 0, "Total revenue should not be negative"

def test_merge_bins():
    new_cutoffs = merge_bins(cutoffs, propensities, predictions, min_samples=3)
    assert len(new_cutoffs) <= len(cutoffs), "New cutoffs should be less than or equal to the original cutoffs"
    assert np.all(new_cutoffs >= 0) and np.all(new_cutoffs <= 1), "Cutoffs should be between 0 and 1"
