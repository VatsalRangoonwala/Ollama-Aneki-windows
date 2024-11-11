import datetime
import json
from pathlib import Path
from rich.live import Live
from rich.table import Table
import ollama
from llmware.models import ModelCatalog
from utility.richtables import Tables
from utility.textSearch import txt


class RunModel:

    def new_run(model_name):

        def length_ret(leng, hist):
            if leng < len(hist):
                return hist[(len(hist) - leng) :]
            else:
                return hist

        model = ModelCatalog().load_model("slim-emotions-tool")
        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.txt")
        length = 2 * int(txt.search("memory_length", "saves/default/config.txt"))
        max_respose_size = int(
            txt.search("max_respose_size", "saves/default/config.txt")
        )
        frequency = int(txt.search("frequency", "saves/default/config.txt"))
        Path(custom + "/history/").mkdir(parents=True, exist_ok=True)
        with open(custom + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now
            history = []
            history.append(memory[0])
            history.append(memory[1])
            while True:
                history.append({"role": "user", "content": input("\n>> ")})
                print("\n")
                stream = ollama.chat(
                    # model="llama3.2",
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
                        response = model.function_call(msg)["llm_response"]["emotions"][
                            0
                        ]
                    live.update(
                        Tables.table_with_emotion(
                            msg, txt.search_image(response, custom)
                        )
                    )
                history.append({"role": "assistant", "content": response + "." + msg})

                with open(custom + f"/history/{model_name}-{now}.json", "w") as chats:
                    json.dump(history, chats, indent=2)
