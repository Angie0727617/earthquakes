# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

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
    

    max_earthquake = max(earthquakes, key=get_magnitude)
    max_magnitude = get_magnitude(max_earthquake)
    max_location = get_location(max_earthquake)
    
    return max_magnitude, max_location


def get_year(earthquake):
    timestamp = earthquake['properties']['time']
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.year


def earthquakes_per_year(data):
    earthquakes = data['features']
    years = [get_year(eq) for eq in earthquakes]
    
    yearly_counts = pd.Series(years).value_counts().sort_index()
    return yearly_counts


def average_magnitude_per_year(data):
    earthquakes = data['features']
    
    year_mag_pairs = []
    for eq in earthquakes:
        year = get_year(eq)
        magnitude = get_magnitude(eq)
        year_mag_pairs.append((year, magnitude))
    
    df = pd.DataFrame(year_mag_pairs, columns=['year', 'magnitude'])
    yearly_avg_mag = df.groupby('year')['magnitude'].mean()
    
    return yearly_avg_mag


def plot_frequency(yearly_counts, save_path='earthquake_frequency.png'):
    plt.figure(figsize=(12, 6))
    
    plt.bar(yearly_counts.index, yearly_counts.values, 
            color='skyblue', edgecolor='navy', alpha=0.7)
    
    plt.title('Earthquake Frequency Per Year (2000-2018)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Earthquakes', fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.xticks(rotation=45)
    
    for i, count in enumerate(yearly_counts.values):
        plt.text(yearly_counts.index[i], count + 0.1, str(count), 
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✅ Saved: {save_path}")
    return save_path


def plot_magnitude(yearly_avg_mag, save_path='average_magnitude.png'):
    plt.figure(figsize=(12, 6))
    
    plt.plot(yearly_avg_mag.index, yearly_avg_mag.values, 
             marker='o', linewidth=2, markersize=6, 
             color='coral', markerfacecolor='red', markeredgecolor='darkred')
    
    plt.title('Average Earthquake Magnitude Per Year (2000-2018)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Magnitude', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    for year, mag in yearly_avg_mag.items():
        plt.text(year, mag + 0.01, f'{mag:.2f}', 
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✅ Saved: {save_path}")
    return save_path


def main():
    print("=== Start analyse ===")
    
    print("loading...")
    data = get_data()
    total_earthquakes = count_earthquakes(data)
    print(f"✅ seccussed {total_earthquakes} cases")

    max_magnitude, max_location = get_maximum(data)
    print(f"💥 Max: magnitude {max_magnitude}, location {max_location}")
    
    print("\nLoading...")
    yearly_counts = earthquakes_per_year(data)
    print("amount per year:")
    for year, count in yearly_counts.items():
        print(f"  {year}: {count} times earthquakes")
    
    print("\nLoading...")
    yearly_avg_mag = average_magnitude_per_year(data)
    print("Average magnitude:")
    for year, avg_mag in yearly_avg_mag.items():
        print(f"  {year}: {avg_mag:.2f}")

    print("\nLoading...")
    freq_plot_path = plot_frequency(yearly_counts)
    mag_plot_path = plot_magnitude(yearly_avg_mag)
    
    print(f"\n🎉 Finished!")
    print(f"📊 frequence: {freq_plot_path}")
    print(f"📈 magnitude: {mag_plot_path}")
    
    return yearly_counts, yearly_avg_mag



if __name__ == "__main__":
    yearly_counts, yearly_avg_mag = main()