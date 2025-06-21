from sqlalchemy import create_engine
import pandas as pd

#connection string
engine = create_engine('postgresql://postgres:anirudh9@localhost:5432/postgres')

# SQL query
query = """
SELECT * FROM top_rated_coffee_clean;
"""

# Run the query
df = pd.read_sql_query(query, engine)
df = df.drop(index=0).reset_index() # Dropping the first row (as it is the same as the headers)
print(df.head()) # Display the first five rows

# SQL query
query2 = """
SELECT roast_level, COUNT(roast_level) FROM top_rated_coffee_clean GROUP BY roast_level;
"""

# Run the query
df2 = pd.read_sql_query(query2, engine)
df2 = df2.reset_index(drop=True)
df2 = df2.drop(index=0).reset_index(drop=True) # Dropping the first row (as it is useless)
df2 = df2.drop(index=1).reset_index(drop=True) # Dropping the first row (as it is useless)

df['roast_level2'] = df2['roast_level']
df['roast_level_count'] = df2['count']

# SQL query
query3 = """
SELECT total_score, COUNT(total_score) FROM top_rated_coffee_clean GROUP BY total_score;
"""

# Run the query
df3 = pd.read_sql_query(query3, engine)
df3 = df3.drop(index=0).reset_index(drop=True)
df3 = df3.drop(index=3).reset_index(drop=True)

df['total_score2'] = df3['total_score']
df['total_score_count'] = df3['count']

df.to_csv('updated_top_rated_coffee.csv')