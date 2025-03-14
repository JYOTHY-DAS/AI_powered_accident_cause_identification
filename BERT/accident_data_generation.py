import csv
import random
import os
from datetime import datetime, timedelta

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
causes = ['over-speeding', 'drunk driving', 'distracted driving', 'red light jumping',
          'weather conditions', 'wrong side driving', 'vehicle malfunction', 'road conditions', 'traffic rule violation']

# List of Kerala cities and notable highways
locations = [
    'Vattiyoorkavu', 'Vanchiyoor', 'Thumba', 'Kazhakkuttom', 'Thiruvallam', 'Nemom', 'Medical College',
    'Poonthura', 'Peroorkada', 'Sreekariyam', 'Thiruvallam', 'Fort', 'Valiyathura', 'Poojappura', 'Museum', 'Vizhinjam', 'Thampanoor', 'Cantonment', 
    'Pettah', 'Kovalam', 'Thiruvallam', 'Mannanthala', 'Kovalam', 'Karamana', 'Kadinamkulam', 'Varkala', 'Balaramapuram', 'Aruvikkara', 'Chirayinkil', 
    'Attingal', 'Palode', 'Vellarada', 'Pothencode', 'Vattappara', 'Maranalloor', 'Ayiroor', 'Kallambalam', 'Poovar', 'Neyyattinkara', 'Kilimanoor', 
    'Varkala', 'Malayinkil', 'Kallambalam', 'Pangode', 'Mangalapuram', 'Nedumangad', 'Kanjiramkulam'
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
    'auto-rickshaw': None,
    'bicycle': None,
    'Jeep': 'seatbelt'
}

# Function to generate a random date and time
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Function to determine the primary cause
# def determine_primary_cause(cause):
#     if cause in ['drunk driving', 'over-speeding', 'distracted driving', 'wrong side driving']:
#         return cause.capitalize()
#     return "Other"

def determine_primary_cause(cause):
    if cause in causes:
        return cause.capitalize()
    else:
        return "Other"

# Function to determine secondary cause
def determine_secondary_cause(entity, gear_status):
    if entity == "two-wheeler" and gear_status == "not wearing":
        return "Helmet Violation"
    elif entity in ["car", "Jeep", "truck"] and gear_status == "not wearing":
        return "Seatbelt Violation"
    return "No Violation"

# Function to determine risk factor
def determine_risk_factor(time, location, cause):
    risk = "Medium"
    
    # High risk conditions
    if "PM" in time and ("NH" in location or "highway" in location):
        risk = "High"
    if cause in ["drunk driving", "over-speeding"]:
        risk = "High"
    
    return risk

# Start and end dates for random date generation
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 2, 11)



# Define the path to save data file
data_path = os.path.join("..", "data", "raw", "unsupervised_accident_data.csv")



# Open a CSV file to write the supervised data
with open(data_path, mode='w', newline='') as file:
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
        gear = vehicle_protective_gear.get(example1, None)
        if gear:
            gear_status = random.choice(['not wearing', 'wearing'])
            gear_text = f", {gear_status} a {gear},"
        else:
            gear_text = ""
            gear_status = "wearing"  # Default for non-gear cases

        # Generate report text
        report = (
            f"On {date_time}, a {example1} collided with a {example2} at {location}. "
            f"The rider{gear_text} suffered a {injury} and {outcome}. "
            f"The cause of the accident was determined to be {cause}."
        )

        # Determine labels
        # primary_cause = determine_primary_cause(cause)
        # secondary_cause = determine_secondary_cause(example1, gear_status)
        # risk_factor = determine_risk_factor(date_time, location, cause)

        # Write to CSV
        writer.writerow([report])
        
print(f"Unupervised learning dataset generated successfully and saved at: {data_path}")
