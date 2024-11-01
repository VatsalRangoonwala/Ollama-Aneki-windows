from llmware.models import ModelCatalog

ls = [
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


model = ModelCatalog().load_model("slim-emotions-tool")
for l in ls:
    response = model.function_call(l)
    print(str(ls.index(l)) + " " + l + "  " + (response["llm_response"]["emotions"][0]))
