import pandas as pd
from scipy.stats import ttest_1samp

# 5. Find vehicles with biased GPS data

# Preprocessing
relpos_df = pd.read_csv("trimet_relpos_2022-12-07.csv")
relpos_df.columns = [col.strip().lower() for col in relpos_df.columns]
assert 'vehicle_number' in relpos_df.columns
assert 'relpos' in relpos_df.columns

# Drop rows with missing relpos
relpos_df = relpos_df.dropna(subset=['relpos'])

# Convert relpos to float if not already
relpos_df['relpos'] = relpos_df['relpos'].astype(float)

# 5Ai. For the entire data set:
# store all RELPOS values for all vehicles as an array to be used in the t-test below
all_relpos_values = relpos_df['relpos'].values

# Dictionary to store p-values per vehicle
biased_vehicles = []

# Group by vehicle and perform one-sample t-test against 0.0 (null hypothesis of no bias)
for vehicle_id, group in relpos_df.groupby('vehicle_number'):
    # 5Bi. find all RELPOS values for the vehicle
    vehicle_relpos = group['relpos'].values
    
    # 5Bii. Use a t-test to determine the probability that the vehicle’s observed RELPOS values occurred given the (null hypothesis) 
    # that there is no bias in the data as compared to the RELPOS values for all vehicles.
    t_stat, p_value = ttest_1samp(vehicle_relpos, popmean=0.0)
    
    # 5C. List the IDs of vehicles (and their corresponding p values) having p < 0.005 
    if p_value < 0.005:
        biased_vehicles.append((vehicle_id, len(vehicle_relpos), round(p_value, 6)))

biased_vehicles.sort(key=lambda x: x[2])

print("Vehicle    RelPos Count   p-value")
for vid, count, p in biased_vehicles:
    print(f"{vid:<10} {count:<14} {p:.6f}")
