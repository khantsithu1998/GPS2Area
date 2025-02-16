import json
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
from math import radians, sin
from shapely.geometry import Polygon
from pyproj import Proj, Transformer

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def convert_gps_to_cartesian(latitudes, longitudes):
    x, y = [0], [0]
    for i in range(1, len(latitudes)):
        x.append(haversine_distance(latitudes[0], longitudes[0], latitudes[i], longitudes[0]))
        y.append(haversine_distance(latitudes[0], longitudes[0], latitudes[0], longitudes[i]))
    return np.array(x), np.array(y)

def compute_area_trapezoidal(x, y):
    return abs(np.trapz(y, x))

def compute_area_shoelace(x, y):
    return 0.5 * abs(sum(x[i] * y[i + 1] - x[i + 1] * y[i] for i in range(len(x) - 1)))

def compute_area_spherical(latitudes, longitudes):
    """Calculate the exact area on a spherical Earth."""
    R = 6371000  # Earth's radius in meters
    area = 0
    for i in range(len(latitudes) - 1):
        lat1, lon1 = radians(latitudes[i]), radians(longitudes[i])
        lat2, lon2 = radians(latitudes[i+1]), radians(longitudes[i+1])
        area += (lon2 - lon1) * (sin(lat1) + sin(lat2)) / 2
    return abs(area * R**2)

def compute_area_gis(latitudes, longitudes):
    """Compute exact area using Shapely with UTM projection."""
    if len(latitudes) < 3:
        return 0.0
    avg_lat = sum(latitudes) / len(latitudes)
    avg_lon = sum(longitudes) / len(longitudes)
    proj = Proj(proj="utm", zone=int((avg_lon + 180) / 6) + 1, ellps="WGS84")
    transformer = Transformer.from_proj("epsg:4326", proj, always_xy=True)
    utm_coords = [transformer.transform(lon, lat) for lat, lon in zip(latitudes, longitudes)]
    polygon = Polygon(utm_coords)
    return polygon.area

def get_user_coordinates():
    latitudes, longitudes = [], []
    print("\n📍 Enter GPS coordinates (latitude longitude). Type 'done' when finished.")
    while True:
        user_input = input("Enter latitude and longitude (or 'done' to finish): ")
        if user_input.lower() == 'done':
            break
        try:
            lat, lon = map(float, user_input.split())
            latitudes.append(lat)
            longitudes.append(lon)
        except ValueError:
            print("❌ Invalid input! Enter two numbers separated by space.")
    if len(latitudes) < 3:
        raise ValueError("A shape must have at least 3 points.")
    latitudes.append(latitudes[0])
    longitudes.append(longitudes[0])
    return latitudes, longitudes

def save_to_geojson(latitudes, longitudes, filename="shapes.geojson"):
    coordinates = [[lon, lat] for lat, lon in zip(latitudes, longitudes)]
    geojson_data = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "User-defined shape"}, "geometry": {"type": "Polygon", "coordinates": [coordinates]}}]}
    with open(filename, "w") as geojson_file:
        json.dump(geojson_data, geojson_file, indent=4)
    print(f"\n✅ Shape saved as {filename}")

def plot_shape(x, y):
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', label="User Shape", color="blue")
    plt.fill(x, y, color="cyan", alpha=0.3, label="Enclosed Area")
    plt.xlabel("X Distance (meters)")
    plt.ylabel("Y Distance (meters)")
    plt.legend()
    plt.title("Computed Area of Irregular Shape")
    plt.grid(True)
    plt.show()

try:
    latitudes, longitudes = get_user_coordinates()
    x, y = convert_gps_to_cartesian(latitudes, longitudes)
    area_trapezoidal = compute_area_trapezoidal(x, y)
    area_shoelace = compute_area_shoelace(x, y)
    area_spherical = compute_area_spherical(latitudes, longitudes)
    area_gis = compute_area_gis(latitudes, longitudes)
    print(f"\n✅ Estimated Area using Trapezoidal Rule: {area_trapezoidal:.2f} m²")
    print(f"✅ Estimated Area using Shoelace Theorem: {area_shoelace:.2f} m²")
    print(f"🌍 Exact Area using Spherical Polygon Method: {area_spherical:.2f} m²")
    print(f"📍 True GIS-Calculated Area: {area_gis:.2f} m²")
    save_to_geojson(latitudes, longitudes)
    plot_shape(x, y)
except Exception as e:
    print(f"❌ Error: {e}")
g