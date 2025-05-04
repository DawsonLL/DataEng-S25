import pandas as pd

# Load the CSV file
df = pd.read_csv('bc_trip259172515_230215.csv')

# Print the number of breadcrumb records (rows)
print(f"Number of breadcrumb records: {len(df)}")