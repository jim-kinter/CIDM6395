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

# Create Quarter-Year column
df_historic['Quarter-Year'] = df_historic['Date'].dt.to_period('Q').astype(str)
df_forecast['Quarter-Year'] = df_forecast['Date'].dt.to_period('Q').astype(str)

# Calculate quarterly averages for historic data
quarterly_avg = df_historic.groupby('Quarter-Year')['Bookings'].mean().reset_index()

# For forecast data, calculate averages and prediction intervals
forecast_quarterly = df_forecast.groupby('Quarter-Year').agg({
    'Bookings Forecast': 'mean',
    'Lower Bound': 'mean',
    'Upper Bound': 'mean'
}).reset_index()

# Combine data
quarterly_data = pd.concat([
    quarterly_avg.rename(columns={'Bookings': 'Average Bookings'}),
    forecast_quarterly.rename(columns={'Bookings Forecast': 'Average Bookings'})
])
quarterly_data['Source'] = ['Historic'] * len(quarterly_avg) + ['Forecast'] * len(forecast_quarterly)

# Plot
plt.figure(figsize=(10, 5))
sns.lineplot(data=quarterly_data, x='Quarter-Year', y='Average Bookings', hue='Source', palette=['blue', 'orange'], marker='o')

# Add 95% prediction interval for forecast quarters
forecast_quarters = quarterly_data[quarterly_data['Source'] == 'Forecast'].merge(
    forecast_quarterly[['Quarter-Year', 'Lower Bound', 'Upper Bound']],
    on='Quarter-Year',
    how='left'
)

# Debug: Check columns in forecast_quarters
print("Columns in forecast_quarters:", forecast_quarters.columns.tolist())

# Add error bars with corrected column names
plt.errorbar(
    forecast_quarters['Quarter-Year'],
    forecast_quarters['Average Bookings'],
    yerr=[
        forecast_quarters['Average Bookings'] - forecast_quarters['Lower Bound_y'],
        forecast_quarters['Upper Bound_y'] - forecast_quarters['Average Bookings']
    ],
    fmt='none', ecolor='orange', capsize=5, label='95% Prediction Interval'
)

plt.title('Average Daily Short-Term Rental Bookings by Quarter')
plt.xlabel('Quarter-Year')
plt.ylabel('Average Daily Bookings')
plt.xticks(rotation=45)
plt.grid(False)
plt.legend()
plt.tight_layout()
plt.show()