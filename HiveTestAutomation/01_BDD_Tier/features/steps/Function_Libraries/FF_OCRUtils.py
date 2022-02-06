from PIL import Image, ImageOps, ImageFilter
import pytesseract
from subprocess import call
import os
import numpy as np
import re
from Thermostat_Screen_Text import EE_Thermostat_ScreenText_En as oENText
from Thermostat_Screen_Text import EE_Thermostat_ScreenText_Ita as oITAText
from Thermostat_Screen_Text import EE_Thermostat_ScreenText_Fr as oFRText
import FF_device_utils as dutils
import FF_SLT4_OCRUtil as outils
import time

def capture(context):
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    timestamp = context.reporter.getTimeStamp(False)
    call(["raspistill", "--timeout", "2", "-q", "100", "-br", "50", "-sh", "100", "-ex", "night", "-awb", "auto", "-o",
          path + '/capture' + timestamp + '.jpg', "-ss", "10000"])
    context.capturePath = path
    imgName = 'capture' + timestamp + '.jpg'
    img = Image.open(path + '/capture' + timestamp + '.jpg')
    context.img = img
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(context.capturePath + '/test.jpg')
    img = Image.open(context.capturePath + '/test.jpg')
    return img, imgName


def captureOriginal(context):
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    timestamp = context.reporter.getTimeStamp(False)
    call(["raspistill", "--timeout", "1", "-q", "100", "-br", "50", "-sh", "100", "-ex", "night", "-awb", "auto", "-o",
          path + '/capture' + timestamp + '.jpg', "-ss", "10000"])
    context.capturePath = path
    imgName = 'capture' + timestamp + '.jpg'
    img = Image.open(path + '/capture' + timestamp + '.jpg')
    context.img = img
    img = ImageOps.autocontrast(img)
    # process.terminate()
    #img, imgName = "", ""
    return img, imgName


def loadImage(imgName, context):
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = Image.open(path + "/" + imgName)
    context.img = img
    img = ImageOps.autocontrast(img)
    return img


def getDay(img, context):
    width, height = img.size
    left = width / 8
    right = width / 5
    bottom = height / 3.5
    top = height / 10
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(context.capturePath + '/Date.jpg')
    img = Image.open(context.capturePath + '/Date.jpg')
    word = pytesseract.image_to_string(img)
    print("Date = " + word.encode('ascii', 'ignore').decode('ascii'))
    return word


def getModes(img, context):
    width, height = img.size
    left = width / 8
    right = width / 1.05
    bottom = height / 3.8
    top = height / 3
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(context.capturePath + '/HeatMode.jpg')
    img = Image.open(context.capturePath + '/HeatMode.jpg')
    word = pytesseract.image_to_string(img)
    word = str(word).encode('ascii', 'ignore').decode('ascii')
    print("Heat Mode = " + word)
    return word

def pressAndCature(context, myNodeId, ep, strButton, strAction, intSleepTime, strLogType, strDesciption, strStatus):
    dutils.pressDeviceButton(myNodeId, ep, strButton, strAction)
    time.sleep(intSleepTime)
    _, imgName = captureOriginal(context)
    context.reporter.ReportEvent(strLogType, strDesciption, strStatus)
    return _, imgName

def pressAndAppendList(context, myNodeId, ep, strButton, strAction, intSleepTime, strLogType, strDesciption, strStatus, lstReport):
    _, imgName = pressAndCature(context, myNodeId, ep, strButton, strAction, intSleepTime, strLogType, strDesciption, strStatus)
    lstReport.append([imgName, strLogType, strDesciption, strStatus])


def rotateAndCature(context, myNodeId, ep, strAction, intTimes, intSleepTime,strLogType, strDesciption, strStatus):
    dutils.rotateDial(myNodeId, ep, strAction, intTimes)
    time.sleep(intSleepTime)
    _, imgName = captureOriginal(context)
    context.reporter.ReportEvent(strLogType, strDesciption, strStatus)
    return _, imgName
def getText(img, context):
    word = pytesseract.image_to_string(img)
    word = str(word).encode('ascii', 'ignore').decode('ascii')
    print("Conversion = " + word)
    return word


def getActualTemp(img, context):
    tempImg = img
    width, height = img.size
    left = width / 8
    right = width / 3.2
    bottom = height / 4
    top = height / 6
    frameTime = img.crop((int(top), int(left), int(right), int(bottom)))
    frameTime.save(context.capturePath + '/Time.jpg')
    img = Image.open(context.capturePath + '/Time.jpg')
    word = pytesseract.image_to_string(img)
    print("Time = " + word)
    img = Image.open(context.capturePath + '/test.jpg')
    width, height = img.size
    left = width / 2.2
    right = width / 1.18
    bottom = height / 1.8
    top = height / 1.8
    frameTarget = img.crop((int(top), int(left), int(right), int(bottom)))
    frameTarget.save(context.capturePath + '/Target.jpg')
    img = Image.open(context.capturePath + '/Target.jpg')
    word = pytesseract.image_to_string(img)
    value = ""
    for values in word.split("\n\n"):
        if "ACTUAL" not in str(values).strip() and (values.strip() != ""):
            value = values
            break
    print("Actual Temp = " + value)
    strTemp = value

    img = tempImg
    width, height = img.size
    left = width / 2.2
    right = width / 1.08
    bottom = height / 1.5
    top = height / 1.55
    frameTarget = img.crop((int(top), int(left), int(right), int(bottom)))
    frameTarget.save(context.capturePath + '/TargetA.jpg')
    img = Image.open(context.capturePath + '/TargetA.jpg')
    word = pytesseract.image_to_string(img)
    value = ""
    for values in word.split("\n\n"):
        if "." in str(values):
            value = values
            break
    print("Actual Temp Decimal= " + value)
    strTemp = strTemp + value
    return strTemp


def getTargetTemp(img, context):
    tempImg = img
    img = ImageOps.autocontrast(img)
    # img = ImageOps.invert(img)
    # img = img.convert('1')
    width, height = img.size
    left = width / 2  # top
    right = width / 1.08
    bottom = height / 1.7
    top = height / 11  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(context.capturePath + '/test1.jpg')
    img = Image.open(context.capturePath + '/test1.jpg')
    word = pytesseract.image_to_string(img)
    value = ""
    value = word.split("\n\n")[0].split(".")[0]
    print("Target Temp = " + value)
    strTemp = value
    img = tempImg
    img = ImageOps.autocontrast(img)
    # img = img.convert('1')
    width, height = img.size
    left = width / 2  # top
    right = width / 2.8
    bottom = height / 1.77
    top = height / 6.5  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(context.capturePath + '/test2.jpg')
    img = Image.open(context.capturePath + '/test2.jpg')
    word = pytesseract.image_to_string(img)
    value = ""
    for values in word.split("\n\n"):
        if "." in str(values):
            value = values
            break
    print("Target Temp = " + value)
    strTemp = strTemp + value
    return strTemp


