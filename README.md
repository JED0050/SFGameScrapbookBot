# Shakes and Fidget - Scrapbook bot
## What is it?
A bot for the game Shakes and Fidget. It can be used to find items which are not registered in your scrapbook yet.
You need to have the Real Holy Grail! without it script would not work.
## How to use it?
- start your SFGame on steam
- open Hall of Fame in game and start at position X
- run python script ```bot.py```
- write posion X from Hall of Fame to script console
- choose scroll direction (1 = down, 0 = up) by writing numbner to script console
- positions of found players will be writen in file ```bot_output_YYYY_MM_DD_HH_mm.txt```
- simpli find those plyers by HoF posion in txt file and kill those players for scrap credit
## Dependences
Python libraries pywinauto and Pillow. Propably this script works only for windows.
```bash
pip install pywinauto
pip install Pillow
```
## Credit
inspired and based on: [nkaers/ShakesBot](https://github.com/nkaers/ShakesBot)
