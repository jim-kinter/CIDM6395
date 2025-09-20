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

# Combine into Bookings Unified
bookings['Bookings Unified'] = bookings['Bookings']
predictions['Bookings Unified'] = predictions['Bookings Forecast']

# Drop original columns
bookings = bookings.drop(columns=['Bookings'])
predictions = predictions.drop(columns=['Bookings Forecast'])

# Merge
df = pd.concat([bookings, predictions], ignore_index=True)

# Filter historic data
df_historic = df[df['Source'] == 'Historic'].copy()

# Calculate average bookings by day of week
day_avg = df_historic.groupby('Day')['Bookings Unified'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
).reset_index()

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=day_avg, x='Day', y='Bookings Unified', color='blue')

plt.title('Average Daily Short-Term Rental Bookings by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Daily Bookings')
plt.tight_layout()
plt.show()