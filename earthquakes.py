# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # 可选：保存数据到文件以便查看结构
    with open("earthquakes_data.json", "w") as f:
        f.write(text)
    
    # We need to interpret the text to get values we can work with.
    # What format is the text in? How can we load the values?
    data = json.loads(text)
    return data


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = earthquake['geometry']['coordinates']
    longitude = coordinates[0]
    latitude = coordinates[1]
    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    earthquakes = data['features']
    
    if not earthquakes:
        return 0, (0, 0)
    
    # 找到震级最大的地震
    max_earthquake = max(earthquakes, key=get_magnitude)
    max_magnitude = get_magnitude(max_earthquake)
    max_location = get_location(max_earthquake)
    
    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)} earthquakes")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")