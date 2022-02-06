"""
Created on 16 Jun 2015

@author: ranganathan.veluswamy

@author: Hitesh Sharma - 15 July 2016
@note: class HeatingNotification - Identifier for Heating Notifications screen and updated LoginPageLocators to fix login issue
"""

from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//XCUIElementTypeOther[1]/XCUIElementTypeNavigationBar[1]/XCUIElementTypeOther[1]")
    USERNAME_EDTBOX = (By.XPATH, "//*[@label='Email']")
    PASSWORD_EDTBOX = (By.XPATH, "//*[@label='Password']")
    LOGIN_BUTTON = (By.XPATH,
                    "//XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeOther[6]/XCUIElementTypeButton[2]")
    LOG_OUT_BUTTON = (By.XPATH, "//*[@label='Log out']")
    HIVE_LOGO = (By.NAME, 'Hive_Logo_Loop_Orange_0')
    LOGIN_OPTIONS = (By.NAME, 'Login options')
    LOGIN_OPTIONS_DONE = (By.NAME, 'Done')
    INT_PROD = (By.NAME, 'Internal Prod')
    BETA = (By.NAME, 'Beta')
    LIVE = (By.NAME, 'Live')
    STAGING = (By.NAME, 'Staging')
    NA_BETA = (By.NAME, 'North America Beta')
    DONT_LOGIN = (By.NAME, "Don't autologin")


class HomePageLocators(object):
    SKIP_BUTTON = (By.NAME, 'Skip')
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'Last updated')]")
    MENU_BUTTON = (By.NAME, 'Menu')
    ALL_RECIPES = (By.NAME, 'All Recipes')
    MENU_TITLE = (By.NAME, 'Menu, screen')
    GOT_IT_BUTTON = (By.XPATH, "//*[@label='Got it!']")
    HEAT_CONTROL_MENU_LINK = (By.NAME, 'Heating control')
    HEAT_SCHEDULE_MENU_LINK = (By.NAME, 'Heating schedule')
    SETTINGS_MENU_LINK = (By.NAME, 'Settings')
    HOLIDAY_MODE_MENU_LINK = (By.NAME, 'Holiday mode')
    GEOLOCATION_LINK = (By.NAME, 'Geolocation')
    NOTIFICATIONS_MENU_LINK = (By.NAME, 'Notifications')
    ACCOUNT_DETAILS_MENU_LINK = (By.NAME, 'Account details')
    HOT_WATER_CONTROL_MENU_LINK = (By.NAME, 'Hot water control')
    HOT_WATER_SCHEDULE_MENU_LINK = (By.NAME, 'Hot water schedule')
    LINK_COLAPSE_BUTTON = (By.NAME, 'c')
    SETTINGS_MAIN_MENU = (By.NAME, 'Settings')
    CHANGE_PASSWORD_SUB_MENU = (By.NAME, 'Change password')
    PINLOCK_SUB_MENU = (By.NAME, 'PIN lock')
    HELP_SUPPORT_LINK = (By.XPATH, "//*[@value='Help & Support']")
    TEXT_CONTROL_LINK = (By.XPATH, "//*[@value='Text control']")
    PLUG_CONTROL_LINK = (By.NAME, 'Plug control')
    PLUG_SCHEDULE_LINK = (By.NAME, 'Plug schedule')
    MOTIONSENSOR_ON_LOCATOR = (By.XPATH, "//*[@label='Hall, on']")
    MOTIONSENSOR_OFF_LOCATOR = (By.XPATH, "//*[@label='Hall, off']")
    strLOCAL_ON = "//*[contains(@label,'name, on')]"
    strLOCAL_OFF = "//*[contains(@label,'name, off')]"
    strLOCAL_OFFLINE = "//*[contains(@label,'name, offline')]"
    NOTIFICATION_RECIPE_DEFAULT = "//*[contains(@label,'Notify me when 'name' detects motion')]"
    DEVICE_OFFLINE_LABEL = (By.XPATH, "//*[contains(@label,'Device offline')]")
    FLIP_TO_HONEYCOMB = (By.XPATH, "//*[@label='Flip to honeycomb dashboard']")
    PAGE_NAVIGATOR = (By.XPATH, "//*[contains(@value, 'page 1 of 2')]")
    FLIP_TO_DEVICE_LIST = (By.XPATH, "//*[@label='Flip to list']")
    Plug_runtime_Dashboard_on = "//*[contains(@label, 'devicename, on')]"
    Plug_runtime_Dashboard_off = "//*[contains(@label, 'devicename, off')]"
    DASHBOARD_TITLE = (By.XPATH, "//*[contains(@label, 'My Hive Home')]")
    MENU_BUTTON_SHOW = (By.NAME, 'Menu')
    PAGE_INDICATOR = (By.XPATH, "//*[contains(@type, 'XCUIElementTypePageIndicator')]")
    HEATING_LOC = (By.XPATH, "//*[contains(@label, 'Heating')]")
    DEVICE_STATE_LOC = "//*[contains(@label, 'deviceString')]"
    DEVICELIST = "//*[contains(@label, 'devicename')]/following-sibling::XCUIElementTypeStaticText"
    DEVICELIST_HIERARCHY = "//XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[DeviceCounter]/XCUIElementTypeStaticText[1]"
    DEVICE_NAME = "//*[contains(@value,'name')]"


