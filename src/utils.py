import numpy as np

def default_revenue_function(bin_index: int) -> float:
    '''
    Default revenue function based on the bin index.

    Args:
        bin_index (int): Index of the bin.

    Returns:
        float: Revenue value calculated based on the bin index.
    '''
    return 3 ** bin_index  # Example function; can be customized

def default_cost_function(bin_index: int) -> float:
    '''
    Default cost function based on the bin index.

    Args:
        bin_index (int): Index of the bin.

    Returns:
        float: Cost value calculated based on the bin index.
    '''
    return 2 ** bin_index  # Example function; can be customized

def calculate_total_revenue_with_penalty(
    cutoffs: np.ndarray,
    propensities: np.ndarray,
    predictions: np.ndarray,
    penalty_factor: float,
    revenue_func: callable,
    cost_func: callable
) -> float:
    '''
    Calculate total revenue considering penalties for conversion rates.

    Args:
        cutoffs (np.ndarray): Array of cutoff values.
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        penalty_factor (float): Penalizing value for not exploring values.
        revenue_func (callable): Function to calculate revenue based on bin index.
        cost_func (callable): Function to calculate cost based on bin index.

    Returns:
        float: Total revenue calculated.
    '''
    total_revenue = 0
    cutoffs = np.concatenate(([0], cutoffs, [1]))  # Adding 0 and 1 as bounds
    prev_conversion_rate = None  # Track previous conversion rate for penalty

    for i_bin in range(len(cutoffs) - 1):
        # Define the bin range based on cutoffs
        bin_mask = (propensities >= cutoffs[i_bin]) & (propensities < cutoffs[i_bin + 1])
        
        # Calculate bin size
        bin_size = bin_mask.sum()
        
        # Skip bin if it doesn't meet the minimum sample size
        if bin_size == 0:
            continue
            
        # Calculate conversion rate only if the bin size is valid
        conversion_rate = predictions[bin_mask].mean() if bin_size > 0 else 0
        
        # Calculate revenue and cost for the current bin using user-defined functions
        revenue = revenue_func(i_bin) * bin_size * conversion_rate  # Revenue depends on bin index and size
        cost = cost_func(i_bin) * bin_size  # Cost depends only on bin index
        
        # Penalty: increase cost if the conversion rate is too close to the previous bin
        penalty = 0
        if prev_conversion_rate is not None:
            penalty = np.abs(prev_conversion_rate - conversion_rate)
        
        # Net revenue (revenue minus cost and penalty)
        net_revenue = revenue - cost - penalty_factor * penalty  # Amplifying the penalty
        
        # Add to total revenue
        total_revenue += net_revenue
        
        # Update previous conversion rate for the next iteration
        prev_conversion_rate = conversion_rate
        
    return total_revenue

def merge_bins(
    cutoffs: np.ndarray,
    propensities: np.ndarray,
    predictions: np.ndarray,
    min_samples: int = 1
) -> np.ndarray:
    '''
    Merge bins based on the provided cutoff values.

    Args:
        cutoffs (np.ndarray): Array of cutoff values.
        propensities (np.ndarray): Array of propensity scores.
        predictions (np.ndarray): Array of predicted values.
        min_samples (int): Minimum samples required for a bin (default: 1).

    Returns:
        np.ndarray: Array of new cutoffs after merging.
    '''
    cutoffs = np.concatenate(([0], cutoffs, [1]))  # Add bounds 0 and 1
    new_cutoffs = []
    
    # Track previous bin size and conversion rate
    prev_bin_size = 0
    prev_conversion_rate = None
    
    for i_bin in range(len(cutoffs) - 1):
        bin_mask = (propensities >= cutoffs[i_bin]) & (propensities < cutoffs[i_bin + 1])
        bin_size = bin_mask.sum()
        
        # If the current bin has enough samples, keep it
        if bin_size >= min_samples:
            if prev_bin_size > 0:  # Only add if there was a previous bin
                new_cutoffs.append(cutoffs[i_bin])
            prev_bin_size = bin_size
            prev_conversion_rate = predictions[bin_mask].mean() if bin_size > 0 else 0
        else:
            # Merge with previous bin
            prev_bin_size += bin_size
            if prev_conversion_rate is not None:
                prev_conversion_rate = (
                    (prev_conversion_rate * (prev_bin_size - bin_size)) +
                    (predictions[bin_mask].mean() * bin_size)
                ) / prev_bin_size
    
    new_cutoffs.append(cutoffs[-1])  # Always add the last bound
    
    return np.array(new_cutoffs)
