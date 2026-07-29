import sqlite3
import pandas as pd

DB_PATH = "Data/ChicagoFoodInspection.db"
CSV_PATH = "Data/Step 0 - Raw - Food-Inspections-20251023.csv"

# Read CSV into a DataFrame
df = pd.read_csv(CSV_PATH)

# Connect and create table
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
df.to_sql('raw', conn, if_exists='replace', index=False)
conn.close()

print(f"Loaded {len(df)} rows into {DB_PATH}")
