import pandas as pd
from scipy.stats import ttest_ind

# Load the data
url = 'https://raw.githubusercontent.com/Umuzi-org/statistics-Ikokobetseng/refs/heads/main/data/statistics_data.csv?token=GHSAT0AAAAAADFO3O4J6JSSG6KFDPT3N66A2CQRFLA'
data = pd.read_csv(url)

# Descriptive Statistics
## Mean, median, mode, and standard deviation for age and hours_of_screen_time
print("Age stats:")
print(f"Mean: {data['age'].mean()}")
print(f"Median: {data['age'].median()}")
print(f"Mode: {data['age'].mode().values[0]}")
print(f"Standard Deviation: {data['age'].std()}")

print("\nHours of screen time stats:")
print(f"Mean: {data['hours_of_screen_time'].mean()}")
print(f"Median: {data['hours_of_screen_time'].median()}")
print(f"Mode: {data['hours_of_screen_time'].mode().values[0]}")
print(f"Standard Deviation: {data['hours_of_screen_time'].std()}")

## 25th, 50th, and 75th percentiles of age
print("\nAge percentiles:")
print(f"25th percentile: {data['age'].quantile(0.25)}")
print(f"50th percentile: {data['age'].quantile(0.5)}")
print(f"75th percentile: {data['age'].quantile(0.75)}")

## Proportion of individuals with internet access and chronic condition
data['has_internet_access'] = data['internet_access'].apply(lambda x: x != 'No')
print(f"\nProportion with internet access: {data['has_internet_access'].mean()}")
print(f"Proportion with chronic condition: {data['has_chronic_condition'].mean()}")

## Group by gender and compute average hours_of_screen_time and median monthly_income
income_map = {
    "<5k": 2500,
    "5k–10k": 7500,
    "10k–20k": 15000,
    ">20k": 25000
}
data['monthly_income_numeric'] = data['monthly_income'].map(income_map)
grouped_df = data.groupby('gender')
print("\nAverage hours of screen time by gender:")
print(grouped_df['hours_of_screen_time'].mean())
print("\nMedian monthly income by gender:")
print(grouped_df['monthly_income_numeric'].median())

# Probability & Inference
## Probability that a randomly selected person is over 30 and has internet access
prob_over_30_and_internet = ((data['age'] > 30) & data['has_internet_access']).mean()
print(f"\nProbability of being over 30 and having internet access: {prob_over_30_and_internet}")

## Probability that a randomly selected person is under 25 and does not have a chronic condition
prob_under_25_and_no_chronic = ((data['age'] < 25) & ~data['has_chronic_condition']).mean()
print(f"\nProbability of being under 25 and not having a chronic condition: {prob_under_25_and_no_chronic}")

## Frequency table of monthly_income vs internet_access
print("\nFrequency table of monthly_income vs internet_access:")
print(pd.crosstab(data['monthly_income'], data['internet_access']))

## Percentage of high earners with "Unrestricted" access
high_earners = data[data['monthly_income'] == '>20k']
percentage_unrestricted = (high_earners['internet_access'] == 'Unrestricted').mean()
print(f"\nPercentage of high earners with unrestricted access: {percentage_unrestricted}")

## Hypothesis test: People with chronic conditions have significantly higher screen time than those without
chronic_condition_df = data[data['has_chronic_condition']]
no_chronic_condition_df = data[~data['has_chronic_condition']]
t_stat, p_value = ttest_ind(chronic_condition_df['hours_of_screen_time'], no_chronic_condition_df['hours_of_screen_time'])
print(f"\nP-value for hypothesis test: {p_value}")

# Summary
with open('summary.txt', 'w') as f:
    f.write("Descriptive stats:\n")
    f.write(f"Mean age: {data['age'].mean()}\n")
    f.write(f"Mean hours of screen time: {data['hours_of_screen_time'].mean()}\n")
    f.write(f"Proportion with internet access: {data['has_internet_access'].mean()}\n")
    f.write(f"Proportion with chronic condition: {data['has_chronic_condition'].mean()}\n")
    f.write("\nKey proportions:\n")
    f.write(f"Probability of being over 30 and having internet access: {prob_over_30_and_internet}\n")
    f.write(f"Probability of being under 25 and not having a chronic")