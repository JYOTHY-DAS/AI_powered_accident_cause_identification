import csv
import random
from datetime import datetime, timedelta

# List of possible entities involved in accidents
entities = ['vehicle', 'pedestrian', 'animal', 'stationary object']
# Specific examples for each entity type
entity_examples = {
    'vehicle': ['car', 'bus', 'truck', 'auto-rickshaw', 'bicycle'],
    'pedestrian': ['a pedestrian'],
    'animal': ['a stray dog', 'a cow'],
    'stationary object': ['a tree', 'a building', 'a pole']
}
# Ensure at least one vehicle is involved
entity1 = 'vehicle'
entity2 = random.choice(entities)
# List of accident causes
causes = [
    'over-speeding', 'drunk driving', 'distracted driving', 'red light jumping',
    'weather conditions', 'wrong side driving', 'vehicle malfunction', 'road conditions','traffic rule violation']

# List of Kerala cities and notable highways
locations = [
    'Trivandrum', 'Kochi', 'Kozhikode', 'Thrissur', 'Kollam', 'Alappuzha', 'Palakkad',
    'Malappuram', 'Kottayam', 'Kannur', 'Idukki', 'Pathanamthitta', 'Wayanad', 'Kasargod'
]
highways = ['NH66', 'NH544', 'NH85', 'NH183', 'NH766']

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
    'auto-rickshaw': None,  # Typically, auto-rickshaws do not have seatbelts
    'bicycle': None
}

# Function to generate a random date and time
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Start and end dates for random date generation
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 2, 11)

# Open a CSV file to write the data
with open('accident_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Accident Report'])

    for _ in range(20000):
        date_time = random_date(start_date, end_date).strftime('%d %b %Y, at %I:%M %p')
        example1 = random.choice(entity_examples[entity1])
        example2 = random.choice(entity_examples[entity2])
        location = f"{random.choice(highways)} near {random.choice(locations)}"
        injury = random.choice(injuries)
        outcome = random.choice(outcomes)
        cause = random.choice(causes)
        
        # Determine protective gear and status
        gear = vehicle_protective_gear[example1]
        if gear:
            gear_status = random.choice(['not wearing', 'wearing'])
            gear_text = f", {gear_status} a {gear},"
        else:
            gear_text = ""
        
        report = (
            f"On {date_time}, a {example1} collided with a {example2} at {location}. "
            f"The rider{gear_text} suffered a {injury} and {outcome}. "
            f"The cause of the accident was determined to be {cause}."
        )
        
        writer.writerow([report])