class HeatingControlPageLocators(object):
    # TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[contains(@label, 'Heating target temperature')]")
    TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[contains(@label, 'Temperature control')]")
    PRESET_TEMP_BUTTON = (By.NAME, 'Switch between the temperature control and temperature presets')
    SCHEDULE_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Heating mode Schedule')]")
    MANUAL_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Heating mode Manual')]")
    OFF_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Heating mode Off')]")
    BOOST_MODE_LINK = (By.NAME, 'Boost')
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@label, 'selected')]")
    FLAME_ICON = (By.XPATH, "//*[contains(@label, 'Your heating is o')]")
    BOOST_TIME_SCROLL = (By.XPATH, "//XCUIElementTypePickerWheel")
    BOOST_CURRENT_TIME_BUTTON = (
        By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeButton[2]")
    BOOST_STOP = (By.NAME, 'Stop Boost')
    BOOST_SAVE = (By.NAME, 'Save')
    SLIDER_DOTS = (By.XPATH,
                   "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]")


class HotWaterControlPageLocators(object):
    RUNNING_STATE_CIRCLE = (By.ID, 'hotWaterCircleView')
    BOOST_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Boost')]")
    SCHEDULE_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water schedule')]")
    MANUAL_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water mode On')]")
    OFF_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water mode Off')]")
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@label, 'selected')]")
    HOT_WATER_CURRENT_STATE = (By.XPATH, "//*[contains(@label, 'Hot Water, currently')]")
    RUNNING_STATE_ON = (By.NAME, 'On')
    RUNNING_STATE_OFF = (By.NAME, 'Off')
    BOOST_TIME_SCROLL = (By.XPATH, "//UIAScrollView[1]/UIATableView[1]/UIAPickerWheel[1]")
    BOOST_CURRENT_TIME_BUTTON = (By.XPATH, "//*[contains(@name,'0')][1]")
    BOOST_STOP = (By.NAME, 'Stop boost')
    BOOST_SAVE = (By.NAME, 'Save')


class SchedulePageLocators(object):
    MON_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Monday')]")
    TUE_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Tuesday')]")
    WED_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Wednesday')]")
    THU_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Thursday')]")
    FRI_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Friday')]")
    SAT_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Saturday')]")
    SUN_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Sunday')]")
    TODAY_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'today')]")

    EVENT_LABEL = (By.XPATH, "//*[contains(@label, 'target temperature')]")
    EVENT_ARROW = (By.NAME, 'z')
    EVENT_CELL = (By.XPATH, "//UIATableCell[contains(@label, 'until')]")
    SCHEDULE_OPTIONS_BUTTON = (By.NAME, 'Schedule options')
    ALL_SLOTS_FILLED = (By.XPATH, "//*[contains(@label, 'Add time slot, all time slots filled')]")
    ADD_TIME_SLOT_SUBMENU = (By.XPATH, "//*[contains(@label, 'Add a time slot')]")
    SCHEDULE_RESETOK_BUTTON = (By.XPATH, "//*[@label = 'Reset']")
    SCHEDULE_RESET_SUBMENU = (By.XPATH, "//*[contains(@label, 'Reset')]")
    COPY_SCHEDULE_SUBMENU = (By.XPATH, "//*[contains(@label, 'Copy')]")
    DELETE_TIME_SLOT = (By.XPATH, "//*[contains(@label, 'Delete time slot')]")
    DELETE_TIME_SLOT_POPUP = (By.NAME, 'Delete')
    SCHEDULE_START_TIME = (By.XPATH, "//*[@name = 'edit start time']/preceding-sibling::XCUIElementTypeStaticText")
    DAY_COPY_SCHEDULE = "//*[contains(@label, 'day, button')]"
    SELECT_SLOT = "//*[contains(@label,'strSlotTime')]"
    CANCEL_SUBMENU = (By.NAME, 'Cancel')
    SAVE_SCHEDULE = (By.NAME, 'Save')

    SLOT_ONE = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[3]")
    SLOT_TWO = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[4]")
    SLOT_THREE = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[5]")
    SLOT_FOUR = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[6]")
    SLOT_FIVE = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[7]")
    SLOT_SIX = (By.XPATH, "//XCUIElementTypeScrollView[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[8]")


class EditTimeSlotPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Edit time')]")
    ADD_SLOT_TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Add time slot')]")
    EVENT_TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    START_TIME_BUTTON = (By.ID, 'startTime')
    START_TIME_LABEL = (By.XPATH, "//*[contains(@label, 'start time')]")
    HOUR_SCROLL = (By.XPATH, "//*[contains(@value, 'clock')]")
    HOT_WATER_TOGGLE_BUTTON_SCROLL = (By.XPATH, "//*[contains(@label, 'Hot water')]")
    MINUTE_SCROLL = (By.XPATH, "//*[contains(@value, 'minutes')]")
    CANCEL_BUTTON = (By.ID, 'Cancel')
    SAVE_BUTTON = (By.NAME, 'Save')
    DELETE_EVENT_BUTTON = (By.NAME, 'Delete time slot')
    DELETE_CONFIRM_BUTTON = (By.NAME, 'Delete')
    HOT_WATER_TOGGLE_BUTTON = (By.XPATH, "//UIAButton[contains(@name, 'o')]")
    PLUG_TOGGLE_BUTTON = (By.XPATH, "//UIAButton[contains(@name, 'Plug')]")
    PLUG_STATE_ON = (By.XPATH, "//UIAButton[contains(@name, ' on')]")
    PLUG_STATE_OFF = (By.XPATH, "//UIAButton[contains(@name, ' off')]")


class ChangePasswordLocators(object):
    OLDPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='Old Password']")
    NEWPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='New Password']")
    RETYPEPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='Retype Password']")
    SAVE_BUTTON = (By.NAME, 'Save')
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'screen')]")


