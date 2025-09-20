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

# Split data
df_historic = df[df['Source'] == 'Historic'].copy()
df_forecast = df[df['Source'] == 'Forecast'].copy()

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df_historic['Date'], df_historic['Bookings Unified'], label='Historic', color='blue')
plt.plot(df_forecast['Date'], df_forecast['Bookings Unified'], label='Forecast', color='orange')
plt.fill_between(
    df_forecast['Date'],
    df_forecast['Lower Bound'],
    df_forecast['Upper Bound'],
    color='orange', alpha=0.2, label='95% Prediction Interval'
)

plt.title('Daily Short-Term Rental Bookings (Historic and Forecast)')
plt.xlabel('Date')
plt.ylabel('Daily Bookings')
plt.legend()
plt.tight_layout()
plt.show()