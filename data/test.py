import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load the data from the CSV file
df = pd.read_csv('all_data.csv')

df['Date'] = pd.to_datetime(df['Date'])

# Compute the correlation matrix for numeric columns
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()
# Drop completely NaN rows and columns from correlation matrix
corr_matrix = corr_matrix.dropna(axis=0, how='all').dropna(axis=1, how='all')

print(corr_matrix)

sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, 
            linewidths=0.5, linecolor='black')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.figure(figsize=(12, 10))
ax = sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", 
                 linewidths=1, linecolor='black')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
plt.title("Correlation Matrix")

plt.show()



