import os


def start():
    print("Updating requirements.txt")
    # os.system("pipreqs --encoding utf-8 --force")
    os.system("pip freeze > requirements.txt")


if __name__ == "__main__":
    start()