import os


def install():
    print("Installing Prerequisite")
    os.system("pip install -r requirements.txt")
    print("All Prerequisite Installed")


if __name__ == "__main__":
    install()