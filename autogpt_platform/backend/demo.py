# %%

import asyncio

import requests

# %%
topic = "Artificial Intelligence"
url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
rsp = requests.get(url)
rsp


# %%

# %%
event_loop = asyncio.new_event_loop()
event_loop.run_forever()


# %%
def hello_printer():
    print(
        "hi, i a"
        "Hi, I am a lowly, simple printer, though I have all I "
        "need in life -- \nfresh paper and my dearly beloved octopus "
        "partner in crime."
    )


hello_printer()


async def loudmouth_penguin(magic_number: int):
    print(
        "I am a super special talking penguin. Far cooler than that printer. "
        f"By the way, my lucky number is: {magic_number}."
    )
