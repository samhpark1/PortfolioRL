import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('cleaned_data.csv')
data = df.to_numpy()

#70% train, 30% remaining 
train_data, temp_data = train_test_split(data, test_size=0.3, random_state=42)

# 15% validation, 15% test
val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

print("Train shape:", train_data.shape)
print("Validation shape:", val_data.shape)
print("Test shape:", test_data.shape)
