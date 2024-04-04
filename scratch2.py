import pandas as pd

# Create a DataFrame
df = pd.DataFrame({'A': [['1', '2', '3'], ['foo'], [], ['3', '4']], 'B': 1})
print(df)

# Convert list-like data to a DataFrame and concatenate it with the original DataFrame
df_new = pd.concat([df, pd.DataFrame(df['A'].to_list())], axis=1)

print(df_new)