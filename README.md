# Optimization-Based Customer Segmentation

This repository provides an optimization-based segmentation tool for business intelligence, enabling data-driven segmentation of customers for targeted marketing efforts. The algorithm uses customer propensities (predicted probabilities of an event) and historical data (actual outcomes) to optimize the segmentation process, maximizing expected revenue while accounting for costs and penalties. This dynamic approach leads to more effective and fine-tuned segments compared to naive or percentile-based methods.

## Key Features
- **Optimized Segmentation**: The algorithm dynamically adjusts segmentation boundaries to maximize expected revenue, based on conversion rates and customer acquisition costs.
- **Customizable Functions**: Users can define their own revenue and cost functions depending on business needs.
- **Adaptable to Different Data**: The tool adapts to the actual distribution of customer propensities and conversion behaviors, ensuring resource allocation to the most promising segments.
- **Merge Small Bins**: Automatically merges bins that don't meet a minimum sample size, leading to more robust segmentation.
  
This segmentation tool is particularly useful for business intelligence teams seeking to enhance the return on investment (ROI) for marketing campaigns by focusing on high-value segments.

## Advantages of Optimization Algorithm Segmentation

### 1. **Higher Conversion Rates in Key Segments**
   - The algorithm identifies high-potential segments with significantly higher conversion rates. It balances conversion rates effectively across segments, unlike naive or percentile methods that might overlook smaller but valuable segments.

### 2. **Fine-Grained Segmentation**
   - Provides finely tuned segments based on customer behavior, enabling more precise and dynamic targeting. This allows for personalized marketing strategies that can adapt to changing customer behavior.

### 3. **Dynamic Response to Customer Behavior**
   - The algorithm adapts to the actual distribution of customer propensities and conversion behaviors. It adjusts in real-time, unlike fixed-interval methods which may misrepresent certain customer groups.

### 4. **Mitigation of Underperformance in Small Bins**
   - Bins with insufficient samples are automatically merged, ensuring that small bins don’t distort insights or lead to poor resource allocation in marketing campaigns.

### 5. **Holistic Revenue Consideration**
   - The algorithm factors in both conversion rates and acquisition costs, aiming to maximize net revenue rather than focusing solely on conversion rates.

### 6. **Strategic Focus on High-Value Segments**
   - By optimizing segmentation based on expected revenue, businesses can prioritize high-value customer segments, leading to improved marketing ROI and a strategic focus on growth areas.

## Installation

You can install the package from the PyPI repository
    
```bash
pip install smart-segment
```

## Usage

This example shows how to use the `find_optimal_bins` function to find the optimal segmentation for a marketing campaign:

```python
import pandas as pd
from smart_segment.segmentation import find_optimal_bins

# Example data
data = {'propensity': [0.1, 0.2, 0.3, 0.4, 0.5],
        'y': [0, 1, 1, 0, 1]}

df = pd.DataFrame(data)

# Find optimal bins with custom revenue and cost functions
result = find_optimal_bins(df['propensity'], df['y'], n_bins=10, 
                        revenue_fn=lambda ix: 30,
                        cost_fn=lambda ix: 2 * ix,
                        min_samples=10, global_search=True)
best_n_bins, best_cutoffs, max_revenue = result

# Apply the segmentation to the DataFrame
df['optim_global'] = pd.cut(df['propensity'], best_cutoffs, include_lowest=False, duplicates='drop')

print(f"Best number of bins: {best_n_bins}")
print(f"Best cutoffs: {best_cutoffs}")
print(f"Maximum Revenue: {max_revenue}")
```

## Repository

The repository is available on Github if you would like to install the latest version of the code.

### Structure

The repository is organized as follows:

```bash
├── src
│   ├── segmentation.py         # Main segmentation logic
│   ├── optimization.py         # Optimization methods for cutoffs
│   └── utils.py                # Utility functions for calculating revenue, merging bins
├── tests
│   ├── test_segmentation.py    # Unit tests for segmentation logic
│   ├── test_optimization.py    # Unit tests for optimization methods
│   └── test_utils.py           # Unit tests for utility functions
├── examples
│   ├── Example.html            # Example of Jupyter notebook
│   ├── segments.csv            # Example of results across various methods
│   └── example.py              # Example Python file showcasing usage
├── requirements.txt            # Required Python packages
├── setup.py                    # Installation script for the package
└── README.md                   # This file
```

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/astronights/smart-segment.git
   cd smart-segment
   ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. To install the package in your Python environment:
    ```bash
    pip install .
    ```

### Running Tests

To ensure that everything works as expected, you can run the test suite using `pytest`:

1. Install pytest if you don't have it already:

    ```
    pip install pytest
    ```

2. Run the tests:

    ```bash
    pytest
    ```

This will execute the test files located in the tests directory and validate that the segmentation tool is functioning correctly.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as long as the terms of the license are met. For more information, see the LICENSE file.

## Contributions
Contributions are welcome! If you have ideas for improvements or find any issues, please feel free to open an issue or submit a pull request. Community contributions are encouraged to help make this tool even better.