import pandas as pd
from datetime import datetime, timedelta

# 1. Get data set
# Load the CSV file
df = pd.read_csv('bc_trip259172515_230215.csv')

# Print the number of breadcrumb records (rows)
print(f"Number of breadcrumb records: {len(df)}")


# 2. Filter
# 2A. and 2B. Drop unused columns using drop() method
df = df.drop(columns=['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP'])
print("drop() result: \n", df.head())

# 2C. Use the usecols parameter
# First, get all column names (without loading full data)
all_columns = pd.read_csv('bc_trip259172515_230215.csv', nrows=0).columns.tolist()

# Filter out unwanted columns
columns_to_use = [col for col in all_columns if col not in ['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP']]

# Load the CSV file with selected columns
df_filtered = pd.read_csv('bc_trip259172515_230215.csv', usecols=columns_to_use)

print("usecols result: \n", df_filtered.head())

# 3. Decode
# Decode timestamp
def decode_timestamp(row):
    base_date = datetime.strptime(row['OPD_DATE'], "%d%b%Y:%H:%M:%S")  # Convert to datetime
    time_offset = timedelta(seconds=row['ACT_TIME'])
    return base_date + time_offset

# Apply the function row-wise
df_filtered['TIMESTAMP'] = df_filtered.apply(decode_timestamp, axis=1)

# Drop OPD_DATE and ACT_TIME
df_decoded = df_filtered.drop(columns=['OPD_DATE', 'ACT_TIME'])

print("Remaining columns after decoding timestamp: \n", df_decoded.columns.tolist())
print("Resulting Table: \n", df_decoded.head())


# 4. Enhance
# 4i. Utilize the pandas.DataFrame.diff() method for this calculation. 
df_decoded['dMETERS'] = df_decoded['METERS'].diff()
df_decoded['dTIMESTAMP'] = df_decoded['TIMESTAMP'].diff().dt.total_seconds()

# 4ii. use apply() (with a lambda function) to calculate SPEED = dMETERS / dTIMESTAMP.
df_decoded['SPEED'] = df_decoded.apply(
    lambda row: row['dMETERS'] / row['dTIMESTAMP'] if row['dTIMESTAMP'] and row['dTIMESTAMP'] > 0 else 0,
    axis=1
)

# 4iii. Filter/drop the unneeded dMETERS and dTIMESTAMP columns.
df_final = df_decoded.drop(columns=['dMETERS', 'dTIMESTAMP'])

print(f"Minimum speed: {df_final['SPEED'].min():.2f}")
print(f"Maximum speed: {df_final['SPEED'].max():.2f}")
print(f"Average speed: {df_final['SPEED'].mean():.2f}")

print("\n")

print("Displaying Relevant Speed Columns: \n", df_final[['TIMESTAMP', 'METERS', 'SPEED']].head())