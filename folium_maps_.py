from sqlalchemy import create_engine
import pandas as pd
import folium
import requests

#connection string
engine = create_engine('postgresql://postgres:anirudh9@localhost:5432/postgres')

query = """
SELECT roaster_location, COUNT(roaster_location) FROM top_rated_coffee_clean GROUP BY roaster_location ORDER BY count DESC;
"""

# Run the query
df4 = pd.read_sql_query(query, engine)
df4 = df4.drop(index=0).reset_index(drop=True)
df4 = df4.head(20)

df4['lat'] = None
df4['long'] = None

lat_long_map = {
    "Chia-Yi, Taiwan": {"latitude": 23.4791, "longitude": 120.4404},
    "Taipei, Taiwan": {"latitude": 25.0330, "longitude": 121.5654},
    "San Diego, California": {"latitude": 32.7157, "longitude": -117.1611},
    "Minneapolis, Minnesota": {"latitude": 44.9778, "longitude": -93.2650},
    "Sacramento, California": {"latitude": 38.5816, "longitude": -121.4944},
    "Yilan, Taiwan": {"latitude": 24.7570, "longitude": 121.7516},
    "Floyd, Virginia": {"latitude": 36.9126, "longitude": -80.3306},
    "Topeka, Kansas": {"latitude": 39.0473, "longitude": -95.6752},
    "Lexington, Virginia": {"latitude": 37.7818, "longitude": -79.4447},
    "Boulder, Colorado": {"latitude": 40.0150, "longitude": -105.2705},
    "Chicago, Illinois": {"latitude": 41.8781, "longitude": -87.6298},
    "Jersey City, New Jersey": {"latitude": 40.7282, "longitude": -74.0776},
    "Lee, Massachusetts": {"latitude": 42.2870, "longitude": -73.2384},
    "Ramsey, Minnesota": {"latitude": 45.2636, "longitude": -93.4244},
    "Taoyuan City, Taiwan": {"latitude": 24.9943, "longitude": 121.3010},
    "Taichung, Taiwan": {"latitude": 24.1478, "longitude": 120.6736},
    "Holualoa, Hawai’i": {"latitude": 19.6457, "longitude": -155.9754},
    "Los Angeles, California": {"latitude": 34.0522, "longitude": -118.2437},
    "Taoyuan, Taiwan": {"latitude": 24.9943, "longitude": 121.3010},
    "Acton, Massachusetts": {"latitude": 42.4900, "longitude": -71.4300}
}

for index, row in df4.iterrows():
    location = row['roaster_location']
    df4.loc[index, 'lat'] = lat_long_map[location]['latitude']
    df4.loc[index, 'long'] = lat_long_map[location]['longitude']

# Define the world map
world_map = folium.Map()

# Instantiate a feature group
roasts = folium.map.FeatureGroup()

# Add styled circle markers with popups
for lat, lng, label in zip(df4.lat, df4.long, df4['count']):
    folium.CircleMarker(
        location=[lat, lng],
        radius=5,
        color='yellow',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=str(label)  # make sure label is a string
    ).add_to(roasts)

# Add the feature group to the map
world_map.add_child(roasts)

# add pop-up text to each marker on the map
latitudes = list(df4.lat)
longitudes = list(df4.long)
labels = list(df4['count'])

for lat, lng, label, loc in zip(latitudes, longitudes, labels, df4['roaster_location']):
    folium.Marker([lat, lng], popup=f'Location: {loc}, Count: {label}').add_to(world_map)

# Save to an HTML file
world_map.save('map1.html')


query2 = """
SELECT origin_country, COUNT(origin_country) FROM top_rated_coffee_clean GROUP BY origin_country ORDER BY count DESC;
"""
# Set max column width to display longer entries
pd.set_option('display.max_colwidth', None)

# Run the query
df5 = pd.read_sql_query(query2, engine)
df5 = df5.drop(index=0).reset_index(drop=True)

df5['origin_country'] = df5['origin_country'].replace('Rica', 'Costa Rica')
df5['origin_country'] = df5['origin_country'].replace('Salvador', 'El Salvador')
df5 = df5.drop(index=31)
df5 = df5.drop(index=32)
df5 = df5.head(20)

# URL of the GeoJSON file
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json"

# Download and save it locally
response = requests.get(url)

with open("world_countries.json", "wb") as f:
    f.write(response.content)

print("GeoJSON file downloaded successfully!")

world_geo = r'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json' # geojson file

# create a plain world map
world_map2 = folium.Map(location=[0, 0], zoom_start=2)

# Add choropleth layer
folium.Choropleth(
    geo_data=world_geo,
    data=df5,
    columns=['origin_country', 'count'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Count',
    nan_fill_color='gray'
).add_to(world_map2)

# Show the map
world_map2.save('map2.html')