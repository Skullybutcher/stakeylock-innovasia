from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# Simulate traffic data
np.random.seed(42)
data = {
    'Hour': np.tile(range(24), 30),
    'Day': np.repeat(range(1, 31), 24),
    'Incoming Point 1': np.random.randint(100, 500, size=720),
    'Outgoing Point 1': np.random.randint(80, 400, size=720),
    'Incoming Point 2': np.random.randint(120, 550, size=720),
    'Outgoing Point 2': np.random.randint(100, 450, size=720),
    'Incoming Point 3': np.random.randint(90, 480, size=720),
    'Outgoing Point 3': np.random.randint(70, 420, size=720),
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate derived columns
df['Total Incoming'] = (
    df['Incoming Point 1'] + df['Incoming Point 2'] + df['Incoming Point 3']
)
df['Total Outgoing'] = (
    df['Outgoing Point 1'] + df['Outgoing Point 2'] + df['Outgoing Point 3']
)

# Simulate Buffers (random variations)
df['Incoming Buffer (Point 1)'] = np.random.uniform(-20, 20, size=720)
df['Outgoing Buffer (Point 1)'] = np.random.uniform(-15, 15, size=720)
df['Incoming Buffer (Point 2)'] = np.random.uniform(-25, 25, size=720)
df['Outgoing Buffer (Point 2)'] = np.random.uniform(-20, 20, size=720)
df['Incoming Buffer (Point 3)'] = np.random.uniform(-30, 30, size=720)
df['Outgoing Buffer (Point 3)'] = np.random.uniform(-25, 25, size=720)

# Target variable: Simulate 'Traffic at Junction'
df['Traffic at Junction'] = (
    df['Total Incoming']
    - df['Total Outgoing']
    + df['Incoming Buffer (Point 1)']
    + df['Outgoing Buffer (Point 1)']
    + df['Incoming Buffer (Point 2)']
    + df['Outgoing Buffer (Point 2)']
    + df['Incoming Buffer (Point 3)']
    + df['Outgoing Buffer (Point 3)']
)

# Features and target
X = df[
    [
        'Total Incoming',
        'Total Outgoing',
        'Incoming Buffer (Point 1)',
        'Outgoing Buffer (Point 1)',
        'Incoming Buffer (Point 2)',
        'Outgoing Buffer (Point 2)',
        'Incoming Buffer (Point 3)',
        'Outgoing Buffer (Point 3)',
        'Day',
        'Hour',
    ]
]
y = df['Traffic at Junction']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Display evaluation metrics
print("Model Evaluation on Test Data:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R² Score (Coefficient of Determination): {r2:.2f}")

# Save the model
joblib.dump(model, 'traffic_ml_model.pkl')

# Save simulated data for testing
df.to_csv('simulated_traffic_data.csv', index=False)


# Calculate accuracy percentage
accuracy = 100 - (mae / y_test.mean() * 100)
print(f"Estimated Prediction Accuracy: {accuracy:.2f}%")


# Visualize actual vs predicted traffic
plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label="Actual Traffic", color='blue', linestyle='--')
plt.plot(y_pred, label="Predicted Traffic", color='red', alpha=0.7)
plt.title("Actual vs Predicted Traffic at the Junction (30 days)")
plt.xlabel("Test Data Points")
plt.ylabel("Traffic")
# plt.text("Model Evaluation on Test Data:")
# plt.text(f"Mean Absolute Error (MAE): {mae:.2f}")
# plt.text(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
# plt.text(f"R² Score (Coefficient of Determination): {r2:.2f}")
metrics_text = f"MAE: {mae:.2f}\nRMSE: {rmse:.2f}\nR²: {r2:.2f}\nAccuracy: {accuracy:.2f}%"

# Place the metrics text box at a specific location in axes coordinates (top-right)
plt.text(0.95, 0.95, metrics_text, horizontalalignment='right', verticalalignment='top',
         transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=1'))


plt.legend()
plt.grid(True)
plt.savefig('graph-30', dpi=300, bbox_inches='tight')
plt.show()
