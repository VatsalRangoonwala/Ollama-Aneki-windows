# import ollama

# stream = ollama.chat(
#     model='llama3.2',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk, end='', flush=True)


import ollama

prev = [
    {
        "role": "user",
        "content": "hello my name is megh",
    },
    {
        "role": "assistant",
        "content": "Hi Megh, it's nice to meet you. Is there something I can help you with or would you like to chat?",
    },
]
while True:
    prev.append(
        {
            "role": "user",
            "content": input(">> "),
        },
    ),
    response = ollama.chat(
        model="llama3.2",
        messages=prev,
    )
    prev.append(response["message"])
    print(response["message"]["content"])