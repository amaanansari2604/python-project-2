import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('311_Service_Requests_from_2010_to_Present.csv')

# Convert date columns to datetime datatype
df['Created Date'] = pd.to_datetime(df['Created Date'])
df['Closed Date'] = pd.to_datetime(df['Closed Date'])

# Create new column 'Request_Closing_Time' as the time elapsed between request creation and request closing
df['Request_Closing_Time'] = df['Closed Date'] - df['Created Date']

# Visualization of major complaint types using a bar chart
complaint_types = df['Complaint Type'].value_counts().head(10)
plt.bar(complaint_types.index, complaint_types.values)
plt.xticks(rotation=90)
plt.xlabel('Complaint Type')
plt.ylabel('Number of Complaints')
plt.title('Top 10 Complaint Types')
plt.show()

# Order the complaint types based on the average 'Request_Closing_Time', grouping them for different locations
grouped = df.groupby(['Complaint Type', 'City'], as_index=False).agg({'Request_Closing_Time': 'mean'})
grouped = grouped.sort_values(by='Request_Closing_Time', ascending=False)
print(grouped.head())

# Statistical test to check if the average response time across complaint types is similar or not
from scipy.stats import f_oneway

complaints = df['Complaint Type'].unique()
complaints_data = []

for complaint in complaints:
    data = df[df['Complaint Type'] == complaint]['Request_Closing_Time'].dt.total_seconds()
    complaints_data.append(data)

f, p = f_oneway(*complaints_data)
print(f"The F-statistic is {f} and the p-value is {p}")
