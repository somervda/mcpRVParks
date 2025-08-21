import pandas as pd
import sqlite3

# Define file and database names
csv_filename = 'merged_RVParks.csv'  # Replace with your actual CSV path
db_filename = 'rvParks.db'
table_name = 'park'

# Step 1: Read CSV using pandas
df = pd.read_csv(csv_filename)


print(df.head())

# Step 3: Convert latitude and longitude to numeric (optional: errors='coerce' turns invalid values to NaN)
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['zip'] = pd.to_numeric(df['zip'], errors='coerce')

# Step 4: Connect to SQLite database
conn = sqlite3.connect(db_filename)

# Step 5: Write data to SQLite table
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Step 6: Close the connection
conn.close()

print(f"Data from '{csv_filename}' has been successfully loaded into '{db_filename}'.")
