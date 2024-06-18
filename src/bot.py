import math
import operator
from functools import reduce
from time import sleep
from datetime import datetime

import keyboard  # pip install keyboard
import win32gui
from PIL import ImageGrab  # pip install Pillow
from PIL import ImageOps



def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))


# this function searches for the Game Application and returns it window_handle
def get_app_list(handles=[]):
    mlst = []
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        if "Shakes & Fidget" in handle[1]:
            mlst.append(handle)
    return mlst


# this function compares two given Images and returns the difference as an Integer
def compare(i1, i2):
    h1 = i1.histogram()
    h2 = i2.histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    return rms


def write_to_file(file_name, line):
    with open(file_name, 'a') as f:
        f.write(f"{line}\n")


def find_too_many(found_players):
    # we found 10 scraps in last 50 players (it's too many, something went wrong)
    len_found = len(found_players)

    if len_found < 50:
        return False
    if abs(found_players[len_found - 51] - found_players[len_found - 1]) > 501:
        return False
    return True


def main():

    # intro talk
    version = "1.1"
    print("Welvome to SFGame-ScrapbookBot v" + version)
    print("\t\t\t-by G3S")
    print()
    print("Place your game on main monitor and on fullscreen")

    # search for the Game Window and store it in the shakes variable
    appwindows = get_app_list()
    if len(appwindows) == 0:  # SFGame app not found
        rect = [0, 0, 1928, 1048]
        leftcrop = 1150
        botcrop = 400
    else:
        shakes = appwindows[0][0]

        # set the Game Window as the active window
        win32gui.SetForegroundWindow(shakes)

        # store the coordinates which we use later to find and crop the images
        rect = win32gui.GetWindowRect(shakes)
        leftcrop = int(rect[2] / 1.68)
        botcrop = int(rect[3] / 2.62)

    # init
    pos_hof = int(input("Hall of Fame start position\t: "))
    scan_dir = input("Scan direction, UP = 0 | DOWN = 1\t: ")
    found_players = []

    act_scan = 0
    max_scan = 10000

    min_diff_scrap = 3.0

    time = datetime.now()
    file_name = time.strftime("bot_output_%Y_%m_%d_%H_%M_%S.txt")

    if scan_dir == "1":
        scan_dir = "down" 
    else:
        scan_dir = "up"

    old_image = None


    print(f"\nClick into game to player on HoF position {pos_hof} in next 5 seconds!")
    sleep(5)
    print("Bot started!\n")

    while pos_hof > 1 and act_scan < max_scan:
        # Exit program
        if keyboard.is_pressed("q") or keyboard.is_pressed("z") or keyboard.is_pressed("esc"):
            return

        sleep(0.2)

        images = []
        new_image_raw = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
        new_image_crop = ImageOps.crop(new_image_raw, (leftcrop, 0, 0, botcrop))
        #new_image_crop.save(f"crop_tmp_img_act_scan.png")

        # Player is not refreshed
        if old_image is not None and compare(old_image, new_image_crop) < 50.0:    
            for i in range(3):
                sleep(0.175)
                keyboard.press_and_release("down")
                sleep(0.175)
                keyboard.press_and_release("up")
            sleep(0.4)
            new_image_raw = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
            new_image_crop = ImageOps.crop(new_image_raw, (leftcrop, 0, 0, botcrop))

        old_image = new_image_crop
        images.append(new_image_crop)

        max_diff = 0.0

        for k in range(3):
            sleep(0.15)
            new_image_raw = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
            new_image_crop = ImageOps.crop(new_image_raw, (leftcrop, 0, 0, botcrop))
            images.append(new_image_crop)
            sleep(0.15)

            for i in range(k+1):
                new_diff = compare(images[i], new_image_crop)
                if new_diff > max_diff:
                    max_diff = new_diff
                    if max_diff > min_diff_scrap:
                        break
            
            if max_diff > min_diff_scrap:
                break

        # compute the difference and print it to the console
        print(f"Pos: {pos_hof}\tDiff: {max_diff}\tFound: {found_players}")
        if act_scan % 100 == 0:
            print("\tpress 'q' or 'esc' to exit program")

        # if the Images are different enough the loop will break since the Bot expects to have found an unknown item
        # if the Images are the same the bot will increment its counter and go up to the next player
        if max_diff > min_diff_scrap:
            found_players.append(pos_hof)
            print(f"Player with missing item found! Position: {pos_hof}")
            write_to_file(file_name, pos_hof)

        if find_too_many(found_players):
            break

        keyboard.press_and_release(scan_dir)
        act_scan += 1
        if scan_dir == "up":
            pos_hof -= 1
        else:
            pos_hof += 1

    print(f"Players with items to scrapbook: {found_players}")


if __name__ == "__main__":
    main()