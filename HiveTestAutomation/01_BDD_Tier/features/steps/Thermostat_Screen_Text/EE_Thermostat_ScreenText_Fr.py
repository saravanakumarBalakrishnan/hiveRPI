class HomeScreen(object):
    Heat_Boost_ModeText = "BOOST"
    Heat_Off_ModeText = "OFF"
    Heat_Schedule_ModeText = "SCH"
    Heat_Manual_ModeText = "MANUAL"
    Heat_Holiday_Day_ModeText = "DAYS"
    Heat_Holiday_Hour_ModeText = "HOURS"

    Water_Boost_ModeText = "BOOST"
    Water_Off_ModeText = "OFF"
    Water_Schedule_ModeText = "SCH"
    Water_On_ModeText = "ON"

    Target_Text = "TARGET"
    Actual_Text = "ACTUAL"

    Day_Mon = "MON"
    Day_Tue = "TUE"
    Day_Wed = "WED"
    Day_Thu = "THU"
    Day_Fri = "FRI"
    Day_Sat = "SAT"
    Day_Sun = "SUN"

    Boost_Screen_Title = "Which boost would you like to cancel?"
    Boost_Screen_HW = "Hot Water"
    Boost_Screen_Heat = "Heat"
    Boost_Screen_InstructionText = "Turn dial to select, press to confirm."

    Child_Lock_Text = "Locked"


class MainMenuScreen(object):
    MainMenuTitle = "MENU"
    MainMenuHeatOptionText = "Heat"
    MainMenuHotWaterOptionText = "Hot Water"
    MainMenuHolidayOptionText = "Holiday"
    MainMenuSettingsOptionText = "Settings"
    MainMenuInstructionText = "Turn dial to select, press to confirm."


class HeatMenuScreen(object):
    HeatMenuTitle = "HEAT MENU"
    HeatMenuHeatOffOptionText = "Off"
    HeatMenuHeatScheduleOptionText = "Schedule"
    HeatMenuHeatManualOptionText = "Manual"
    HeatMenuInstructionText = "Turn dial to select, press to confirm."

    HeatOffMenuInstructionText = "Press tick to confirm Heat Off."

    HeatBoostMenuTitle = "HEAT BOOST"
    HeatBoostMenuInstruction1 = "Press heat boost button to set duration,"
    HeatBoostMenuInstruction2 = "turn dial to change temp, press tick to confirm."

    HeatScheduleMenuTitle = "HEAT SCHEDULE MENU"
    HeatScheduleResumeOptionText = "Resume"
    HeatScheduleEditOptionText = "View/Edit Current"
    HeatScheduleStartOptionText = "Start Over"
    HeatScheduleInstructionText = "Turn dial to select, press to confirm."

    HeatResumeMenuTitle = "HEAT SCH: MON-SUN"

    HeatStartOverInstruction = "Let's schedule your heat"
    HeatStartOverInstruction2 = "Press dial to continue"

    HeatStartOverSelectionTitle = "Which is more important for you?"
    HeatStartOverOptionsEE = "Energy Efficient"
    HeatStartOverOptionsC = "Comfort"
    HeatStartOverSelectionInstruction = "Turn dial to select, press to confirm."

    HeatStartOverEEMenuTitle = "RECOMMENDED DAILY SCHEDULE"
    HeatStartOverEEInstructionText = "Please tick to confirm. Or press"

    HeatStartOverConfirmTitle = "Continue on to hot water guided set up or exit?"
    HeatStartOverHotWaterOption = "Hot Water"
    HeatStartOverExitOption = "Exit"
    HeatStartOverConfirmInstructionText = "Turn dial to select, press to confirm."


class HotMenuScreen(object):
    HotMenuTitle = "HOT WATER MENU"
    HotMenuHotOffOptionText = "Always Off"
    HotMenuHotScheduleOptionText = "Schedule"
    HotMenuHotManualOptionText = "Always On"
    HotMenuInstructionText = "Turn dial to select, press to confirm."

    HotOffMenuInstructionText = "Press tick to confirm Hot Water Off."

    HotBoostMenuTitle = "HOT WATER BOOST"
    HotBoostMenuInstruction1 = "Press hot water boost button to set duration,"
    HotBoostMenuInstruction2 = "press tick to confirm."

    HotScheduleMenuTitle = "HOT WATER SCHEDULE MENU"
    HotScheduleResumeOptionText = "Resume"
    HotScheduleEditOptionText = "View/Edit Current"
    HotScheduleStartOptionText = "Start Over"
    HotScheduleInstructionText = "Turn dial to select, press to confirm."

    HotResumeMenuTitle = "HOT WATER SCH: MON-SUN"


class BootScreen(object):
    ReceivingText = "Receiving..."


class HolidayScreen(object):
    HolidayStartMenuTitle = "HOLIDAY START"
    HolidayStartDateInstructionText = "Turn dial to select start day, press to confirm."
    HolidayStartMonthInstructionText = "Turn dial to select month, press to confirm."
    HolidayStartYearInstructionText = "Turn dial to select year, press to confirm."
    HolidayStartHourInstructionText = "Turn dial to select start hour, press to confirm."
    HolidayStartMinuteInstructionText = "Turn dial to select minutes, press to confirm."

    HolidayStartConfirmInstructionText = "Press dial to confirm holiday start and set end."

    HolidayendMenuTitle = "HOLIDAY END"
    HolidayendDateInstructionText = "Turn dial to select end day, press to confirm."
    HolidayendMonthInstructionText = "Turn dial to select month, press to confirm."
    HolidayendYearInstructionText = "Turn dial to select year, press to confirm."
    HolidayendHourInstructionText = "Turn dial to select end hour, press to confirm."
    HolidayendMinuteInstructionText = "Turn dial to select minutes, press to confirm."

    HolidayendConfirmInstructionText = "Press dial to confirm holiday end and set temp."

    HolidayTempMenuTitle = "HOLIDAY TEMPERATURE"

    HolidayTempInstructionText1 = "Turn dial to set holiday temperature"
    HolidayTempInstructionText2 = "press to confirm."

    HolidayConfirmMenuTitle = "HOLIDAY SUMMARY"
    HolidayConfirmInstructionText = "please tick to confirm."

    HolidayConfirmInstructionText1 = "Hot water will be switched to"
    HolidayConfirmInstructionText2 = "off while in holiday mode"

class HolidayCancelScreenOptions(object):
    HolidayCancelScreenTitle = "HOLIDAY MENU"
    HolidayMenuCancelOptionText = "Cancel"
    HolidayMenuEditOptionText = "Edit"
    HolidayCancelScreenConfirmInstructionText = "Turn dial to select, press to confirm."

class SettingsMenuOptions(object):
    SettingsMenuTitle = "SETTINGS MENU"
    SettingsDateTimeOptionText = "Date & Time"
    SettingsFrostProtTempOptionText = "Frost Prot Temp"
    SettingsChildLockOptionText = "Child Lock"
    SettingsLanguageOptionText = "Language"