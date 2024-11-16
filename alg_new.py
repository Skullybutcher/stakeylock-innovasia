import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to predict traffic at the junction based on incoming, outgoing, and buffer values
def predict_traffic(incoming, outgoing, buffer_in, buffer_out):
    total_incoming = sum(incoming) + sum(buffer_in)  # Include rerouted incoming traffic to the junction
    total_outgoing = sum(outgoing) + sum(buffer_out)  # Include rerouted outgoing traffic from the junction
    
    total_traffic = total_incoming - total_outgoing  # Net traffic at the junction
    
    # Simulate traffic variation with normal distribution (you can adjust standard deviation)
    net_traffic = np.random.normal(total_traffic, np.std([total_incoming, total_outgoing]))
    
    return net_traffic

# Read the Excel file
df = pd.read_excel('ddata.xlsx')

# Ensure there are no missing values in the relevant columns
df = df.dropna(subset=['Total Incoming', 'Total Outgoing'])

# Clean column names by stripping extra spaces
df.columns = df.columns.str.strip()

# Add a new column for the predicted traffic at the junction
df['Predicted Traffic at Junction'] = np.nan

# Implement the prediction algorithm for traffic at the junction
for i in range(24, len(df)):
    # Extract the last 24 hours of incoming and outgoing traffic data
    window_incoming = df.iloc[i-24:i][['Incoming (Point 1)', 'Incoming (Point 2)', 'Incoming (Point 3)']].sum(axis=1).tolist()
    window_outgoing = df.iloc[i-24:i][['Outgoing (Point 1)', 'Outgoing (Point 2)', 'Outgoing (Point 3)']].sum(axis=1).tolist()
    
    # Handle missing or undefined buffer columns if necessary
    # Check if buffer columns exist, otherwise use default (zero buffer) for simulation
    buffer_columns_in = ['Incoming Buffer (Point 1)', 'Incoming Buffer (Point 2)', 'Incoming Buffer (Point 3)']
    buffer_columns_out = ['Outgoing Buffer (Point 1)', 'Outgoing Buffer (Point 2)', 'Outgoing Buffer (Point 3)']
    
    # If the buffer columns exist, extract the data
    if all(col in df.columns for col in buffer_columns_in) and all(col in df.columns for col in buffer_columns_out):
        buffer_in = df.iloc[i-24:i][buffer_columns_in].sum(axis=1).tolist()
        buffer_out = df.iloc[i-24:i][buffer_columns_out].sum(axis=1).tolist()
    else:
        # If buffer columns are missing, assume no rerouting (buffer = 0)
        buffer_in = [0] * 3
        buffer_out = [0] * 3
    
    # Predict traffic at the junction using the provided function
    df.at[i, 'Predicted Traffic at Junction'] = predict_traffic(window_incoming, window_outgoing, buffer_in, buffer_out)

# Use 'Day' and 'Hour' columns for analysis
df['Day'] = df['Day'].astype(str)  # Ensure 'Day' is a string
df['Hour'] = df['Hour'].astype(int)  # Ensure 'Hour' is an integer

# Aggregate data for weekly analysis
weekly_traffic = df.groupby('Day')['Predicted Traffic at Junction'].sum()

# Aggregate data for daily (hourly) analysis
hourly_traffic = df.groupby('Hour')['Predicted Traffic at Junction'].mean()

# Plot weekly traffic patterns at the junction
plt.figure(figsize=(10, 6))
weekly_traffic.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Weekly Traffic Analysis at the Junction')
plt.xlabel('Day of the Week')
plt.ylabel('Total Predicted Traffic')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Plot hourly traffic patterns at the junction
plt.figure(figsize=(10, 6))
hourly_traffic.plot(kind='line', marker='o', color='orange')
plt.title('Hourly Traffic Analysis at the Junction')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Predicted Traffic')
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.show()

# Save the updated DataFrame to a new Excel file with predictions
df.to_excel('updated_traffic_analysis.xlsx', index=False)
