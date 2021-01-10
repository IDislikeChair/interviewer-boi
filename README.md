# Interviewer Boi

Interviewer Boi is a program that reads flash cards for speaking or interview style exam, with some functionality to replace some word in card with flags and display text.
This boi makes use of Google text-to-speech API.


## Setup

For windows user, there is an `.exe` file provided. See [Release](https://github.com/IDislikeChair/interviewer-boi/releases/latest).

TO DO !

## How to use

Interview Boi uses a deck `.json` file. `example.json` is provided as an example.

```interviewer-boi -i example.json```


## Deck `.json` Formatting

`lang` value specify language for text-to-speech.
`deck` value is an array containing cards.

Each cards contains
* `read_text` - text that that TTS read. See [gtts.lang](https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang).
* `display_text` - array of text that display after the TTS. If multiple strings are provided, one will be selected randomly. (optional)
* **replacement flags** - array of text that replace flags in `read_text`. Flag is contain in curly braces `{flag}`. See the second in `example.json` for a replacement example. A `read_text` can have any number of flags.

Part of `example.json`
```
{
    "lang": "ko",
    "flash_cards": [
        {
            "read_text": "이것이 무엇입니까?",
            "display_text": [
                "The object is textbook",
                "The object is desk"
            ]
        },

        {
            "read_text": "이것이 {object}입니까?",
            "display_text": [
                "The object is textbook",
                "The object is desk"
            ],
            "object" : [
                "공책"
                "잭상",
            ]
        },
        ...
    ]
}
```

# Command line arguments

* `-s --speed` - Speed of TTS (Default to 1.0)
* `-t --time ` - Time in seconds to wait before the text is read (Default to 3)


## Special Thanks to
ルーノ•アルスヴェール (Luno) for coming up this creative name.