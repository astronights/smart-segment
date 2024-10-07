import pytest
import numpy as np

from smart_segment.optimization import (
    optimize_cutoffs_with_quantiles,
    optimize_cutoffs_with_global_search,
)

# Sample data for testing
propensities = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
predictions = np.array([1, 0, 1, 1, 0])

cost_fn = lambda ix: 2*ix
revenue_fn = lambda ix: 10*ix

def test_optimize_cutoffs_with_quantiles():
    n_bins = 3
    cutoffs = optimize_cutoffs_with_quantiles(n_bins, propensities, predictions, 0, cost_fn, revenue_fn)
    assert len(cutoffs) == n_bins - 1, "The number of cutoffs should be n_bins - 1"
    assert np.all(cutoffs >= 0) and np.all(cutoffs <= 1), "Cutoffs should be between 0 and 1"

def test_optimize_cutoffs_with_global_search():
    n_bins = 3
    cutoffs = optimize_cutoffs_with_global_search(n_bins, propensities, predictions, 0, cost_fn, revenue_fn)
    assert len(cutoffs) == n_bins - 1, "The number of cutoffs should be n_bins - 1"
    assert np.all(cutoffs >= 0) and np.all(cutoffs <= 1), "Cutoffs should be between 0 and 1"

def test_optimize_cutoffs_with_invalid_bins():
    n_bins = 1  # Invalid case
    with pytest.raises(ValueError):
        optimize_cutoffs_with_quantiles(n_bins, propensities, predictions, 0, cost_fn, revenue_fn)

def test_optimize_cutoffs_with_global_search_invalid_bins():
    n_bins = 1  # Invalid case
    with pytest.raises(ValueError):
        optimize_cutoffs_with_global_search(n_bins, propensities, predictions, 0, cost_fn, revenue_fn)