class PinLockPageLocators(object):
    PINLOCK_LINK = (By.NAME, 'PIN lock')
    PINLOCK_SETPIN = (By.XPATH, "//UIATableCell[1][@name='PIN lock']")
    PINKEY_ONE = (By.XPATH, "//UIAKey[1][@name='1']")
    PINKEY_TWO = (By.XPATH, "//UIAKey[2][@name='2']")
    PINKEY_THREE = (By.XPATH, "//UIAKey[3][@name='3']")
    PINKEY_FOUR = (By.XPATH, "//UIAKey[4][@name='4]")
    PINSET_ON = (By.XPATH, "//*[@name='On']")
    PINLOCK_CHANGEPIN = (By.XPATH, "//UIATableCell[2][@name='Change PIN']")
    PINLOCK_FORGOTPIN = (By.XPATH, "//UIATableCell[3][@name='Forgot PIN']")
    PINLOCK_LOGOUT = (By.XPATH, "//UIAStaticText[@label='log out']")
    PINLOCK_LOGOUT_OK = (By.XPATH,)


class DemoChangePasswordLocators(object):
    OLDPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='Old Password']")
    NEWPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='New Password']")
    RETYPEPASSWORD_EDTBOX = (By.XPATH, "//UIASecureTextField[@label='Retype Password']")
    SAVE_BUTTON = (By.NAME, 'Save')


class DemoHomePageLocators(object):
    DEMO_LINK = (By.NAME, 'Demo mode')
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'screen')]")
    MENU_BUTTON = (By.NAME, 'Menu')
    MENU_TITLE = (By.NAME, 'Menu, screen')
    GOT_IT_BUTTON = (By.XPATH, "//*[@label='Got it!']")
    HEAT_CONTROL_MENU_LINK = (By.NAME, 'Heating control')
    HEAT_SCHEDULE_MENU_LINK = (By.NAME, 'Heating schedule')
    SETTINGS_MENU_LINK = (By.NAME, 'Settings')
    HOLIDAY_MODE_MENU_LINK = (By.NAME, 'Holiday mode')
    GEOLOCATION_LINK = (By.NAME, 'Geolocation')
    NOTIFICATIONS_MENU_LINK = (By.NAME, 'Notifications')
    ACCOUNT_DETAILS_MENU_LINK = (By.NAME, 'Account details')
    HOT_WATER_CONTROL_MENU_LINK = (By.NAME, 'Hot water control')
    HOT_WATER_SCHEDULE_MENU_LINK = (By.NAME, 'Hot water schedule')
    LINK_COLAPSE_BUTTON = (By.NAME, 'c')
    SETTINGS_MAIN_MENU = (By.NAME, 'Settings')
    CHANGE_PASSWORD_SUB_MENU = (By.NAME, 'Change password')
    EXIT_DEMO_MODE = (By.NAME, 'Exit Demo mode')


class HeatingNotification(object):
    SUB_MENU_HEATING_NOTIFICATION = (By.XPATH, "//*[@name ='Heating notifications'][1]")
    MAX_TEMPRATURE = (By.XPATH, "//*[contains(@label, 'Maximum Temperature')]")
    MAX_TEMPRATURE_NOTSET = (By.XPATH, "//*[contains(@label, 'Maximum Temperature, Not set')]")
    MIN_TEMPRATURE = (By.XPATH, "//*[contains(@label, 'Minimum Temperature')]")
    MIN_TEMPRATURE_NOTSET = (By.XPATH, "//*[contains(@label, 'Minimum Temperature, Not set')]")
    RECEIVE_WARNINGS = (By.XPATH, "//*[contains(@label, 'Receive warnings')]")
    RECEIVE_WARNINGS_ON = (By.XPATH, "//*[@value = '1'][2]")
    RECEIVE_WARNINGS_OFF = (By.XPATH, "//*[@value = '0']")
    BTN_BACK = (By.XPATH, "//*[@label ='Back'][1]")
    SAVE_CHANGES = (By.XPATH, "//*[contains(@label, 'Save Changes')]")
    EMAIL_ME = (By.XPATH, "//*[contains(@label, 'Email when temperature')]")
    EMAIL_ME_OFF = (By.XPATH, "//*[@value = '0']")
    EMAIL_ME_ON = (By.XPATH, "//*[@value = '1']")
    TARGET_TEMPERATURE_SCROLL_HN = (By.NAME, 'Temperature control')