def getMainMenuTitle(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strTitle = word.split("\n")[0]
    print("Main Menu Tile = " + strTitle.encode('ascii', 'ignore').decode('ascii'))
    word = strTitle.encode('ascii', 'ignore').decode('ascii')"""
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/test.jpg')
    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 7
    right = width / 1.05
    bottom = height / 5
    top = height / 10
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg')
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img, config='-psm 13')
    word = word.encode('ascii', 'ignore').decode('ascii')
    return word


def getMainMenuOptions(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strOptions = word.split("\n")[1] + word.split("\n")[2]
    if str(oLang.MainMenuScreen.MainMenuSettingsOptionText).upper() in word.split("\n")[3].upper():
        strOptions = strOptions + word.split("\n")[3]
    print("Main Menu Options = " + strOptions.encode('ascii', 'ignore').decode('ascii'))
    word = strOptions.encode('ascii', 'ignore').decode('ascii')"""

    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/test.jpg')
    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.5
    right = width / 3.2
    bottom = height / 3.8
    top = height / 5.5
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatModeMain.jpg')
    img = Image.open(path + '/testHeatModeMain.jpg')
    word = pytesseract.image_to_string(img)

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.5
    right = width / 1.9
    bottom = height / 3.8
    top = height / 3.5
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatModeMain.jpg')
    img = Image.open(path + '/testHeatModeMain.jpg')
    word = word + " " + pytesseract.image_to_string(img)

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.5
    right = width / 1.4
    bottom = height / 3.8
    top = height / 2.3
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatModeMain.jpg')
    img = Image.open(path + '/testHeatModeMain.jpg')
    word = word + " " + pytesseract.image_to_string(img)

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.5
    right = width / 1
    bottom = height / 3.8
    top = height / 1.7
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatModeMain.jpg')
    img = Image.open(path + '/testHeatModeMain.jpg')
    word = word + " " + pytesseract.image_to_string(img, config='-psm 13')

    word = word.encode('ascii', 'ignore').decode('ascii')

    return word


def getMainMenuInstructionText(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strInstruction = word.split("\n")[3]
    print("Main Menu Instruction Text = " + strInstruction.encode('ascii', 'ignore').decode('ascii'))
    word = strInstruction.encode('ascii', 'ignore').decode('ascii')
    return word"""
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/ctest.jpg')
    img = Image.open(path + '/ctest.jpg')
    width, height = img.size
    left = width / 3.3
    right = width / 1.05
    bottom = height / 3
    top = height / 10
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg')
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img)
    word = word.encode('ascii', 'ignore').decode('ascii')
    return word


def getHeatMenuTitle(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strTitle = word.split("\n")[0]
    print("HeatMenuTile = " + strTitle.encode('ascii', 'ignore').decode('ascii'))
    word = strTitle.encode('ascii', 'ignore').decode('ascii')
    return word"""
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/test.jpg')
    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 7
    right = width / 1.05
    bottom = height / 5
    top = height / 10
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg')
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img)
    word = word.encode('ascii', 'ignore').decode('ascii')
    return word


def getMenuInstruction(img, oLang, context):
    img = ImageOps.autocontrast(img)
    word = pytesseract.image_to_string(img)
    strInstruction = word.split("\n")[1]
    word = strInstruction.encode('ascii', 'ignore').decode('ascii')
    print(word)
    return word


def getHeatMenuOptions(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strOptions = word.split("\n")[1] + word.split("\n")[2]

    if str(oLang.HomeScreen.Heat_Off_ModeText).upper() in word.split("\n")[3].upper():
        strOptions = strOptions + word.split("\n")[3]
    print("Heat Menu Options = " + strOptions.encode('ascii', 'ignore').decode('ascii'))
    word = strOptions.encode('ascii', 'ignore').decode('ascii')"""
    timestamp = context.reporter.getTimeStamp(False)
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/test.jpg')
    img = Image.open(path + '/test.jpg')

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 2.3
    bottom = height / 3.8
    top = height / 4.5
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg', dpi=(1000, 1000))
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img, config='-psm 13')

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 1.5
    bottom = height / 3.8
    top = height / 2.3
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/' + timestamp + 'manualtestHeatMode.jpg', dpi=(1000, 1000))

    orig_color = (100, 100, 100)
    replacement_color = (255, 255, 255)
    img = Image.open(path + '/' + timestamp + 'manualtestHeatMode.jpg').convert('RGB')
    data = np.array(img)
    data[(data < orig_color).all(axis=-1)] = (0, 0, 0)
    img2 = Image.fromarray(data, mode='RGB')
    data = np.array(img2)
    data[(data > orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    img2 = img2.filter(ImageFilter.SHARPEN)
    img2.save(path + '/' + timestamp + 'manualtestHeatModeedited.jpg')
    word = word + " " + pytesseract.image_to_string(img2, config='-psm 13')

    orig_color = (50, 50, 50)
    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 1.1
    bottom = height / 3.8
    top = height / 1.6
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/' + timestamp + 'testHeatMode.jpg')
    replacement_color = (255, 255, 255)
    img = Image.open(path + '/' + timestamp + 'testHeatMode.jpg').convert('RGB')
    data = np.array(img)
    data[(data < orig_color).all(axis=-1)] = (0, 0, 0)
    img2 = Image.fromarray(data, mode='RGB')
    data = np.array(img2)
    data[(data > orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    img2 = img2.filter(ImageFilter.SHARPEN)
    img2.save(path + '/' + timestamp + 'testHeatModeedited.jpg')
    word = word + " " + pytesseract.image_to_string(img2, config='-psm 13')

    word = word.encode('ascii', 'ignore').decode('ascii')

    return word


def getHotMenuOptions(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strOptions = word.split("\n")[1] + word.split("\n")[2]

    if str(oLang.HomeScreen.Heat_Off_ModeText).upper() in word.split("\n")[3].upper():
        strOptions = strOptions + word.split("\n")[3]
    print("Heat Menu Options = " + strOptions.encode('ascii', 'ignore').decode('ascii'))
    word = strOptions.encode('ascii', 'ignore').decode('ascii')"""
    timestamp = context.reporter.getTimeStamp(False)
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/test.jpg')
    img = Image.open(path + '/test.jpg')

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 2.3
    bottom = height / 3.8
    top = height / 5.5
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg', dpi=(1000, 1000))
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img, config='-psm 13')

    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 1.5
    bottom = height / 3.8
    top = height / 3.0
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/' + timestamp + 'manualtestHeatMode.jpg', dpi=(1000, 1000))

    orig_color = (100, 100, 100)
    replacement_color = (255, 255, 255)
    img = Image.open(path + '/' + timestamp + 'manualtestHeatMode.jpg').convert('RGB')
    data = np.array(img)
    data[(data < orig_color).all(axis=-1)] = (0, 0, 0)
    img2 = Image.fromarray(data, mode='RGB')
    data = np.array(img2)
    data[(data > orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    img2 = img2.filter(ImageFilter.SHARPEN)
    img2.save(path + '/' + timestamp + 'manualtestHeatModeedited.jpg')
    word = word + " " + pytesseract.image_to_string(img2, config='-psm 13')

    orig_color = (50, 50, 50)
    img = Image.open(path + '/test.jpg')
    width, height = img.size
    left = width / 4.3
    right = width / 1.1
    bottom = height / 3.8
    top = height / 1.8
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/' + timestamp + 'testHeatMode.jpg')
    replacement_color = (255, 255, 255)
    img = Image.open(path + '/' + timestamp + 'testHeatMode.jpg').convert('RGB')
    data = np.array(img)
    data[(data < orig_color).all(axis=-1)] = (0, 0, 0)
    img2 = Image.fromarray(data, mode='RGB')
    data = np.array(img2)
    data[(data > orig_color).all(axis=-1)] = replacement_color
    img2 = Image.fromarray(data, mode='RGB')
    img2 = img2.filter(ImageFilter.SHARPEN)
    img2.save(path + '/' + timestamp + 'testHeatModeedited.jpg')
    word = word + " " + pytesseract.image_to_string(img2, config='-psm 13')

    word = word.encode('ascii', 'ignore').decode('ascii')

    return word


def getHeatMenuInstructionText(img, oLang, context):
    """word = pytesseract.image_to_string(img)
    strInstruction = ""
    if len(word.split("\n")) > 3:
        for count in range(3,len(word.split("\n"))):
            strInstruction = strInstruction + word.split("\n")[count]
        print("Heat Menu Instruction text = " + strInstruction.encode('ascii', 'ignore').decode('ascii'))
        word = strInstruction.encode('ascii', 'ignore').decode('ascii')"""
    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/ctest.jpg')
    img = Image.open(path + '/ctest.jpg')
    width, height = img.size
    left = width / 3.3
    right = width / 1.05
    bottom = height / 3
    top = height / 10
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHeatMode.jpg')
    img = Image.open(path + '/testHeatMode.jpg')
    word = pytesseract.image_to_string(img)
    word = word.encode('ascii', 'ignore').decode('ascii')
    return word


def getHeatOffScreenText(img, oLang):
    word = pytesseract.image_to_string(img)
    return word


def getHeatBoostMenuTitle(img, oLang):
    word = pytesseract.image_to_string(img)
    strTitle = word.split("\n")[0]
    print("HeatBoostMenuTile = " + strTitle.encode('ascii', 'ignore').decode('ascii'))
    word = strTitle.encode('ascii', 'ignore').decode('ascii')
    return word


def getHeatBoostMenuOptions(img, oLang):
    word = pytesseract.image_to_string(img)
    strOptions = word.split("\n")[1] + word.split("\n")[2]
    if str(oLang.HeatMenuScreen.HeatBoostMenuInstruction1).upper() in word.split("\n")[3].upper():
        strOptions = strOptions + word.split("\n")[3]
    print("Heat Boost Menu Options = " + strOptions.encode('ascii', 'ignore').decode('ascii'))
    word = strOptions.encode('ascii', 'ignore').decode('ascii')
    return word


def getHeatBoostMenuInstructionText(img, oLang):
    word = pytesseract.image_to_string(img)
    strInstruction = ""
    if len(word.split("\n")) > 3:
        for count in range(3, len(word.split("\n"))):
            strInstruction = strInstruction + word.split("\n")[count]
        print("Heat Boost Menu Instruction text = " + strInstruction.encode('ascii', 'ignore').decode('ascii'))
        word = strInstruction.encode('ascii', 'ignore').decode('ascii')
    return word


def validateStartOverInitialScreen(oImg, oImgName, oLang, context):
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strHeatBoostMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverInstruction),
                                    strHeatMenuInstructionText,
                                    "Schedule start over Instruction 1")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverInstruction2),
                                    strHeatBoostMenuInstructionText,
                                    "Schedule start over Instruction 2")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=oImgName)


