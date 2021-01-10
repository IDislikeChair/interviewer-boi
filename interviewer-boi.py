# TODO: Better error handling and clean-up

import argparse
import os
import json
import random as rd
from gtts   import gTTS
from io     import BytesIO
from gtts.tts import gTTSError
from pydub  import AudioSegment
from pydub.playback import play
from rich.console   import Console
from time   import sleep


class CONST:
    PLAYBACK_SPEED = 1.0 # playback speed > 1.25 makes the TTS sounds like they are on Helium.
    # DEFAULT_JSON = os.path.join(os.path.dirname(__file__), "example.json")
    SLEEP_TIME = 3


def text_to_speech(text: str, lang: str) -> None:
    byte = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(byte)
    byte.seek(0)

    sound = AudioSegment.from_file(byte, format="mp3")
    sound_speed_changed = sound._spawn(
        sound.raw_data,
        overrides={
            "frame_rate": int(sound.frame_rate * CONST.PLAYBACK_SPEED)
        }
    )
    play(sound_speed_changed)


def fill_in_blank(text:str, card:dict) -> str:
    text_filled = text
    to_replace = ""
    for i, char in enumerate(text):
        if to_replace != "":
            to_replace += char
            if char == "}":
                try:
                    text_filled = text_filled.replace(
                        to_replace, 
                            rd.choice(card[to_replace[1:-1]])

                    )
                except KeyError:
                    raise KeyError((f"Cannot replace [yellow]{to_replace}[/] in [yellow]{text}[/]."))
                to_replace = ""
        if char == "{":
            to_replace += "{"
    
    return text_filled


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TODO")
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        "-i",
        # type=str, default=CONST.DEFAULT_JSON,
        help=f"Specify input .json file",
        required=True
    )
    parser.add_argument(
        "-s", "--speed", 
        type=float, default=CONST.PLAYBACK_SPEED,
        help=f"Set playback speed (default = {CONST.PLAYBACK_SPEED})"
    )
    parser.add_argument(
        "-t", "--time",
        type=int, default=CONST.SLEEP_TIME,
        help=f"Time in seconds before the audio play (default = {CONST.SLEEP_TIME})"
    )
    args = parser.parse_args()

    console = Console()

    try:
        with open(args.i, "r", encoding="utf-8") as f:
            data = f.read()
        obj = json.loads(data)
        lang = obj["lang"]
        deck = obj["deck"]
    except FileNotFoundError:
        console.print("JSON not found")
        console.input("Press Enter to continue...")
        quit()
    except json.JSONDecodeError:
        console.print("Invalid JSON")
        console.input("Press Enter to continue...")
        quit()
    except KeyError as e:
        console.print(f"{e} is not specified in JSON")
        console.input("Press Enter to continue...")
        quit()

    i = 1
    while True:
        try:
            console.clear()
            card = rd.choice(deck)
            console.print(f"Q.{i} ", end="")

            try:
                read_text = fill_in_blank(card["read_text"], card)
            except KeyError as e:
                console.print(str(e))
                console.print("Skipping this card")
                console.input("Press Enter to continue...")
                continue

            for _ in range(args.time):
                sleep(1)
                console.print("● ", end="", style="blue")
            console.print()
                
            text_to_speech(read_text, lang)


            if "display_text" in card:
                console.print(rd.choice(card["display_text"]))

            while True:
                action = console.input("[green]Enter - continue[/] | [yellow]r - replay[/] | [blue]s - show question[/] | [red]ctrl+C - exit[/]: ")
                if action.lower() == "r":
                    text_to_speech(read_text, lang)
                if action.lower() == "s":
                    console.print(read_text)
                elif action.lower() == "":
                    break

            i+=1

        except gTTSError as e:
            console.print(str(e))
            console.input("Press Enter to continue...")
            quit()

        except KeyboardInterrupt:
            break