class SmartPlugsLocators(object):
    PLUG_ON_BUTTON = (By.XPATH, "//*[@name='Plug - now on']")
    PLUG_OFF_BUTTON = (By.XPATH, "//*[@name='Plug - now off']")
    PLUG_BUTTON = (By.XPATH, "//*[contains(@label,'Plug - now')]")
    PLUG_SCHEDULE = (By.XPATH, "//*[contains(@label,'Plug schedule')]")
    TITLE_LABEL = (By.NAME, 'Add holiday, screen')
    TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Holiday mode, screen')]")
    ACTIVATE_HOLIDAYMODE_BUTTON = (By.NAME, 'Activate holiday mode')
    CANCEL_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[contains(@name,'Cancel holiday mode')]")
    EDIT_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[@label='Edit']")
    CANCEL_HOLIDAYMODE_ALERT = (By.XPATH, "//UIAAlert[@label='Cancel holiday mode']")
    STOP_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[contains(@name,'Stop holiday mode')]")
    TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    YES_ALERT_BUTTON = (By.XPATH, "//UIACollectionCell[@name='Yes']")
    SET_DEPARTURE = (By.NAME, 'Set departure')
    SET_RETURN = (By.NAME, 'Set return')
    DAY_PICKER = (By.XPATH, "(//UIAPicker[@type='UIAPickerWheel])[1]")
    HOUR_PICKER = (By.XPATH, "(//UIAPicker[@type='UIAPickerWheel])[2]")
    MINUTE_PICKER = (By.XPATH, "(//UIAPicker[@type='UIAPickerWheel])[3]")
    DEFAULT_DDAY = (By.XPATH, "//UIATableCell[1]/UIAStaticText[2]")
    DEFAULT_DMONTH_YEAR = (By.XPATH, "//UIATableCell[1]/UIAStaticText[3]")
    DEFAULT_DTIME = (By.XPATH, "//UIATableCell[1]/UIAStaticText[4]")
    DEFAULT_RDAY = (By.XPATH, "//UIATableCell[1]/UIAStaticText[6]")
    DEFAULT_RMONTH_YEAR = (By.XPATH, "//UIATableCell[1]/UIAStaticText[7]")
    DEFAULT_RTIME = (By.XPATH, "//UIATableCell[1]/UIAStaticText[8]")
    DEFAULT_TEMP = (By.XPATH, "//UIATableCell[2]/UIAStaticText[1]")
    PLUG_MODE_VIEW = (By.XPATH, "//*[contains(@label, 'Plug  mode')]")


class MotionSensorPageLocators(object):
    TABBAR_CONTROL = (By.NAME, '3')
    TABBAR_RECIPES = (By.NAME, 'm')
    MOTIONSENSOR_TITLE = (By.NAME, 'screen')
    MOTION_LABEL = (By.XPATH, "//*[@label='motion']")
    NOMOTION_LABEL = (By.XPATH, "//*[@label='no motion']")
    EVENTLOG_BUTTON = (By.XPATH, "//*[@label='arrow up']")
    CLOSE_LOG_BUTTON = (By.XPATH, "//*[@label='Close']")
    NO_MOTION_LOG = (By.XPATH, "//*[contains(@label,'No motion detected')]")
    INTERRUPTED_MOTION_LOG = (By.XPATH, "//*[contains(@label,'Motion')]")
    CURRENT_MOTION_LOG = (By.XPATH, "//*[contains(@label,'Motion detected')]")
    RECIPE_SCREEN_HEADER = (
        By.XPATH, "//*[contains(@label,'Here you can set up your recipes to make your home work for you')]")
    SET_RECIPE_BUTTON = (By.XPATH, "//*[@label='z']")
    RECIPE_ALWAYS_ON = (By.XPATH, "//*[contains(@label,'Your notifications are set to always on')]")
    RECIPE_SCHEDULED = (By.XPATH, "//*[contains(@label,'Your notifications are scheduled')]")
    CANCEL_RECIPE = (By.XPATH, "//*[@label='Cancel']")

    SENSOR_RECIPE = (By.XPATH, "//*[contains(@label,'detects motion')]")
    ADD_RECIPE = (By.XPATH, "//*[contains(@label,'Add a new recipe')]")
    RECIPE_SCREEN_HEADER_NEW = (By.XPATH,
                                "//*[contains(@label,'Select from the recipes below and define which settings and devices you want to connect')]")
    DAY1_LOG = (By.XPATH, "//XCUIElementTypeOther[16]")  # 6
    DAY2_LOG = (By.XPATH, "//XCUIElementTypeOther[18]")  # 5
    DAY3_LOG = (By.XPATH, "//XCUIElementTypeOther[20]")  # 4
    DAY4_LOG = (By.XPATH, "//XCUIElementTypeOther[22]")  # 3
    DAY5_LOG = (By.XPATH, "//XCUIElementTypeOther[24]")  # 2
    DAY6_LOG = (By.XPATH, "//XCUIElementTypeOther[26]")  # 1
    DAY7_LOG = (By.XPATH, "//XCUIElementTypeOther[28]")


class TextControlLocators(object):
    ADD_NEW_USER_LINK = (By.XPATH, "//UIATableCell[contains(@label,'User, Add a new user,')]")
    NAME_EDTBOX = (By.XPATH, "//*[@value='Name']")
    MOBILE_EDTBOX = (By.XPATH, "//*[@value='Mobile']")
    SAVE_BUTTON = (By.XPATH, "//*[@label='Save']")
    DELETE_BUTTON = (By.NAME, 'Delete')
    USER_TABLE = (By.XPATH, "//UIAWindow[2]/UIATableView[1]")
    CLEAR_TEXT_BUTTON = (By.NAME, 'Clear text')
    ERROR_MESSAGE = (By.XPATH, "//UIATableView[1]/UIATableCell[1]")


class DashboardPageLocators(object):
    DEVICE_LIST_BUTTON = (By.XPATH, "//*[@name='Flip to list']")
    HOT_WATER_CONTROL_DASHBOARD = (By.XPATH, "//*[contains(@label,'Hot water')]")
    PLUG_CONTROL_DASHBOARD = (By.XPATH, "//*[contains(@label,'Plug')]")
    HEAT_CONTROL_DASHBOARD = (By.XPATH, "//*[contains(@label,'Heating')]")
    HONEYCOMB_DASHBOARD_BUTTON = (By.XPATH, "//*[@name='Flip to honeycomb dashboard']")
    # TAB_BAR_CONTROL_BUTTON=(By.XPATH,"//*[@name='3']")
    TAB_BAR_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@name,'Schedule, tab')]")
    TAB_BAR_RECIPES_BUTTON = (By.XPATH, "//*[contains(@name,'Actions, tab')]")
    TAB_BAR_CONTROL_BUTTON = (By.XPATH, "//*[contains(@name,'Control, tab')]")


