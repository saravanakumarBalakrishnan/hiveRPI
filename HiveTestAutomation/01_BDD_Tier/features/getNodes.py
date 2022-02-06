from tkinter import *

sys.path.append("steps")
sys.path.append("steps/PageObjects")
sys.path.append("steps/Locators")
sys.path.append("steps/Function_Libraries")
import FF_device_utils as dUtils

oDict = dUtils.getNodes(False)
dUtils.putZigbeeDevicesJson(oDict)
