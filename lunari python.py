# -*- coding: utf-8 -*-
"""Lunari

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11-8tJqDZ8rJVVo5TRdoaqTV-GB30ayPD
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import plot_tree
from sklearn.datasets import make_regression

# Set random seed for reproducibility
np.random.seed(0)

# Parameters
num_samples = 1000
ages = np.random.randint(13, 52, num_samples)
ethnicities = np.random.choice(['Black', 'East Asian', 'Hispanic', 'South Asian', 'White'], num_samples)
bmis = np.random.uniform(18, 25, num_samples)
phases = np.random.choice(['late luteal', 'menstruation', 'late follicular', 'mid luteal', 'ovulation'], num_samples)

# Function to generate nutrient values based on phase, age, BMI, and ethnicity
def generate_nutrient_values(menstrual_phase, age, bmi, ethnicity):
    # Base nutrient percentages that sum to 100 for each phase
    nutrient_values = {
        'MoodStable': 0,
        'Iron': 0,
        'Antioxy': 0,
        'Omega-3': 0,
        'Cramps': 0,
        'Hormonal Balance': 0,
        'Reducing Inflammation': 0,
        'Hydration': 0
    }

    # Nutritional needs by phase (percentages summing to 100)
    if menstrual_phase == 'ovulation':
        nutrient_values = {
            'MoodStable': 30,
            'Hormonal Balance': 25,
            'Omega-3': 20,
            'Hydration': 15,
            'Antioxy': 5,
            'Reducing Inflammation': 5,
            'Cramps': 0,
            'Iron': 0
        }

    elif menstrual_phase == 'late follicular':
        nutrient_values = {
            'MoodStable': 25,
            'Iron': 15,
            'Antioxy': 25,
            'Reducing Inflammation': 15,
            'Cramps': 5,
            'Hormonal Balance': 5,
            'Omega-3': 5,
            'Hydration': 5
        }

    elif menstrual_phase == 'mid luteal':
        nutrient_values = {
            'MoodStable': 25,
            'Hormonal Balance': 30,
            'Cramps': 15,
            'Hydration': 10,
            'Antioxy': 10,
            'Reducing Inflammation': 5,
            'Omega-3': 5,
            'Iron': 0
        }

    elif menstrual_phase == 'late luteal':
        nutrient_values = {
            'MoodStable': 20,
            'Iron': 15,
            'Cramps': 20,
            'Reducing Inflammation': 15,
            'Hormonal Balance': 10,
            'Omega-3': 5,
            'Hydration': 5,
            'Antioxy': 5
        }

    elif menstrual_phase == 'menstruation':
        nutrient_values = {
            'MoodStable': 15,
            'Iron': 30,
            'Cramps': 25,
            'Hydration': 10,
            'Antioxy': 10,
            'Reducing Inflammation': 5,
            'Omega-3': 5,
            'Hormonal Balance': 0
        }

    # Adjust based on age and BMI
    age_adjustment = (age - 20) * 0.5  # Simplified age factor
    bmi_adjustment = (25 - bmi) * 0.5  # Higher BMI lowers some values

    # Apply adjustments to nutrient values
    adjusted_values = {}

    for key in nutrient_values:
        adjusted_value = nutrient_values[key] + age_adjustment + bmi_adjustment
        adjusted_values[key] = max(adjusted_value, 0)  # Ensure no negative values

    # Normalize to ensure the percentages add up to 100
    total = sum(adjusted_values.values())
    if total > 0:
        for key in adjusted_values:
            adjusted_values[key] = (adjusted_values[key] / total) * 100

    return adjusted_values

# Generate data
data = []
for i in range(num_samples):
    phase = phases[i]
    nutrient_values = generate_nutrient_values(phase, ages[i], bmis[i], ethnicities[i])
    data.append([
        ages[i],
        ethnicities[i],
        round(bmis[i], 1),
        phase,
        nutrient_values['MoodStable'],
        nutrient_values['Iron'],
        nutrient_values['Antioxy'],
        nutrient_values['Omega-3'],
        nutrient_values['Cramps'],
        nutrient_values['Hormonal Balance'],
        nutrient_values['Reducing Inflammation'],
        nutrient_values['Hydration']
    ])

# Create DataFrame
columns = ['Age', 'Ethnicity', 'BMI', 'Menstrual Phase', 'MoodStable', 'Iron', 'Antioxy', 'Omega-3', 'Cramps', 'Hormonal Balance', 'Reducing Inflammation', 'Hydration']
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('refined_menstrual_nutrition_data.csv', index=False)

"""# New Section"""

#convert categorical variables into numerical format
label_encoder_ethnicity = LabelEncoder()
df['Ethnicity'] = label_encoder_ethnicity.fit_transform(df['Ethnicity'])

label_encoder_phase = LabelEncoder()
df['Menstrual Phase'] = label_encoder_phase.fit_transform(df['Menstrual Phase'])

print("Known ethnicity categories:", label_encoder_ethnicity.classes_)

# Separate features and target variables
X = df[['Age', 'Ethnicity', 'BMI', 'Menstrual Phase']]
y = df[['MoodStable', 'Iron', 'Antioxy', 'Omega-3', 'Cramps', 'Hormonal Balance', 'Reducing Inflammation', 'Hydration']]

# Standardize the features using the same scaler from training
scaler = StandardScaler()
X.loc[:, ['Age', 'BMI']] = scaler.fit_transform(X[['Age', 'BMI']])

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a multi-output regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate using Mean Squared Error
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
print("Mean Squared Error for each food group:", mse)

# New sample data
new_data = pd.DataFrame({
    'Age': [19],
    'Ethnicity': ['South Asian'],
    'BMI': [19],
    'Menstrual Phase': ['late luteal']
})

new_data['Ethnicity'] = label_encoder_ethnicity.transform(new_data['Ethnicity'])
new_data['Menstrual Phase'] = label_encoder_phase.transform(new_data['Menstrual Phase'])
new_data[['Age', 'BMI']] = scaler.transform(new_data[['Age', 'BMI']])

# Predict percentages for each food group
predicted_percentages = model.predict(new_data)
print("Predicted Food Group Percentages:", predicted_percentages)

#data visualization
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.show()

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)  # RMSE by setting squared=False
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R²):", r2)

X, y = make_regression(n_samples=100, n_features=4, noise=0.1, random_state=42)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the RandomForestRegressor
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Calculate mean squared error for performance evaluation
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Scatter plot of true vs. predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='b')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Line of perfect prediction
plt.xlabel("True Values")
plt.ylabel("Predicted Values")
plt.title("RandomForestRegressor: True vs. Predicted Values")
plt.show()