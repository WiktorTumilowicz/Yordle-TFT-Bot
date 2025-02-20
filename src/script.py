from contextlib import nullcontext
from enum import Enum
import cv2
import numpy as np
import keyboard
import mss
import pyautogui
import pytesseract
import re
from time import time, sleep

tesseract_location = open('tesseract.txt', 'r').read()
pytesseract.pytesseract.tesseract_cmd = tesseract_location

# Importing images for matching
yordle_card_image = cv2.imread('charCards\\yordleCard.png', cv2.IMREAD_UNCHANGED)
janna_image = cv2.imread('charCards\\janna.png', cv2.IMREAD_UNCHANGED)
common_orb_image = cv2.imread('orbPickups\\commonOrb.png', cv2.IMREAD_UNCHANGED)
rare_orb_image = cv2.imread('orbPickups\\rareOrb.png', cv2.IMREAD_UNCHANGED)
legendary_orb_image = cv2.imread('orbPickups\\legendaryOrb.png', cv2.IMREAD_UNCHANGED)

# Importing Stage Images
stage_one_image = cv2.imread('stageNumbers\\stageOne.png', cv2.IMREAD_UNCHANGED)
stage_two_image = cv2.imread('stageNumbers\\stageTwo.png', cv2.IMREAD_UNCHANGED)
stage_three_image = cv2.imread('stageNumbers\\stageThree.png', cv2.IMREAD_UNCHANGED)
stage_four_image = cv2.imread('stageNumbers\\stageFour.png', cv2.IMREAD_UNCHANGED)
stage_five_image = cv2.imread('stageNumbers\\stageFive.png', cv2.IMREAD_UNCHANGED)
stage_six_image = cv2.imread('stageNumbers\\stageSix.png', cv2.IMREAD_UNCHANGED)

dash_one_image = cv2.imread('stageNumbers\\dashOne.png', cv2.IMREAD_UNCHANGED)
dash_two_image = cv2.imread('stageNumbers\\dashTwo.png', cv2.IMREAD_UNCHANGED)
dash_three_image = cv2.imread('stageNumbers\\dashThree.png', cv2.IMREAD_UNCHANGED)
dash_four_image = cv2.imread('stageNumbers\\dashFour.png', cv2.IMREAD_UNCHANGED)
dash_five_image = cv2.imread('stageNumbers\\dashFive.png', cv2.IMREAD_UNCHANGED)
dash_six_image = cv2.imread('stageNumbers\\dashSix.png', cv2.IMREAD_UNCHANGED)
dash_seven_image = cv2.imread('stageNumbers\\dashSeven.png', cv2.IMREAD_UNCHANGED)

# Importing Yordle Ult Images
poppy_ult_image = cv2.imread('ultIcons\\poppyUlt.png', cv2.IMREAD_UNCHANGED)
ziggs_ult_image = cv2.imread('ultIcons\\ziggsUlt.png', cv2.IMREAD_UNCHANGED)
lulu_ult_image = cv2.imread('ultIcons\\luluUlt.png', cv2.IMREAD_UNCHANGED)
tristana_ult_image = cv2.imread('ultIcons\\tristanaUlt.png', cv2.IMREAD_UNCHANGED)
heimer_ult_image = cv2.imread('ultIcons\\heimerUlt.png', cv2.IMREAD_UNCHANGED)
vex_ult_image = cv2.imread('ultIcons\\vexUlt.png', cv2.IMREAD_UNCHANGED)

class Champions(Enum) :
    Nothing=0
    Something=1
    Poppy=2
    Ziggs=3
    Lulu=4
    Tristana=5
    Heimerdinger=6
    Vex=7
    Janna=8
    Veigar=9

