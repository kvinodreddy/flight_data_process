import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

base_path = os.path.join(os.getcwd(), "tmp", "flights")

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def analyze_flight_data():
    all_flights = pd.DataFrame()
    start_time = datetime.now()

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(folder_path, file_name)
                    flights_df = process_file(file_path)
                    all_flights = pd.concat([all_flights, flights_df], ignore_index=True)

    end_time = datetime.now()
    total_run_duration = (end_time - start_time).total_seconds()

    clean_flights = all_flights.dropna(subset=['date', 'origin_city', 'destination_city', 'flight_duration_secs', 'num_passengers'])

    total_records = all_flights.shape[0]
    dirty_records = total_records - clean_flights.shape[0]

    flight_durations = clean_flights.groupby('destination_city')['flight_duration_secs'].agg(['mean', lambda x: np.percentile(x, 95)])
    flight_durations.columns = ['avg_duration', 'p95_duration']

    passenger_arrival = clean_flights.groupby('destination_city')['num_passengers'].sum()
    passenger_departure = clean_flights.groupby('origin_city')['num_passengers'].sum()

    top_25_destinations = passenger_arrival.nlargest(25)
    max_arrival_city = passenger_arrival.idxmax()
    max_departure_city = passenger_departure.idxmax()

    result = {
        "processed_records_count": total_records,
        "dirty_records": dirty_records,
        "total_run_duration_seconds": total_run_duration,
        "destination_stats": flight_durations.loc[top_25_destinations.index].reset_index(),
        "max_passengers_arrived_city": max_arrival_city,
        "max_passengers_left_city": max_departure_city
    }

    return result


result = analyze_flight_data()

print(f"Total records processed: {result['processed_records_count']}")
print(f"Total dirty records: {result['dirty_records']}")
print(f"Total run duration (seconds): {result['total_run_duration_seconds']:.2f}")
print("Top 25 destination cities (average and 95th percentile of flight duration):")
for _, row in result["destination_stats"].iterrows():
    print(f"  {row['destination_city']}: AVG Duration = {row['avg_duration']:.2f} secs, P95 Duration = {row['p95_duration']:.2f} secs")

print(f"City with maximum passengers arrived: {result['max_passengers_arrived_city']}")
print(f"City with maximum passengers left: {result['max_passengers_left_city']}")
