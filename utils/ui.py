import time
import sys
from colorama import Fore


def loading(text="Loading", delay=0.3):

    print(Fore.YELLOW + text, end="")

    for _ in range(3):

        time.sleep(delay)

        print(".", end="")

        sys.stdout.flush()

    print("\n")


def success(msg):

    print(Fore.GREEN + "✔ " + msg)


def error(msg):

    print(Fore.RED + "✖ " + msg)


def info(msg):

    print(Fore.BLUE + "ℹ " + msg)