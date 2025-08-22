import time
import sqlite3
import math
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RVParks")


def distance_between_points(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    
    Inputs are in decimal degrees. Output is in kilometers.
    """
    # Earth radius in kilometers
    earth_radius = 6371

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    diff_lat = lat2 - lat1
    diff_lon = lon2 - lon1

    # Haversine formula
    a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in miles
    distance = earth_radius * c * 0.62
    return distance

def lat_lon_range(latitude, longitude, distance_miles):
    """
    Calculates the latitude and longitude range based on a given point and distance.

    Args:
        latitude (float): Latitude of the center point in degrees.
        longitude (float): Longitude of the center point in degrees.
        distance_miles (float): Distance in miles to calculate the range.

    Returns:
        tuple: A tuple containing the minimum and maximum latitude and longitude
               (min_lat, max_lat, min_lon, max_lon).
    """
    earth_radius_miles = 3959  # Earth radius in miles

    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Angular distance in radians
    angular_distance = distance_miles / earth_radius_miles

    # Calculate minimum and maximum latitude
    min_lat = math.degrees(lat_rad - angular_distance)
    max_lat = math.degrees(lat_rad + angular_distance)

    # Calculate the change in longitude
    delta_lon = math.degrees(math.asin(math.sin(angular_distance) / math.cos(lat_rad)))

    # Calculate minimum and maximum longitude
    min_lon = longitude - delta_lon
    max_lon = longitude + delta_lon

    return (min_lat, max_lat, min_lon, max_lon)

def get_db_connection():
    conn = sqlite3.connect("rvParks.db")
    conn.row_factory = sqlite3.Row  # Enables dict-like access to rows
    return conn

@mcp.tool()
def get_parks_by_distance(latitude: float,longitude:float,miles: int ) -> str:
    """
    Gets a list of Gets a list of all the RV parks in Pennsylvania,New York,
     Delaware and Ohio by distance in miles from a location
    Args:
        latitude: A floating point number for the latitude of a location  
        longitude: A floating point number for the longitude of a location  
        miles: An integer representing how many miles distance 
    """
    # Get all the RV parks within distance-miles of the latitude, longitude provided
    # Test data 40.176415/-75.304980/10
    lat=float(latitude)
    long=float(longitude)
    min_lat, max_lat, min_lon, max_lon = lat_lon_range(lat,long,miles)
    conn = get_db_connection()
    cursor = conn.cursor()
    select =   "SELECT * FROM park where latitude>={:.4f} and latitude <={:.4f} and longitude>={:.4f} and longitude<={:.4f}".format(min_lat, max_lat, min_lon, max_lon)
    print(select)
    cursor.execute(select)
    rows = cursor.fetchall()
    conn.close()
    parks = [dict(row) for row in rows]  # Convert to list of dictionaries items
    parkAndDistance=[]
    for park in parks:
        park['distance']=distance_between_points(lat,long,park.get("latitude"),park.get("longitude"))
        parkAndDistance.append(park)
    return json.dumps(parkAndDistance)

if __name__ == '__main__':
    mcp.run()