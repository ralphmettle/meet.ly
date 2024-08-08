import folium
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Define a function that takes a nested list with the stucture [[lat, long], [lat, long], ...] as the input
# Convert the lists to a numpy array
# Define a k-means with a single cluster and fit the location data
# Return the centre point of the cluster as [lat, long]

test_coordinates = [
  [51.5074, -0.1278],  # Central London
  [51.5154, -0.1410],  # Near Oxford Circus
  [51.5115, -0.1197],  # Covent Garden
  [51.5033, -0.1195],  # Trafalgar Square
  [51.5194, -0.1270],  # British Museum
  [51.5085, -0.1257],  # London Eye
  [51.5077, -0.0894],  # Tower Bridge
]
def coordinate_builder(data):
    coordinates = []
    
    for i in data:
        coordinates.append([i['latitude'], i['longitude']])
    return coordinates

def location_clustering(locations):
    locations_to_array = np.array(locations)

    kmeans = KMeans(n_clusters=1, random_state=0)
    kmeans.fit(locations_to_array)

    central_location = kmeans.cluster_centers_[0]
    return central_location.tolist()

def location_visualiser(locations, central_location):
  map = folium.Map(location=central_location, zoom_start=12)

  for location in locations:
    folium.Marker(location).add_to(map)

  folium.Marker(central_location, icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')).add_to(map)
  folium.Circle(central_location, radius=1500, color='#219fff', fill=True, fillOpacity=0.2).add_to(map)

  map.save('map.html')

test = location_clustering(test_coordinates)

if __name__ == '__main__':
  location_visualiser(test_coordinates, test)