# Hex Positions
hex_positions = [[561, 444, 0], [679, 444, 0], [787, 444, 0], [900, 444, 0], [1020, 444, 0], [1136, 444, 0], [1250, 444, 0],
                 [607, 515, 0], [730, 515, 0], [846, 515, 0], [963, 515, 0], [1081, 515, 0], [1200, 515, 0], [1320, 515, 0],
                 [561, 591, 0], [679, 591, 0], [787, 591, 0], [900, 591, 0], [1020, 591, 0], [1136, 591, 0], [1250, 591, 0],
                 [607, 670, 0], [730, 670, 0], [846, 670, 0], [963, 670, 0], [1081, 670, 0], [1200, 670, 0], [1320, 670, 0]]

bench_positions = [[457, 787, 0], [575, 787, 0], [683, 787, 0], [802, 787, 0], [920, 787, 0], [1040, 787, 0], [1156, 787, 0], [1270, 787, 0], [1390, 787, 0]]

# Screenshotter
sct = mss.mss()

bottomval = 0.9

yordlesBought = 0

singleExpBuy = 0

type = 'null'

gold = 0
level = 1

# Shop Area
shop_dimensions = {
        'left': 472,
        'top': 924,
        'width': 1010,
        'height': 151
    }

monitor_dimensions = {
        'left': 0,
        'top': 0,
        'width': 1920,
        'height': 1080
    }

level_dimensions = {
        'left': 265,
        'top': 878,
        'width': 160,
        'height': 30
    }

gold_dimensions = {
        'left': 868,
        'top': 883,
        'width': 40,
        'height': 30
    }

stage_dimensions = {
        'left': 740,
        'top': 1,
        'width': 440,
        'height': 34
    }

def orbPickups():

    sleep(0.4)
    boardScr = np.array(sct.grab(monitor_dimensions))

    # Common Orbs
    matchedCommonOrbs = cv2.matchTemplate(boardScr, common_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedRareOrbs = cv2.matchTemplate(boardScr, rare_orb_image, cv2.TM_CCOEFF_NORMED)
    matchedLegendaryOrbs = cv2.matchTemplate(boardScr, legendary_orb_image, cv2.TM_CCOEFF_NORMED)

    orbLocations = []

    # Adding Common Orbs
    yloc, xloc = np.where(matchedCommonOrbs >= 0.72)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(common_orb_image.shape[1]), int(common_orb_image.shape[0])])
        break
    
    # Adding Rare Orbs
    yloc, xloc = np.where(matchedRareOrbs >= 0.72)

    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(rare_orb_image.shape[1]), int(rare_orb_image.shape[0])])
        break

    # Adding Legendary Orbs
    yloc, xloc = np.where(matchedLegendaryOrbs >= 0.72)
    
    for (x, y) in zip(xloc, yloc):
        orbLocations.append([int(x), int(y), int(legendary_orb_image.shape[1]), int(legendary_orb_image.shape[0])])
        break

    for (x, y, w, h) in orbLocations:
        pyautogui.moveTo(x=x, y=y, duration=0.2)
        pyautogui.mouseDown(button='right')
        sleep(0.1)
        pyautogui.mouseUp(button='right')
        sleep(1.5)