def validateStartOverSelectionScreen(oImg, imgName, oLang, context):
    strMenuTitle = getHeatMenuTitle(oImg, oLang, context)
    strOptions = getMenuInstruction(oImg, oLang, context)
    strMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverSelectionTitle), strMenuTitle,
                                    "Heat Schedule Start Over Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverOptionsEE),
                                    strOptions,
                                    "Heat Schedule Start Over Energy Efficient option")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverOptionsC),
                                    strOptions,
                                    "Heat Schedule Start Over Energy Comfort option")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatBoostMenuInstruction2),
                                    strMenuInstructionText,
                                    "Heat Schedule Start Over Instruction 2")
    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgName)


def validateBoostCancelSelectionScreen(oImg, imgName, oLang, context):
    strMenuTitle = getHeatMenuTitle(oImg, oLang, context)
    strOptions = getMenuInstruction(oImg, oLang, context)
    strMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HomeScreen.Boost_Screen_Title), strMenuTitle,
                                    "Boost screen Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HomeScreen.Boost_Screen_HW),
                                    strOptions,
                                    "Boost screen Hot Water option")
    strLog = strLog + validationLog(context, str(oLang.HomeScreen.Boost_Screen_Heat),
                                    strOptions,
                                    "Boost screen Heat option")
    strLog = strLog + validationLog(context, str(oLang.HomeScreen.Boost_Screen_InstructionText),
                                    strMenuInstructionText,
                                    "Boost screen Instruction text")
    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgName)


def validateStartOverTypeSelectionScreen(oImg, imgName, oLang, context, Option):
    strMenuTitle = getHeatMenuTitle(oImg, oLang, context)
    strOptions = getText(oImg, context)
    strMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverEEMenuTitle), strMenuTitle,
                                    "Heat Schedule Start Over Menu Title")
    if oLang.HeatMenuScreen.HeatStartOverOptionsEE in Option:
        strLog = strLog + validationLogPattern(context, r'.*06:30.*08:30.*12:00.*14:00.*16:30.*22:00.*18.*18.*',
                                               strOptions,
                                               "Heat Schedule Start Over Energy Efficient schedule",
                                               r'.*06:30.*08:30.*12:00.*14:00.*16:30.*22:00.*18.*18.*')
    elif oLang.HeatMenuScreen.HeatStartOverOptionsC in Option:
        strLog = strLog + validationLogPattern(context, r'.*06:30.*08:30.*12:00.*14:00.*16:30.*22:00.*20.*20.*',
                                               strOptions,
                                               "Heat Schedule Start Over Energy Comfort schedule",
                                               r'.*06:30.*08:30.*12:00.*14:00.*16:30.*22:00.*20.*20.*')
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatBoostMenuInstruction2),
                                    strMenuInstructionText,
                                    "Heat Schedule Start Over EC Instruction")
    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgName)

def validateMinOrMaxEvent(oImg, imgName, oLang, context, Option):
    strOptions = getText(oImg, context)
    if "MIN" in str(Option).upper():
        if "00:00" in str(strOptions):
            context.reporter.ReportEvent("Test Validation","The minimum event is 00:00","PASS")
        else:
            context.reporter.ReportEvent("Test Validation","The minimum event is not 00:00 <Br> OCR = "+strOptions,"Fail")
    if "MAX" in str(Option).upper():
        if "23:30" in str(strOptions):
            context.reporter.ReportEvent("Test Validation","The maximum event is 23:30","PASS")
        else:
            context.reporter.ReportEvent("Test Validation","The maximum event is not 23:30 <Br> OCR = "+strOptions,"Fail")



def validateStartOverConfirmationScreen(oImg, imgName, oLang, context):
    strMenuTitle = getHeatMenuTitle(oImg, oLang, context)
    strOptions = getText(oImg, context)
    strMenuInstructionText = getHeatMenuInstructionText(oImg, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverConfirmTitle), strMenuTitle,
                                    "Heat Schedule Start Over Guidede set up Menu Title")

    strLog = strLog + validationLogPattern(context,
                                           r'.*' + oLang.HeatMenuScreen.HeatStartOverHotWaterOption + '.*' + oLang.HeatMenuScreen.HeatStartOverExitOption + '.*',
                                           strOptions,
                                           "Heat Schedule Guided set up for hot water",
                                           oLang.HeatMenuScreen.HeatStartOverHotWaterOption + " " + oLang.HeatMenuScreen.HeatStartOverExitOption)
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatStartOverConfirmInstructionText),
                                    strMenuInstructionText,
                                    "Heat Schedule Start Over Guided Set up Instruction")
    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgName)


def validateIfScreenNotInHome(strMainMenuOptions, imgMenuName, context):
    if (
                            "OFF" in strMainMenuOptions or "BOOST" in strMainMenuOptions or "MANUAL" in strMainMenuOptions or "SCH" in strMainMenuOptions):
        context.reporter.ReportEvent("Test Validation", "Menu Screen is not present", "FAIL", ocrImagePath=imgMenuName)
        exit()


