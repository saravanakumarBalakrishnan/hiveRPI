class HomeScreen(object):
    Heat_Boost_ModeText = "BOOST"
    Heat_Off_ModeText = "ACCESA"
    Heat_Schedule_ModeText = "PROG"
    Heat_Manual_ModeText = "MANUALE"

    Water_Boost_ModeText = "BOOST"
    Water_Off_ModeText = "SPENTO"
    Water_Schedule_ModeText = "PROG"
    Water_On_ModeText = "ACCESA"

    Target_Text = "OBIETTIVO"
    Actual_Text = "ATTUALE"

    Day_Mon = "LUN"
    Day_Tue = "MAR"
    Day_Wed = "MER"
    Day_Thu = "GIO"
    Day_Fri = "VEN"
    Day_Sat = "SAB"
    Day_Sun = "DOM"

    Boost_Screen_Title = "Which boost would you like to cancel?"
    Boost_Screen_HW = "Hot Water"
    Boost_Screen_Heat = "Heat"
    Boost_Screen_InstructionText = "Turn dial to select, press to confirm."

    Child_Lock_Text = "Locked"

class MainMenuScreen(object):
    MainMenuTitle = "MENU"
    MainMenuHeatOptionText = "RISCALDAMENTO"
    MainMenuHotWaterOptionText = "ACQUA CALDA"
    MainMenuHolidayOptionText = "Vacanze"
    MainMenuSettingsOptionText = "Altro"
    MainMenuInstructionText = "Ruota per selezionare, premi per modificare."


class HeatMenuScreen(object):
    HeatMenuTitle = "RISCALDAMENTO MENU"
    HeatMenuHeatOffOptionText = "spenta"
    HeatMenuHeatScheduleOptionText = "Programmazione"
    HeatMenuHeatManualOptionText = "Manuale"
    HeatMenuInstructionText = "Ruota per selezionare, premi per modificare"

    HeatOffMenuInstructionText = "Riscaldamento spento, premi tasto Conferma"

    HeatBoostMenuTitle = "RISCALDAMENTO BOOST"
    HeatBoostMenuInstruction1 = "Premi Boost per impostare la durata, ruota"
    HeatBoostMenuInstruction2 = "per regolare la temp e premi Conferma"

    HeatScheduleMenuTitle = "HEAT SCHEDULE MENU"
    HeatScheduleResumeOptionText = "Resume"
    HeatScheduleEditOptionText = "View/Edit Current"
    HeatScheduleStartOptionText = "Start Over"

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
    HolidayStartDateInstructionText = "Turn dial to select start day, please press to confirm."
    HolidayStartMonthInstructionText = "Turn dial to select month, please press to confirm."
    HolidayStartYearInstructionText = "Turn dial to select year, please press to confirm."
    HolidayStartHourInstructionText = "Turn dial to select start hour, please press to confirm."
    HolidayStartMinuteInstructionText = "Turn dial to select minutes, please press to confirm."

    HolidayStartConfirmInstructionText = "Press dial to confirm holiday start and set end."

    HolidayendMenuTitle = "HOLIDAY END"
    HolidayendDateInstructionText = "Turn dial to select end day, please press to confirm."
    HolidayendMonthInstructionText = "Turn dial to select month, please press to confirm."
    HolidayendYearInstructionText = "Turn dial to select year, please press to confirm."
    HolidayendHourInstructionText = "Turn dial to select end hour, please press to confirm."
    HolidayendMinuteInstructionText = "Turn dial to select minutes, please press to confirm."

    HolidayendConfirmInstructionText = "Press dial to confirm holiday end and set temp."

    HolidayTempMenuTitle = "HOLIDAY TEMPERATURE"

    HolidayTempInstructionText1 = "Turn dial to set holiday temperature"
    HolidayTempInstructionText2 = "please press to confirm."

    HolidayConfirmMenuTitle = "HOLIDAY SUMMARY"
    HolidayConfirmInstructionText = "please tick to confirm."

class HolidayCancelScreenOptions(object):
    HolidayCancelScreenTitle = "MENU VACANZA"
    HolidayMenuCancelOptionText = "Annulla"
    HolidayMenuEditOptionText = "Modifica"
    HolidayCancelScreenConfirmInstructionText = "Ruota per selezionare, premi per confermare"