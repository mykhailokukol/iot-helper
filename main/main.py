import os
import queue
import json

# import sounddevice as sd
import vosk

from services.common import UserConfigService


def main():
    UserConfigService().process()


if __name__ == "__main__":
    main()