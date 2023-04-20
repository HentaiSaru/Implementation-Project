import ModCheck

"""
自用單線程無優化
"""

test = [
    "https://blackmod.net/threads/12167/",
    "https://blackmod.net/threads/28267/",
]

ModCheck.run(test)

for out in ModCheck.processing.Result():
    print(out)