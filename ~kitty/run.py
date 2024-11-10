import datetime
import json
from pathlib import Path
import ollama
from utility.textSearch import txt


class RunModel:

    def new_run(model_name):

        def length_ret(leng, hist):
            if leng < len(hist):
                return hist[(len(hist) - leng) :]
            else:
                return hist

        now = str(datetime.datetime.now())
        custom = txt.search("custom_path", "saves/default/config.txt")
        length = 2 * int(txt.search("memory_length", "saves/default/config.txt"))
        Path(custom + "/history/").mkdir(parents=True, exist_ok=True)
        with open(custom + f"/models/{model_name}.json", "r") as file:
            memory = json.load(file)
            memory[0]["content"] += ". The current time is " + now
            history = []
            history.append(memory[0])
            history.append(memory[1])
            while True:
                history.append({"role": "user", "content": input("\n>> ")})
                stream = ollama.chat(
                    # model="llama3.2",
                    model=model_name,
                    messages=length_ret(length, history),
                    stream=True,
                )
                msg = ""
                for chunk in stream:
                    msg += chunk["message"]["content"]
                    print(chunk["message"]["content"], end="", flush=True)
                    
                    
                    
                history.append({"role": "assistant", "content": msg})
                with open(custom + f"/history/{model_name}-{now}.json", "w") as chats:
                    json.dump(history, chats, indent=2)
