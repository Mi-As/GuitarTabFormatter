# GuitarTabFormatter

Use this script to download chords from **ultimate-guitar.com** as text or convert them to latex syntax.

### Usage

Download and run the script with pyhton. (You may have to install some additional packages e.g. `bs4` and `urllib`)

```
python3 ultimate_guitar_parser.py
```

Follow the instruction and submit the song url (Only **ultimate-guitar** tabs type **chords** are supported).

```
Enter the ultimate guitar web link for your tabs:
https://tabs.ultimate-guitar.com/tab/boywithuke/two-moons-chords-3757571
```

The file called `TabFormatter.txt` will contain the output.

```
[Verse 1]

F#m                 A                              E
   Two moons, I can feel myself start catching on fire
                    Bm
You knew, yeah you kept it to yourself, to your self
...
```

### Latex Support

To convert the tabs directly to the Latex Syntax (see [The Songs Package](http://songs.sourceforge.net/songsdoc/songs.html#sec5.7)) you can use the `write_latex_tab` funktion from the `TabFormatter` class.