def purchaseUnits():

    global yordlesBought
    sleep(0.4)
    shopScr = np.array(sct.grab(shop_dimensions))

    matchedYordleCards = cv2.matchTemplate(shopScr, yordle_card_image, cv2.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(matchedYordleCards >= bottomval)

    yordleCards = []

    for (x, y) in zip(xloc, yloc):
        yordlesBought = yordlesBought + 1
        yordleCards.append([int(x), int(y), int(yordle_card_image.shape[1]), int(yordle_card_image.shape[0])])

    if level >= 7:
        
        matchedJannaCard = cv2.matchTemplate(shopScr, janna_image, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(matchedJannaCard >= bottomval)

        for (x, y) in zip(xloc, yloc):
            yordleCards.append([int(x), int(y), int(janna_image.shape[1]), int(janna_image.shape[0])])


    for (x, y, w, h) in yordleCards:
        pyautogui.moveTo(x=x+472+(w/2), y=y+924+(h/2), duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()


def getStageNumber():

    sleep(0.4)
    stageScr = np.array(sct.grab(stage_dimensions))

    StageOne = cv2.matchTemplate(stageScr, stage_one_image, cv2.TM_CCOEFF_NORMED).max()
    StageTwo = cv2.matchTemplate(stageScr, stage_two_image, cv2.TM_CCOEFF_NORMED).max()
    StageThree = cv2.matchTemplate(stageScr, stage_three_image, cv2.TM_CCOEFF_NORMED).max()
    StageFour = cv2.matchTemplate(stageScr, stage_four_image, cv2.TM_CCOEFF_NORMED).max()
    StageFive = cv2.matchTemplate(stageScr, stage_five_image, cv2.TM_CCOEFF_NORMED).max()
    StageSix = cv2.matchTemplate(stageScr, stage_six_image, cv2.TM_CCOEFF_NORMED).max()

    stageVals = [StageOne, StageTwo, StageThree, StageFour, StageFive, StageSix]
    maxStageMatch = max(stageVals)
    stageValue = stageVals.index(maxStageMatch) + 1


    DashOne = cv2.matchTemplate(stageScr, dash_one_image, cv2.TM_CCOEFF_NORMED).max()
    DashTwo = cv2.matchTemplate(stageScr, dash_two_image, cv2.TM_CCOEFF_NORMED).max()
    DashThree = cv2.matchTemplate(stageScr, dash_three_image, cv2.TM_CCOEFF_NORMED).max()
    DashFour = cv2.matchTemplate(stageScr, dash_four_image, cv2.TM_CCOEFF_NORMED).max()
    DashFive = cv2.matchTemplate(stageScr, dash_five_image, cv2.TM_CCOEFF_NORMED).max()
    DashSix = cv2.matchTemplate(stageScr, dash_six_image, cv2.TM_CCOEFF_NORMED).max()
    DashSeven = cv2.matchTemplate(stageScr, dash_seven_image, cv2.TM_CCOEFF_NORMED).max()

    dashNums = [DashOne, DashTwo, DashThree, DashFour, DashFive, DashSix, DashSeven]
    maxDashMatch = max(dashNums)
    dashValue = dashNums.index(maxDashMatch) + 1


    return stageValue * 10 + dashValue

def roundType():
    # PvE Stage. Checking for Stage '1 - x', 'x - 1', or 'x - 7'

    if stageNumber == 11 or (stageNumber - 4) % 10 == 0:
        type = 'carousel'
    elif stageNumber < 20 or (stageNumber - 7) % 10 == 0:
        type = 'pve'
    elif (stageNumber - 1) % 10 == 0:
        type = 'postpve'
    else:
        type = 'standard'

    return type

def goldRead():

    sleep(0.4)
    goldScr = np.array(sct.grab(gold_dimensions))
    goldScr = np.flip(goldScr[:, :, :3], 2)

    goldCurrent = 0

    # Reading the gold and saving it
    try:
        goldText = pytesseract.image_to_string(goldScr, config='--psm 8')
        goldNumFind = re.findall('[0-9]+', goldText)
        goldCurrent = int(goldNumFind[0])
    except:
        print("Not tabbed onto league!")

    return goldCurrent

def levelRead():

    sleep(0.4)
    # Changing to RGB
    levelScr = np.array(sct.grab(level_dimensions))
    levelScr = np.flip(levelScr[:, :, :3], 2)

    levelCurrent = 1

    # Reading the level and saving it
    try:
        levelText = pytesseract.image_to_string(levelScr)
        lvlNumFind = re.findall('[0-9]+', levelText)
        levelCurrent = int(lvlNumFind[0])
    except:
        print("Not tabbed onto league!")

    return levelCurrent

def checkYordle(yor):

    # 0 = Nothing, 1 = Something, 2 = Poppy, 3 = Ziggs, 4 = Lulu, 5 = Tristana, 6 = Heimerdinger, 7 = Vex, 8 = Janna, 9 = Veigar
    # Right clicking to see character
    pyautogui.moveTo(x=bench_positions[yor][0], y=bench_positions[yor][1], duration=0.2)

    pyautogui.mouseDown(button='right')
    sleep(0.1)
    pyautogui.mouseUp(button='right')
    sleep(0.4)

    # Right Clicked Unit Screenshot
    unitScr = np.array(sct.grab(monitor_dimensions))

    poppySpot = cv2.matchTemplate(unitScr, poppy_ult_image, cv2.TM_CCOEFF_NORMED).max()
    ziggsSpot = cv2.matchTemplate(unitScr, ziggs_ult_image, cv2.TM_CCOEFF_NORMED).max()
    luluSpot = cv2.matchTemplate(unitScr, lulu_ult_image, cv2.TM_CCOEFF_NORMED).max()
    tristanaSpot = cv2.matchTemplate(unitScr, tristana_ult_image, cv2.TM_CCOEFF_NORMED).max()
    heimerSpot = cv2.matchTemplate(unitScr, heimer_ult_image, cv2.TM_CCOEFF_NORMED).max()
    vexSpot = cv2.matchTemplate(unitScr, vex_ult_image, cv2.TM_CCOEFF_NORMED).max()
    
    yorVals = [poppySpot, ziggsSpot, luluSpot, tristanaSpot, heimerSpot, vexSpot]
    maxYordleMatch = max(yorVals)
    
    if maxYordleMatch > 0.95:
        return yorVals.index(maxYordleMatch) + 2
    else:
        return 0
        




def stageOneTwo():
    # Moving first unit on
    pyautogui.moveTo(x=bench_positions[0][0], y=bench_positions[0][1], duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x=hex_positions[2][0], y=hex_positions[2][1], duration=0.2)
    pyautogui.mouseUp()

    hex_positions[2][2] = checkYordle(2)

def stageOneThree():
    # Buying a second unit
    pyautogui.moveTo(x=565, y=1000, duration=0.2)
    pyautogui.mouseDown()
    sleep(0.05)
    pyautogui.mouseUp()

    # Moving on a unit
    pyautogui.moveTo(x=bench_positions[0][0], y=bench_positions[0][1], duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(x=hex_positions[2][0], y=hex_positions[2][1], duration=0.2)
    pyautogui.mouseUp()

# Game Loop
def level_up():
    pyautogui.moveTo(x=360, y=960, duration=0.2)
    pyautogui.mouseDown()
    sleep(0.05)
    pyautogui.mouseUp()

while True:

    sleep(0.1)

    # Format stage in 10's, dash in 1's eg 2-3 is 23
    stageNumber = getStageNumber()

    # Checking if standard, PvE, or carousel
    type = roundType()
    
    print(stageNumber)

    # YORDLE PURCHASING FROM NATURAL ROLL
    purchaseUnits()

    # LEVEL & GOLD INFORMATION

    gold = goldRead()

    level = levelRead()

    print(level)
    print(gold)
    print(type)

    if singleExpBuy == 0 and gold > 14:
        level_up()

        singleExpBuy = singleExpBuy + 1


    # Level if below 6
    while (gold >= 54 and level < 6):
        level_up()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()
    
    # Roll if 6
    while (gold >= 52 and level == 6):

        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()

    # Skip to 8 (Janna and Veigar)
    if (gold >= 70 and level == 7):
        while (level < 8):
            level_up()

            level = levelRead()


    while (gold >= 12 and level >= 8):
        pyautogui.moveTo(x=360, y=1040, duration=0.2)
        pyautogui.mouseDown()
        sleep(0.05)
        pyautogui.mouseUp()

        purchaseUnits()

        gold = goldRead()
        level = levelRead()

    if (stageNumber == 12):
        stageOneTwo()

    if (stageNumber == 13):
        stageOneThree()


    while stageNumber == getStageNumber():
        if (type == 'pve' or type == 'postpve'):
            orbPickups()

        purchaseUnits()
