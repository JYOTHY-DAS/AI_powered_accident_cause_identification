import pandas as pd
import random
from datetime import datetime, timedelta

# Sample data for generating reports
locations = ["NH66 near Trivandrum", "MG Road, Bangalore", "Outer Ring Road, Hyderabad", "Marine Drive, Mumbai"]
vehicles = ["two-wheeler", "car", "truck", "bus", "auto-rickshaw"]
causes = [
    ("Drunk Driving", "DUI-related accident"),
    ("Rash Driving", "Over speeding and reckless maneuvering"),
    ("Weather Issues", "Heavy rain, fog, or slippery roads"),
    ("Road Conditions", "Potholes, construction work, or lack of signs"),
    ("Helmet Violation", "Two-wheeler rider not wearing a helmet"),
    ("Seatbelt Violation", "Car passengers not wearing seatbelts"),
    ("Signal Violation", "Jumping red lights or ignoring stop signs"),
    ("Pedestrian Negligence", "Jaywalking or crossing in unsafe zones")
]

# Function to generate a random accident report
def generate_accident_report():
    date_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 60), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    vehicle1 = random.choice(vehicles)
    vehicle2 = random.choice(vehicles)
    location = random.choice(locations)
    primary_cause, primary_desc = random.choice(causes)
    secondary_cause, secondary_desc = random.choice(causes) if random.random() > 0.5 else ("None", "No secondary cause")
    risk_factor = "High" if random.random() > 0.7 else "Moderate"
    
    report_text = f"On {date_time.strftime('%d %b %Y, at %I:%M %p')}, a {vehicle1} collided with a {vehicle2} at {location}. {primary_desc}. {secondary_desc if secondary_cause != 'None' else ''}"
    
    return [report_text, primary_cause, secondary_cause, risk_factor]

# Generate dataset
dataset = [generate_accident_report() for _ in range(10000)]

# Save to CSV
df = pd.DataFrame(dataset, columns=["Accident Report", "Primary Cause", "Secondary Cause", "Risk Factor"])
df.to_csv("accident_dataset.csv", index=False)

print("Dataset generated successfully: accident_dataset.csv")
