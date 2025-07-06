import sqlite3

# Connect to your database
conn = sqlite3.connect("news.db")
cursor = conn.cursor()

# See what tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in DB:", cursor.fetchall())

# Fetch all rows from your table (e.g., articles)
cursor.execute("SELECT * FROM articles;")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
