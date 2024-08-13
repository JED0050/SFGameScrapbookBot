# Shakes and Fidget - Scrapbook Bot
## What is it?
A bot for the game Shakes and Fidget. It can be used to find items that are not yet registered in your scrapbook.
You need to have the Real Holy Grail! Without it, the script will not work.
## How to use it?
- Start your SFGame on Steam in fullscreen.
- Open the Hall of Fame in the game and start at position X.
- Run the Python script ```bot.py```.
- Enter position X from the Hall of Fame into the script console.
- Choose the scroll direction (1 = down, 0 = up) by entering the number into the script console.
- The positions of found players will be written to the file ```bot_output_YYYY_MM_DD_HH_mm.txt```.
- Simply find those players by their HoF position in the text file and defeat those players for scrapbook credit.
## Dependencies
Python libraries keyboard and Pillow. This script probably works only on Windows.
```bash
pip install keyboard
pip install Pillow
```
## Credit
Inspired by and based on: [nkaers/ShakesBot](https://github.com/nkaers/ShakesBot)
