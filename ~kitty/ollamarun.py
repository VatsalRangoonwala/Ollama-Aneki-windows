import ollama
from llmware.models import ModelCatalog

model = ModelCatalog().load_model("slim-emotions-tool")
Text = ""
while Text != "exit":
    Text = input("\n\n>>> ")
    stream = ollama.chat(
        model="phi3.5",
        messages=[{"role": "user", "content": Text}],
        stream=True,
    )
    flag = True
    Text = ""
    for chunk in stream:
        Text += chunk["message"]["content"]
        print(chunk["message"]["content"], end="", flush=True)
        if len(Text) > 100 and flag:
            flag = False
            response = model.function_call(Text)
            # print((response["llm_response"]["emotions"][0]),end="")
            print((response["llm_response"]["emotions"]), end="")

    if flag:
        response = model.function_call(Text)
        # print((response["llm_response"]["emotions"][0]),end="")
        print((response["llm_response"]["emotions"]), end="")
