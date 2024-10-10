import random

import pandas as pd

df = pd.read_csv("data.csv")
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
data = []
for emotion in emotion_columns:
    group = list(df[df[emotion] == 1]["text"])
    random.shuffle(group)
    data.extend([(text, emotion) for text in group])
random.shuffle(data)
data_dict = [
    [{"from": "human", "value": text}, {"from": "gpt", "value": str(emotion)}]
    for text, emotion in data
]

# data_dict = [{"human": text, "gpt": str(emotion)} for text, emotion in data]
# pd.DataFrame(data_dict).to_csv("filtered.csv", index=False)