class DashboardTutorialPageLocators(object):
    ALLOW_BUTTON = (By.XPATH, "//*[@name='Allow']")
    RHCDASHBOARD_IMAGE = (By.XPATH, "//*[@name='rhc_dashboard']")
    NEXT_BUTTON = (By.XPATH, "//*[@name='next']")
    TAP_GOTO_DEVICE = (By.XPATH, "//*[@name ='Tap to go to your device']")
    TAP_GOTO_DEVICE_LIST = (By.XPATH, "//*[@name ='Tap to view all your devices in a list']")
    TAP_MENU = (By.XPATH, "//*[@name ='Tap to get to your menu']")
    DONE_BTN = (By.XPATH, "//*[@name ='done']")


class HolidayModePageLocators(object):
    MENU_BUTTON = (By.NAME, "Close Menu")
    TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Holiday mode, screen')]")
    ACTIVATE_HOLIDAYMODE_BUTTON = (By.NAME, 'Activate holiday mode')
    CANCEL_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[contains(@name,'Cancel holiday mode')]")
    EDIT_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[@label='Edit']")
    SAVE_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[@label='Save']")
    EDIT_HOLIDAYMODE_TEXT = (By.XPATH, "//*[@label='Edit your holiday mode settings.']")
    CANCEL_HOLIDAYMODE_ALERT = (By.XPATH, "//UIAAlert[@label='Cancel holiday mode']")
    STOP_HOLIDAYMODE_BUTTON = (By.XPATH, "//*[contains(@name,'Stop holiday mode')]")
    TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    YES_ALERT_BUTTON = (By.XPATH, "//XCUIElementTypeButton[@name='Yes']")
    NO_ALERT_BUTTON = (By.XPATH, "//XCUIElementTypeButton[@name='No']")
    SET_DEPARTURE = (By.NAME, 'Set departure')
    SET_RETURN = (By.NAME, 'Set return')

    DDAY_PICKER = (By.XPATH, "//XCUIElementTypeCell[2]/XCUIElementTypeOther[1]/XCUIElementTypePickerWheel[1]")
    # Alternate Xpath
    # DDAY_PICKER = (By.XPATH, "//*[@label = 'Set departure']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[1]")
    DHOUR_PICKER = (By.XPATH,
                    "//*[@label = 'Set departure']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[2]")
    DMIN_PICKER = (By.XPATH,
                   "//*[@label = 'Set departure']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[3]")

    RDAY_PICKER = (By.XPATH, "//XCUIElementTypeCell[4]/XCUIElementTypeOther[1]/XCUIElementTypePickerWheel[1]")
    # Alternate Xpath
    # RDAY_PICKER = (By.XPATH, "//*[@label = 'Set return']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[1]")
    RHOUR_PICKER = (By.XPATH,
                    "//*[@label = 'Set return']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[2]")
    RMIN_PICKER = (By.XPATH,
                   "//*[@label = 'Set return']/../following-sibling::XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypePickerWheel[3]")
    TEMP_PICKER = (By.XPATH, "//*[contains(@label,'Heating target temperature')]")

    DDAY = (By.XPATH, "//*[@label = 'Departure']/following-sibling::XCUIElementTypeStaticText[1]")
    DMONTH_YEAR = (By.XPATH, "//*[@label = 'Departure']/following-sibling::XCUIElementTypeStaticText[2]")
    DTIME = (By.XPATH, "//*[@label = 'Departure']/following-sibling::XCUIElementTypeStaticText[3]")

    RDAY = (By.XPATH, "//*[@label = 'Return']/following-sibling::XCUIElementTypeStaticText[1]")
    RMONTH_YEAR = (By.XPATH, "//*[@label = 'Return']/following-sibling::XCUIElementTypeStaticText[2]")
    RTIME = (By.XPATH, "//*[@label = 'Return']/following-sibling::XCUIElementTypeStaticText[3]")

    TEMP = (By.XPATH, "//*[contains(@label , 'Heating:  now')]/following-sibling::XCUIElementTypeStaticText[1]")
    # Alternate Xpath
    # TEMP = (By.XPATH, "//*[@label = 'Holiday mode']/preceding-sibling::XCUIElementTypeStaticText[1]")
    HOT_WATER = (By.XPATH, "//*[contains(@label , 'Hot Water:  now')]/following-sibling::XCUIElementTypeStaticText[1]")

    HEATING_CELL = (By.XPATH, "//XCUIElementTypeOther[contains(@label,'Heating')]")
    HEATING_CONTROL = (By.XPATH, "//XCUIElementTypeOther[contains(@label,'Heating control, screen')]")
    HEATING_RECIPE_SWITCHES = (By.XPATH, "//XCUIElementTypeSwitch[contains(@label,'Heating')]")
    HEATING_RECIPE_CONTROL = (By.NAME, 'Recipes')


class ContactSensorLocators(object):
    CS_STATUS_OPEN = (By.XPATH, "//*[@label='open']")
    CS_STATUS_CLOSED = (By.XPATH, "//*[@label='closed']")
    LOGS = (By.XPATH, "//*[@label='arrow up']")
    OPEN_ALL_DAY = (By.XPATH, "//*[contains(@label,'Open all day')]")
    OPEN_MUTLIPE_LOG = (By.XPATH, "//*[contains(@label,'Open')]")
    OPEN_CURRENT_LOG = (By.XPATH, "//*[contains(@label,'Opened')]")
    NO_EVENTS = (By.XPATH, "//*[contains(@label,'no events')]")


