import sys
sys.path.append("01_BDD_Tier/features/steps")
sys.path.append("01_BDD_Tier/features/steps/PageObjects")
sys.path.append("01_BDD_Tier/features/steps/Locators")
sys.path.append("01_BDD_Tier/features/steps/Function_Libraries")

import FF_device_utils as dUtils

oDict = dUtils.getNodes(True)
dUtils.putZigbeeDevicesJson(oDict)
print("Done")