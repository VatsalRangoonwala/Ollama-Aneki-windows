import random

import ollama
from llmware.models import ModelCatalog
from rich.live import Live
from rich.table import Table
from rich_pixels import Pixels

model = ModelCatalog().load_model("slim-emotions-tool")


path = ""


def emotion_path(text):
    response = model.function_call(text)["llm_response"]["emotions"][0]
    global path
    emotions = [
        "afraid",
        "anger",
        "angry",
        "annoyed",
        "anticipating",
        "anxious",
        "apprehensive",
        "ashamed",
        "caring",
        "confident",
        "content",
        "devastated",
        "disappointed",
        "disgusted",
        "embarrassed",
        "excited",
        "faithful",
        "fear",
        "furious",
        "grateful",
        "guilty",
        "hopeful",
        "impressed",
        "jealous",
        "joy",
        "joyful",
        "lonely",
        "love",
        "nostalgic",
        "prepared",
        "proud",
        "sad",
        "sadness",
        "sentimental",
        "surprise",
        "surprised",
        "terrified",
        "trusting",
    ]
    if response not in emotions:
        print("emotion is outof the bounds")
    path = "saves/custom/lowres/" + response + ".png"
    try:
        Pixels.from_image_path(path)
        return path
    except:
        return "saves/default/lowres/" + random.choice(emotions) + ".png"


def generate_table(ip, flag):
    global path
    emotion = ""
    try:
        emotion = Pixels.from_image_path(path)
    except:
        emotion = Pixels.from_image_path("saves/default/lowres/" + "grateful" + ".png")
    if flag:
        path = emotion_path(ip)
        emotion = Pixels.from_image_path(path)
    table = Table(show_header=False)
    table.add_column("", width=60, overflow="fold")
    table.add_column("", width=100, overflow="fold")
    table.add_row(emotion, ip)

    return table


ip = ""

while ip != "exit":
    path = ""
    ip = input("\n>> ")
    stream = ollama.chat(
        model="aneki",
        messages=[{"role": "user", "content": ip}],
        stream=True,
    )
    with Live(Table(), refresh_per_second=4) as live:
        msg = ""
        flag = False
        for chunk in stream:
            msg = msg + chunk["message"]["content"]
            if len(msg) % 50 ==0:
                flag = True
            else:
                flag = False
            if msg.count("\n---") >= 1:
                break
            live.update(generate_table(msg.replace("\n---", ""), flag))
