# Proof-of-concept AI reasoning layer:

from .config import system_prompt,MAX_MESSAGES
from .api import send_to_model
from .memory import save_memory,load_memory

#-----------------------------------
#-----Main Structure
#----------------------------------

def clean_text(text):
    if not isinstance(text,str):
        text = str(text)
    replacements = {
        "–": "-",
        "—": "-",
        "→": "->",
        "“": '"',
        "”": '"',
        "’": "'",
        "👋": ""
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

conversation = load_memory()

system_message = {
    "role": "system",
    "content": clean_text(system_prompt)
}

if not conversation:
    conversation = [system_message]
elif conversation[0].get("role") == "system":
    conversation[0] = system_message
else:
    conversation.insert(0, system_message)


#        Function call and Prompt input
def cli_loop():
    while True:
        try:
            prompt = input("You: ")
            if not prompt:
                continue

            conversation.append({"role":"user","content":clean_text(prompt)})
            answer=send_to_model(conversation)

        except (KeyboardInterrupt, EOFError):
            print("Exiting Decyphra.\n")
            break

        if answer:
            conversation.append({"role":"assistant","content":clean_text(answer)})
            if len(conversation) > MAX_MESSAGES:
                conversation[:]=[conversation[0]] + conversation[-(MAX_MESSAGES-1):]

            save_memory(conversation)

            print("\nResults:")
            print(answer)
        else:
            print("No response from model")

