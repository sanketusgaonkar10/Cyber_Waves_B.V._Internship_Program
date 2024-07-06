import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Sample data
data = [
    {'id': 1, 'event': 'SOSP', 'dateStamp': 43831, 'timeStamp': 0.708333, 'voyage_From': 'Port A', 'lat': 34.0522, 'lon': -118.2437, 'imo_num': '9434761', 'voyage_Id': '6', 'allocatedVoyageId': None},
    {'id': 2, 'event': 'EOSP', 'dateStamp': 43831, 'timeStamp': 0.791667, 'voyage_From': 'Port A', 'lat': 34.0522, 'lon': -118.2437, 'imo_num': '9434761', 'voyage_Id': '6', 'allocatedVoyageId': None},
    {'id': 3, 'event': 'SOSP', 'dateStamp': 43832, 'timeStamp': 0.333333, 'voyage_From': 'Port B', 'lat': 36.7783, 'lon': -119.4179, 'imo_num': '9434761', 'voyage_Id': '6', 'allocatedVoyageId': None},
    {'id': 4, 'event': 'EOSP', 'dateStamp': 43832, 'timeStamp': 0.583333, 'voyage_From': 'Port B', 'lat': 36.7783, 'lon': -119.4179, 'imo_num': '9434761', 'voyage_Id': '6', 'allocatedVoyageId': None}
]

df = pd.DataFrame(data)

# Calculate precise UTC date-times for events
df['event_utc'] = pd.to_datetime(df['dateStamp'] - 2, unit='D', origin='1899-12-30') + pd.to_timedelta(df['timeStamp'], unit='D')

# Identify and segment different voyage stages
sosp_events = df[df['event'] == 'SOSP'].reset_index(drop=True)
eosp_events = df[df['event'] == 'EOSP'].reset_index(drop=True)

# Merging SOSP and EOSP events
voyage_segments = pd.merge(sosp_events, eosp_events, left_index=True, right_index=True, suffixes=('_start', '_end'))

# Calculate sailing time in hours
voyage_segments['sailing_time'] = (voyage_segments['event_utc_end'] - voyage_segments['event_utc_start']).dt.total_seconds() / 3600

# Calculate distance between ports
def calculate_distance(row):
    start_coords = (row['lat_start'], row['lon_start'])
    end_coords = (row['lat_end'], row['lon_end'])
    return geodesic(start_coords, end_coords).nautical

voyage_segments['distance_travelled'] = voyage_segments.apply(calculate_distance, axis=1)

# Visualizing the timeline of events
plt.figure(figsize=(12, 6))
plt.plot(voyage_segments['event_utc_start'], np.zeros(len(voyage_segments)), 'go', label='Start of Sea Passage')
plt.plot(voyage_segments['event_utc_end'], np.ones(len(voyage_segments)), 'ro', label='End of Sea Passage')
plt.vlines(voyage_segments['event_utc_start'], 0, 1, colors='gray', linestyles='dotted')
plt.vlines(voyage_segments['event_utc_end'], 0, 1, colors='gray', linestyles='dotted')

for i, row in voyage_segments.iterrows():
    plt.text(row['event_utc_start'], 0.5, f"{row['sailing_time']:.2f} hrs, {row['distance_travelled']:.2f} NM", rotation=90, verticalalignment='center')

plt.xlabel('Event UTC Time')
plt.ylabel('Event')
plt.title('Voyage Event Timeline')
plt.legend()
plt.show()