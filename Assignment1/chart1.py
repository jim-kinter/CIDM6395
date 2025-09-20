import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load both sheets
bookings = pd.read_excel('airbnb.xlsx', sheet_name='bookings')
predictions = pd.read_excel('airbnb.xlsx', sheet_name='predictions')

# Derive missing columns in predictions
predictions['Month'] = predictions['Date'].dt.strftime('%B')
predictions['Year'] = predictions['Date'].dt.year
predictions['Week'] = predictions['Date'].dt.isocalendar().week
predictions['Day'] = predictions['Date'].dt.strftime('%A')

# Add Source column
bookings['Source'] = 'Historic'
predictions['Source'] = 'Forecast'

# Merge
df = pd.concat([bookings, predictions], ignore_index=True)

# Split data
df_historic = df[df['Bookings'].notnull()].copy()
df_forecast = df[df['Bookings Forecast'].notnull()].copy()

# Calculate annual averages for historic data
df_historic['Year'] = df_historic['Date'].dt.year
annual_avg = df_historic.groupby('Year')['Bookings'].mean().reset_index()

# For forecast data, calculate averages and prediction intervals
df_forecast['Year'] = df_forecast['Date'].dt.year
forecast_avg = df_forecast.groupby('Year').agg({
    'Bookings Forecast': 'mean',
    'Lower Bound': 'mean',
    'Upper Bound': 'mean'
}).reset_index()

# Combine data
annual_data = pd.concat([
    annual_avg.rename(columns={'Bookings': 'Average Bookings'}),
    forecast_avg.rename(columns={'Bookings Forecast': 'Average Bookings'})
])

# Add prediction intervals to annual_data
annual_data = annual_data.merge(
    forecast_avg[['Year', 'Lower Bound', 'Upper Bound']],
    on='Year',
    how='left'
)

# Convert Year to string for better x-axis labels
annual_data['Year'] = annual_data['Year'].astype(str)

# Plot
plt.figure(figsize=(8, 5))
sns.lineplot(data=annual_data, x='Year', y='Average Bookings', marker='o', color='blue', label='Average Bookings')

# Add 95% prediction interval as error bars for forecast years
forecast_years = annual_data[annual_data['Lower Bound_y'].notnull()]
plt.errorbar(
    forecast_years['Year'],
    forecast_years['Average Bookings'],
    yerr=[
        forecast_years['Average Bookings'] - forecast_years['Lower Bound_y'],
        forecast_years['Upper Bound_y'] - forecast_years['Average Bookings']
    ],
    fmt='none', ecolor='orange', capsize=5, label='95% Prediction Interval'
)

plt.title('Average Daily Short-Term Rental Bookings by Year')
plt.xlabel('Year')
plt.ylabel('Average Daily Bookings')
plt.grid(False)
plt.legend()
plt.tight_layout()
plt.show()