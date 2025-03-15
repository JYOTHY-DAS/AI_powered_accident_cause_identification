import csv
import random
import os
from datetime import datetime, timedelta


# List of possible weather conditions
weather_conditions = ["clear", "light rain", "heavy rain", "fog", "squally wind", "drizzle", "overcast"]

# List of possible entities involved in accidents
entities = ['vehicle', 'pedestrian', 'animal', 'stationary object']

# Specific examples for each entity type
entity_examples = {
    'vehicle': ['car', 'bus', 'truck', 'auto-rickshaw', 'bicycle', 'Jeep', 'two-wheeler'],
    'pedestrian': ['a pedestrian'],
    'animal': ['a stray dog', 'a cow'],
    'stationary object': ['a tree', 'a building', 'a pole']
}

# Ensure at least one vehicle is involved
entity1 = 'vehicle'
entity2 = random.choice(entities)

# List of accident causes
causes = ['over-speeding', 'drunk driving', 'distracted driving', 'red light jumping', 'Overloading',
          'wrong side driving', 'vehicle malfunction', 'road conditions', 'traffic rule violation']

# Mapping of highways, state highways, and major city roads to the locations they pass through
road_location_map = {
    # National Highways
    'NH66': ['Trivandrum', 'Kollam', 'Alappuzha', 'Ernakulam', 'Thrissur', 'Kozhikode', 'Kannur', 'Kasargod'],
    'NH544': ['Ernakulam', 'Thrissur', 'Palakkad'],
    'NH85': ['Kochi', 'Idukki'],
    'NH183': ['Kottayam', 'Pathanamthitta'],
    'NH766': ['Kozhikode', 'Wayanad'],

    # State Highways
    'SH1 (MC Road)': ['Trivandrum', 'Kottayam', 'Ernakulam'],
    'SH8': ['Kottayam', 'Pala', 'Thodupuzha'],
    'SH40': ['Alappuzha', 'Changanassery'],
    'SH66': ['Kozhikode', 'Mananthavady'],
    'SH69': ['Palakkad', 'Ottapalam'],

    # Major City Roads
    'MG Road': ['Trivandrum', 'Kochi', 'Thrissur'],
    'Banerji Road': ['Kochi'],
    'Marine Drive Road': ['Kochi'],
    'Kaloor-Kadavanthra Road': ['Kochi'],
    'Kowdiar Road': ['Trivandrum'],
    'Vellayambalam-Sasthamangalam Road': ['Trivandrum'],
    'Gandhi Road': ['Kottayam'],
    'Calicut Beach Road': ['Kozhikode'],
    'Mavoor Road': ['Kozhikode'],
    'Karikkamuri Road': ['Kochi'],
    'Perandoor Road': ['Kochi'],
    'MG Road (Kozhikode)': ['Kozhikode'],
    'Rajaji Road': ['Kochi'],
    'Palarivattom Bypass Road': ['Kochi'],
    'Thrissur Round': ['Thrissur'],
    'East Fort Road': ['Thrissur'],
    'West Hill Road': ['Kozhikode'],
    'Kannur City Road': ['Kannur']
}


# List of injuries
injuries = ['head injury', 'leg fracture', 'arm fracture', 'multiple injuries', 'minor bruises']

# List of outcomes
outcomes = ['succumbed', 'is in critical condition', 'is recovering', 'was declared dead on the spot']

# Mapping of vehicles to their protective gear
vehicle_protective_gear = {
    'two-wheeler': 'helmet',
    'car': 'seatbelt',
    'bus': None,
    'truck': 'seatbelt',
    'auto-rickshaw': None,
    'bicycle': None,
    'Jeep': 'seatbelt'
}

# Function to generate a random date and time
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def determine_primary_cause(cause):
    if cause in causes:
        return cause.capitalize()
    else:
        return "Other"

# Function to determine secondary cause
def determine_secondary_cause(entity, gear_status, cause, time, location):
    if entity == "two-wheeler" and gear_status == "not wearing":
        return "Helmet Violation"
    elif entity in ["car", "Jeep", "truck"] and gear_status == "not wearing":
        return "Seatbelt Violation"
    elif entity in ["bus", "truck", "auto-rickshaw"] and random.random() < 0.3:  # 30% chance
        return "Overloading Violation"
    elif cause == "over-speeding":
        return "Speeding Violation"
    elif cause == "red light jumping":
        return "Signal Violation"
    elif cause == "wrong side driving":
        return "Wrong Lane Violation"
    elif cause == "distracted driving":
        return "Mobile Phone Violation"
    elif cause == "drunk driving":
        return "Drunk Driving Violation"
    elif entity == "pedestrian" and "crossing" in location.lower():
        return "Zebra Crossing Violation"
    elif random.random() < 0.02 and "PM" in time:  # 20% chance at night
        return "Failure to Use Headlights at Night"
    elif random.random() < 0.2:  # 20% chance
        return "Reckless Driving Violation"
    elif random.random() < 0.15:  # 15% chance
        return "Tailgating Violation"
    
    return "No Violation"


# Function to determine risk factor
def determine_risk_factor(time, location, cause):
    risk = "Medium"
    
    # High risk conditions
    if "PM" in time and ("NH" in location or "highway" in location):
        risk = "High"
    elif cause in ["drunk driving", "over-speeding", "road conditions"]:
        risk = "High"
        
    return risk

# Start and end dates for random date generation
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 2, 11)



# Define the path to save data file
data_path = os.path.join("..", "data", "raw", "supervised_accident_data.csv")



# Open a CSV file to write the supervised data
with open(data_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Accident Report', 'Primary Cause', 'Secondary Cause', 'Risk Factor'])

    for _ in range(20000):
        date_time = random_date(start_date, end_date).strftime('%d %b %Y, at %I:%M %p')
        example1 = random.choice(entity_examples[entity1])
        example2 = random.choice(entity_examples[entity2])
        selected_highway = random.choice(list(road_location_map.keys()))
        selected_location = random.choice(road_location_map[selected_highway])
        location = f"{selected_highway} near {selected_location}"
        injury = random.choice(injuries)
        outcome = random.choice(outcomes)
        cause = random.choice(causes)
        weather = random.choice(weather_conditions)  # Randomly select weather condition

        # Determine protective gear and status
        gear = vehicle_protective_gear.get(example1, None)
        if gear:
            gear_status = random.choice(['not wearing', 'wearing'])
            gear_text = f", {gear_status} a {gear},"
        else:
            gear_text = ""
            gear_status = "wearing"  # Default for non-gear cases

        # Generate report text
        report = (
            f"On {date_time}, under {weather} conditions, a {example1} collided with a {example2} at {location}. "
            f"The rider{gear_text} suffered a {injury} and {outcome}. "
            f"The cause of the accident was determined to be {cause}."
        )

        # Determine labels
        primary_cause = determine_primary_cause(cause)
        secondary_cause = determine_secondary_cause(example1, gear_status, cause, date_time, location)
        risk_factor = determine_risk_factor(date_time, location, cause)

        # Write to CSV
        writer.writerow([report, primary_cause, secondary_cause, risk_factor])
        
print(f"Supervised learning dataset generated successfully and saved at: {data_path}")
