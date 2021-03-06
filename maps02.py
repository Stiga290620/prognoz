import pandas as pd
import numpy as np
import folium
import json

centroid_lat = 16.7
centroid_lon = 81.095

x = .01

n = 10

o_lats = np.random.uniform(low=centroid_lat - x, high=centroid_lat + x, size=(n,))
o_lons = np.random.uniform(low=centroid_lon - x, high=centroid_lon + x, size=(n,))
d_lats = np.random.uniform(low=centroid_lat - x, high=centroid_lat + x, size=(n,))
d_lons = np.random.uniform(low=centroid_lon - x, high=centroid_lon + x, size=(n,))

df = pd.DataFrame({'origin_lng' : o_lons, 'origin_lat' : o_lats,
                   'destination_lng': d_lons, 'destination_lat': d_lats})

print(df.head())

m = folium.Map([centroid_lat, centroid_lon], zoom_start=11)

for _, row in df.iterrows():
    folium.CircleMarker([row['origin_lat'], row['origin_lng']],
                        radius=15,
                        fill_color="#3db7e4", # divvy color
                        ).add_to(m)

    folium.CircleMarker([row['destination_lat'], row['destination_lng']],
                        radius=15,
                        fill_color="red", # divvy color
                        ).add_to(m)

    folium.PolyLine([[row['origin_lat'], row['origin_lng']],
                     [row['destination_lat'], row['destination_lng']]]).add_to(m)


m.save("map0001.html")
cache1 = "map0001.html"
with open(cache1, 'r') as f:
    txtx = f.read()
