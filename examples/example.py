## Imports
import numpy as np
import pandas as pd
from smart_segment import find_optimal_bins

## Data Creation
np.random.seed(42)

# Gamma Distribution parameters and data size
k, theta = 2, 2
size = 100_000

# Generating Gamma values within 0-1
gamma_values = np.random.gamma(k ,theta, size)
propensities = np.sort(np.clip(gamma_values, 0, 20)/20.0)
print('Propensities: ', propensities.shape)

# Creating the DataFrame
df = pd.DataFrame(propensities, columns=['propensity'])

# Simulating the true binary outcome
df['y'] = df['propensity'].apply(lambda s: np.random.choice([0, 1], p=[1-s, s]))

## Segmentation Algorithms

# Uniform segment
df['uniform'] = pd.cut(df['propensity'], 10)

# Percentile segment
df['percentile'] = pd.qcut(df['propensity'], 10, duplicates='drop')

# Quantile Based
result = find_optimal_bins(df['propensity'], df['y'], n_bins=10, 
                           revenue_fn=lambda ix: 10000,
                           cost_fn=lambda ix: 2**ix,
                           penalty_factor=0,
                           min_samples=10, global_search=False)
best_n_bins, best_cutoffs, max_revenue = result
df['optim_quantile'] = pd.cut(df['propensity'], best_cutoffs, include_lowest=False, duplicates='drop')

# Global Search
result = find_optimal_bins(df['propensity'], df['y'], n_bins=10, 
                           revenue_fn=lambda ix: 30,
                           cost_fn=lambda ix: 2*ix,
                           penalty_factor=0,
                           min_samples=10, global_search=True)
best_n_bins, best_cutoffs, max_revenue = result
df['optim_global'] = pd.cut(df['propensity'], best_cutoffs, include_lowest=False, duplicates='drop')

df.to_csv('segments.csv', index=False)