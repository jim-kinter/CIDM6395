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

# Combine Bookings and Bookings Forecast into Bookings Unified
bookings['Bookings Unified'] = bookings['Bookings']
predictions['Bookings Unified'] = predictions['Bookings Forecast']

# Drop original columns
bookings = bookings.drop(columns=['Bookings'])
predictions = predictions.drop(columns=['Bookings Forecast'])

# Merge
df = pd.concat([bookings, predictions], ignore_index=True)

# Create Month-Year column
df['Month-Year'] = df['Date'].dt.strftime('%m %Y')

# Calculate monthly averages
monthly_avg = df.groupby(['Month-Year', 'Source'])['Bookings Unified'].mean().reset_index()

# For forecast data, calculate prediction intervals
forecast_monthly = df[df['Source'] == 'Forecast'].groupby('Month-Year').agg({
    'Bookings Unified': 'mean',
    'Lower Bound': 'mean',
    'Upper Bound': 'mean'
}).reset_index()

# Rename for plotting
monthly_avg = monthly_avg.rename(columns={'Bookings Unified': 'Average Bookings'})
forecast_monthly = forecast_monthly.rename(columns={'Bookings Unified': 'Average Bookings'})

# Sort by date for chronological order
monthly_avg['Date'] = pd.to_datetime(monthly_avg['Month-Year'], format='%m %Y')
monthly_avg = monthly_avg.sort_values('Date')

# Plot
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly_avg, x='Month-Year', y='Average Bookings', hue='Source', palette=['blue', 'orange'], marker='o')

# Add 95% prediction interval for forecast months
forecast_months = monthly_avg[monthly_avg['Source'] == 'Forecast'].merge(
    forecast_monthly[['Month-Year', 'Lower Bound', 'Upper Bound']],
    on='Month-Year',
    how='left'
)

plt.errorbar(
    forecast_months['Month-Year'],
    forecast_months['Average Bookings'],
    yerr=[
        forecast_months['Average Bookings'] - forecast_months['Lower Bound'],
        forecast_months['Upper Bound'] - forecast_months['Average Bookings']
    ],
    fmt='none', ecolor='orange', capsize=5, label='95% Prediction Interval'
)

plt.title('Average Daily Short-Term Rental Bookings by Month')
plt.xlabel('Month-Year')
plt.ylabel('Average Daily Bookings')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()