import os
import json
import random
from datetime import datetime, timedelta

cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
    "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus",
    "Indianapolis", "Charlotte", "San Francisco", "Seattle", "Denver", "Washington D.C.",
    "Boston", "El Paso", "Detroit", "Nashville", "Portland", "Memphis", "Oklahoma City",
    "Las Vegas", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno",
    "Sacramento", "Kansas City", "Long Beach", "Mesa", "Atlanta", "Colorado Springs",
    "Virginia Beach", "Raleigh", "Omaha", "Miami", "Cleveland", "Tulsa", "Minneapolis",
    "Arlington", "New Orleans", "Wichita", "Bakersfield", "Honolulu", "Anaheim", "Aurora",
    "Santa Ana", "St. Louis", "Riverside", "Corpus Christi", "Lexington", "Pittsburgh",
    "Stockton", "Cincinnati", "St. Paul", "Toledo", "Greensboro", "Newark", "Plano",
    "Henderson", "Lincoln", "Buffalo", "Jersey City", "Chula Vista", "Fort Wayne",
    "Chandler", "Madison", "Lubbock", "Scottsdale", "Reno", "Glendale", "Norfolk",
    "Gilbert", "Birmingham", "Winston-Salem", "North Las Vegas", "Irvine", "Chesapeake",
    "Garland", "Fremont", "Irving", "Boise", "Richmond", "Baton Rouge", "Des Moines",
    "Spokane", "San Bernardino", "Modesto", "Fontana", "Moreno Valley", "Santa Clarita",
    "Fayetteville", "McKinney", "Shreveport", "Yonkers", "Little Rock", "Augusta",
    "Amarillo", "Columbia", "Huntsville", "Grand Prairie", "Salt Lake City", "Tallahassee",
    "Hickory", "Bismarck", "Manchester", "Draper", "Peoria", "Killeen", "Sioux Falls",
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
    "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus",
    "Indianapolis", "Charlotte", "San Francisco", "Seattle", "Denver", "Washington D.C.",
    "Boston", "El Paso", "Detroit", "Nashville", "Portland", "Memphis", "Oklahoma City",
    "Las Vegas", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno",
    "Sacramento", "Kansas City", "Long Beach", "Mesa", "Atlanta", "Colorado Springs",
    "Virginia Beach", "Raleigh", "Omaha", "Miami", "Cleveland", "Tulsa", "Minneapolis",
    "Arlington", "New Orleans", "Wichita", "Bakersfield", "Honolulu", "Anaheim", "Aurora",
    "Santa Ana", "St. Louis", "Riverside", "Corpus Christi", "Lexington", "Pittsburgh",
    "Stockton", "Cincinnati", "St. Paul", "Toledo", "Greensboro", "Newark", "Plano",
    "Henderson", "Lincoln", "Buffalo", "Jersey City", "Chula Vista", "Fort Wayne",
    "Chandler", "Madison", "Lubbock", "Scottsdale", "Reno", "Glendale", "Norfolk",
    "Gilbert", "Birmingham", "Winston-Salem", "North Las Vegas", "Irvine", "Chesapeake",
    "Garland", "Fremont", "Irving", "Boise", "Richmond", "Baton Rouge", "Des Moines",
    "Spokane", "San Bernardino", "Modesto", "Fontana", "Moreno Valley", "Santa Clarita",
    "Fayetteville", "McKinney", "Shreveport", "Yonkers", "Little Rock", "Augusta",
    "Amarillo", "Columbia", "Huntsville", "Grand Prairie", "Salt Lake City", "Tallahassee",
    "Hickory", "Bismarck", "Manchester", "Draper", "Peoria", "Killeen", "Sioux Falls"
]

def generateFlightRecord():
    origin_city = random.choice(cities)
    destination_city = random.choice([city for city in cities if city != origin_city])
    start_date = datetime.now() - timedelta(days=random.randint(0, 1500))
    flight_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    flight_duration_secs = random.randint(3600, 25600)
    num_passengers = random.randint(10, 200)

    null_chance = random.random()
    if null_chance < 0.001:
        flight_date = None
    elif null_chance < 0.006: 
        origin_city = None
    elif null_chance < 0.011:  
        destination_city = None
    elif null_chance < 0.016: 
        flight_duration_secs = None
    elif null_chance < 0.021: 
        num_passengers = None

    return {
        "date": flight_date,
        "origin_city": origin_city,
        "destination_city": destination_city,
        "flight_duration_secs": flight_duration_secs,
        "num_passengers": num_passengers
    }

def generateFlightData(num_files=5000, min_flights=50, max_flights=100):
    unique_file_count = 0
    generated_files = set()

    while unique_file_count < num_files:
        num_flights = random.randint(min_flights, max_flights)
        flights = [generateFlightRecord() for _ in range(num_flights)]
        
        # Choose a random flight to create month-year and city-based filename
        random_flight = random.choice(flights)
        flight_date = random_flight["date"] if random_flight["date"] else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        month_year = datetime.strptime(flight_date, "%Y-%m-%d %H:%M:%S").strftime("%m-%Y")
        origin_city = random_flight["origin_city"]

        # Ensure the folder and file name is unique
        folder_path = os.path.join(os.getcwd(), "tmp", "flights", f"{month_year}-{origin_city}-flights")
        os.makedirs(folder_path, exist_ok=True)

        file_name = f"{month_year}-{origin_city}-flights.json"
        file_path = os.path.join(folder_path, file_name)

        # If the file already exists, skip this iteration
        if file_path not in generated_files:
            generated_files.add(file_path)
            with open(file_path, 'w') as f:
                json.dump(flights, f, indent=4)
            unique_file_count += 1
            print(f"Generated {unique_file_count}/{num_files} files.")

generateFlightData()