def validateMainMenu(oImgMenu, imgMenuName, oLang, context):
    if oLang.HomeScreen.Target_Text in getText(oImgMenu, context):
        context.reporter.ReportEvent("Event Log", "Main menu not found", "Fail")
        exit()
    strMainMenuTitle = getMainMenuTitle(oImgMenu, oLang, context)
    strMainMenuOptions = getMainMenuOptions(oImgMenu, oLang, context)
    strMainMenuInstructionText = getMainMenuInstructionText(oImgMenu, oLang, context)
    print(strMainMenuOptions)
    strText = getText(oImgMenu, context)
    validateButton(context, oImgMenu, BackButton=True, MenuButton=True, TickButton=False)
    validateIfScreenNotInHome(strMainMenuOptions, imgMenuName, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuTitle),
                                    strMainMenuTitle, "Main Menu Title")
    if True:
        strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuHeatOptionText),
                                        strMainMenuOptions.split(" ")[0], "Main Menu Heat Text")
        print(strLog + "\n")
        strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuHotWaterOptionText),
                                        strMainMenuOptions.split(" ")[1] + " " + strMainMenuOptions.split(" ")[2],
                                        "Main Menu Hotwater Text")
        print(strLog + "\n")
        strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuHolidayOptionText),
                                        strMainMenuOptions.split(" ")[3],
                                        "Main Menu Holiday Text")
        print(strLog + "\n")
        if (len(strMainMenuOptions.split(" ")) > 4):
            strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuSettingsOptionText),
                                            strMainMenuOptions.split(" ")[4],
                                            "Main Menu Settings Text ")
        print(strLog + "\n")
        strLog = strLog + validationLog(context, str(oLang.MainMenuScreen.MainMenuInstructionText),
                                        strMainMenuInstructionText,
                                        "Main Menu Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgMenuName)


def validateHeatMenu(oImgHeat, imgHeatName, oLang, context):
    if oLang.HomeScreen.Target_Text in getText(oImgHeat, context):
        context.reporter.ReportEvent("Event Log", "Main menu not found", "Fail")
        exit()
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    strHeatMenuOptions = getHeatMenuOptions(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)
    validateButton(oImgHeat, BackButton=True, MenuButton=True, TickButton=False)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuTitle),
                                    strHeatMenuTitle, "Heat Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuHeatScheduleOptionText),
                                    strHeatMenuOptions.split(" ")[0], "Heat Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuHeatManualOptionText),
                                    strHeatMenuOptions.split(" ")[1],
                                    "Heat Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuHeatOffOptionText),
                                    strHeatMenuOptions.split(" ")[2],
                                    "Heat Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleInstructionText),
                                    strHeatMenuInstructionText,
                                    "Heat Menu Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHeatScheduleMenu(oImgHeat, imgHeatName, oLang, context):
    if oLang.HomeScreen.Target_Text in getText(oImgHeat, context):
        context.reporter.ReportEvent("Event Log", "Main menu not found", "Fail")
        exit()
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    strHeatMenuOptions = getHeatMenuOptions(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)

    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleMenuTitle),
                                    strHeatMenuTitle, "Schedule Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleResumeOptionText),
                                    strHeatMenuOptions.split(" ")[0], "Schedule Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleEditOptionText),
                                    strHeatMenuOptions.split(" ")[1],
                                    "Schedule Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleStartOptionText),
                                    strHeatMenuOptions.split(" ")[2],
                                    "Schedule Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuInstructionText),
                                    strHeatMenuInstructionText,
                                    "Schedule Menu Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHotScheduleMenu(oImgHeat, imgHeatName, oLang, context):
    if oLang.HomeScreen.Target_Text in getText(oImgHeat, context):
        context.reporter.ReportEvent("Event Log", "Main menu not found", "Fail")
        exit()
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    strHeatMenuOptions = getHeatMenuOptions(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)

    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotScheduleMenuTitle),
                                    strHeatMenuTitle, "Schedule Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotScheduleResumeOptionText),
                                    strHeatMenuOptions.split(" ")[0], "Schedule Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotScheduleEditOptionText),
                                    strHeatMenuOptions.split(" ")[1],
                                    "Schedule Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotScheduleStartOptionText),
                                    strHeatMenuOptions.split(" ")[2],
                                    "Schedule Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuInstructionText),
                                    strHeatMenuInstructionText,
                                    "Schedule Menu Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHeatScheduleResumeMenu(oImgHeat, imgHeatName, oLang, context):
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    '''strHeatMenuOptions = getHeatMenuOptions(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)
    '''
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatResumeMenuTitle),
                                    strHeatMenuTitle, "Schedule Resume Menu Title")
    '''strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleResumeOptionText),
                                    strHeatMenuOptions.split(" ")[0], "Schedule Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleEditOptionText),
                                    strHeatMenuOptions.split(" ")[1] + " "+strHeatMenuOptions.split(" ")[2],
                                    "Schedule Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleStartOptionText),
                                    strHeatMenuOptions.split(" ")[3]+ " "+strHeatMenuOptions.split(" ")[4],
                                    "Schedule Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuInstructionText),
                                    strHeatMenuInstructionText,
                                    "Schedule Menu Instruction Text")'''

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHotScheduleResumeMenu(oImgHeat, imgHeatName, oLang, context):
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    '''strHeatMenuOptions = getHeatMenuOptions(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)
    '''
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotResumeMenuTitle),
                                    strHeatMenuTitle, "Schedule Resume Menu Title")
    '''strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleResumeOptionText),
                                    strHeatMenuOptions.split(" ")[0], "Schedule Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleEditOptionText),
                                    strHeatMenuOptions.split(" ")[1] + " "+strHeatMenuOptions.split(" ")[2],
                                    "Schedule Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatScheduleStartOptionText),
                                    strHeatMenuOptions.split(" ")[3]+ " "+strHeatMenuOptions.split(" ")[4],
                                    "Schedule Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatMenuInstructionText),
                                    strHeatMenuInstructionText,
                                    "Schedule Menu Instruction Text")'''

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHolidayMenu(oImgHeat, imgHeatName, oLang, context, strScreen, strSubScreen=""):
    strHeatMenuTitle = getHeatMenuTitle(oImgHeat, oLang, context)
    strHeatMenuInstructionText = getHeatMenuInstructionText(oImgHeat, oLang, context)
    strInstruction1 = getMenuInstruction(oImgHeat, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    context.reporter.ReportEvent("OCR Debug Log", strInstruction1, "Done")
    if "FROM" in str(strScreen).upper():
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartMenuTitle), strHeatMenuTitle,
                                        "Holiday Start Menu Title")
        if "DATE" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartDateInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu Date Instruction Text")
        if "MONTH" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartMonthInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu Month Instruction Text")
        if "YEAR" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartYearInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu year Instruction Text")
        if "HOUR" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartHourInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu Hour Instruction Text")
        if "MINUTE" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartMinuteInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu Minute Instruction Text")
        if "CONFIRM" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayStartConfirmInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday Start Menu Confirm Instruction Text")
    if "TO" in str(strScreen).upper():
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendMenuTitle), strHeatMenuTitle,
                                        "Holiday End Menu Title")
        if "DATE" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendDateInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu Date Instruction Text")
        if "MONTH" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendMonthInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu Month Instruction Text")
        if "YEAR" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendYearInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu year Instruction Text")
        if "HOUR" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendHourInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu Hour Instruction Text")
        if "MINUTE" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendMinuteInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu Minute Instruction Text")
        if "CONFIRM" in strSubScreen:
            strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayendConfirmInstructionText),
                                            strHeatMenuInstructionText,
                                            "Holiday end Menu Confirm Instruction Text")
    if "TEMP" in str(strScreen).upper():
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayTempMenuTitle), strHeatMenuTitle,
                                        "Holiday Temperature Menu Title")
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayTempInstructionText2),
                                        strHeatMenuInstructionText,
                                        "Holiday Temperature Instruction Text")
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayTempInstructionText1),
                                        strInstruction1,
                                        "Holiday Temperature Instruction Text")
    if "CONFIRM" in str(strScreen).upper():
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayConfirmMenuTitle), strHeatMenuTitle,
                                        "Holiday Confirmation Menu Title")
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayConfirmInstructionText),
                                        strHeatMenuInstructionText,
                                        "Holiday Confirmation Instruction Text")

    if "CONFIRMINSTRUCTION" in str(strScreen).upper():
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayConfirmInstructionText1),
                                        strHeatMenuInstructionText,
                                        "Holiday Temperature Instruction Text")
        strLog = strLog + validationLog(context, str(oLang.HolidayScreen.HolidayConfirmInstructionText2),
                                        strInstruction1,
                                        "Holiday Temperature Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHeatName)


def validateHotMenu(oImgHot, imgHotName, oLang, context):
    strHotMenuTitle = getHeatMenuTitle(oImgHot, oLang, context)
    strHotMenuOptions = getHotMenuOptions(oImgHot, oLang, context)
    strHotMenuInstructionText = getHeatMenuInstructionText(oImgHot, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuTitle),
                                    strHotMenuTitle, "Hot Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuHotScheduleOptionText),
                                    strHotMenuOptions.split(" ")[0], "Hot Menu Schedule Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuHotManualOptionText),
                                    strHotMenuOptions.split(" ")[1],
                                    "Hot Menu Manual Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuHotOffOptionText),
                                    strHotMenuOptions.split(" ")[2],
                                    "Hot Menu Off Text")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotMenuInstructionText),
                                    strHotMenuInstructionText,
                                    "Hot Menu Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgHotName)


