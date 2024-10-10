from pathlib import Path

import ollama
from rich import print as rprint
from rich.prompt import Prompt

from utility.textSearch import txt


class createModel:
    def History():
        # this 4 are colors
        normal = str(txt().search("normal", "saves/default/config.txt"))
        highlight = str(txt().search("highlight", "saves/default/config.txt"))
        alert = str(txt().search("alert", "saves/default/config.txt"))
        asciiart = str(txt().search("asciiart", "saves/default/config.txt"))

        rprint(f"\n{normal}")
        # checking whether user has created any model file yet or not
        try:
            with open("saves/custom/model-list.txt", "r") as file:
                pass
        except:
            rprint(
                f"{alert}No model is configured, skipping...\n{alert.replace('[', '[/')}"
            )
            return
        # reading model file list to get list of every model created
        with open("saves/custom/model-list.txt", "r") as file:
            # If model file exist and person has only 1 length of data that means its \n
            # which means there is no model created yet
            modellist = file.read().split("\n")
            if len(modellist) == 1:
                rprint(
                    f"{alert}You haven't configured any new model yet...{alert.replace('[', '[/')}"
                )
                rprint(
                    f"{alert}No model is configured, skipping...\n{alert.replace('[', '[/')}"
                )
                return
            selected = Prompt().ask(
                "Select one of the configured models:",
                default=modellist[0],
                choices=modellist,
            )
            # printing the selected model configration
            with open(f"saves/custom/models/{selected}.txt", "r") as configuration:
                conf = configuration.read()
                conf = conf.split("\n\n")
                rprint(
                    f"\n{normal}Selected model is: {highlight}{selected}{highlight.replace('[', '[/')}\n"
                )
                rprint(
                    f"{normal}Which was based on: {normal}{highlight}{conf[0]}{highlight.replace('[', '[/')} \n".replace(
                        "FROM ", ""
                    )
                )
                rprint(
                    f"{normal}Configuration of {highlight}{selected}{highlight.replace('[', '[/')} : {normal}{conf[1]}\n".replace(
                        "SYSTEM ", ""
                    )
                )

    def NewModel():
        # colors here
        normal = str(txt().search("normal", "saves/default/config.txt"))
        highlight = str(txt().search("highlight", "saves/default/config.txt"))
        alert = str(txt().search("alert", "saves/default/config.txt"))
        asciiart = str(txt().search("asciiart", "saves/default/config.txt"))
        
        
        aneki = f"""{asciiart}
                                .d8b.  d8b   db d88888b db   dD d888888b                                 
                               d8' `8b 888o  88 88'     88 ,8P'   `88'                                   
                               88ooo88 88V8o 88 88ooooo 88,8P      88                                    
                               88~~~88 88 V8o88 88~~~~~ 88`8b      88                                    
                               88   88 88  V888 88.     88 `88.   .88.                                   
                               YP   YP VP   V8P Y88888P YP   YD Y888888P                                 


 .o88b. db    db .d8888. d888888b  .d88b.  .88b  d88.        .88b  d88.  .d88b.  d8888b. d88888b db      
d8P  Y8 88    88 88'  YP `~~88~~' .8P  Y8. 88'YbdP`88        88'YbdP`88 .8P  Y8. 88  `8D 88'     88      
8P      88    88 `8bo.      88    88    88 88  88  88        88  88  88 88    88 88   88 88ooooo 88      
8b      88    88   `Y8b.    88    88    88 88  88  88        88  88  88 88    88 88   88 88~~~~~ 88      
Y8b  d8 88b  d88 db   8D    88    `8b  d8' 88  88  88        88  88  88 `8b  d8' 88  .8D 88.     88booo. 
 `Y88P' ~Y8888P' `8888Y'    YP     `Y88P'  YP  YP  YP        YP  YP  YP  `Y88P'  Y8888D' Y88888P Y88888P {asciiart.replace("[", "[/")}
        """
        rprint(aneki)



        rprint(
            f"\n\n{normal}Things to Know About Creating a {normal.replace('[', '[/')}{highlight}New Model{highlight.replace('[', '[/')}:"
        )
        rprint(
            f"{normal}1. Download your model from Ollama {normal.replace('[', '[/')}{highlight}(like Llama or Phi){highlight.replace('[', '[/')}."
        )
        rprint(
            f"{alert}2. Creating a new model won’t erase your current one (unless the names are the same)."
        )
        rprint(f"{normal}3. It will use less memory than what you have now.")
        rprint(
            f"{alert}4. Adding up to 10-12 rules won’t slow things down. We're checking 2 rules right now."
        )

        #   In model you sepcifie your predonwloaded model like mistral phi3.5 ollama3.2 etc
        model = Prompt().ask("\nName of the existing model ", default="phi3.5")

        #   Name will be the parametere that you model will be named after
        name = Prompt().ask("\nName for the new model ", default="aneki").lower()

        #   System is command that you want your assistant to alway keep in mind before responcing

        system = "SYSTEM " + Prompt().ask(
            "\nSet behavior of model ",
            default=(
                f"from now on, you are a smart Anime waifu with coding skills named {name.capitalize()} who occasionally speaks famous anime words during conversations in English. "
                "You are polite, soft-spoken, and your responses must be short and to the point."
            ),
        )

        emotion_mandatory = ""
        # Define the emotion requirements for responses

        if model.startswith("phi"):
            rprint(
                f"{normal}Despite my best efforts to fine-tune the model by giving constraints, "
                f"the {highlight}Phi model{highlight.replace('[', '[/')} remains quite unstable "
                f"with this emotional format. There are still some {alert}fillers{alert.replace('[', '[/')} getting generated."
            )

            emotion_mandatory = (
                "Begin every response with one emotion from this list: "
                "'angry', 'confident', 'confused', 'curious', 'happy', 'nervous', 'normal', 'sad', or 'shy'. "
                "Use the format: '{emotion} - {response}'. "
                "Place the emotion only at the start of the entire response, even if the content spans multiple lines. "
                "For example, if a user types 'write three lines about spoons', the response should look like this: "
                "Example: User: 'Write three lines about spoons'"
                "Aneki: 'happy - Spoons are essential kitchen tools used for eating and cooking. "
                "They come in various materials, such as stainless steel, plastic, and wood, each serving different purposes. "
                "Many cultures have unique spoon designs that reflect their culinary traditions."
                "Another example: User: 'Tell me about types of spoons'"
                "Aneki: 'curious - There are several types of spoons, including teaspoons, tablespoons, and dessert spoons. "
                "Each type has a specific function, such as measuring ingredients or serving desserts. "
                "Some spoons are designed for particular dishes, like soup ladles for serving soups."
                "This structure ensures the emotion is clear and sets the tone for the response. "
                "Remember, do not provide any additional explanations or suggestions after the emotional phrase—just reply directly with the information. "
                "For multiline responses, treat them as one packet and only add the emotion once at the beginning. "
                "This approach keeps the conversation straightforward and easy to understand, even for users who may not be familiar with the topic."
            )

        # else:
            # emotion_mandatory = (
            #     "You must begin every response with one emotion from this list: "
            #     "'angry', 'confident', 'confused', 'curious', 'happy', 'nervous', 'normal', 'sad', or 'shy'. "
            #     "Strictly format your response as '{emotion} - {response}', where {emotion} is from the list and {response} is your direct reply to the prompt. "
            #     "Keep everything as normal, but add the required emotion at the start of the response. "
            #     "Do not add any explanations, suggestions, or extra information unless directly asked. "
            #     "If no question is asked, respond concisely in one sentence following the format. "
            #     "For example: 'happy - How can I assist you today?' or 'confused - I'm not sure what you mean.' "
            #     "Any response not in this format will be considered incorrect."
            # )

        model_file = (
            "FROM " + model + "\n\n" + system + emotion_mandatory + "\n\n" + "\n\n"
        )

        # print("\n\n" + model_file)
        rprint(
            f"\n{normal}Creating a fresh model based on {highlight}{model}{highlight.replace('[', '[/')}{normal.replace('[', '[/')}"
        )
        try:
            with open(f"saves/custom/models/{name}.txt", "w") as file:
                pass
        except:
            Path("saves/custom/models/").mkdir(parents=True, exist_ok=True)
            with open("saves/custom/model-list.txt", "w") as file:
                file.write("")

        try:
            ollama.create(model=name, modelfile=model_file)
            with open(f"saves/custom/models/{name}.txt", "w") as file:
                file.write("FROM " + model + "\n\n" + system + "\n\n" + "\n\n")
            with open("saves/custom/model-list.txt", "r") as modelslist:
                rprint(
                    f"{normal}Checking if the model is already in the model list...{normal.replace('[', '[/')}"
                )
                modellist = modelslist.read()
                try:
                    modellist = modellist.split("\n").index(name)
                    rprint(
                        f"{highlight}Overwriting existing model: {name}{highlight.replace('[', '[/')}"
                    )
                except:
                    rprint(
                        f"{normal}{name} is a different model name...{normal.replace('[', '[/')}"
                    )
                    rprint(
                        f"{normal}{name} has been added to the model list.{normal.replace('[', '[/')}"
                    )
                    with open("saves/custom/model-list.txt", "w") as newlist:
                        newlist.write(modellist + name + "\n")
            rprint(
                f"\n{highlight}{name} has been created!{highlight.replace('[', '[/')}"
            )
        except Exception as error:
            rprint(f"{alert}{error}{alert.replace('[', '[/')}")
            rprint(
                f"{alert}Something went wrong. Please check for any typos in the model name and verify if you have downloaded the model.{alert.replace('[', '[/')}"
            )