class RecipeScreenLocators(object):
    REMOVE_RECIPE = (By.XPATH, "//*[contains(@label,'Remove recipe')]")
    RECIPE_SCREEN_HEADER = (
        By.XPATH, "//*[contains(@label,'Here you can set up your recipes to make your home work for you')]")
    ADD_RECIPE = (By.XPATH, "//*[contains(@label,'Add a new recipe')]")
    ADD_A_NEW_RECIPE = (By.XPATH,
                        "//*[contains(@label,'Select from the recipes below and define which settings and devices you want to connect')]")
    CANCEL_BUTTON = (By.XPATH, "//*[@label='Cancel']")
    REMOVE_RECIPE = (By.XPATH, "//*[@label='Remove recipe']")
    REMOVE_POPUP = (By.XPATH, "//*[@label='Remove']")
    MS_RECIPE = (By.XPATH, "//*[contains(@label,'detects motion')]")
    CSO_RECIPE = (By.XPATH, "//*[contains(@label,'is opened')]")
    CSC_RECIPE = (By.XPATH, "//*[contains(@label,'is closed')]")
    MENU_BUTTON = (By.NAME, 'Close menu')
    NOTIFICATION_RECIPE = (By.XPATH, "//*[contains(@label,'Notify me')]")
    TYPE_OF_NOTIFICATION = (By.XPATH, "//*[contains(@label,'Notify me By')]")
    THEN_EXIST = (By.XPATH, "//*[contains(@label,'Notify me, By')]")
    THEN_NOTIFICATION = (By.XPATH, "//*[contains(@label,'Notify me by')]")
    THEN_DONE = (By.XPATH, "//*[@label='Done']")
    SAVE_BUTTON = (By.NAME, 'Save')
    'Updated objects'
    PUSH_SWITCH = (By.XPATH, "//XCUIElementTypeCell[5]/XCUIElementTypeSwitch[1]")
    MAIL_SWITCH = (By.XPATH, "//XCUIElementTypeCell[6]/XCUIElementTypeSwitch[1]")
    TEXT_SWITCH = (By.XPATH, "//XCUIElementTypeCell[7]/XCUIElementTypeSwitch[1]")
    NOT_NOW = (By.NAME, 'Not now')

    TAP_TO_CHOOSE = (By.NAME, 'Tap to choose')
    SELECTED_SENSOR = (By.XPATH, "//XCUIElementTypeCell[2]/XCUIElementTypeStaticText[1]")

    # Recipe Template objects
    MS_NOT_RECIPE = (By.XPATH, "//*[contains(@label,'Notify me when a motion sensor detects motion')]")
    CSO_NOT_RECIPE = (By.XPATH, "//*[contains(@label,'Notify me when a window or door sensor is opened')]")
    CSC_NOT_RECIPE = (By.XPATH, "//*[contains(@label,'Notify me when a window or door sensor is closed')]")
    MS_PL_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a plug ON or OFF when a motion sensor detects motion')]")
    CSO_PL_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a plug ON or OFF when a window or door sensor is opened')]")
    CSC_PL_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a plug ON or OFF when a window or door sensor is closed')]")
    MS_BU_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a light ON or OFF when a motion sensor detects motion')]")
    CSO_BU_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a light ON or OFF when a window or door sensor is opened')]")
    CSC_BU_RECIPE = (By.XPATH, "//*[contains(@label,'Turn a light ON or OFF when a window or door sensor is closed')]")
    NOTIFICATION_PICKER = (
        By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[5]/UIAPicker[1]/UIAPickerWheel[1]")


class BulbScreenLocators(object):
    BULB_NAME = "name"
    BULB_LOCATOR = "//*[contains(@name,'deviceName')]"
    BULB_OFFLINE = "//*[contains(@name,'deviceName, offline')]"
    BULB_TONE = "//*[contains(@label,'name white tone')]"
    BULB_BRIGHTNESS = "//*[contains(@label,'name brightness')]"
    LIGHT_SCHEDULE_BRIGHTNESS = (By.NAME, 'Brightness')
    BULB_COLOUR = "//*[contains(@label,'name colour')]"

    TONE_BUTTON = (By.NAME, 'tone')
    COLOUR_BUTTON = (By.NAME, 'colour')
    DIMMER_BUTTON = (By.NAME, 'dimmer')

    BULB_MODE = "//*[(@label = 'deviceName mode') and (contains(@value,'currently Schedule active') or (@value = 'currently Manual'))]"
    BULB_MODE_SCHEDULE = "//*[@label = 'deviceName mode'][contains(@value,'currently Schedule active')]"
    SCHEDULE_MODE_LABEL = (By.XPATH, "//*[contains(@value, 'Schedule active')]")
    MANUAL_MODE_LABEL = (By.XPATH, "//*[contains(@value, 'currently Manual')]")
    EDIT_SCHEDULE_MODE_LINK = (By.NAME, 'Schedule')
    CONTROL_LINK = (By.NAME, 'Control')
    SCHEDULE_OFF = (By.XPATH, "//*[contains(@label, 'schedule is not being used')]")
    SCHEDULE_ON = (By.XPATH, "//*[contains(@label, 'schedule is active')]")
    BULB_STATUS_DEVICE_LIST = "//XCUIElementTypeStaticText[@label = 'name']/following-sibling::XCUIElementTypeStaticText"

    DASHBOARD_HONEYCOMB = "//*[@label='Flip to honeycomb dashboard']"


class PlugLocators(object):
    PLUG_TITLE = "//*[contains(@label, 'devicename, Last updated')]"
    DASHBOARD_ICON = (By.XPATH, "//*[contains(@label, 'Flip to honeycomb dashboard')]")
    DEVICELIST_ICON = (By.XPATH, "//*[contains(@label, 'Flip to list')]")
    PLUG_STATE = (By.NAME, 'Plug')
    SCHEDULE_ICON = (By.XPATH, "//*[contains(@label, 'Schedule')]")
    CONTROL_ICON = (By.XPATH, "//*[contains(@label, 'Control')]")
    RECIPES_ICON = (By.XPATH, "//*[contains(@label, 'Actions')]")
    PLUG_OFF = (By.XPATH, "//*[contains(@value, 'off')]")
    PLUG_ON = (By.XPATH, "//*[contains(@value, 'on')]")
    PLUG_MANUAL_MODE = (By.XPATH, "//*[contains(@value, 'currently Manual')]")
    PLUG_SCHEDULE_MODE = (By.XPATH, "//*[contains(@value, 'currently Schedule active')]")
    PLUG_SCHEDULE_SCREEN = (By.XPATH, "//*[contains(@label, 'Plug schedule, Last updated')]")
    PLUG_RECIPES_SCREEN = (By.NAME, 'Here you can set up your actions to make your home work for you.')
    PLUG_DEVICELIST = "//*[contains(@label, 'devicename')]/following-sibling::XCUIElementTypeStaticText"
    # PLUG_MODE_VIEW = (By.XPATH, "//*[contains(@label, 'Plug  mode')]")
    PLUG_MODE_MANUAL = (By.XPATH, "//*[contains(@value, 'currently Manual')]")
    PLUG_MODE_SCHEDULE = (By.XPATH, "//*[contains(@value, 'currently Schedule')]")


class MainMenuLocators(object):
    MYHIVEHOME_MAIN_MENU = (By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'My Hive Home')]")
    MENUPAGE_TITLE = (By.XPATH, "//*[contains(@label, 'Menu, screen')]")
    MANAGEDEVICES_MAIN_MENU = (
        By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'Manage devices')]")
    INSTALLDEVICES_MAIN_MENU = (
        By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'Install devices')]")
    ALLRECIPES_MAIN_MENU = (By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'All Recipes')]")
    SETTINGS_MAIN_MENU = (By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'Settings')]")
    HELP_MAIN_MENU = (By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'Help & Support')]")
    HELP_S__MAIN_MENU = (By.XPATH, "//XCUIElementTypeTable/XCUIElementTypeOther[contains(@label, 'Help & Support')]")
    LOGOUT_MAIN_MENU = (By.XPATH, "//XCUIElementTypeTable/XCUIElementTypeOther[contains(@label, 'Log out')]")
    LOGOUT_S__MAIN_MENU = (By.XPATH, "//XCUIElementTypeOther/XCUIElementTypeOther[contains(@label, 'Log out')]")
    MANAGEDEVICE_TITLE = (By.XPATH, "//*[contains(@label, 'Manage devices, screen')]")
    INSTALLDEVICE_TITLE = (By.XPATH, "//*[contains(@label, 'Install devices, screen')]")
    ADDZONE_INSTALLDEVICE = (By.XPATH, "//*[contains(@label, 'Add heating zone')]")
    UPGRADE_INSTALLDEVICE = (By.XPATH, "//*[contains(@label, 'Upgrade to Hive 2')]")
    ADDANOTHERDEVICE_INSTALLDEVICE = (By.XPATH, "//*[contains(@label, 'Add another device')]")
    ALLRECIPES_TITLE = (By.XPATH, "//*[contains(@label, 'All Recipes, screen')]")
    GEOLOCATION_SETTINGS = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Geolocation')]")
    HOLIDAYMODE_SETTINGS = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Holiday mode')]")
    HEATINGNOTIFICATIONS_SETTINGS = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Zone notifications')]")
    ACCOUNTDETAILS_SETTINGS = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Account details')]")
    PINLOCK_SETTINGS = (By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'PIN lock')]")
    CHANGEPASSWORD_SETTINGS = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Change password')]")
    PRODUCTIDEAS_HELP = (By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Product ideas')]")
    HELPIMPROVEHIVE_HELP = (By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Help')]")
    SERVICESTATUS_HELP = (
        By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Service status')]")
    TEXTCONTROL_HELP = (By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[contains(@label, 'Text control')]")
    LOGINPAGE_TITLE = (By.XPATH, "//*[contains(@label, 'Log in, screen')]")


class DashboardCustomisationLocators(object):
    ADD_DEVICE_BUTTON = (By.NAME, 'Add item to your dashboard')
    SAVE_CHANGES_BUTTON = (By.NAME, 'Save')
    CANCEL_CHANGES_BUTTON = (By.NAME, 'Cancel')
    ADD_DEVICE_TITLE = (By.XPATH, "//*[contains(@label, 'Choose a device you wish to place on your dashboard')]")
    CANCEL_ADD_DEVICE = (By.NAME, 'Cancel placing device on the dashboard')
    CELL = "//XCUIElementTypeButton[contains(@label, 'deviceName')]"
    DEVICE_IN_LIST = "//XCUIElementTypeCell[contains(@label, 'deviceName')]"
    DELETE_DEVICE_BUTTON = "//XCUIElementTypeOther/XCUIElementTypeButton[contains(@name,'deviceName')]/preceding-sibling::XCUIElementTypeButton[@name='close']"


class LeakSensorPageLocators(object):
    # Dashboard icon
    LEAK_SENSOR_ICON = (By.XPATH, "//*[contains(@name,'Hive Leak Sensor')]")

    # Large flow related objects
    LARGE_FLOW_ALERT = (By.NAME, 'High water usage')
    LARGE_FLOW_ALERT_TEXT = (By.XPATH, "//*[contains(@name,'A large amount of water has been flowing for over')]")
    LARGE_FLOW_CONTINUOUS_ALERT = (
        By.XPATH, "//*[contains(@name,'We will continue to alert you if water is running for over')]")

    # Small flow related objects
    SMALL_FLOW_ALERT = (By.NAME, 'Low water flow')
    SMALL_FLOW_ALERT_TEXT = (By.XPATH,
                             "//*[contains(@name,'Hello, we have detected small amounts of water continuously flowing in your home.')]")
    SMALL_FLOW_OK = (By.NAME, 'OK')
    SMALL_FLOW_REFRESH = (By.NAME, 'Refresh')

    # Normal flow related objects
    NORMAL_FLOW = (By.NAME, 'All OK')

    # battery objects
    FULL_BATTERY = (By.NAME, 'R')
    NORMAL_BATTERY = (By.NAME, 'Q')
    LOW_BATTERY = (By.NAME, 'P')

    # general objectss
    CALL_HIVE = (By.NAME, 'call hive normal')
    SETTINGS_BUTTON = (By.NAME, 'Settings')
    CANCEL_BUTTON = (By.NAME, 'Cancel')
    FLOW_YES = (By.NAME, 'Yes')
    FLOW_NO = (By.NAME, 'No')
    POPUP_YES = (By.XPATH, "//XCUIElementTypeOther[2]/XCUIElementTypeButton[1]")
    POPUP_NO = (By.XPATH, "//XCUIElementTypeOther[2]/XCUIElementTypeButton[2]")
    CALIBRATING_SCREEN = (By.NAME, 'clock')
    BACK_BUTTON = (By.NAME, 'Back')
    DONE_BUTTON = (By.NAME, 'Done')
    CONFIRM_BUTTON = (By.NAME, 'Confirm')
    SAVE_BUTTON = (By.NAME, 'Save')

    # Notification Settings
    ALERT_NOTIFICATION = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[2]")
    PUSH_NOTIFICATION_STATUS = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[2]")
    EMAIL_STATUS = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[3]")
    TEXT_STATUS = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[4]")
    PUSH_NOTIFICATION_BUTTON = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[2]/XCUIElementTypeButton[1]")
    EMAIL_BUTTON = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[3]/XCUIElementTypeButton[1]")
    TEXT_BUTTON = (By.XPATH, "//XCUIElementTypeTable[1]/XCUIElementTypeCell[4]/XCUIElementTypeButton[1]")
    THRESHOLD_TIME = (By.XPATH, "//XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[1]")


class NATLocators(object):
    NAT_TITLE = "//*[contains(@label, 'devicename, Last updated')]"
    NAT_TITLE_CHANGE = (By.XPATH, "//*[contains(@label, 'Last updated')]")
    DASHBOARD_ICON = (By.XPATH, "//*[contains(@label, 'Flip to honeycomb dashboard')]")
    DEVICELIST_ICON = (By.XPATH, "//*[contains(@label, 'Flip to list')]")
    THERMOSTAT_SETTINGS_ICON = (By.NAME, 'More')
    THERMOSTAT_SETTINGS_SAVE = (By.NAME, 'Save')
    THERMOSTAT_SETTINGS_CANCEL = (By.NAME, 'Cancel')
    THERMOSTAT_SETTINGS_TITLE = (By.NAME, 'Settings')
    THERMOSTAT_MODE_OFF_ICON = (By.XPATH, "//*[contains(@value, 'Off')]")
    THERMOSTAT_MODE_HEAT_ICON = (By.XPATH, "//*[contains(@value, 'Heat')]")
    THERMOSTAT_MODE_DUAL_ICON = (By.NAME, 'Heat, C')
    THERMOSTAT_MODE_COOL_ICON = (By.XPATH, "//*[contains(@value, 'Cool')]")
    THERMOSTAT_MODE_HOLD_ICON = (By.NAME, 'Hold')
    THERMOSTAT_MODE_SCHEDULE_ICON = (By.NAME, 'Schedule')
    THERMOSTAT_CONTROL = (By.NAME, 'Temperature control')
    THERMOSTAT_CONTROL_HEAT = (By.XPATH, "//*[contains(@value, 'Heating target temperature')]")
    THERMOSTAT_CONTROL_COOL = (By.XPATH, "//*[contains(@value, 'Cooling target temperature')]")
    THERMOSTAT_FLAKEICON = (By.XPATH, "//*[contains(@label, 'Your cooling is currently on')]")
    THERMOSTAT_FLAMEICON = (By.XPATH, "//*[contains(@label, 'Your heating is currently on')]")
    THERMOSTAT_FLAKEICON_DUAL = (By.XPATH, "//*[contains(@label, 'F')]")
    THERMOSTAT_FLAMEICON_DUAL = (By.XPATH, "//*[contains(@label, 'j')]")
    THERMOSTAT_SCHEDULE_MODE_ICON = (By.XPATH, "//*[contains(@label, 'next time slot')]")
    THERMOSTAT_MANUAL_MODE_ICON = (By.XPATH, "//*[contains(@label, 'Hold mode')]")
