import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import folium
from sqlalchemy import text
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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




# First, let's make a copy to avoid SettingWithCopyWarning
df_cleaned = df.copy()

# Convert 'agtron_ground' to numeric
# 'coerce' will turn any non-convertible values into NaN (Not a Number)
df_cleaned['agtron_ground'] = pd.to_numeric(df_cleaned['agtron_ground'], errors='coerce')

# Convert 'agtron_roast' to numeric
df_cleaned['agtron_roast'] = pd.to_numeric(df_cleaned['agtron_roast'], errors='coerce')

# Drop NaN values (we will need this to construct our linear regression equation yhat)
df_cleaned.dropna(subset=['agtron_ground', 'agtron_roast'], inplace=True)

width = 12
height = 12
plt.figure(figsize=(width, height))
sns.regplot(x="agtron_ground", y="agtron_roast", data=df_cleaned)
plt.ylim(0,)
plt.show() # Add plt.show() to display the plot if you're not seeing it automatically


lm = LinearRegression()
X = df_cleaned[['agtron_ground']]
Y = df_cleaned['agtron_roast']
lm.fit(X,Y)
yhat=lm.predict(X)

#lm.intercept_.round(2)
#lm.coef_.round(2)
print('The R-square is: ', lm.score(X,Y))

width = 15
height = 15
plt.figure(figsize=(width, height))
sns.regplot(x="agtron_ground", y="agtron_roast", data=df_cleaned)
plt.ylim(0,)
plt.annotate('Massive Outlier',
             xy=(50, 700),           # Coordinates of the point
             xytext=(40, 700),       # Where the label appears
             fontsize=20,
             color='red')
plt.show() # Add plt.show() to display the plot if you're not seeing it automatically

mse = mean_squared_error(df_cleaned['agtron_roast'], yhat)
print('The mean square error of agtron_roast and predicted value is: ', mse)
print(df_cleaned['agtron_roast'].max())
print(df_cleaned[df_cleaned['agtron_roast'] == 689.0])
df_cleaned.drop(df_cleaned[df_cleaned['agtron_roast'] == 689.0].index, inplace=True)

width = 15
height = 15
plt.figure(figsize=(width, height))
sns.regplot(x="agtron_ground", y="agtron_roast", data=df_cleaned)
plt.ylim(0,)
plt.show() # Add plt.show() to display the plot if you're not seeing it automatically

width = 15
height = 15
plt.figure(figsize=(width, height))
sns.residplot(x=df_cleaned['agtron_ground'], y=df_cleaned['agtron_roast'])
plt.show()

lm = LinearRegression()
X = df_cleaned[['agtron_ground']]
Y = df_cleaned['agtron_roast']
lm.fit(X,Y)

yhat=lm.predict(X)

print('The R-square is: ', lm.score(X,Y))

mse = mean_squared_error(df_cleaned['agtron_roast'], yhat)
print('The mean square error of agtron_roast and predicted value is: ', mse)

df_corr = df_cleaned[['agtron_ground','agtron_roast']]
print(df_corr.corr())