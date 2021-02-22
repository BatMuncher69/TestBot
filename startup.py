import os


# Any function within this file will be executed when the bot
# is launched, it must be a function or will be ignored!
# (or potentially crash the program)
executed_functions = []  # used to ensure that if a function calls another one on startup, it is not ran again after


def data_dir():
    print("Data dir executed")
    if not os.path.exists("./data"):
        os.mkdir("./data")


def token_file():
    try:
        if not os.path.exists("./data/token"):
            open("./data/token", "w").close()
    except FileNotFoundError:
        data_dir()
        executed_functions.append(data_dir)


def auth_json():
    try:
        if not os.path.exists("./data/auth.json"):
            auth = open("./data/auth.json", "w")
            auth.write("{}")  # validates json file
            auth.close()
    except FileNotFoundError:
        data_dir()
        executed_functions.append(data_dir)
