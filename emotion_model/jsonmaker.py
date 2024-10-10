import json
import random

import pandas as pd

# Read the CSV file
df = pd.read_csv("data.csv")

# List of emotion columns
emotion_columns = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral",
]

# Initialize lists for the 60-20-20 splits
data60 = []
data80 = []
data100 = []

# Iterate through each emotion column
for emotion in emotion_columns:
    # Get the texts for the current emotion
    group = list(df[df[emotion] == 1]["text"])

    # Shuffle the group to randomize the selection
    random.shuffle(group)

    # Calculate split sizes
    sixty = int(len(group) * 0.6)
    eighty = int(len(group) * 0.8)

    # Add 60% of the group to the data60 list
    data60.extend([(text, emotion) for text in group[:sixty]])

    # Add the next 20% to the data80 list
    data80.extend([(text, emotion) for text in group[sixty:eighty]])

    # Add the last 20% to the data100 list
    data100.extend([(text, emotion) for text in group[eighty:]])

# Shuffle the data for randomness and balanced distribution
random.shuffle(data60)
random.shuffle(data80)
random.shuffle(data100)

# Convert the lists to dictionaries (text: emotion)
data60_dict = [
    [{"from": "human", "value": text}, {"from": "gpt", "value": str(emotion)}]
    for text, emotion in data60
]
data80_dict = [
    [{"from": "human", "value": text}, {"from": "gpt", "value": str(emotion)}]
    for text, emotion in data80
]
data100_dict = [
    [{"from": "human", "value": text}, {"from": "gpt", "value": str(emotion)}]
    for text, emotion in data100
]
data60_dict = {"conversations": data60_dict}
# Write the data to JSON files
with open("data60.json", "w") as outfile:
    json.dump(data60_dict, outfile, indent=1)

with open("data80.json", "w") as outfile:
    json.dump(data80_dict, outfile, indent=1)

with open("data100.json", "w") as outfile:
    json.dump(data100_dict, outfile, indent=1)

print("60-20-20 splits saved to JSON files.")