def validateHeatBoostScreen(oImgBoost, imgBoostName, oLang, context):
    strHeatBoostMenuTitle = getHeatMenuTitle(oImgBoost, oLang, context)
    strHeatBoostMenuOptions = getMenuInstruction(oImgBoost, oLang, context)
    strHeatBoostMenuInstructionText = getHeatMenuInstructionText(oImgBoost, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatBoostMenuTitle), strHeatBoostMenuTitle,
                                    "Heat Boost Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatBoostMenuInstruction1),
                                    strHeatBoostMenuOptions,
                                    "Heat Boost Menu Instruction 1")
    strLog = strLog + validationLog(context, str(oLang.HeatMenuScreen.HeatBoostMenuInstruction2),
                                    strHeatBoostMenuInstructionText,
                                    "Heat Boost Menu Instruction 2")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgBoostName)


def validateHotBoostScreen(oImgBoost, imgBoostName, oLang, context):
    strHotBoostMenuTitle = getHeatMenuTitle(oImgBoost, oLang, context)
    strHotBoostMenuOptions = getMenuInstruction(oImgBoost, oLang, context)
    strHotBoostMenuInstructionText = getHeatMenuInstructionText(oImgBoost, oLang, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotBoostMenuTitle), strHotBoostMenuTitle,
                                    "Hot Water Boost Menu Title")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotBoostMenuInstruction1),
                                    strHotBoostMenuOptions,
                                    "Hot Water Boost Menu Instruction 1")
    strLog = strLog + validationLog(context, str(oLang.HotMenuScreen.HotBoostMenuInstruction2),
                                    strHotBoostMenuInstructionText,
                                    "Hot Water Boost Menu Instruction 2")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgBoostName)


def validationLog(context, strExpected, strActual, strAttribute):
    log = ""
    if strExpected in strActual:
        log = "$~" + strAttribute + " $$ " + strExpected + " $$" + strActual
    else:
        log = "$~" + strAttribute + " $$ " + strExpected + " $$ ||" + strActual
    return log


def validationLogPattern(context, strLogPattern, strActual, strAttribute, strExpected):
    log = ""
    matchObjOFFOFF = re.match(strLogPattern, strActual,
                              re.M | re.I)
    if matchObjOFFOFF:
        log = "$~" + strAttribute + " $$ " + strExpected + " $$" + strActual
    else:
        log = "$~" + strAttribute + " $$ " + strExpected + " $$ ||" + strActual
    return log

def getLanguage(strLang):
    oLang = oENText
    if str(strLang).upper() == "ITALIAN":
        oLang = oITAText
    if str(strLang).upper() == 'ENGLISH':
        oLang = oENText
    if str(strLang).upper() == 'FRENCH':
        oLang = oFRText
    return oLang


def getModeText(strMode, strType, oLang):
    strText = ""
    if str(strType).upper() == "HEAT":
        if str(strMode).upper() == "OFF":
            strText = oLang.HomeScreen.Heat_Off_ModeText
        if str(strMode).upper() == "BOOST":
            strText = oLang.HomeScreen.Heat_Boost_ModeText
        if str(strMode).upper() == "MANUAL":
            strText = oLang.HomeScreen.Heat_Manual_ModeText
        if str(strMode).upper() == "SCHEDULE":
            strText = oLang.HomeScreen.Heat_Schedule_ModeText
        if str(strMode).upper() == "OVERRIDE":
            strText = oLang.HomeScreen.Heat_Schedule_ModeText + "-OVERRIDE"
        if str(strMode).upper() == "HOLIDAY":
            strText = oLang.HomeScreen.Heat_Holiday_Day_ModeText + "," + oLang.HomeScreen.Heat_Holiday_Hour_ModeText
    elif str(strType).upper() == "HOTWATER":
        if str(strMode).upper() == "OFF":
            strText = oLang.HomeScreen.Water_Off_ModeText
        if str(strMode).upper() == "BOOST":
            strText = oLang.HomeScreen.Water_Boost_ModeText
        if str(strMode).upper() == "ON":
            strText = oLang.HomeScreen.Water_On_ModeText
        if str(strMode).upper() == "SCHEDULE":
            strText = oLang.HomeScreen.Water_Schedule_ModeText
        if str(strMode).upper() == "HOLIDAY":
            strText = oLang.HomeScreen.Heat_Holiday_Day_ModeText + "," + oLang.HomeScreen.Heat_Holiday_Hour_ModeText
    elif str(strType).upper() == "HOLIDAY":
        strText = oLang.HomeScreen.Heat_Holiday_Day_ModeText + "," + oLang.HomeScreen.Heat_Holiday_Hour_ModeText
    return strText


def printHolidayDurationHome(Mode, context, oLang):
    Mode = str(Mode).strip()
    Mode = Mode.replace("0FF", "OFF").replace("0N", "ON")
    context.reporter.ReportEvent("OCR Log", "OCR text is " + Mode, "DONE")
    # context.reporter.ReportEvent("OCR Log", "OCR text is " +Mode.split(" ")[0] + " -- "+Mode.split(" ")[1] + " -- "+Mode.split(" ")[2] + " -- "+Mode.split(" ")[3] + " -- "+Mode.split(" ")[4] + " -- "+Mode.split(" ")[5] + " -- ", "DONE")

    if oLang.BootScreen.ReceivingText in Mode:
        context.reporter.ReportEvent("OCR Log", "The device is in Receiving state", "FAIL")
        exit()
    if oLang.HomeScreen.Target_Text in Mode.split(" ")[5] or oLang.HomeScreen.Target_Text in Mode.split(" ")[3]:
        context.reporter.ReportEvent("OCR Log", "first attempt = " + Mode.split(" ")[5] + " -- " + Mode.split(" ")[3],
                                     "Done")
        if (oLang.HomeScreen.Actual_Text not in Mode.split(" ")[7] or oLang.HomeScreen.Actual_Text not in
            Mode.split(" ")[6]):
            context.reporter.ReportEvent("Event Log",
                                         "Attributes $$ Value @@@ $~Current Heat Mode$$" + Mode.split(" ")[
                                             7] + " $~ Current Hot Water Mode$$" + Mode.split(" ")[6], "Done")
            return Mode.split(" ")[7], Mode.split(" ")[6]
        else:
            context.reporter.ReportEvent("OCR Log", "Unable to find the mode", "FAIL")
            exit()
    else:
        context.reporter.ReportEvent("OCR Log", "first attempt = " + Mode.split(" ")[3] + " -- " + Mode.split(" ")[5],
                                     "Done")
        context.reporter.ReportEvent("Event Log",
                                     "Attributes $$ Value @@@ $~Current Heat Mode$$" + Mode.split(" ")[
                                         5] + " $~ Current Hot Water Mode$$" + Mode.split(" ")[3], "Done")
        return Mode.split(" ")[5], Mode.split(" ")[3]


