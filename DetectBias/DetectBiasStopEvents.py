import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 2. Transform the Data
# Load the HTML file
with open("trimet_stopevents_2022-12-07.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Read all tables from the HTML file
all_tables = pd.read_html("trimet_stopevents_2022-12-07.html")

# Concatenate them into a single DataFrame
stops_df = pd.concat(all_tables, ignore_index=True)

# Normalize column names by removing any extra whitespace and ensuring all characters are lowercase
stops_df.columns = [col.strip().lower() for col in stops_df.columns]

# Extract trip_id from heading text, i.e: "Stop events for PDX_TRIP 214799544"
heading = soup.find(string=lambda text: text and "PDX_TRIP" in text)
trip_id = int(heading.split()[-1])  # grabs the last word as the trip ID

# Add trip_id column to DataFrame
stops_df['trip_id'] = trip_id

# Ensure the needed columns exist using assertions
required_columns = ['trip_id', 'vehicle_number', 'arrive_time', 'location_id', 'ons', 'offs']
assert all(col in stops_df.columns for col in required_columns)

# The tstamp column should be a datetime value computed using the arrive_time 
# column in the stop event data (arrive_time indicates seconds since midnight) 
midnight = datetime(2022, 12, 7)
stops_df['tstamp'] = stops_df['arrive_time'].apply(lambda x: midnight + timedelta(seconds=int(x)))

# The TriMet Stop Event data is in .html form. Use python, BeautifulSoup and pandas to transform it 
# into one DataFrame (called stops_df) containing these columns: 
# trip_id, vehicle_number, tstamp, location_id, ons, offs
stops_df = stops_df[['trip_id', 'vehicle_number', 'tstamp', 'location_id', 'ons', 'offs']]

# The DataFrame should contain 93912 stop events. 
print("Total stop events:", len(stops_df))

# 2A. How many vehicles are contained in the data?
num_vehicles = stops_df['vehicle_number'].nunique()
print("Number of vehicles:", num_vehicles)

# 2B. How many stop locations (how many unique values of location_id)?
num_locations = stops_df['location_id'].nunique()
print("Number of stop locations:", num_locations)

# 2C. Min and Max values of tstamp? 
min_time = stops_df['tstamp'].min()
max_time = stops_df['tstamp'].max()
print("Min tstamp:", min_time)
print("Max tstamp:", max_time)

# 2D. How many stop events at which at least one passenger boarded (stop events for which ons >= 1)?
stops_with_boarding = stops_df[stops_df['ons'] >= 1]
num_with_boarding = len(stops_with_boarding)
print("Stop events with at least one boarding:", num_with_boarding)

# 2E. Percentage of stop events with at least one passenger boarding?
percentage_with_boarding = (num_with_boarding / len(stops_df)) * 100
print(f"Percentage with at least one boarding: {percentage_with_boarding:.2f}%")

print("\n")
# ----------------------------- #

# 3. Validate
# 3A. For location 6913
location_6913_df = stops_df[stops_df['location_id'] == 6913]
print(f"Location 6913:")

# 3Ai. How many stops made at this location?
num_stops_location_6913 = len(location_6913_df)
print(f"Stops made: {num_stops_location_6913}")

# 3Aii. How many different buses stopped at this location?
num_vehicles_location_6913 = location_6913_df['vehicle_number'].nunique()
print(f"Different buses: {num_vehicles_location_6913}")

# 3Aiii. For what percentage of stops at this location did at least one passenger board?
stops_with_boarding_loc = location_6913_df[location_6913_df['ons'] >= 1]
percent_boarding_location_6913 = (len(stops_with_boarding_loc) / num_stops_location_6913) * 100 if num_stops_location_6913 > 0 else 0
print(f"Percentage with at least one boarding: {percent_boarding_location_6913:.2f}%")

# 3B. For vehicle 4062:
vehicle_4062_df = stops_df[stops_df['vehicle_number'] == 4062]
print(f"Vehicle 4062:")

# 3Bi. How many stops made by this vehicle?
num_stops_vehicle_4062 = len(vehicle_4062_df)
print(f"Stops made: {num_stops_vehicle_4062}")

# 3Bii. How many total passengers boarded this vehicle?
total_ons_vehicle_4062 = vehicle_4062_df['ons'].sum()
print(f"Total passengers boarded: {total_ons_vehicle_4062}")

# 3Biii. How many passengers deboarded this vehicle?
total_offs_vehicle_4062 = vehicle_4062_df['offs'].sum()
print(f"Total passengers deboarded: {total_offs_vehicle_4062}")

# 3Biv. Percentage of this vehicle’s stops with at least one passenger boarding
stops_with_boarding_vehicle = vehicle_4062_df[vehicle_4062_df['ons'] >= 1]
percent_boarding_vehicle_4062 = (len(stops_with_boarding_vehicle) / num_stops_vehicle_4062) * 100 if num_stops_vehicle_4062 > 0 else 0
print(f"Percentage with at least one boarding: {percent_boarding_vehicle_4062:.2f}%")

print("\n")
# ----------------------------- #

# 4. Find vehicles with biased boarding data (“ons”)
from scipy.stats import binomtest

alpha = 0.05  # significance threshold

# System-wide proportion of stops with at least one boarding (from step 2E)
overall_boarding_rate = (stops_df['ons'] >= 1).mean()

# Store results
biased_vehicles = []

# Group by vehicle_number
for vehicle, group in stops_df.groupby('vehicle_number'):
    n = len(group)  # total stop events
    x = (group['ons'] >= 1).sum()  # stop events with at least one boarding
    # Perform binomial test
    result = binomtest(x, n, overall_boarding_rate, alternative='two-sided')
    p_value = result.pvalue
    
    if p_value < alpha:
        biased_vehicles.append((vehicle, x, n, p_value))

# Sort by p-value ascending
biased_vehicles.sort(key=lambda x: x[3])

# Print results
print(f"{'Vehicle':<10} {'Boarding Events':<17} {'Total Stops':<12} {'p-value':<10}")
for vehicle, x, n, p in biased_vehicles:
    print(f"{vehicle:<10} {x:<17} {n:<12} {p:.5f}")

print("\n")
# ----------------------------- #

from scipy.stats import chi2_contingency

# 6Bi. Total number of "offs"
total_offs = stops_df['offs'].sum()
print(f"Total offs across all vehicles: {total_offs}")

# 6Bi. Total number of "ons"
total_ons = stops_df['ons'].sum()
print(f"Total ons across all vehicles: {total_ons}\n")

vehicle_counts = stops_df.groupby('vehicle_number').agg({'offs': 'sum', 'ons': 'sum'}).reset_index()

# Add a new column for p-value after performing chi-square test
p_values = []

# 6Ciii. Use a X2 test to determine p, the probability that the vehicle’s proportion of offs/ons will 
# be observed given the overall proportion of offs/ons in the entire system.
for _, row in vehicle_counts.iterrows():
    vehicle = row['vehicle_number']
    offs = row['offs']
    ons = row['ons']

    # Construct 2x2 contingency table
    contingency_table = [
        [offs, ons],
        [total_offs - offs, total_ons - ons]
    ]

    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    p_values.append(p_value)

# Add p-values to the vehicle_counts DataFrame
vehicle_counts['p_value'] = p_values

# 6Ci. number of “offs”
# 6Cii. number of “ons” 
print(vehicle_counts.to_string(index=False))

# Filter and sort biased vehicles
biased_vehicles = vehicle_counts[vehicle_counts['p_value'] < 0.05].sort_values(by='p_value')

# 6D. List the IDs of vehicles, and their corresponding p values, for vehicles having p < 0.05 
print("Vehicles with biased offs/ons ratios (p < 0.05):")
print(f"{'Vehicle':<10} {'Offs':<10} {'Ons':<10} {'p-value':<10}")
for _, row in biased_vehicles.iterrows():
    print(f"{int(row['vehicle_number']):<10} {int(row['offs']):<10} {int(row['ons']):<10} {row['p_value']:.6f}")
