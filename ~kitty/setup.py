from rich import print as rprint
from rich.prompt import Prompt

from model import createModel
from tui.asciart import asciiArt
from tui.pngpixel import pngPix
from utility.textSearch import txt

asciiart = txt().search("asciiart", "saves/default/config.txt")
normal = txt().search("normal", "saves/default/config.txt")
highlight = txt().search("highlight", "saves/default/config.txt")
alert = txt().search("alert", "saves/default/config.txt")
user = ""

rprint(
    asciiart
    + asciiArt.LoadArt(int(txt().search("asciiart_index", "saves/default/config.txt")))
)

while user != "exit":
    print("\n")
    user = Prompt.ask(
        "",
        default="emotion",
        choices=["run", "help", "exit", "new", "history", "emotion"],
    )
    if user == "run":
        print("Running...")
    elif user == "help":
        rprint(
            f"{normal}\nWelcome to the help section! Here’s a brief overview of the commands available:{normal.replace('[', '[/')} \n"
        )

        rprint(
            f"{highlight}run:{highlight.replace('[', '[/')}\n"
            f"Launch a model by name.\n"
            f"If it exists, it will run.\n"
            f"{alert}Make sure the model is available!{alert.replace('[', '[/')} \n"
        )

        rprint(
            f"{highlight}exit:{highlight.replace('[', '[/')}\n"
            f"Exit the setup program.\n"
            f"All progress is saved automatically.\n"
            f"{alert}You can return later to continue!{alert.replace('[', '[/')} \n"
        )

        rprint(
            f"{highlight}new:{highlight.replace('[', '[/')}\n"
            f"Create a new custom model.\n"
            f"Base it on an existing model.\n"
            f"{alert}Choose a unique name for it!{alert.replace('[', '[/')} \n"
        )

        rprint(
            f"{highlight}history:{highlight.replace('[', '[/')}\n"
            f"View past model configurations.\n"
            f"Even deleted ones can be restored.\n"
            f"{alert}Recreate them if needed!{alert.replace('[', '[/')} \n"
        )

        rprint(
            f"{highlight}emotion:{highlight.replace('[', '[/')}\n"
            f"Change emotional model files.\n"
            f"Replace files with the same name.\n"
            f"{alert}Improper changes may cause issues!{alert.replace('[', '[/')} \n"
        )
        rprint(
            f"{normal}Feel free to ask for help anytime!{normal.replace('[', '[/')} \n"
        )

    elif user == "exit":
        print("Exiting...")
    elif user == "new":
        createModel.NewModel()
    elif user == "history":
        createModel.History()

    elif user == "emotion":
        cls = pngPix(
            height=int(txt().search("height", "saves/default/config.txt")),
            width=int(txt().search("width", "saves/default/config.txt")),
            normal=str(txt().search("normal", "saves/default/config.txt")),
            highlight=str(txt().search("highlight", "saves/default/config.txt")),
            alert=str(txt().search("alert", "saves/default/config.txt")),
        )
        cls.lower_resolution()
    else:
        pass
    print("\n")