def printModesHome(Mode, context, oLang):
    Mode = str(Mode).strip()
    Mode = Mode.replace("0FF", "OFF").replace("0N", "ON").replace("oN", "ON").replace("oFF","OFF").replace("BO0ST","BOOST").replace("MANuAL","MANUAL").replace("BoosT","BOOST")
    context.reporter.ReportEvent("OCR Log", "OCR text is " + Mode, "DONE")
    if oLang.BootScreen.ReceivingText in Mode:
        context.reporter.ReportEvent("OCR Log", "The device is in Receiving state", "FAIL")
        exit()
    try:
        matchObjOFFOFF = re.match(
            r'.*' + oLang.HomeScreen.Water_Off_ModeText + '.*' + oLang.HomeScreen.Heat_Off_ModeText + '.*', Mode,
            re.M | re.I)
        strTextFirst = ""
        strTextSecond = ""
        if matchObjOFFOFF:
            strTextFirst,strTextSecond = oLang.HomeScreen.Heat_Off_ModeText, oLang.HomeScreen.Water_Off_ModeText
        matchObjOFFSCH = re.match(
            r'.*' + oLang.HomeScreen.Water_Off_ModeText + '.*' + oLang.HomeScreen.Heat_Schedule_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjOFFSCH:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Schedule_ModeText, oLang.HomeScreen.Water_Off_ModeText
        matchObjOFFON = re.match(
            r'.*' + oLang.HomeScreen.Water_Off_ModeText + '.*' + oLang.HomeScreen.Heat_Manual_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjOFFON:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Manual_ModeText, oLang.HomeScreen.Water_Off_ModeText
        matchObjOFFBOOST = re.match(
            r'.*' + oLang.HomeScreen.Water_Off_ModeText + '.*' + oLang.HomeScreen.Heat_Boost_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjOFFBOOST:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Boost_ModeText, oLang.HomeScreen.Water_Off_ModeText
        matchObjONOFF = re.match(
            r'.*' + oLang.HomeScreen.Water_On_ModeText + '.*' + oLang.HomeScreen.Heat_Off_ModeText + '.*', Mode,
            re.M | re.I)
        if matchObjONOFF:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Off_ModeText, oLang.HomeScreen.Water_On_ModeText
        matchObjONSCH = re.match(
            r'.*' + oLang.HomeScreen.Water_On_ModeText + '.*' + oLang.HomeScreen.Heat_Schedule_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjONSCH:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Schedule_ModeText, oLang.HomeScreen.Water_On_ModeText
        matchObjONMANUAL = re.match(
            r'.*' + oLang.HomeScreen.Water_On_ModeText + '.*' + oLang.HomeScreen.Heat_Manual_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjONMANUAL:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Manual_ModeText, oLang.HomeScreen.Water_On_ModeText
        matchObjONBOOST = re.match(
            r'.*' + oLang.HomeScreen.Water_On_ModeText + '.*' + oLang.HomeScreen.Heat_Boost_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjONBOOST:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Boost_ModeText, oLang.HomeScreen.Water_On_ModeText
        matchObjSCHOFF = re.match(
            r'.*' + oLang.HomeScreen.Water_Schedule_ModeText + '.*' + oLang.HomeScreen.Heat_Off_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjSCHOFF:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Off_ModeText, oLang.HomeScreen.Water_Schedule_ModeText
        matchObjSCHSCH = re.match(
            r'.*' + oLang.HomeScreen.Water_Schedule_ModeText + '.*' + oLang.HomeScreen.Heat_Schedule_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjSCHSCH:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Schedule_ModeText, oLang.HomeScreen.Water_Schedule_ModeText
        matchObjSCHMANUAL = re.match(
            r'.*' + oLang.HomeScreen.Water_Schedule_ModeText + '.*' + oLang.HomeScreen.Heat_Manual_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjSCHMANUAL:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Manual_ModeText, oLang.HomeScreen.Water_Schedule_ModeText
        matchObjSCHBOOST = re.match(
            r'.*' + oLang.HomeScreen.Water_Schedule_ModeText + '.*' + oLang.HomeScreen.Heat_Boost_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjSCHBOOST:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Boost_ModeText, oLang.HomeScreen.Water_Schedule_ModeText
        matchObjBOOSTOFF = re.match(
            r'.*' + oLang.HomeScreen.Water_Boost_ModeText + '.*' + oLang.HomeScreen.Heat_Off_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjBOOSTOFF:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Off_ModeText, oLang.HomeScreen.Water_Boost_ModeText
        matchObjBOOSTSCH = re.match(
            r'.*' + oLang.HomeScreen.Water_Boost_ModeText + '.*' + oLang.HomeScreen.Heat_Schedule_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjBOOSTSCH:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Schedule_ModeText, oLang.HomeScreen.Water_Boost_ModeText
        matchObjBOOSTMANUAL = re.match(
            r'.*' + oLang.HomeScreen.Water_Boost_ModeText + '.*' + oLang.HomeScreen.Heat_Manual_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjBOOSTMANUAL:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Manual_ModeText, oLang.HomeScreen.Water_Boost_ModeText
        matchObjBOOSTBOOST = re.match(
            r'.*' + oLang.HomeScreen.Water_Boost_ModeText + '.*' + oLang.HomeScreen.Heat_Boost_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjBOOSTBOOST:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Boost_ModeText, oLang.HomeScreen.Water_Boost_ModeText
        matchObjBOOSTBOOST = re.match(
            r'.*' + oLang.HomeScreen.Heat_Holiday_Day_ModeText + '.*' + oLang.HomeScreen.Heat_Holiday_Hour_ModeText + '.*',
            Mode,
            re.M | re.I)
        if matchObjBOOSTBOOST:
            strTextFirst, strTextSecond = oLang.HomeScreen.Heat_Holiday_Hour_ModeText, oLang.HomeScreen.Heat_Holiday_Day_ModeText
        matchObjLocked = re.match(
            r'.*' + oLang.HomeScreen.Child_Lock_Text + '.*',
            Mode,
            re.M | re.I)
        if matchObjLocked:
            strTextFirst, strTextSecond = oLang.Child_Lock_Text, ""
        context.reporter.ReportEvent("Event Log",
                                     "Attributes $$ Value @@@ $~Current Heat Mode$$" + strTextFirst
                                     + " $~ Current Hot Water Mode$$" + strTextSecond, "Done")
        return strTextFirst, strTextSecond
    except:
        print("Error - Exception")
        exit()


def validateHolidayCancelOptions(oImgMenu, imgMenuName, oLang, context):
    if oLang.HomeScreen.Target_Text in getText(oImgMenu, context):
        context.reporter.ReportEvent("Event Log", "Main menu not found", "Fail")
        exit()
    strHolidayMenuTitle = getMainMenuTitle(oImgMenu, oLang, context)
    strHolidayMenuOptions = getHolidayMenuOptions(oImgMenu, oLang, context)
    strHolidayMenuInstructionText = getMainMenuInstructionText(oImgMenu, oLang, context)
    print(strHolidayMenuOptions)
    strText = getText(oImgMenu, context)
    strLog = "Attribute $$ Expected $$ Actual @@@"
    strLog = strLog + validationLog(context, str(oLang.HolidayCancelScreenOptions.HolidayCancelScreenTitle),
                                    strHolidayMenuTitle, "Holiday Menu Title")
    if True:
        strLog = strLog + validationLog(context, str(oLang.HolidayCancelScreenOptions.HolidayMenuCancelOptionText),
                                        strHolidayMenuOptions.split(" ")[1], "Holiday Menu Cancel Text")
        print(strLog + "\n")
        strLog = strLog + validationLog(context, str(oLang.HolidayCancelScreenOptions.HolidayMenuEditOptionText),
                                        strHolidayMenuOptions.split(" ")[0], "Holiday Menu Edit Text")
        print(strLog + "\n")
        strLog = strLog + validationLog(context, str(oLang.HolidayCancelScreenOptions.HolidayCancelScreenConfirmInstructionText),
                                        strHolidayMenuInstructionText,
                                        "Holiday Instruction Text")

    context.reporter.ReportEvent("Event Log", strLog, "Done", ocrImagePath=imgMenuName)

def getHolidayMenuOptions(img, oLang, context):

    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/Holidaytest.jpg')
    img = Image.open(path + '/Holidaytest.jpg')
    width, height = img.size
    left = width / 4.2
    right = width / 1.5
    bottom = height / 3.5
    top = height / 2
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/testHolidayEditMode.jpg')
    img = Image.open(path + '/testHolidayEditMode.jpg')
    word = pytesseract.image_to_string(img)

    img = Image.open(path + '/Holidaytest.jpg')
    width, height = img.size
    left = width / 4.2  # top
    right = width / 1.8
    bottom = height / 3.5
    top = height / 3  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/testHolidayCancelMode.jpg')
    img = Image.open(path + '/testHolidayCancelMode.jpg')
    word = word + " " +pytesseract.image_to_string(img)
    word = word.encode('ascii', 'ignore').decode('ascii')

    return word

def navigateToHeatScreen(context, myNodeId, ep):
    _, imgMenuName = pressAndCature(context, myNodeId, ep, "Menu", "Press", 1, "Event Log",
                                    "Menu is Pressed from Home", "Done")
    _, imgHeatName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                    "Dial is Pressed for Heat Mode", "Done")
    return imgMenuName, imgHeatName

def navigateToHeadScheduleScreen(context, myNodeId, ep):
    imgMenuName, imgHeatName = navigateToHeatScreen(context, myNodeId, ep)
    _, imgSchModeName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                    "Dial is Pressed for Schedule Mode", "Done")
    return imgMenuName, imgHeatName, imgSchModeName

def navigateToHotWaterScheduleStartOverEE(context, myNodeId, ep):
    imgMenuName, imgHeatName, imgSchModeName = navigateToHeadScheduleScreen(context, myNodeId, ep)
    _, imgSOModeName = rotateAndCature(context, myNodeId, ep, "CLOCKWISE", 2, 1, "Event Log",
                                        "Dial is rotated clockwise to Heat Schedule startover mode", "Done")
    _, imgSOModeConfirmName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                            "Dial is Pressed for Heat Schedule StartOver", "Done")

    _, imgTypeConfirmName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                            "Dial is Pressed for Heat Schedule StartOver Confirm", "Done")

    _, imgSOModeEEName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                            "Dial is Pressed for Heat Schedule StartOver Efficient", "Done")

    _, imgSOModeEEEdit = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                            "Dial is Pressed for Heat Schedule StartOver Energy Efficient", "Done")
    return imgMenuName, imgHeatName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName, imgSOModeEEName, imgSOModeEEEdit

def naviagateToScheduleScreen(context, myNodeId, ep):
    _, imgMenuName = pressAndCature(context, myNodeId, ep, "Menu", "Press", 1, "Event Log",
                                    "Menu is Pressed from Home", "Done")
    _, imgHotMenuName = rotateAndCature(context, myNodeId, ep, "CLOCKWISE", 1, 1, "Event Log",
                                        "Dial is rotated clockwise to Water mode", "Done")
    _, imgHotWaterMenuName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                                            "Dial is Pressed for Hot Water Mode", "Done")
    _, imgSchModeName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 2, "Event Log",
                                       "Dial is Pressed on Schedule mode", "Done")
    return imgMenuName,imgHotMenuName, imgHotWaterMenuName, imgSchModeName


def navigateToHotWaterStartover(context, myNodeId, ep):
    imgMenuName, imgHotMenuName, imgHotWaterMenuName, imgSchModeName = naviagateToScheduleScreen(context, myNodeId, ep)
    _, imgSOModeName = rotateAndCature(context, myNodeId, ep, "CLOCKWISE", 1, 1, "Event Log",
                           "Dial is rotated clockwise to Water Schedule Resume mode", "Done")
    _, imgSOModeConfirmName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 2, "Event Log",
                          "Dial is Pressed for Water Schedule StartOver", "Done")
    _, imgTypeConfirmName = pressAndCature(context, myNodeId, ep, "Dial", "Press", 2, "Event Log",
                          "Dial is Pressed for Water Schedule StartOver Confirm", "Done")
    return imgMenuName,imgHotMenuName, imgHotWaterMenuName, imgSchModeName, imgSOModeName, imgSOModeConfirmName, imgTypeConfirmName

def getButtonType(img,context):

    path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
    img = ImageOps.autocontrast(img)
    width, height = img.size
    left = width / 5  # top
    right = width / 1.5
    bottom = height / 1.4
    top = height / 2  # left
    frame = img.crop((int(top), int(left), int(right), int(bottom)))
    frame.save(path + '/Button.jpg')
    img = Image.open(path + '/Button.jpg')

    #Crop for Back Button
    width, height = img.size
    left = width / 1.2  # top
    right = width / 3.6
    bottom = height / 1.1
    top = height / 9  # left
    frameDate = img.crop((int(top), int(left), int(right), int(bottom)))
    frameDate.save(path + '/BackButton.jpg')

    # Crop for Tick Button
    img = Image.open(path + '/Button.jpg')
    width, height = img.size
    left = width / 1.2  # top
    right = width / 1
    bottom = height / 1.1
    top = height / 1.5  # left
    frameTest = img.crop((int(top), int(left), int(right), int(bottom)))
    frameTest.save(path + '/TickButton.jpg')

    # Crop for Menu Button
    img = Image.open(path + '/Button.jpg')
    width, height = img.size
    left = width / 1.2  # top
    right = width / 1.4
    bottom = height / 1.1
    top = height / 2.69  # left
    frameMenu = img.crop((int(top), int(left), int(right), int(bottom)))
    frameMenu.save(path + '/MenuButton.jpg')

    return frameDate, frameTest, frameMenu

def navigateAndSetHWScheduleEvents(context, myNodeId, ep, oRows, lstReport, edit=False, startover=False):
    timeValue = {"00": 0, "15": 1, "30": 2, "45": 3}
    continueFlag = True
    if not startover:
        pressAndAppendList(context,myNodeId, ep, "Dial", "Press",3 ,"Event Log", "Dial is Pressed to Select " + oRows['Day'], "Done", lstReport)
        pressAndAppendList(context,myNodeId, ep, "Dial", "Press",3 ,"Event Log", "Dial is Pressed to Select " + oRows['Day'], "Done", lstReport)
    else:
        dutils.pressDeviceButton(myNodeId, ep, "Tick", "Press")
        time.sleep(5)
        _, imgSOModeEEM = captureOriginal(context)
        lstReport.append([imgSOModeEEM, "Event Log",
                          "Tick is Pressed to Select " + oRows['Day'],
                          "Done"])
    intDecRot = 0
    if(edit or startover):
        time.sleep(1)
        dutils.rotateDial(myNodeId, ep, "AntiClockwise", 30)
        time.sleep(1)
        oImg, imgSOModeEEM = captureOriginal(context)
        if oRows['Event1'] is not None:
            if str(oRows['Event1']) is "":
                context.reporter.ReportEvent("Event Log", "Please enter the event1", "FAIL")
                exit()
        intRot = (int(str(oRows['Event1']).split(":")[0]) * 4) + timeValue[
            str(oRows['Event1']).split(":")[1].split(",")[0]]
        if intRot > 0:
            time.sleep(3)
            dutils.rotateDial(myNodeId, ep, "clockwise", intRot)
        time.sleep(4)
        _, imgSOModeEEM = captureOriginal(context)
        lstReport.append([imgSOModeEEM, "Event Log",
                          "Dial is Rotatate to start time " + str(oRows['Event1']).split(",")[0],
                          "Done"])
        if int(str(oRows['Event1']).split(",")[1].split(".")[1]) > 0:
            intDecRot = 1
    pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 3, "Event Log","Dial is Pressed to Select " + oRows['Day'], "Done", lstReport)
    if not startover:
        if "OFF" in (str(oRows['Event1']).split(",")[1].split(".")[0]):
            dutils.rotateDial(myNodeId, ep, "clockwise", 1)
        time.sleep(2)
        _, imgSOModeEEM = captureOriginal(context)
        lstReport.append([imgSOModeEEM, "Event Log",
                          "Dial is rotated for the temperature " + str(oRows['Event1']).split(",")[1],
                          "Done"])
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 2, "Event Log","Dial is Pressed at start time " + str(oRows['Event1']).split(",")[1], "Done", lstReport)
    if(edit or startover):
        intValue = (int(str(oRows['Event2']).split(":")[0]) * 4) + timeValue[
            str(oRows['Event2']).split(":")[1].split(",")[0]] - (intRot + 8)
        if intValue > 0:
            dutils.rotateDial(myNodeId, ep, "clockwise", intValue)

        if intValue < 0:
            dutils.rotateDial(myNodeId, ep, "anticlockwise", intValue)
        time.sleep(2)
        intRot = intRot + 8 + intValue
        _, imgSOModeEEM = captureOriginal(context)
        lstReport.append([imgSOModeEEM, "Event Log",
                          "Dial is rotated to time " + str(oRows['Event2']).split(",")[0],
                          "Done"])
    pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)
    if not startover:
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)
        if "ON" in (str(oRows['Event2']).split(",")[1].split(".")[0]):
            dutils.rotateDial(myNodeId, ep, "clockwise", 1)
        time.sleep(2)
        _, imgSOModeEEM = captureOriginal(context)
        lstReport.append([imgSOModeEEM, "Event Log",
                          "Dial is rotated for the temperature " + str(oRows['Event2']).split(",")[
                              1],
                          "Done"])
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 2, "Event Log","Dial is Pressed at start time " + str(oRows['Event2']).split(",")[1], "Done", lstReport)
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at start time " + str(oRows['Event3']).split(",")[1], "Done", lstReport)
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 3, "Event Log","Dial is Pressed at event", "Done", lstReport)
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0], "Done", lstReport)
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed for Event 3 confirmation", "Done", lstReport)

        lstReport.append([imgSOModeEEM, "Event Log",
                          "Dial is Pressed at start time " + str(oRows['Event3']).split(",")[0],
                          "Done"])
    else:
        if str(oRows['Event3']) is not "":
            dutils.rotateDial(myNodeId, ep, "clockwise", 1)
            time.sleep(3)
            _, imgSOModeEEM = captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is rotated to No",
                              "Done"])
            dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
            time.sleep(3)
            _, imgSOModeEEM = captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is Pressed at No",
                              "Done"])
        else:
            continueFlag = False
    if continueFlag:
        if "ON" in (str(oRows['Event3']).split(",")[1].split(".")[0]):
            dutils.rotateDial(myNodeId, ep, "clockwise", 1)

            time.sleep(1)
            _, imgSOModeEEM = captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is rotated for the temperature " +
                              str(oRows['Event3']).split(",")[1],
                              "Done"])

        if(edit or startover):
            intValue = (int(str(oRows['Event4']).split(":")[0]) * 4) + timeValue[
                str(oRows['Event4']).split(":")[1].split(",")[0]] - (intRot + 14)
            if intValue > 0:
                dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
            if intValue < 0:
                dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                time.sleep(1)
            intRot = intRot + 14 + intValue
            _, imgSOModeEEM = captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is rotated to time " + str(oRows['Event4']).split(",")[0],
                              "Done"])
        pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed for Event 3 confirmation", "Done", lstReport)
        if not startover:
            pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End time", "Done", lstReport)
            pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End time", "Done", lstReport)
            pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End time", "Done", lstReport)

            if "ON" in (str(oRows['Event4']).split(",")[1].split(".")[0]):
                dutils.rotateDial(myNodeId, ep, "clockwise", 1)
            time.sleep(2)
            _, imgSOModeEEM = captureOriginal(context)
            lstReport.append([imgSOModeEEM, "Event Log",
                              "Dial is rotated for the temperature " + str(oRows['Event4']).split(",")[
                                  1],
                              "Done"])

            pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at start time " + str(oRows['Event4']).split(",")[1], "Done", lstReport)
        else:
            if str(oRows['Event5']) is not "":
                dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                time.sleep(3)
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is rotated to No",
                                  "Done"])
                dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
                time.sleep(3)
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is Pressed at No",
                                  "Done"])
            else:
                continueFlag = False
        if continueFlag:
            if(edit or startover):
                intValue = (int(str(oRows['Event5']).split(":")[0]) * 4) + timeValue[
                    str(oRows['Event5']).split(":")[1].split(",")[0]] - (intRot + 14)
                if intValue > 0:
                    dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                if intValue < 0:
                    dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                time.sleep(1)
                intRot = intRot + 14 + intValue
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is rotated to time " + str(oRows['Event5']).split(",")[
                                      0],
                                  "Done"])
            pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at start time " + str(oRows['Event5']).split(",")[0], "Done", lstReport)
            if not startover:
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at No", "Done", lstReport)
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 3, "Event Log","Dial is Pressed at No", "Done", lstReport)
                if "OFF" in (str(oRows['Event5']).split(",")[1].split(".")[0]):
                    dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                time.sleep(1)
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is rotated for the temperature " +
                                  str(oRows['Event5']).split(",")[1],
                                  "Done"])
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 3, "Event Log","Dial is Pressed for Event 3 confirmation", "Done", lstReport)
            if(edit or startover):
                intValue = (int(str(oRows['Event6']).split(":")[0]) * 4) + timeValue[
                    str(oRows['Event6']).split(":")[1].split(",")[0]] - (intRot + 26)
                if intValue > 0:
                    dutils.rotateDial(myNodeId, ep, "clockwise", intValue)
                if intValue < 0:
                    dutils.rotateDial(myNodeId, ep, "anticlockwise", (intValue * -1))
                time.sleep(1)
                intRot = intRot + 26 + intValue
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is rotated to time " + str(oRows['Event6']).split(",")[
                                      0],
                                  "Done"])
            if not startover:
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)
                pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log","Dial is Pressed at End Time", "Done", lstReport)

                if "ON" in (str(oRows['Event6']).split(",")[1].split(".")[0]):
                    dutils.rotateDial(myNodeId, ep, "clockwise", 1)
                time.sleep(2)
                _, imgSOModeEEM = captureOriginal(context)
                lstReport.append([imgSOModeEEM, "Event Log",
                                  "Dial is rotated for the temperature " + str(oRows['Event6']).split(",")[
                                      1],
                                  "Done"])

    pressAndAppendList(context, myNodeId, ep, "Dial", "Press", 1, "Event Log",
                       "Dial is Pressed at start time " + str(oRows['Event6']).split(",")[1], "Done", lstReport)
    pressAndAppendList(context, myNodeId, ep, "Tick", "Press", 5, "Event Log", "Tick is Pressed to confirm", "Done",
                       lstReport)
    time.sleep(2)
    dutils.rotateDial(myNodeId, ep, "clockwise", 1)
    time.sleep(3)
    _, imgSOModeEEM = captureOriginal(context)
    lstReport.append([imgSOModeEEM, "Event Log",
                      "Dial is rotated to No",
                      "Done"])
    dutils.pressDeviceButton(myNodeId, ep, "Dial", "Press")
    time.sleep(3)
    _, imgSOModeEEM = captureOriginal(context)
    lstReport.append([imgSOModeEEM, "Event Log",
                      "Dial is Pressed at No",
                      "Done"])

