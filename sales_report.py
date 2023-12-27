import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# Connect to the database
conn = sqlite3.connect('path_to_your_database')

# Retrieve the data
query = "SELECT total_amount, date_added FROM purchases;"
df = pd.read_sql_query(query, conn)

# Convert 'date_added' column to datetime type
df['date_added'] = pd.to_datetime(df['date_added'])

# Group the data by month and calculate total sales
monthly_sales = df.groupby(df['date_added'].dt.to_period('M')).sum()

# Generate a graph
monthly_sales.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Monthly Sales')
plt.xticks(rotation=45)
plt.show()

# Close the database connection
conn.close()
