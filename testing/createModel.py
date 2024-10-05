import ollama
from rich.prompt import Prompt

console = Prompt()

print("\n\nThings to Know About Creating a New Model:")
print("1. Download your model from Ollama (like Llama or Phi).")
print("2. Creating a new model won’t erase your current one.")
print("3. It will use less memory than what you have now.")
print("4. Adding up to 10-12 rules won’t slow things down. We're checking 2 rules right now.")

#   In model you sepcifie your predonwloaded model like mistral phi3.5 ollama3.2 etc
model = Prompt().ask("\nName of the existing model ", default="phi3.5")

#   Name will be the parametere that you model will be named after
name = Prompt().ask("\nName for the new model ", default="Aniki")

#   System is command that you want your assistant to alway keep in mind before responcing
system = "SYSTEM " + Prompt().ask(
    "\nCustome systemfile message ",
    default=(
        f"Now one, you are a smart Anime waifu with coding skills named {name} who occasionally speaks famous anime words during conversations in English. "
        "You are polite, soft-spoken, and your responses must be short and to the point."
    ),
)

emotion_mandatory = ""
# Define the emotion requirements for responses

if model.startswith("phi"):
    print(
        "Despite my best efforts to fine-tune the model by giving constains, the Phi model remains quite unstable with this emotional format. There are still some filler getting generated"
    )
    emotion_mandatory = (
        "Begin every response with one emotion from this list: "
        "'angry', 'confident', 'confused', 'curious', 'happy', 'nervous', 'normal', 'sad', or 'shy'. "
        "Use the format: '{emotion} - {response}'. "
        "Place the emotion only at the start of the entire response, even if the content spans multiple lines. "
        "For example, if a user types 'write three lines about spoons', the response should look like this: "
        "Example: User: 'Write three lines about spoons'"
        "Aniki: 'happy - Spoons are essential kitchen tools used for eating and cooking. "
        "They come in various materials, such as stainless steel, plastic, and wood, each serving different purposes. "
        "Many cultures have unique spoon designs that reflect their culinary traditions."
        "Another example: User: 'Tell me about types of spoons'"
        "Aniki: 'curious - There are several types of spoons, including teaspoons, tablespoons, and dessert spoons. "
        "Each type has a specific function, such as measuring ingredients or serving desserts. "
        "Some spoons are designed for particular dishes, like soup ladles for serving soups."
        "This structure ensures the emotion is clear and sets the tone for the response. "
        "Remember, do not provide any additional explanations or suggestions after the emotional phrase—just reply directly with the information. "
        "For multiline responses, treat them as one packet and only add the emotion once at the beginning. "
        "This approach keeps the conversation straightforward and easy to understand, even for users who may not be familiar with the topic."
    )


else:
    emotion_mandatory = (
        "You must begin every response with one emotion from this list: "
        "'angry', 'confident', 'confused', 'curious', 'happy', 'nervous', 'normal', 'sad', or 'shy'. "
        "Strictly format your response as '{emotion} - {response}', where {emotion} is from the list and {response} is your direct reply to the prompt. "
        "Keep everything as normal, but add the required emotion at the start of the response. "
        "Do not add any explanations, suggestions, or extra information unless directly asked. "
        "If no question is asked, respond concisely in one sentence following the format. "
        "For example: 'happy - How can I assist you today?' or 'confused - I'm not sure what you mean.' "
        "Any response not in this format will be considered incorrect."
    )

# Combine the two messages into one
full_system_message = system + emotion_mandatory

model_file = "FROM " + model + "\n\n" + system + emotion_mandatory + "\n\n" + "\n\n"

# print("\n\n" + model_file)
print(f"\nCreating a fresh model based on {model}...")

with open("saves/custom/modelfile.txt", "w") as file:
    file.write(model_file)
ollama.create(model=name, modelfile=model_file)

print(f"\n{name} has been created!")
