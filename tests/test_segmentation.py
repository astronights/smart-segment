import pytest
import numpy as np

from src.segmentation import find_optimal_bins

# Sample data for testing
propensities = np.array([0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
predictions = np.array([1, 0, 1, 1, 0, 1, 0, 1, 0, 1])

def test_find_optimal_bins():
    # Test default behavior with a reasonable number of bins
    n_bins, cutoffs, max_revenue = find_optimal_bins(propensities, predictions, revenue_fn=lambda ix: 10**ix, cost_fn=lambda ix: 0)
    assert n_bins > 0, "Number of bins should be greater than 0"
    assert len(cutoffs) == n_bins + 1, "Cutoffs length should be equal to n_bins + 1"
    assert max_revenue >= 0, "Max revenue should not be negative"

def test_find_optimal_bins_with_min_samples():
    # Test behavior when setting minimum sample size
    n_bins, cutoffs, max_revenue = find_optimal_bins(propensities, predictions, min_samples=5)
    assert n_bins >= 2, "Number of bins should be at least 2"
    
def test_find_optimal_bins_global_search():
    # Test behavior with global search
    n_bins, cutoffs, max_revenue = find_optimal_bins(propensities, predictions, global_search=True)
    assert n_bins > 0, "Number of bins should be greater than 0"

def test_find_optimal_bins_no_bins():
    # Test behavior when no valid bins can be found
    empty_propensities = np.array([])
    empty_predictions = np.array([])
    n_bins, _, _ = find_optimal_bins(empty_propensities, empty_predictions)
    assert n_bins == 0, "No bins should be found for empty input"
