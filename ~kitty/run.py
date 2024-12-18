import datetime
import json
import subprocess
from pathlib import Path

import ollama
from llmware.models import ModelCatalog
from rich import print as rprint
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

from utility.richtables import Tables
from utility.textSearch import txt


class RunModel:
    def __init__(self):
        pass

    def read(self, logs):
        cpath = txt.search("custom_path", "saves/default/config.txt")
        with open(
            cpath + "/history/" + logs + ".json",
            "r",
        ) as history:
            history = json.load(history)[2:]
            user_conversation = txt.search(
                "user_conversation", "saves/default/config.txt"
            )
            try:
                if (
                    int(txt.search("emotion_generation", "saves/default/config.txt"))
                    < 1
                ):
                    raise
                with open(
                    cpath + "/history/" + logs + "-emotions.json",
                    "r",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    j = 0
                    for i in range(int(len(history) / 2)):
                        rprint("\n" + user_conversation + " " + history[j]["content"])
                        rprint(
                            Tables.table_with_emotion(
                                history[j + 1]["content"],
                                txt.search_image(emotionlist[i], cpath),
                            )
                        )
                        j += 2
            except:
                for i in range(len(history)):
                    if i % 2 == 0:
                        rprint("\n" + user_conversation + " " + history[i]["content"])
                    else:
                        rprint(Tables.table_without_emotion(history[i]["content"]))

    def ConinueFromWhereItLeft(self, logs):
        now = str(datetime.datetime.now())
        cpath = txt.search("custom_path", "saves/default/config.txt")
        model_name = Prompt.ask(
            "Select Model: ",
            default="aizen",
            choices=open(
                cpath + "/model-list.txt",
                "r",
            )
            .read()
            .split("\n")[:-1],
        )
        memory_list = []
        emotionlist = []
        with open(cpath + f"/models/{model_name}.json", "r") as file:
            memory_list = json.load(file)
            memory_list[0]["content"] += ". The current time is " + now

        with open(
            cpath + "/history/" + logs + ".json",
            "r",
        ) as history:
            history = json.load(history)[2:]
            choices = []
            print("\n")
            for i in range(int(len(history) / 2)):
                choices.append(str(i + 1))
                rprint(
                    txt.search("highlight", "saves/default/config.txt")
                    + str(i + 1)
                    + " "
                    + txt.search("normal", "saves/default/config.txt")
                    + history[i * 2]["content"]
                )
            print("\n")
            indexs = int(
                Prompt.ask(
                    "From where do you want to continue",
                    default=str(int(len(history) / 2)),
                    choices=choices,
                )
            )
            history = history[: (indexs) * 2]
            with open(cpath + "/history/" + logs + ".json", "w") as chats:
                for h in history:
                    memory_list.append(h)
                json.dump(memory_list, chats, indent=2)
            try:
                with open(
                    cpath + "/history/" + logs + "-emotions.json",
                    "r",
                ) as emotionlist:
                    emotionlist = json.load(emotionlist)
                    emotionlist=emotionlist[:indexs]
                    with open(
                        cpath + "/history/" + logs + "-emotions.json",
                        "w",
                    ) as emotion:
                    
                        json.dump(emotionlist, emotion, indent=2)
            except:
                pass

        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.txt")
        )
        length = 2 * int(txt.search("memory_length", "saves/default/config.txt"))
        user_conversation = txt.search("user_conversation", "saves/default/config.txt")
        frequency = int(txt.search("frequency", "saves/default/config.txt"))
        with open(cpath + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    print(new_hist)
                    return new_hist
                else:
                    return hist

            history = memory_list
            if int(txt.search("emotion_generation", "saves/default/config.txt")) >= 1:
                emotions = emotionlist
                model = ModelCatalog().load_model("slim-emotions-tool")
                if int(txt.search("auto_clear", "saves/default/config.txt")) >= 1:
                    subprocess.run(["clear"])
                    self.read(logs)
                user_input = input("\n" + user_conversation + " ")
                while user_input.lower() != "exit":
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        response = "joyful"
                        art = txt.search_image(response, cpath)
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            if len(msg) % frequency < 3 and len(msg) < max_respose_size:
                                response = model.function_call(msg)["llm_response"][
                                    "emotions"
                                ][0]
                                art = txt.search_image(response, cpath)
                            live.update(Tables.table_with_emotion(msg, art))
                        if len(msg) > max_respose_size:
                            response = model.function_call(msg[: max_respose_size - 1])[
                                "llm_response"
                            ]["emotions"][0]
                        else:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                        live.update(
                            Tables.table_with_emotion(
                                msg, txt.search_image(response, cpath)
                            )
                        )
                    emotions.append(response)
                    with open(cpath + f"/history/{logs}-emotions.json", "w") as emotion:
                        json.dump(emotions, emotion, indent=2)

                    history.append(
                        {
                            "role": "assistant",
                            "content": msg,
                        }
                    )
                    with open(cpath + f"/history/{logs}.json", "w") as chats:
                        json.dump(history, chats, indent=2)

                    if (
                        int(txt.search("reprint_everytime", "saves/default/config.txt"))
                        >= 1
                    ):
                        subprocess.run(["clear"])
                        self.read(logs)
                    user_input = input("\n" + user_conversation + " ")
            else:
                self.read(logs)
                user_input = input("\n" + user_conversation + " ")
                while user_input.lower() != "exit":
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
                    with open(cpath + f"/history/{logs}.json", "w") as chats:
                        json.dump(history, chats, indent=2)
                    if (
                        int(txt.search("reprint_everytime", "saves/default/config.txt"))
                        >= 1
                    ):
                        subprocess.run(["clear"])
                        self.read(logs)
                    user_input = input("\n" + user_conversation + " ")

    def new_run(model_name):
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.txt")
        user_conversation = txt.search("user_conversation", "saves/default/config.txt")
        ask_for_Topic = (
            int(txt.search("ask_for_Topic", "saves/default/config.txt")) == 1
        )
        Topic = ""
        if ask_for_Topic:
            Topic = Prompt.ask("Save history with name: ", default=now)
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{Topic}\n")
        else:
            with open(custom + "/historylog.txt", "a") as historylog:
                historylog.write(f"{model_name}-{now}\n")

        length = 2 * int(txt.search("memory_length", "saves/default/config.txt"))
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.txt")
        )
        frequency = int(txt.search("frequency", "saves/default/config.txt"))
        Path(custom + "/history/").mkdir(parents=True, exist_ok=True)
        with open(custom + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now

            def length_ret(leng, hist):
                if leng < len(hist):
                    hist = hist[(len(hist) - leng) + 1 :]
                    new_hist = memory
                    for h in hist:
                        new_hist.append(h)
                    print(new_hist)
                    return new_hist
                else:
                    return hist

            history = []
            history.append(memory[0])
            history.append(memory[1])
            if int(txt.search("emotion_generation", "saves/default/config.txt")) >= 1:
                emotions = []
                model = ModelCatalog().load_model("slim-emotions-tool")
                if int(txt.search("auto_clear", "saves/default/config.txt")) >= 1:
                    subprocess.run(["clear"])
                user_input = input("\n" + user_conversation + " ")
                while user_input.lower() != "exit":
                    history.append({"role": "user", "content": user_input})
                    stream = ollama.chat(
                        model=model_name,
                        messages=length_ret(length, history),
                        stream=True,
                    )
                    msg = ""
                    with Live(Table(), auto_refresh=True) as live:
                        response = "joyful"
                        art = txt.search_image(response, custom)
                        for chunk in stream:
                            msg += chunk["message"]["content"]
                            if len(msg) % frequency < 3 and len(msg) < max_respose_size:
                                response = model.function_call(msg)["llm_response"][
                                    "emotions"
                                ][0]
                                art = txt.search_image(response, custom)
                            live.update(Tables.table_with_emotion(msg, art))
                        if len(msg) > max_respose_size:
                            response = model.function_call(msg[: max_respose_size - 1])[
                                "llm_response"
                            ]["emotions"][0]
                        else:
                            response = model.function_call(msg)["llm_response"][
                                "emotions"
                            ][0]
                        live.update(
                            Tables.table_with_emotion(
                                msg, txt.search_image(response, custom)
                            )
                        )
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
                    else:
                        with open(
                            custom + f"/history/{model_name}-{now}.json", "w"
                        ) as chats:
                            json.dump(history, chats, indent=2)

                    user_input = input("\n" + user_conversation + " ")
            else:
                user_input = input("\n" + user_conversation + " ")
                while user_input.lower() != "exit":
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
