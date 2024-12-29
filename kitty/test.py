import array
import datetime
import fcntl
import json
import os
import shutil
import subprocess
import sys
import termios
import tty
from pathlib import Path

import ollama
from llmware.models import ModelCatalog
from PIL import Image
from prompt_toolkit import prompt as input
from rich import print as rprint
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

from tui.pngpixel import pngPix
from utility.richtables import Tables
from utility.textSearch import txt

# def move_cursor(row, col):
#     subprocess.run('echo -e "\\033[s"', shell=True)
#     subprocess.run(f'echo -e "\\033[{row};{col}H"', shell=True)


# def restore_cursor():
#     subprocess.run('echo -e "\\033[u"', shell=True)


def display_image(image_path, rectangle, id):
    subprocess.run(
        [
            "kitten",
            "icat",
            "--z-index",
            "-5",
            "--align",
            "left",
            "--image-id",
            str(id),
            image_path,
        ]
    )
    # subprocess.run(
    #     [
    #         "kitten",
    #         "icat",
    #         "--place",
    #         rectangle,
    #         "--z-index",
    #         "-50",
    #         "--image-id",
    #         str(id),
    #         image_path,
    #     ]
    # )


def clear_kitty_image():
    pass
    # sys.stdout.write("\033c")
    # sys.stdout.flush()


class RunModel:
    def __init__(self):
        pass

    def read(self, logs):
        pass
        # cpath = txt.search("custom_path", "saves/default/config.conf")
        # with open(
        #     cpath + "/history/" + logs + ".json",
        #     "r",
        # ) as history:
        #     history = json.load(history)[2:]
        #     user_conversation = txt.search(
        #         "user_conversation", "saves/default/config.conf"
        #     )
        #     try:

        #         if (
        #             int(txt.search("emotion_generation", "saves/default/config.conf"))
        #             < 1
        #         ):
        #             raise

        #         def requiredLines(img, height, width, char, lines):
        #             buf = array.array("H", [0, 0, 0, 0])
        #             fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
        #             displayresH = buf[3]
        #             displayresW = buf[2]
        #             return int(
        #                 img.height
        #                 / (
        #                     ((img.width / width) / (displayresW / char))
        #                     * (displayresH / lines)
        #                 )
        #             )

        #         with open(
        #             cpath + "/history/" + logs + "-emotions.json",
        #             "r",
        #         ) as emotionlist:
        #             emotionlist = json.load(emotionlist)
        #             j = 0
        #             char, lines = shutil.get_terminal_size()
        #             width = int(txt.search("width", "saves/default/config.conf"))
        #             for _ in range(lines):
        #                 print("")
        #             for i in range(int(len(history) / 2)):
        #                 rprint("\n" + user_conversation + " " + history[j]["content"])
        #                 pngPath = txt.search_image(emotionlist[i], cpath)
        #                 png = Image.open(pngPath)
        #                 height = (
        #                     int(width * png.height / png.width) + 1
        #                     if (
        #                         int(width * png.height / png.width)
        #                         != (width * png.height / png.width)
        #                     )
        #                     else int(width * png.height / png.width)
        #                 )
        #                 required_lines = requiredLines(png, height, width, char, lines)
        #                 rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
        #                     int(lines - required_lines - 5)
        #                 )
        #                 space = ""
        #                 for _ in range(required_lines):
        #                     for _ in range(width):
        #                         space += " "
        #                     space += "\n"

        #                 rprint(
        #                     Tables.table_with_emotion(
        #                         history[j + 1]["content"],
        #                         space,
        #                     )
        #                 )
        #                 print("\n")
        #                 subprocess.run(
        #                     ["kitten", "icat", "--place", rectangle, pngPath]
        #                 )
        #                 for _ in range(required_lines + 1):
        #                     print("")
        #                 j += 2
        #                 print("\n")
        #     except:
        #         subprocess.run(["clear"])
        #         clear_kitty_image()
        #         rprint(
        #             txt.search("highlight", "saves/default/config.conf")
        #             + '"Ollama-Aneki Kitty"'
        #             + txt.search("alert", "saves/default/config.conf")
        #             + "was made to be used in linux KITTY terminal "
        #             + txt.search("highlight", "saves/default/config.conf")
        #             + "b'cos of the icat command"
        #         )
        #         for i in range(len(history)):
        #             if i % 2 == 0:
        #                 rprint("\n" + user_conversation + " " + history[i]["content"])
        #             else:
        #                 rprint(Tables.table_without_emotion(history[i]["content"]))

    def new_run(self, model_name):
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.conf")
        user_conversation = txt.search("user_conversation", "saves/default/config.conf")
        ask_for_Topic = (
            int(txt.search("ask_for_Topic", "saves/default/config.conf")) == 1
        )
        Topic = ""
        if ask_for_Topic:
            Topic = Prompt.ask("Save history with name: ", default=now)
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{Topic}\n")
        else:
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{now}\n")

        length = 2 * int(txt.search("memory_length", "saves/default/config.conf"))
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.conf")
        )
        frequency = int(txt.search("frequency", "saves/default/config.conf"))
        Path(custom + "/history/").mkdir(parents=True, exist_ok=True)
        # subprocess.run(["clear"])
        with open(custom + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    # print(new_hist)
                    return new_hist
                else:
                    return hist

            history = []
            history.append(memory[0])
            history.append(memory[1])

            if int(txt.search("emotion_generation", "saves/default/config.conf")) >= 1:

                def numberOfLinesTaken(msg, chars):
                    msg = msg.split("\n")
                    count = 0
                    for paragraph in msg:
                        count += int(len(paragraph) / chars)

                def requiredLines(img, height, width, char, lines):
                    buf = array.array("H", [0, 0, 0, 0])
                    fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
                    displayresH = buf[3]
                    displayresW = buf[2]
                    return int(
                        img.height
                        / (
                            ((img.width / width) / (displayresW / char))
                            * (displayresH / lines)
                        )
                    )

                emotions = []
                model = ModelCatalog().load_model("slim-emotions-tool")
                if int(txt.search("auto_clear", "saves/default/config.conf")) >= 1:
                    # subprocess.run(["clear"])
                    clear_kitty_image()

                width = int(txt.search("width", "saves/default/config.conf"))
                char, lines = shutil.get_terminal_size()
                pngPath = txt.search_image("joyful", custom)
                png = Image.open(pngPath)
                height = (
                    int(width * png.height / png.width) + 1
                    if (
                        int(width * png.height / png.width)
                        != (width * png.height / png.width)
                    )
                    else int(width * png.height / png.width)
                )
                required_lines = requiredLines(png, height, width, char, lines)
                rectangle = str(width) + "x" + str(height) + "@" "2x" + str(
                    lines - required_lines - 3
                )
                space = ""
                for _ in range(required_lines):
                    for _ in range(width):
                        space += " "
                    space += "\n"
                for _ in range(lines):
                    print(" ")
                user_input = input("\n" + user_conversation + " ")
                id = 0
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    id += 1
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        response = "joyful"
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_with_emotion(msg, space))
                            if len(msg) % frequency < 3 and len(msg) < max_respose_size:
                                response = model.function_call(msg)["llm_response"][
                                    "emotions"
                                ][0]
                                #
                                #
                                # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                                # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                                # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                                # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                                # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                                #
                                #
                                pngPath = txt.search_image(response, custom)
                                # input()
                                # input()
                                # print("help")
                                display_image(pngPath, rectangle=rectangle, id=id)
                                # move_cursor(0, 0)
                                # input()
                                # restore_cursor()
                                # input()
                                # print("help2")
                                # input()

                        if len(msg) > max_respose_size:
                            response = model.function_call(msg[: max_respose_size - 1])[
                                "llm_response"
                            ]["emotions"][0]
                        else:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                        live.update(Tables.table_with_emotion(msg, space))
                        pngPath = txt.search_image(response, custom)

                    #
                    #
                    # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                    #
                    #
                    # display_image(pngPath, rectangle, id=id)
                    print("\n\n")

                    # move_cursor(0, 0)
                    # restore_cursor()
                    # subprocess.run(
                    #     ["kitten", "icat", "--place", rectangle, pngPath]
                    # )

                    for _ in range(required_lines):
                        print(" ")
                    emotions.append(response)
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}-emotions.json", "w"
                        ) as emotion:
                            json.dump(emotions, emotion, indent=2)

                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}-emotions.json", "w"
                        ) as emotion:
                            json.dump(emotions, emotion, indent=2)

                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                        if (
                            int(
                                txt.search(
                                    "reprint_everytime", "saves/default/config.conf"
                                )
                            )
                            >= 1
                        ):
                            # subprocess.run(["clear"])
                            clear_kitty_image()
                            self.read(f"{model_name}-{Topic}")
                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                        if (
                            int(
                                txt.search(
                                    "reprint_everytime", "saves/default/config.conf"
                                )
                            )
                            >= 1
                        ):
                            # subprocess.run(["clear"])
                            clear_kitty_image()
                            self.read(f"{model_name}-{now}")

                    user_input = input("\n" + user_conversation + " ")
            else:
                user_input = input("\n" + user_conversation + " ")
                while (
                    user_input.lower()
                    != txt.search("exit_code", "saves/default/config.conf").lower()
                ):
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            live.update(Tables.table_without_emotion(msg))
                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    if ask_for_Topic:
                        with open(
                            custom + f"/history/{model_name}-{Topic}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)
                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)

                    user_input = input("\n" + user_conversation + " ")