def navigateAndSetHeatScheduleEvents():
    print('hi')

def validateButton(context, oImgWake, BackButton, MenuButton, TickButton):

    imgBackButton, imgMenuButton, imgTickButton = getButtonType(oImgWake, context)

    #Validation for Tick Button enabled
    if TickButton is True:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgTickButton)
        if int(_g) > int(_r) and int(_g) > int(_b):
            context.reporter.ReportEvent("Button Validation",
                                         "Tick Button is displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                         "Tick Button is not displayed ",
                                         "FAIL")
    # Validation for Tick Button disabled
    if TickButton is False:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgTickButton)
        if float(_g) == float(_r) and float(_g) == float(_b) :
            context.reporter.ReportEvent("Button Validation",
                                         "Tick Button is not displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                         "Tick Button is displayed ",
                                         "FAIL")
    #Validation for Back Button is enabled
    if BackButton is True:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgBackButton)
        if int(_r) > int(_g) and int(_r) > int(_b):
            context.reporter.ReportEvent("Button Validation",
                                         "Back Button is displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                         "Back Button is not displayed ",
                                         "FAIL")
    # Validation for Back Button disabled
    if BackButton is False:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgBackButton)
        if float(_g) == float(_r) and float(_g) == float(_b):
            context.reporter.ReportEvent("Button Validation",
                                          " Back Button is not displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                          "Back Button is displayed ",
                                         "FAIL")

    # Validation for Menu Button is enabled
    if MenuButton is True:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgMenuButton)
        if int(_g) == int(_r) and int(_g) == int(_b):
            context.reporter.ReportEvent("Button Validation",
                                         "Menu Button is displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                         "Menu Button is not displayed ",
                                         "FAIL")

    # Validation for Menu Button is disabled
    if MenuButton is False:
        _r, _g, _b = outils.SLT4OCRUtil.get_weighted_color_average(context, imgMenuButton)
        if float(_g) == float(_r) and float(_g) == float(_b):
            context.reporter.ReportEvent("Button Validation",
                                          " Menu Button is not displayed ",
                                         "PASS")
        else:
            context.reporter.ReportEvent("Button Validation",
                                          "Menu Button is displayed ",
                                         "FAIL")