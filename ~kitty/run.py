import datetime
import json
from pathlib import Path

import ollama
from llmware.models import ModelCatalog
from rich.live import Live
from rich.table import Table

from utility.richtables import Tables
from utility.textSearch import txt
from rich.prompt import Prompt


class RunModel:

    def new_run(model_name):
        
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.txt")
        ask_for_Topic = int(txt.search("ask_for_Topic", "saves/default/config.txt")) == 1
        Topic=""
        if ask_for_Topic:
            Topic = Prompt.ask(
                    "Save history with name: ", default=now
            )
            with open(custom + f"historylog.txt", "a") as historylog:
                            historylog.write(f"{model_name}-{Topic}\n")
        else:
            with open(custom + f"historylog.txt", "a") as historylog:
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
            print(type(memory))

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
                user_input = input("\n>> ")
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
                            
                    user_input = input("\n>> ")
            else:
                user_input = input("\n>> ")
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
                            

                    user_input = input("\n>> ")