# def requiredLines(img, width, char, lines):
#     buf = array.array("H", [0, 0, 0, 0])
#     fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
#     displayresH = buf[3]
#     displayresW = buf[2]
#     return int(
#         img.height
#         / (((img.width / width) / (displayresW / char)) * (displayresH / lines))
#     )


# def new_height_width(image_path, width):
#     png = Image.open(image_path)
#     buf = array.array("H", [0, 0, 0, 0])
#     fcntl.ioctl(1, termios.TIOCGWINSZ, buf)
#     displayresH = buf[3]
#     displayresW = buf[2]
#     print(displayresW, displayresH)
#     char, lines = shutil.get_terminal_size()
#     required_height = int(
#         requiredLines(png, width, char, lines) * (displayresH / lines)
#     )
#     required_width = int(width * (displayresW / char))
#     print("old height:", png.height, "new height:", required_height)
#     print("old width:", png.width, "new width:", required_width)
#     return required_width, required_height


# height, width = new_height_width(
#     txt.search_image("joyful", txt.search("custom_path", "saves/default/config.conf")),
#     int(txt.search("width", "saves/default/config.conf")),
# )
# print(height, width)
# pngpixs = pngPix(
#     height=height,
#     width=width,
#     highlight=txt.search("highlight", "saves/default/config.conf"),
#     alert=txt.search("alert", "saves/default/config.conf"),
#     normal=txt.search("normal", "saves/default/config.conf"),
#     paths=txt.search("custom_path", "saves/default/config.conf"),
# )

# subprocess.run(
#     [
#         "kitten",
#         "icat",
#         "--z-index",
#         "-50",
#         "--image-id",
#         "5",
#         "saves/default/lowres/guilty.png",
#     ]
# )
# pngpixs.lower_resolution()
runmodel = RunModel()
runmodel.new_run("aneki")
