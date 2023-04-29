import pandas as pd

# Define two dataframes with the same shape and column names
df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['min', 'median', 'max'])
df2 = pd.DataFrame([[2, 4, 6], [8, 10, 12], [14, 16, 18]], columns=['min', 'median', 'max'])

# Create a boolean mask indicating which rows meet the median comparison criteria
median_mask = (df1['median'] >= df2['min']) & (df1['median'] <= df2['max'])

# Create a dataframe with the max and min comparison results
mm_comparison = pd.DataFrame({
    'max_comparison': df1['max'].max() < df2['max'].max(),
    'min_comparison': df1['min'].min() > df2['min'].min()
}, index=[0])

# Combine the three dataframes into a single dataframe
output_df = pd.concat([mm_comparison, median_mask.astype(int)], axis=1)

# Print the dataframe without the index row
print(output_df.to_string(index=False))