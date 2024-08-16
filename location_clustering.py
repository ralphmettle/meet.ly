import folium
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def coordinate_builder(coordinates):
    return [[coordinate['latitude'], coordinate['longitude']] for coordinate in coordinates]

def location_clustering(coordinate_list):
    list_to_array = np.array(coordinate_list)

    kmeans = KMeans(n_clusters=1, random_state=0)
    kmeans.fit(list_to_array)

    central_coordinates = kmeans.cluster_centers_[0]
    return central_coordinates.tolist()

def location_visualiser(coordinates, central_coordinates):
  map = folium.Map(location=central_coordinates, zoom_start=12)

  for coordinate in coordinates:
    folium.Marker(coordinate).add_to(map)

  folium.Marker(central_coordinates, icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')).add_to(map)
  folium.Circle(central_coordinates, radius=1500, color='#219fff', fill=True, fillOpacity=0.2).add_to(map)

  map.save('map.html')

if __name__ == '__main__':
  test_coordinates = [
  [51.5074, -0.1278],
  [51.5154, -0.1410],
  [51.5115, -0.1197],
  [51.5033, -0.1195],
  [51.5194, -0.1270],
  [51.5085, -0.1257],
  [51.5077, -0.0894],
  ]
  
  test = location_clustering(test_coordinates)
  location_visualiser(test_coordinates, test)
