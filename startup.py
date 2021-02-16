import os


# Any function within this file will be executed when the bot
# is launched, it must be a function or will be ignored!
# (or potentially crash the program)

def data_dir():
    if not os.path.exists("./data"):
        os.mkdir("./data")


def token_file():
    if not os.path.exists("./data/token"):
        open("./data/token", "w").close()
