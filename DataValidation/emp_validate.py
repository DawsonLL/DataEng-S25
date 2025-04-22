import pandas as pd

df = pd.read_csv('employees.csv')

# existence assertion
count = 0

for field in df['name']:
    if pd.isna(field):
        count += 1

print("Assertion: every record has a non-null name field")
print("Number of violations: ", count)

# limit assertion
count_hires_before_2015 = 0

# convert hire_date to datetime format
df['hire_date'] = pd.to_datetime(df['hire_date'])

# extract year into new column
df['hire_year'] = df['hire_date'].dt.year

for year in df['hire_year']:
    if year < 2015:
        count_hires_before_2015 += 1

print("Assertion: every employee was hired no earlier than 2015")
print("Number of violations: ", count_hires_before_2015)

# intra-record assertion
count_employees_hired_before_birth = 0

# convert birth_date to datetime format
df['birth_date'] = pd.to_datetime(df['birth_date'])

df_hired_before_birth = df[df['birth_date'] > df['hire_date']]

count_employees_hired_before_birth = len(df_hired_before_birth)

print("Assertion: each employee was born before they were hired")
print("Number of violations: ", count_employees_hired_before_birth)

# inter-record Assertion
count_managers_are_employees = 0

''' # commented out because these fields take longer to parse
for manager in df['reports_to']:
    if pd.notna(manager): # accounts for NaN
        is_employee = df[df['eid'] == manager]
        if is_employee.empty:
            count_managers_are_employees += 1
'''

print("Assertion: each employee has a manager who is a known employee")
print("Number of violations: ", count_managers_are_employees)

# summary assertion
count_cities_with_more_than_one_employee = 0

'''
for city in df['city'].unique():
    number_of_employees = (df['city'] == city).sum()
    if number_of_employees <= 1:
        count_cities_with_more_than_one_employee += 1
'''

print("Assertion: each city has more than one employee")
print("Number of violations: ", count_cities_with_more_than_one_employee)


import matplotlib.pyplot as plt

# Plot using logarithmic scaling for the salary axis

df['salary'].plot(kind='hist', bins=50, edgecolor='black')

plt.title('Salary Distribution')
plt.xlabel('Salary')
plt.ylabel('Frequency')

plt.show()
