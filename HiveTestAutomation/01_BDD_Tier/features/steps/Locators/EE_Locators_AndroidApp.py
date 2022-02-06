"""
Created on 16 Jun 2015

@author: ranganathan.veluswamy
"""

from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    TITLE_LABEL = (By.ID, 'title')
    USERNAME_EDTBOX = (By.ID, 'login_edit_username')
    PASSWORD_EDTBOX = (By.ID, 'login_edit_password')
    LOGIN_BUTTON = (By.ID, 'login_btn_submit')


class HomePageLocators(object):
    SKIP_BUTTON = (By.ID, 'textBtn')
    CURRENT_TITLE = (By.ID, 'title')
    DASHBOARD_TITLE = (By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.TextView[1][@text='My Hive Home']")
    MENU_BUTTON = (By.NAME, 'Menu button, double tap to open menu')
    MENU_BUTTON_V6 = (By.ID, 'full_product_menu_button_hide')
    MENU_BUTTON_SHOW = (By.ID, 'full_product_menu_button_show')
    HOME_MENU_SCREEN_V6 = (By.XPATH, "//*[@text='Home']")
    HEAT_WATER_MAIN_MENU = (By.ID, 'icon')
    HEAT_WATER_MAIN_MENU_ICON = (By.XPATH, "//*[@text='c']")

    HEAT_WATER_MAIN_MENU_ARROW_UP = (By.XPATH, "//*[@text='j']")
    HEAT_WATER_MAIN_MENU_ARROW_DOWN = (By.XPATH, "//*[@text='k']")
    SwitchOver_Button = (By.XPATH, "//*[contains(@content-desc,'Switch view. Double tap to switch to a list view.')]")
    EmptySlots_Dashboard = (By.ID, 'dbEmptyCircleView')
    HEATING_DASHBOARD_ICON = (By.XPATH, "//*[contains(@content-desc,'Heating')]")
    HEATING_NEWLOOK_OKbutton = (By.ID, 'ok_button')
    HOTWATER_DASHBOARD_ICON = (By.XPATH, "//*[contains(@content-desc,'Hot water')]")
    Plug_Dashboard = (By.XPATH, "//*[@text='Plug']")
    Plug_runtime_Dashboard = "//*[@text='devicename']"
    HEATING_SUBMENU = (By.XPATH, "//*[@text='Heating']")
    HOT_WATER_SUBMENU = (By.XPATH, "//*[@text='Hot water']")
    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    REFRESH_BUTTON_V6 = (By.ID, 'refresh_button')
    SETTINGS_MAIN_MENU = (By.XPATH, "//*[@text='Settings']")
    ACCOUNT_SUB_MENU = (By.XPATH, "//*[@text='Account details']")
    HOLIDAY_SUB_MENU = (By.XPATH, "//*[@text='Holiday mode']")
    CHANGE_PASSWORD_SUBMENU = (By.XPATH, "//*[@text='Change password']")
    HELP_SUPPORT_SUBMENU = (By.XPATH, "//*[@text='Help & Support']")
    ACTIONS_MENU = (By.XPATH, "//*[contains(@text,'Actions')]")
    MY_ACTIONS_MENU = (By.XPATH, "//*[contains(@text,'My Actions')]")
    DEVICE_ICON_DASHBOARD = "//*[@text='deviceName']"


class PlugLocators(object):
    PLUG_TITLE = (By.ID, 'title')
    PLUG_STATUS = (By.ID, 'active_plug_status_text')
    PLUG_OFF_TEXT = (By.XPATH, "//*[contains(@content-desc,'Active plug is OFF. Double click to activate it')]")
    PLUG_ON_TEXT = (By.XPATH, "//*[contains(@content-desc,'Active plug is ON. Double click to deactivate it')]")
    BUTTON_MODE = (By.ID, 'button_mode_right')
    MANUAL_MODE = (By.XPATH, "//*[@text='Manual']")
    MODE_TEXT = (By.ID, 'button_mode_status')
    SCHEDULE_MODE = (By.XPATH, "//*[@text='Schedule active']")
    CONTROL_ICON = (By.XPATH, "//*[contains(@content-desc,'Control tab. Double tap to select')]")
    SCHEDULE_ICON = (By.XPATH, "//*[contains(@content-desc,'Schedule tab. Double tap to select')]")
    ACTIONS_ICON = (By.XPATH, "//*[contains(@content-desc,'Actions tab. Double tap to select')]")
    ADD_ICON = (By.ID, 'schedule_fab')
    ACTIONS_VERIFY_TEXT = (
        By.XPATH, "//*[contains(@content-desc,'Here you can set up your Actions to make your home work for you.')]")
    DASHBOARD_ICON = (By.ID, 'dashboardHomeButton')
    PLUG_OFF_DASH = "//*[contains(@content-desc,'devicename. Your active plug is currently Off.')]"
    PLUG_ON_DASH = "//*[contains(@content-desc,'devicename. Your active plug is currently On.')]"
    PLUG_STATUS = (By.XPATH, "//*[contains(@content-desc,'Double click to')]")


class MainMenuLocators(object):
    MYHIVEHOME_MAIN_MENU = (By.XPATH, "//*[@text='My Hive Home']")
    MENUPAGE_TITLE = (By.XPATH, "//*[@text='Home']")
    MANAGEDEVICES_MAIN_MENU = (By.XPATH, "//*[@text='Manage devices']")
    INSTALLDEVICES_MAIN_MENU = (By.XPATH, "//*[@text='Install devices']")
    ACTIONS_MAIN_MENU = (By.XPATH, "//*[@text='All Actions']")
    SETTINGS_MAIN_MENU = (By.XPATH, "//*[@text='Settings']")
    HELP_MAIN_MENU = (By.XPATH, "//*[@text='Help & Support']")
    LOGOUT_MAIN_MENU = (By.XPATH, "//*[@text='Logout']")
    MANAGEDEVICE_TITLE = (By.XPATH, "//*[@text='Manage devices']")
    INSTALLDEVICE_TITLE = (By.XPATH, "//*[@text='Install devices']")
    ADDZONE_INSTALLDEVICE = (By.XPATH, "//*[@text='Add heating zone']")
    UPGRADE_INSTALLDEVICE = (By.XPATH, "//*[@text='Upgrade to Hive 2']")
    ADDANOTHERDEVICE_INSTALLDEVICE = (By.XPATH, "//*[@text='Add another device']")
    ACTIONS_TITLE = (By.XPATH, "//*[@text='All Actions']")
    GEOLOCATION_SETTINGS = (By.XPATH, "//*[@text='Geolocation']")
    HOLIDAYMODE_SETTINGS = (By.XPATH, "//*[@text='Holiday mode']")
    HEATINGNOTIFICATIONS_SETTINGS = (By.XPATH, "//*[@text='Heating notifications']")
    ACCOUNTDETAILS_SETTINGS = (By.XPATH, "//*[@text='Account details']")
    PINLOCK_SETTINGS = (By.XPATH, "//*[@text='Pin lock']")
    CHANGEPASSWORD_SETTINGS = (By.XPATH, "//*[@text='Change password']")
    FAQ_HELP = (By.XPATH, "//*[@text='FAQs']")
    HELPIMPROVEHIVE_HELP = (By.XPATH, "//*[@text='Help improve Hive']")
    SERVICESTATUS_HELP = (By.XPATH, "//*[@text='Service status']")
    TEXTCONTROL_HELP = (By.XPATH, "//*[@text='Text control']")
    LOGINPAGE_TITLE = (By.XPATH, "//*[@text='Log in']")


class HeatingHomePageLocators(object):
    TITLE_LABEL = (By.NAME, 'Heating')
    TITLE_LABEL1 = (By.XPATH, "//[contains(text(),'Heating')]")

    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    HEAT_CONTROL_TAB = (By.XPATH, "//*[@text='Control']")
    HEAT_SCHEDULE_TAB = (By.XPATH, "//*[@text='Schedule']")


class ChangePasswordLocators(object):
    OLD_PASSWORD_EDITTEXT = (By.ID, 'oldPassword')

    NEW_PASSWORD_EDITTEXT = (By.ID, 'newPassword')

    CONF_PASSWORD_EDITTEXT = (By.ID, 'repeatPassword')

    SAVE_PASSWORD = (By.ID, 'positiveBtn')


class PinLock(object):
    PINLOCK_SUB_MENU = (By.XPATH, "//*[@text='Pin lock']")
    PINLOCK_STATUS_OFF = (By.ID, 'on_off_switch')
    PINLOCK_STATUS_ON = (By.XPATH, "//*[contains(@content-desc,'Pin Lock  is currently ON. Double tap to change.')]")
    PINLOCK_CHANGE_PIN = (By.XPATH, "//*[@text='Change PIN']")
    PINLOCK_FORGOT_PIN = (By.XPATH, "//*[@text='Forgotten pin']")
    PINLOCK_CANCEL = (By.XPATH, "//*[@text='Cancel']")
    ENTER_CURRENT_PIN_CHANGE = (By.ID, 'pin_text_0')
    ENTER_NEW_PIN_CHANGE = (By.ID, 'pin_text_1')
    CONFIRM_NEW_PIN_CHANGE = (By.ID, 'pin_text_2')
    SAVE_CHANGE_PIN = (By.XPATH, "//*[@text='Save']")
    CANCEL_CHANGE_PIN = (By.XPATH, "//*[@text='Cancel']")
    ENTER_REMOVE_PIN = (By.XPATH, "//*[contains(@content-desc,'Enter PIN')]")
    SAVE_REMOVE_PIN = (By.XPATH, "//*[@text='Save']")
    PIN_TITLE = (By.XPATH, "//*[@text='PIN Lock']")
    ENTER_NEW_PIN = (By.XPATH, "//*[contains(@content-desc,'Enter PIN')]")
    REENTER_NEW_PIN = (By.ID, 'pin_text_1')
    SAVE_NEW_PIN = (By.XPATH, "//*[@text='Save']")
    PINLOCK_LOGOUT = (By.ID, 'text_information_view')


class TextControlLocators(object):
    ADD_NEW_USER_LINK = (By.ID, 'plusSign')
    NAME_EDTBOX = (By.ID, 'usernameEditText')
    MOBILE_EDTBOX = (By.ID, 'numberEditText')
    SAVE_BUTTON = (By.ID, 'positiveBtn')
    TEXTCONTROL_SUBMENU = (By.XPATH, "//*[@text='Text control']")


class LogoutLocators(object):
    LOGOUT_OPTION = (By.XPATH, "//*[@text='Logout']")


class HotWaterHomePageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@text='Hot water']")
    TITLE_LABEL_BOOST = (By.XPATH, "//*[@text='Boost']")
    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    HOT_WATER_CONTROL_TAB = (By.XPATH, "//*[@text='Control']")
    HOT_WATER_SCHEDULE_TAB = (By.XPATH, "//*[@text='Schedule']")


class HoneycombDasbordLocators(object):
    HONEYCOMB_SHOW_DASHBOARD = (By.ID, 'btnGetStarted')
    HONEYCOMB_HOTWATER_ON = (By.XPATH, "//*[@text='l']")
    HONEYCOMB_HOTWATER_OFF = (By.XPATH, "//*[@text='k']")
    HONEYCOMB_HEATING_ON = (By.XPATH, "//*[@text='j']")
    HONEYCOMB_HEATING_OFF = (By.XPATH, "//*[@text='i']")
    HONEYCOMB_PLUG_ICON_OFF = (By.XPATH, "//*[@text='o']")
    HONEYCOMB_PLUG_ICON_ON = (By.XPATH, "//*[@text='p']")
    HONEYCOMB_MOTION_OFF = (By.XPATH, "//*[@text='q']")
    HONEYCOMB_MOTION_ON = (By.XPATH, "//*[@text='r']")
    HONEYCOMB_MOTION_SENSOR = (By.XPATH, "//*[@text='Motion Sensor']")
    HONEYCOMB_WINDOW_SENSOR = (By.XPATH, "//*[@text='Win/door Sensor']")
    HONEYCOMB_PLUG = (By.XPATH, "//*[@text='Plug']")
    HONEYCOMB_DEVICE_OFFLINE = (By.XPATH, "//*[@text='Device offline!']")
    DEVICE_TODAYS_LOGS = (By.ID, "logButton")
    DEVICE_TODAYS_LOGS_CLOSE = (By.ID, "full_product_menu_button_close")
    HONEYCOMB_MOTION_SENSOR_1 = (By.XPATH, "//*[@text='Motion Sensor1']")
    HONEYCOMB_LIGHT = "//*[@text='lightName']"

    HONEYCOMB_LIGHT_ON = (By.XPATH, "//*[@text='v']")
    HONEYCOMB_LIGHT_OFF = (By.XPATH, "//*[@text='u']")
    HONEYCOMB_WINDOW_OFF = (By.XPATH, "//*[@text='s']")
    HONEYCOMB_WINDOW_ON = (By.XPATH, "//*[@text='t']")
    HONEYCOMB_INTRO = (By.XPATH, "//*[@text='Show me my dashboard']")
    HONEY_DASHBOARD_HOME_BUTTON = (By.ID, "dashboardHomeButton")
    DASHBOARD_VIEWFLIPPER = (By.ID, "dashboardViewFlipperButtonContainer")
    HONEY_DASHBOARD_TITLE = (By.XPATH, "//*[@text='Dashboard']")

    HONEYCOMB_WARM_WHITE_LIGHT = (By.XPATH, "//*[@text='Warm White Light']")
    HONEYCOMB_TUNEBALE_LIGHT = (By.XPATH, "//*[@text='Tuneable Light']")
    HONEYCOMB_COLOUR_LIGHT = (By.XPATH, "//*[@text='Colour Light']")
    HONEYCOMB_LIGHT = "//*[@text='lightName']"


class MotionSensorLocators(object):
    MOTION_STATUS = (By.ID, "status")
    MOTION_EVENT_LOG = (By.ID, "motionText")
    TODAYS_LOG_SLIDING_LAYOUT = (By.ID, "sliding_layout")
    DAY1_LOG = (By.XPATH, "//android.widget.FrameLayout[7]")
    DAY2_LOG = (By.XPATH, "//android.widget.FrameLayout[6]")
    DAY3_LOG = (By.XPATH, "//android.widget.FrameLayout[5]")
    DAY4_LOG = (By.XPATH, "//android.widget.FrameLayout[4]")
    DAY5_LOG = (By.XPATH, "//android.widget.FrameLayout[3]")
    DAY6_LOG = (By.XPATH, "//android.widget.FrameLayout[2]")
    DAY7_LOG = (By.XPATH, "//android.widget.FrameLayout[1]")
    MOTIONSENSOR_RECEIPES = (By.XPATH, "//*[@text='Actions']")
    RECEIPES_PAGE = (By.ID, "pager")
    RECEIPES_LIST = (By.ID, "rules_list")
    AVAILABLE_RECEIPES_LIST = (By.XPATH, "//android.widget.ListView[1]/android.widget.RelativeLayout")
    ADD_RECEIPES = (By.ID, "recipe_add_recipe_layout")
    ADD_RECEIPES_CANCELBACKFLIPPPER = (By.ID, "backCancelBtnFlipper")
    ADD_RECEIPES_TITLE = (By.ID, "title")
    DELETE_RECEIPE = (By.ID, "trash")
    SENSOR_RECEIPE = (By.XPATH, "//*[contains(@content-desc, 'detects motion')]")
    EDIT_RECEIPES_BACKBTN = (By.ID, "backBtn")


class ActivePlugLocator(object):
    PLUG_STATUS = (By.XPATH, "//*[@text='on']")
    PLUG_MODE = (By.ID, 'button_mode_status')
    PLUG_MODE_RIGHT_ARROW = (By.ID, 'button_mode_right')
    PLUG_MODECHANGE_RIGHT = (By.ID, "dashboardHomeButton")
    PLUG_CONTROL_TAB = (By.XPATH, "//*[contains(@content-desc,'Control tab.')]")
    PLUG_SCHEDULE_TAB = (By.XPATH, "//*[contains(@content-desc,'Schedule tab.')]")
    PLUG_SCHEDULE_STATUS = (By.XPATH, "//*[@text='Schedule active']")


class ActiveplugControlPageLocators(object):
    PLUG_ICON_ON = (By.XPATH, "//*[@text='p']")
    PLUG_ICON_OFF = (By.XPATH, "//*[@text='o']")


class HeatingControlPageLocators(object):
    TARGET_TEMPERATURE_SCROLL = (By.ID, 'heating_control_view')
    PRESET_TEMP_BUTTON = (By.ID, 'heating_control_view')
    SCHEDULE_MODE_LINK = (By.XPATH, "//android.widget.RadioButton[2][@text='Schedule']")
    MANUAL_MODE_LINK = (By.XPATH, "//*[@text='Manual']")
    OFF_MODE_LINK = (By.XPATH, "//*[@text='Off']")
    OFF_MODE_LINK_V6 = (By.XPATH, "//*[contains(@content-desc,'heating Off mode')]")
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@content-desc,'currently active')]")
    FLAME_ICON = (By.ID, "flame")
    BOOST_FLAME_ICON = (By.ID, 'current_state')

    BOOST_MODE_LINK = (By.XPATH, "//*[@text='boost']")
    BOOST_MODE_LINK_V6 = (By.XPATH, "//*[@text='boost']")
    BOOST_STOP_BUTTON = (By.ID, "boost_btn_stop")
    BOOST_TIMER = (By.ID, 'boost_timer')
    BOOST_CURRENT_HOUR = (By.ID, "boost_timer_hour")
    BOOST_CURRENT_MINUTE = (By.ID, "boost_timer_mins")
    BOOST_CURRENT_SECOND = (By.ID, "boost_timer_secs")
    BOOST_TEMP_SCROLL = (By.ID, "heating_control_view")


class EditBoostTimePageLocators(object):
    EDIT_BOOST_TIME_SCREEN = (By.XPATH, "//*[@text='Edit Boost Time']")
    BOOST_TIME_SCROLL = (By.ID, 'boostTimeIntervalList')
    NUMBER_INSDE_SCROLL_ITEM = (By.ID, 'numberpicker_input')
    CANCEL_BUTTON = (By.XPATH, "//*[@text='Cancel']")
    SAVE_BUTTON = (By.XPATH, "//*[@text='Save']")


class HotWaterControlPageLocators(object):
    RUNNING_STATE_CIRCLE = (By.ID, 'hotWaterCircleView')
    RUNNING_STATE_CIRCLE_V6 = (By.ID, 'hotWaterImage')
    HOTWATER_STATUS = (By.ID, 'hwText')
    HOTWATER_STATUS_V6 = (By.ID, 'hwText')
    SCHEDULE_MODE_LINK = (By.XPATH, "//android.widget.RadioButton[1][@text='Schedule']")
    MANUAL_MODE_LINK = (By.XPATH, "//*[@text='On']")
    OFF_MODE_LINK = (By.XPATH, "//*[@text='Off']")
    BOOST_ACTIVE = (By.ID, 'hwText')
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@content-desc,'currently active')]")
    BOOST_MODE_LINK = (By.XPATH, "//*[@text='boost']")
    BOOST_MODE_LINK_V6 = (By.ID, "hotWaterBoost")
    BOOST_STOP_BUTTON = (By.ID, "boost_btn_stop")
    BOOST_TIMER = (By.ID, 'boost_timer')
    BOOST_CURRENT_HOUR = (By.ID, "boost_timer_hour")
    BOOST_CURRENT_MINUTE = (By.ID, "boost_timer_mins")
    BOOST_CURRENT_SECOND = (By.ID, "boost_timer_secs")


class SchedulePageLocators(object):
    MON_SCHEDULE_BUTTON = (By.ID, 'mon_single_weekday')
    TUE_SCHEDULE_BUTTON = (By.ID, 'tue_single_weekday')
    WED_SCHEDULE_BUTTON = (By.ID, 'wed_single_weekday')
    THU_SCHEDULE_BUTTON = (By.ID, 'thu_single_weekday')
    FRI_SCHEDULE_BUTTON = (By.ID, 'fri_single_weekday')
    SAT_SCHEDULE_BUTTON = (By.ID, 'sat_single_weekday')
    SUN_SCHEDULE_BUTTON = (By.ID, 'sun_single_weekday')

    START_TIME_LABEL = (By.ID, 'textViewFromTime')
    END_TIME_LABEL = (By.XPATH, "//*[contains(@text,'.m.')]")
    EVENT_OPTIONS_BUTTON = (By.XPATH, "//*[contains(@content-desc,'More options')]")
    DELETE_EVENT_SUBMENU = (By.XPATH, "//*[@text='Delete']")
    EDIT_TIME_SLOT_SUBMENU = (By.XPATH, "//*[@text='Edit time slot']")
    SCHEDULE_OPTIONS_BUTTON = (By.ID, 'schedule_fab')
    # ADD_TIME_SLOT_SUBMENU = (By.ID, 'add_a_time_slot')
    ADD_TIME_SLOT_SUBMENU = (By.XPATH, "//*[@text='Add a time slot']")
    SCHEDULE_SPINNER_MENU = (By.ID, 'schedule_spinner')
    SIX_EVENT_SUBMENU = (By.XPATH, "//*[@text='6 time slot schedule']")
    FOUR_EVENT_SUBMENU = (By.XPATH, "//*[@text='4 time slot schedule']")
    SCHEDULE_RESET_SUBMENU = (By.ID, 'resetScheduleText')
    SCHEDULE_COPYSCHE_TEXTVIEW = (By.ID, 'copyScheduleText')
    SCHEDULE_COPYSCHEDAY_LAYOUT = (By.ID, 'COPYSCHEDAY')
    SCHEDULE_RESETOK_BUTTON = (By.ID, 'positiveBtn')
    CONTROL_ICON = (By.XPATH, "//*[contains(@content-desc,'Control tab. Double tap to select')]")
    SCHEDULE_ADDTIMESLOT_TEXTVIEW = (By.ID, 'addTimeSlotText')
    SCHEDULE_TIMESLOTOPTION_ICON = (By.XPATH, "//android.widget.RelativeLayout[INDEX]/android.view.ViewGroup[1]/"
                                              "android.support.v7.widget.LinearLayoutCompat[1]/android.widget.ImageView[1]")
    SCHEDULE_DELETETIMESLOT_ICON = (
        By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.TextView[1][@text = 'Delete']")
    SCHEDULE_YES_BUTTON = (By.ID, 'positiveBtn')


class EditTimeSlotPageLocators(object):
    HEATING_TITLE_LABEL = (By.NAME, 'Edit event for Heating Schedule')
    HOT_WATER_TITLE_LABEL = (By.NAME, 'Edit event for Hot Water Schedule')
    EVENT_TARGET_TEMPERATURE_SCROLL = (By.ID, 'editHeatingScheduleTempControlView')
    HOT_WATER_TOGGLE_BUTTON = (By.ID, 'edit_schedule_item_hot_water_toggle_button')
    TOGGLE_BUTTON = (By.XPATH, "//android.widget.Switch[1][contains(@text,'O')]")
    START_TIME_BUTTON = (By.ID, 'startTime')
    HOUR_SCROLL = (By.ID, 'hour')
    FORMAT_SCROLL = (By.ID, 'amPm')
    NUMBER_INSDE_SCROLL_ITEM = (By.ID, 'numberpicker_input')
    MINUTE_SCROLL = (By.ID, 'minute')
    CANCEL_BUTTON = (By.XPATH, "//*[@text='Cancel']")
    # SAVE_BUTTON = (By.ID, 'button_save')
    SAVE_BUTTON = (By.XPATH, "//*[@text='Save']")
    ADD_BUTTON = (By.XPATH, "//*[@text='Save']")
    ADD_BUTTON_V6 = (By.XPATH, "//*[@text='Add']")
    EDIT_TIMESLOT_PAGE_DIMMER_SEEKBAR = (By.ID, 'seekbar')
    EDIT_TIMESLOT_PAGE_CURRENT_DIMMER_VALUE = (By.XPATH, "//*[contains(@content-desc,'')]")
    EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_WARM_WHITE = (By.ID, 'edit_schedule_item_light_white_toggle_button')
    EDIT_TIMESLOT_PAGE_TONE_SEEKBAR = (By.ID, 'light_tunable_tone_seekbar')
    EDIT_TIMESLOT_PAGE_CURRENT_TONE_VALUE = (By.XPATH, "//*[contains(@content-desc,'')]")
    EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_TUNEABLE = (By.ID, 'edit_schedule_item_light_tunable_toggle_button')
    EDIT_TIMESLOT_PAGE_COLOUR_SEEKBAR = (By.ID, 'light_colour_colour_seekbar')
    EDIT_TIMESLOT_PAGE_CURRENT_COLOUR_VALUE = (By.XPATH, "//*[contains(@content-desc,'')]")
    EDIT_TIMESLOT_PAGE_ON_OFF_BUTTON_COLOUR = (By.ID, 'edit_schedule_item_light_colour_toggle_button')
    EDIT_TIMESLOT_AM_FORMAT = (By.XPATH, "//*[contains(@text,'a.m.')]")


class AccountDetailsLocators(object):
    SETTINGS_MAIN_MENU = (By.XPATH, "//*[@text='Settings']")
    ACCOUNT_SUB_MENU = (By.XPATH, "//*[@text='Account details']")


class HolidayModeLocators(object):
    START_DATE_TIME = (By.ID, 'button_holiday_mode_departure')
    END_DATE_TIME = (By.ID, 'button_holiday_mode_return')
    ACTIVATE_HOLIDAY_BUTTON = (By.ID, 'button_start_holiday_mode')
    TITLE = (By.ID, 'title')
    DEPARTURE_SAVE = (By.ID, 'positiveBtn')
    DEPARTURE_MONTH_YEAR = (By.ID, 'calendar_month_year_textview')
    DEPARTURE_ADD_MONTH = (By.ID, 'calendar_right_arrow')
    DEPARTURE_DEL_MONTH = (By.ID, 'calendar_left_arrow')
    DEPARTURE_DATES = (By.XPATH, "//*[@Id = 'calendar_tv' AND @text='CHANGE']")
    DEPARTURE_TIME = (By.ID, 'edit_holiday_mode_set_departure_time')
    ARRIVAL_TIME = (By.ID, 'edit_holiday_mode_set_return_time')
    TARGET_TEMPERATURE = (By.ID, 'tempControlView')
    FROST_TEMP = (By.ID, 'holiday_mode_status_zone_target_temperature_frost_protection')
    TARGET_TEMP = (By.ID, 'holiday_mode_status_zone_target_temperature')
    DECIMAL_TEMP = (By.XPATH,
                    "//android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1][contains(@resource-id, 'zone_detail_depart')]/android.widget.TextView[2][contains(@resource-id, 'holiday_mode_status_zone_target_temperature_degree_decimal')]")
    DEPARTURE_DATE = (By.ID, 'holiday_mode_status_data_day_of_month')
    ARRIVAL_DATE = (By.ID, 'edit_holiday_mode_set_return_date')
    STOP_HOLIDAYMODE_BUTTON = (By.ID, 'button_stop_holiday_mode')
    EDIT_HOLIDAYMODE_BUTTON = (By.ID, 'button_edit_holiday_mode')
    TEMP_PICKER = (By.ID, 'tempControlView')
    RIGHT_ARROW = (By.ID, 'calendar_right_arrow')
    DAY_PICKER = (By.XPATH, "//android.widget.GridView[1]/android.widget.TextView[@text = 'DAY']")
    SET_RETURN = (By.ID, 'negativeBtn')
    RDAY_PICKER = (
        By.XPATH, "//android.support.v4.view.ViewPager[1]/android.widget.GridView[1]/android.widget.TextView[1]")
    RHOUR_PICKER = (By.ID, 'hour')
    RMIN_PICKER = (By.ID, 'minute')
    DEPARTURE_TITLE = (By.XPATH, "//*[@text='Departure']")
    RETURN_TITLE = (By.XPATH, "//*[@text='Return']")
    DEPARTURE_CANCEL = (By.ID, 'negativeBtn')
    DEPARTURE_DAY = (By.ID, 'edit_holiday_mode_set_departure_date')
    ARRIVAL_DAY = (By.ID, 'edit_holiday_mode_set_return_date')
    DAY_ICON = (By.ID, 'holiday_mode_status_data_day_of_month')
    MONTH_YEAR_TIME = (By.ID, 'holiday_mode_status_data_month_year_time')
    CONFIRM_CHECKBOX = (By.ID, 'confirm_checkbox')
    SAVE_BUTTON = (By.ID, 'positiveBtn')
    HOLIDAY_TITLE = (By.ID, 'holiday_mode_status_title')


class HeatingNotificationsLocators(object):
    HEATING_NOTIFICATION = (By.XPATH, "//*[@text='Heating notifications']")
    HEATING_MAX_SWITCH = (By.ID, 'checkbox_max_temperature')
    HEATING_MIN_SWITCH = (By.ID, 'checkbox_min_temperature')
    HEATING_MAXTEMP_ICON = (By.ID, 'temp_control_notifications_max')
    HEATING_MINTEMP_ICON = (By.ID, 'temp_control_notifications_min')
    HEATING_MAX_ON = (
        By.XPATH,
        "//*[contains(@content-desc,'Email me for Maximum Temperature  is currently ON. Double tap to change.')]")
    HEATING_MAX_OFF = (By.XPATH,
                       "//*[contains(@content-desc,'Email me for Maximum Temperature  is currently OFF. Double tap to change.')]")
    HEATING_MIN_ON = (
        By.XPATH,
        "//*[contains(@content-desc,'Email me for Minimum Temperature  is currently ON. Double tap to change.')]")
    HEATING_MIN_OFF = (By.XPATH,
                       "//*[contains(@content-desc,'Email me for Minimum Temperature  is currently OFF. Double tap to change.')]")
    WARNING_OFF = (By.XPATH, "//*[contains(@content-desc,'Email me warnings  is currently OFF. Double tap to change')]")
    WARNING_ON = (By.XPATH, "//*[contains(@content-desc,'Email me warnings  is currently ON. Double tap to change')]")
    SAVE_BUTTON = (By.ID, 'Save')
    CANCEL_HEATING_NOTIFICATION = (By.ID, 'negativeBtn')
    HEATING_NOTI_TITLE = (By.XPATH, "//*[contains(@content-desc,'Notifications')]")
    # TARGET_TEMPERATURE_SCROLL_HN=(By.ID, 'tab_outer_circle')
    TARGET_TEMPERATURE_SCROLL_MIN = (
        By.XPATH, "//android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]/android.widget.TextView[1]")
    TARGET_TEMPERATURE_SCROLL_MAX = (
        By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.TextView[1]")
    NOTIFY_TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[contains(@content-desc,'Maximum temperature Notification')]")
    EVENT_TARGET_TEMPERATURE_SCROLL = (By.ID, 'tempControlView')
    HIGH_TEMP_ICON = (
        By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.TextView[3]")
    LOW_TEMP_ICON = (
        By.XPATH, "//android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]/android.widget.TextView[3]")


class LightBulbLocators(object):
    LIGHT_ON_DB_HONEYCOMBE_VIEW = (By.XPATH, "//*[@text='v']")
    LIGHT_OFF_DB_HONEYCOMBE_VIEW = (By.XPATH, "//*[@text='u']")

    COLOUR_BULB_TONE_RING = (By.ID, 'light_status_text')
    COLOUR_BULB_COLOUR_RING = (By.ID, 'light_colour')
    RING_SWITCHER = (By.ID, 'ring_tone_switcher')
    COLOUR_BULB_DIMMER_RING = (By.ID, 'light_dimmer')
    COLOUR_BULB_TONE_BUTTON = (By.ID, 'ringToneSwitcher')
    COLOUR_BULB_COLOUR_BUTTON = (By.ID, 'ring_colour_switcher')
    COLOUR_BULB_DIMMER_BUTTON = (By.ID, 'ring_dimmer_switcher')

    WHITE_BULB_DIMMER_RING = (By.ID, 'light_dimmer')

    TUNEABLE_BULB_DIMMER_RING = (By.ID, 'light_dimmer')
    TUNEABLE_BULB_TONE_RING = (By.ID, 'light_tone')
    TUNEABLE_BULB_TONE_BUTTON = (By.ID, 'ringSwitcher')
    TUNEABLE_BULB_DIMMER_BUTTON = (By.ID, 'ringSwitcher')

    WARM_DIMMER_CURRENT_VALUE = (By.ID, 'light_status_text')
    TUNEABLE_DIMMER_CURRENT_VALUE = (By.ID, 'light_status_text')
    TUNEABLE_TONE_CURRENT_VALUE = (By.ID, 'light_status_text')
    COLOUR_DIMMER_CURRENT_VALUE = (By.ID, 'light_status_text')
    COLOUR_TONE_CURRENT_VALUE = (By.ID, 'light_status_text')
    COLOUR_COLOUR_CURRENT_VALUE = (By.ID, 'light_toggle_outline')
    MODE_TEXT = (By.ID, 'button_mode_status')
    MODE_RIGHT_ARROW = (By.ID, 'button_mode_right')

    SCHEDULE_TAB_ICON = (By.XPATH, "//*[contains(@content-desc,'Schedule tab')]")


class ActionsScreenLocators(object):
    ALL_RECIPES_SCREEN_HEADER = (By.XPATH, "//*[contains(@content-desc,'Actions screen')]")
    RECIPE_SCREEN_HEADER = (
        By.XPATH, "//*[contains(@label,'Here you can set up your actions to make your home work for you')]")
    ALL_CURRENT_RECIPES = (By.ID, "rules_list")
    ADD_A_NEW_RECIPE_PLUS_BUTTON = (By.ID, "recipes_plus_sign")
    ADD_A_NEW_RECIPE_BUTTON = (By.XPATH, "//*[contains(@content-desc,'Add a new action')]")
    NO_RECIPES_PRESENT = (By.XPATH, "//*[contains(@text,'You currently have no actions set up')]")

    ACTIONS_SCREEN_HEADER = (By.XPATH, "//*[contains(@text,'My Actions')]")
    DISCOVERY_FAB = (By.ID, "fab_open")
    DISCOVERY_DESCRIPTION = (By.XPATH,
                             "//*[contains(@text,'Discover new ways your Hive devices combine to help you make your home work around you.']")
    NO_ACTIONS_DESCRIPTION = (
        By.XPATH,
        "//*[contains(@text,'You currently have no actions setup.Tap the discover to set up your first action.']")
    DISCOVERY_TITLE = (By.NAME, 'Discover actions')
    DISCOVERY_BACK_BUTTON = (By.ID, 'up_button')
    DISCOVERY_WELCOME_HOME_BANNER = (By.ID, 'welcome_home_banner')
    DISCOVERY_CATEGORY_TITLE = (By.XPATH, "//*[contains(@text,'Browse by category']")
    DISCOVERY_COMFORT_ICON = (By.NAME, 'Comfort')
    DISCOVERY_REASSURANCE_ICON = (By.NAME, 'Reassurance')
    DISCOVERY_EFFICIENCY_ICON = (By.NAME, 'Efficiency')

    DISCOVERY_DEVICE_TITLE = (By.NAME, 'Browse by device')
    DISCOVERY_THERMOSTAT_ICON = (By.NAME, 'Thermostat')
    DISCOVERY_PLUGS_ICON = (By.NAME, 'Plugs')
    DISCOVERY_LIGHTS_ICON = (By.NAME, 'Lights')
    DISCOVERY_MOTION_SENSOR_ICON = (By.NAME, 'Motion Sensor')
    DISCOVERY_DOOR_SENSOR_ICON = (By.NAME, 'Win/Door Sensor')
    DISCOVERY_HOT_WATER_SENSOR_ICON = (By.NAME, 'Hot Water')

    DISCOVERY_ALL_ACTIONS_ICON = (By.NAME, 'Show All Actions')
    DISCOVERY_BUILD_YOUR_OWN_ICON = (By.NAME, 'Build Your Own')

    CATEGORY_PAGE_TITLE = 'categoryName'
    CATEGORY_TEMPLATE_NAME = 'templateName'

    TEMPLATE_PREVIEW_TITLE = (By.NAME, 'Preview')
    TEMPLATE_NAME_ON_PREVIEW_PAGE = (By.ID, 'template_header_title')
    CONTINUE_BUTTON__ON_PREVIEW_PAGE = (By.ID, 'button_continue')
    TEMPLATE_DESCRIPTION__ON_PREVIEW_PAGE = (By.ID, 'template_description')
    TEMPLATE_DEVICE_HEADER__ON_PREVIEW_PAGE = (By.ID, 'template_devices_header')

    PERSONALISE_PREVIEW_TITLE = (By.NAME, 'Preview')

    DEVICE_LIST = (By.XPATH, "//android.support.v7.widget.RecyclerView[@index =5]")
    DEVICE_FIRST_ELEMENT = (
        By.XPATH, "//android.support.v7.widget.RecyclerView[@index =5]/android.widget.FrameLayout[@index=0]")
    DEVICE_FOURTH_ELEMENT = (
        By.XPATH, "//android.support.v7.widget.RecyclerView[@index =5]/android.widget.FrameLayout[@index=3]")

    TEMPLATE_ONE = "//android.view.ViewGroup[@index = ONE]"
    TEMPLATE_FOUR = "//android.view.ViewGroup[@index = FOUR]"

    # Recipes on All Recipes page locators
    MS_NOTIFY_RECIPE = "//*[contains(@content-desc,'Notify me when sensorname detects motion')]"
    CSO_NOTIFY_RECIPE = "//*[contains(@content-desc,'Notify me when sensorname is opened')]"
    CSC_NOTIFY_RECIPE = "//*[contains(@content-desc,'Notify me when sensorname is closed')]"

    DEVICE_TURN_MS_RECIPE = "//*[contains(@content-desc,'Turn devicename devicestate when sensor detects motion')]"
    DEVICE_TURN_CSO_RECIPE = "//*[contains(@content-desc,'Turn devicename devicestate when sensor is opened')]"
    DEVICE_TURN_CSC_RECIPE = "//*[contains(@content-desc,'Turn devicename devicestate when sensor is closed')]"

    ARROW_RECIPE_LIST = (By.ID, 'arrow_right')
    ARROW_RECIPE_TEMPLATES = (By.ID, 'arrow_right')
    FIRST_ELEMENT = (By.XPATH, "//android.widget.ListView/android.widget.RelativeLayout[@index= '0']")
    FOURTH_ELEMENT = (By.XPATH, "//android.widget.ListView/android.widget.RelativeLayout[@index= '3']")
    FIFTH_ELEMENT = (By.XPATH, "//android.widget.ListView/android.widget.RelativeLayout[@index= '4']")
    SIXTH_ELEMENT = (By.XPATH, "//android.widget.ListView/android.widget.RelativeLayout[@index= '5']")

    # Edit Recipe page locators

    RECIPE_TEXT_ON_EDIT_PAGE = (By.ID, 'rules_schedule_label')
    RECIPE_DELETE_BUTTON = (By.XPATH, "//*[contains(@content-desc,'Delete')]")
    REMOVE_RECIPE_POP_UP = (By.XPATH, "//*[contains(@content-desc,'Remove this action?']")
    REMOVE_BUTTON_POP_UP = (By.ID, 'positiveBtn')

    CANCEL_BUTTON_POP_UP = (By.XPATH, "//*[contains(@text,'Cancel']")

    EDIT_RECIPE_DOOR_ICON = (By.XPATH, "//*[contains(@content-desc,'Win/Door Sensor']")
    EDIT_RECIPE_MOTION_ICON = (By.XPATH, "//*[contains(@content-desc,'Motion Sensor']")
    EDIT_RECIPE_PLUG_ICON = (By.XPATH, "//*[contains(@content-desc,'Plug']")
    EDIT_RECIPE_DOOR_ICON = (By.XPATH, "//*[contains(@content-desc,'Win/Door Sensor']")

    CANCEL_BUTTON = (By.XPATH, "//*[@label='Cancel']")

    REMOVE_POPUP = (By.XPATH, "//*[@label='Remove']")

    MENU_BUTTON = (By.NAME, 'Close menu')
    NOTIFICATION_RECIPE = (By.XPATH, "//*[contains(@label,'Notify me')]")
    TYPE_OF_NOTIFICATION = (By.XPATH, "//*[contains(@label,'Notify me By')]")
    THEN_EXIST = (By.XPATH, "//*[contains(@label,'By')]")
    THEN_NOTIFICATION = (By.XPATH, "//*[contains(@label,'Notify me by')]")
    THEN_DONE = (By.XPATH, "//*[@label='Done']")
    SAVE_BUTTON = (By.NAME, 'Save')

    # Recipe Template locators
    RECIPE_TEMPLATE = "//android.widget.ListView/android.widget.RelativeLayout[@index= 'indexvalue']/android.widget.TextView[@index= '0']"
    MS_NOT_RECIPE = (By.XPATH, "//*[contains(@text,'Notify me when motion is detected')]")
    CSO_NOT_RECIPE = (By.XPATH, "//*[contains(@text,'Notify me when a window or door sensor is opened')]")
    CSC_NOT_RECIPE = (By.XPATH, "//*[contains(@text,'Notify me when a window or door sensor is closed')]")
    MS_PL_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a plug ON or OFF when motion is detected')]")
    CSO_PL_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a plug ON or OFF when a window or door sensor is opened')]")
    CSC_PL_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a plug ON or OFF when a window or door sensor is closed')]")
    MS_BU_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a light ON or OFF when motion is detected')]")
    CSO_BU_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a light ON or OFF when a window or door sensor is opened')]")
    CSC_BU_RECIPE = (By.XPATH, "//*[contains(@text,'Turn a light ON or OFF when a window or door sensor is closed')]")
    MS_HEAT_RECIPE = (By.XPATH, "//*[contains(@text,'Set heating when motion is detected')]")
    CSO_HEAT_RECIPE = (By.XPATH, "//*[contains(@text,'Set heating when a window or door sensor is opened')]")
    CSC_HEAT_RECIPE = (By.XPATH, "//*[contains(@text,'Set heating when a window or door sensor is opened')]")

    # Add a new Recipe page locators
    NOTIFY_WHEN_PICKER = (By.ID, 'recipe_when_container')
    MULTI_WHEN_PICKER = (By.ID, 'rule_schedule_when_device_name')
    WHEN_CHOOSE_DEVICE = "//*[contains(@text,'device')]"
    WHEN_OK_BUTTON = (By.XPATH, "//*[contains(@text,'OK')]")
    OK_BUTTON = (By.XPATH, "//*[contains(@text,'OK')]")
    NOTIFY_THEN_PICKER = (By.ID, 'recipe_then_container')
    THEN_PUSH_BUTTON = (
        By.XPATH, "//android.widget.ListView[1]/android.widget.LinearLayout[1]/android.widget.Switch[1]")
    THEN_EMAIL_BUTTON = (
        By.XPATH, "//android.widget.ListView[1]/android.widget.LinearLayout[2]/android.widget.Switch[1]")
    THEN_TEXT_BUTTON = (
        By.XPATH, "//android.widget.ListView[1]/android.widget.LinearLayout[3]/android.widget.Switch[1]")
    THEN_BACK_BUTTON = (By.XPATH, "//*[contains(@content-desc,'Navigate back button')]")
    SAVE_BUTTON = (By.XPATH, "//*[contains(@text,'Save')]")
    MULTI_THEN_PICKER = (By.ID, 'rule_schedule_then_device_name')
    THEN_SCREEN_DEVICE_NAME_PRESELECTED = (By.ID, 'recipe_then_screen_device_name')
    THEN_SCREEN_DEVICE_NAME = (By.ID, 'recipe_then_variable_value1')
    THEN_SCREEN_DEVICE_NAME_VALUE = "//*[contains(@text,'value')]"
    THEN_SCREEN_DEVICE_STATE = (By.ID, 'recipe_then_variable_value2')
    THEN_SCREEN_DEVICE_STATE_VALUE = "//*[contains(@text,'value')]"
    THEN_SCREEN_DEVICE_DURATION = (By.ID, 'recipe_then_variable_value3')
    THEN_SCREEN_DEVICE_DURATION_VALUE = "//*[contains(@text,'value')]"

    # Recipe tab on Device Control page
    RECIPES_TAB = (By.XPATH, "//*[contains(@content-desc,'Actions tab')]")


class HoneycombDashboardLocators(object):
    PREVIEW_HONEYCOMB_SUBTITLE_TEXTVIEW = (By.ID, 'sub_title_text')
    PREVIEW_HONEYCOMB_TITLETEXT_TEXTVIEW = (By.ID, 'title_text')
    PREVIEW_HONEYCOMB_MAINTEXT_TEXTVIEW = (By.ID, 'main_text')
    PREVIEW_HONEYCOMB_GETSTARTED_BUTTON = (By.ID, 'btnGetStarted')
    DASHBOARD_ICON_FRAME_LAYOUT = (By.ID, 'DEVICENAME')
    DASHBOARD_ICON = (By.ID, 'deviceSlot1')
    REFRESH_BUTTON_V6 = (By.ID, 'refresh_button')
    SCROLL_VIEW = (By.ID, 'dbPageIndicator')
    HONEYCOMB_ICON_BUTTON = (By.ID, 'dashboardHomeButton')
    HONEYCOMB_TITLE_VIEW = (By.ID, 'title')
    HONEYCOMB_SUBBARTITLE_VIEW = (By.ID, 'topBarSubtitle')
    DEVICELIST_NAME_VIEW = (By.XPATH, "//android.widget.ListView[1]/android.widget.LinearLayout[DEVICEINDEX]")
    DEVICELIST_NAMEICON_VIEW = (By.XPATH, "//android.widget.ListView[1]/android.widget.LinearLayout[1]")
    CONTROL_TEXTVIEW = (By.XPATH, "//*[@text='Control']")
    MENU_ITEMS_VIEW = (By.ID, 'full_product_menu_button_show')
    MENU_ITEMS_TEXTVIEW = (By.XPATH, "//*[@text='MENUITEMNAME']")
    PLUG_ICON_VIEW = (By.XPATH, "//*[contains(@content-desc,'Plug')]")
    HONEYCOMB_ICON = (
        By.XPATH, "//android.widget.LinearLayout[1]/android.widget.TextView[1][contains(@text,'DEVICENAME')]")
    DASHBOARD_LEFT_ICON = (By.ID, 'deviceSlot1')
    DASHBOARD_RIGHT_ICON = (By.ID, 'deviceSlot3')
    DASHBOARD_ICON_SLOT = (By.ID, 'deviceSlot')
    DASHBOARD_MOVERIGHT_SCREEN = (By.ID, 'fl_move_to_right_screen')
    DASHBOARD_MOVELEFT_SCREEN = (By.ID, 'fl_move_to_left_screen')


class PlugScheduleLocators(object):
    PLUG_SCHEDULE_ICON = (By.XPATH, "//android.widget.HorizontalScrollView[1]/android.widget.LinearLayout[1]/"
                                    "android.widget.LinearLayout[2]")
    PLUG_ADD_ICON = (By.ID, 'schedule_fab')
    PLUG_RESETSCHE_TEXTVIEW = (By.ID, 'resetScheduleText')
    PLUG_ADDTIMESLOT_TEXTVIEW = (By.ID, 'addTimeSlotText')
    PLUG_NEWTIMESLOT_TEXTVIEW = (By.ID, 'add_schedule_day')
    PLUG_ADDTSCHEDULESTARTTIME_VIEW = (By.ID, 'add_schedule_time_start')
    PLUG_ADDSCHEDULEENDTIME_VIEW = (By.ID, 'add_schedule_time_end')
    PLUG_COPYSCHE_TEXTVIEW = (By.ID, 'copyScheduleText')
    REFRESH_BUTTON_V6 = (By.ID, 'refresh_button')
    HONEYCOMB_ICON_BUTTON = (By.ID, 'dashboardHomeButton')
    PLUG_RESETOK_BUTTON = (By.ID, 'positiveBtn')
    PLUG_COPYSCHEDAY_LAYOUT = (By.ID, 'COPYSCHEDAY')
    PLUG_SAVEOK_BUTTON = (By.ID, 'positiveBtn')
    PLUG_SELECTEDDAYTICK_VIEW = (By.ID, 'textViewTick')
    PLUG_SELECTINGDAYTICK_VIEW = (By.XPATH, "//android.widget.RelativeLayout[INDEX]/"
                                            "android.widget.RelativeLayout[1]/android.widget.TextView[2]")
    PLUG_TIMESLOTOPTION_ICON = (By.XPATH, "//android.widget.RelativeLayout[INDEX]/android.view.ViewGroup[1]/"
                                          "android.support.v7.widget.LinearLayoutCompat[1]/android.widget.ImageView[1]")
    PLUG_DELETETIMESLOT_ICON = (
        By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.TextView[1][@text = 'Delete']")
    PLUG_EDITTIMESLOT_ICON = (By.XPATH, "//android.widget.RelativeLayout[1]/android.widget.TextView[1]"
                                        "[@text = 'Edit time slot']")
    PLUG_ACTIVEPLUGSTATUS_TEXTVIEW = (
        By.XPATH, "//android.widget.LinearLayout[1]/android.widget.TextView[1][@text = 'Active Plug status']")
    PLUG_SCHEDULESTATUS_BUTTON = (By.ID, 'edit_schedule_item_active_plug_toggle_button')
    PLUG_SCHEDULEHOURPICKER_LAYOUT = (
        By.XPATH, '//android.widget.LinearLayout[1]/android.widget.EditText[1]''[@id = numberpicker_input]')
    PLUG_SCHEDULEMINUTEPICKER_LAYOUT = (By.XPATH, '//android.widget.LinearLayout[2]/android.widget.EditText[1]'
                                                  '[@id = numberpicker_input]')
    PLUG_STARTTIME_BUTTON = (By.ID, 'startTime')
    PLUG_ENDTIME_BUTTON = (By.ID, 'endTime')
    PLUG_EDITTITLE_VIEW = (By.ID, 'title_text')
    PLUG_EDITSCHEDULE_VIEW = (By.ID, 'edit_schedule_day')
    PLUG_EDITSCHEDULESTARTTIME_VIEW = (By.ID, 'edit_schedule_time_start')
    PLUG_EDITSCHEDULEENDTIME_VIEW = (By.ID, 'edit_schedule_time_end')
    PLUG_CANCEL_BUTTON = (By.ID, 'negativeBtn')
    PLUG_DAY_ICON = (By.ID, 'SCHEDULEDAY')
    PLUG_SCHEDULETEXTSTATUS_ICON = (By.XPATH, "//android.widget.RelativeLayout[INDEX]/"
                                              "android.widget.LinearLayout[1]/android.widget.TextView[2]")
    PLUG_SCHEDULEICONSTATUS_ICON = (By.XPATH, "//android.widget.RelativeLayout[INDEX]/"
                                              "android.widget.LinearLayout[1]/android.widget.TextView[1]")
    PLUG_FROMTIME_TEXTVIEW = (
        By.XPATH, "//android.widget.ListView[1]/android.widget.RelativeLayout[INDEX]/android.widget.TextView[1]")
    PLUG_TOTIME_TEXTVIEW = (
        By.XPATH, "//android.widget.ListView[1]/android.widget.RelativeLayout[INDEX]/android.widget.TextView[2]")

    PLUG_MODE_VIEW = (By.ID, 'button_mode_status')
    PLUG_MODECHANGE_ICON = (By.ID, 'button_mode_right')


class DashboardCustomizationLocators(object):
    DASHBOARDCUSTOMIZATION_ADD_BUTTON = (By.ID, 'fab')
    DASHBOARDCUSTOMIZATION_EDIT_CANCEL_BUTTON = (By.ID, 'tv_dashboard_edit_mode_cancel')
    DASHBOARDCUSTOMIZATION_EDIT_SAVE_BUTTON = (By.ID, 'tv_dashboard_edit_mode_apply')
    DASHBOARDCUSTOMIZATION_EDIT_TITLE = (By.ID, 'title')
    DASHBOARDCUSTOMIZATION_DEVICE_ADDSCREEN = (By.ID, 'navigation_view')
    DASHBOARDCUSTOMIZATION_FILLEDSLOTS = (By.ID, 'dbFilledCircleBkg')
    DASHBOARDCUSTOMIZATION_LISTVIEW_LAYOUT = (By.ID, 'navigation_view')
    DASHBOARDCUSTOMIZATION_LISTVIEW_DEVICES = (By.ID, 'navigation_view_list')
    # DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON = "//android.widget.FrameLayout[1]/android.widget.FrameLayout[1][contains(@content-desc, 'deviceName')]/../following-sibling::android.widget.ImageView[1]"
    DASHBOARDCUSTOMIZATION_EDIT_DELETE_ICON = (By.ID, "delete_device_area")
    DASHBOARDCUSTOMIZATION_DEVICE_IN_LISTVIEW = "//*[@text='deviceName']"
    DASHBOARDCUSTOMIZATION_ADD_DEVICE_POPUP = (By.ID, "positiveBtn")


class ContactSensorLocators(object):
    CONTACTSENSOR_CONTROL_STATUS = (By.ID, 'status')
    CONTACTSENSOR_LOGS_BUTTON = (By.ID, 'logButton')
    CONTACTSENSOR_DAY_SELECT = (By.XPATH, '//android.widget.FrameLayout[DEVICEINDEX]/android.widget.CheckedTextView[1]')
    CONTACTSENSOR_EVENT_INFO = (By.ID, 'eventInfo')
    CONTACTSENSOR_CLOSEEVENT_LOGS = (By.ID, 'full_product_menu_button_close')


class NAThermostatLocators(object):
    THERMOSTAT_SETTINGS_ICON = (By.ID, 'setting_button')
    THERMOSTAT_MODE_DUAL_ICON = (By.ID, 'dual')
    THERMOSTAT_MODE_HEAT_ICON = (By.ID, 'heat')
    THERMOSTAT_MODE_COOL_ICON = (By.ID, 'cool')
    THERMOSTAT_MODE_OFF_ICON = (By.ID, 'off')
    THERMOSTAT_MODE_HOLD_ICON = (By.ID, 'operating_mode_hold')
    THERMOSTAT_MODE_SCHEDULE_ICON = (By.ID, 'operating_mode_schedule')
    THERMOSTAT_SETTINGS_TITLE = (By.XPATH, "//*[@text='Settings']")
    THERMOSTAT_NAME = (By.XPATH, "//*[@text='ThermostatName']")
    THERMOSTAT_ICON_PROPERTY = (By.XPATH, "//*[contains(@content-desc,'ThermostatName')]")
    THERMOSTAT_CONTROL = (By.ID, 'tempPickerLayout')
    THERMOSTAT_CONTROL_SECONDARY = (By.ID, 'tempPicker2Layout')
    THERMOSTAT_HEATINGCOOLING = (By.ID, 'heatingOrCoolingIndicationPane')
    THERMOSTAT_FLAMEICON = (By.ID, 'heatingIndicationIcon')
    THERMOSTAT_FLAKEICON = (By.ID, 'coolingIndicationIcon')
    THERMOSTAT_SCHEDULE_MODE_ICON = (By.ID, 'tab_schedule_text_1')
    THERMOSTAT_SCHEDULE_MODE_SLOT_ICON = (By.ID, 'tab_schedule_text_2')
    THERMOSTAT_MANUAL_MODE_ICON = (By.ID, 'holdMessaging')
    THERMOSTAT_OFF_MODE_ICON = (By.ID, 'off_icon')
    THERMOSTAT_TAB_TITLE = (By.ID, 'new_tab_title')
    THERMOSTAT_TEMP_PICKER = (By.ID, 'heat_temp_picker')
    THERMOSTAT_TEMP_VALUE = (By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.TextView[2]")
    THERMOSTAT_TEMP_SET_VALUE = (By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.TextView[3]")
    THERMOSTAT_COOLWHEEL_LAYOUT = (By.ID, 'cooling_wheel_layout')
    THERMOSTAT_HEATWHEEL_LAYOUT = (By.ID, 'heating_wheel_layout')
    THERMOSTAT_STARTTIME_BUTTON = (By.ID, 'startTime')
    NA_FANSETTINGS = (By.ID, "na_settings_fan")
    NA_FANSETTINGS_CIRCULATEDURATION = (By.ID, "na_settings_fan_duration")
    NA_HUMIDITY_SEEKBAR = (By.ID, "seekBar")
    NA_FAN_ALWAYSON_TEXT = (By.ID, "na_settings_fan_always_on_status_text")
    NA_FAN_AUTO_TEXT = (By.ID, "na_settings_fan_auto_status_text")
    NA_FAN_CIRCULATE_TEXT = (By.ID, "na_settings_fan_circulate_status_text")
    NA_FAN_AUTO = (By.ID, "na_settings_fan_auto")
    NA_FAN_CIRCULATE = (By.ID, "na_settings_fan_circulate")
    NA_FAN_CIRCULATE_LOW = (By.ID, "na_settings_fan_duration_low")
    NA_FAN_CIRCULATE_MEDIUM = (By.ID, "na_settings_fan_duration_medium")
    NA_FAN_CIRCULATE_HIGH = (By.ID, "na_settings_fan_duration_high")
    NA_FAN_ALWAYSON = (By.ID, "na_settings_fan_always_on")


class LeakSensorLocators(object):
    HLS_STATUS = (By.ID, 'leak_sensor_status_text')
    HLS_BATTERYSTATUS = (By.ID, 'leak_sensor_battery_icon')
    HLS_SETTINGS_ICON = (By.ID, 'leak_sensor_settings_button')
    HLS_DETAIL_STATUS_TEXT = (By.ID, 'leak_sensor_status_detail_body')
    # High Flow Locators
    HLS_HIGHFLOW_TEXT = (By.ID, 'leak_sensor_control_guide_high_flow_body_text')
    HLS_WATERUSAGE_YES_BUTTON = (By.ID, 'leak_sensor_control_guide_high_flow_yes_button')
    HLS_WATERUSAGE_NO_BUTTON = (By.ID, 'leak_sensor_control_guide_high_flow_no_button')
    # TroubleShoot
    HLS_TROUBLESHOOT_YES_BUTTON = (By.ID, 'leak_sensor_troubleshooting_flow_yes_button')
    HLS_TROUBLESHOOT_NO_BUTTON = (By.ID, 'leak_sensor_troubleshooting_flow_no_button')
    HLS_TROUBLESHOOT_REMIND_TEXT = (By.ID, 'leak_sensor_troubleshooting_flow_remind_text')
    HLS_FIX_DIALOG_YES_BUTTON = (By.ID, 'leak_sensor_troubleshooting_flow_dialog_yes_button')
    HLS_FIX_DIALOG_NO_BUTTON = (By.ID, 'leak_sensor_troubleshooting_flow_dialog_no_button')
    HLS_CALL_SUPPORT_ICON = (By.ID, 'leak_sensor_help_call_icon')
    HLS_CALL_SUPPORT_TEXT = (By.ID, 'leak_sensor_help_title_text')
    # Small flow Locators
    HLS_LOWFLOW_OK_BUTTON = (By.ID, 'leak_sensor_control_guide_low_flow_ok_button')
    # Calibration
    HLS_FIX_HEADER = (By.XPATH, "//*[@text = 'Thanks for fixing']")
    HLS_FIX_BODY = (By.XPATH, "//*[@text = 'Your Leak Sensor needs some time to learn about your water, "
                              "this can take up to 24 hours. We'll let you know if anything changes.']")
    HLS_FIX_TIP = (By.XPATH, "//*[@text = 'Tip: The Leak Sensor will learn faster if less "
                             "water is used during this time.']")
    HLS_PROGRESS_BAR = (By.XPATH, "//android.widget.ProgressBar[1]")
    # Settings Locators
    HLS_TITLE = (By.ID, 'title')
    HLS_LEAK_WIFI_LAYOUT = (By.ID, 'leak_wifi')
    HLS_LEAK_NOTIFICATIONS_LAYOUT = (By.ID, 'leak_alert_notifications')
    HLS_LEAK_FLOWALERT_LAYOUT = (By.ID, 'leak_flow_alert')
    HLS_LEAK_DEVICE_ID_TEXT = (By.ID, 'leak_sensor_device_id')
    HLS_FIRMWARE_TEXT = (By.ID, 'leak_sensor_firmware_version')
    HLS_HELP_TEXT = (By.ID, 'need_help')
    HLS_BACK_ICON = (By.ID, 'backBtn')
    # Alert Notifications screen
    HLS_PUSH_CHECK = (By.ID, 'cbPush')
    HLS_EMAIL_CHECK = (By.ID, 'cbEmail')
    HLS_TEXT_CHECK = (By.ID, 'cbText')
    HLS_SAVE = (By.ID, 'save')
    # Large Flow Alert
    HLS_LEAK_TIME = (By.ID, 'leak_time')
    HLS_FLOW_SCROLL = (By.ID, 'flowTimeIntervalList')
    HLS_NUMBER_INPUT = (By.ID, 'numberpicker_input')
    HLS_SET_BUTTON = (By.ID, 'positiveBtn')
    HLS_CANCEL_BUTTON = (By.ID, 'negativeBtn')
    HLS_ALERT_SURE_TEXT = (By.XPATH, "//*[text='This means that you could have a burst pipe or a tap fully running"
                                     " and we will only notify you after the time you have now selected.]")
    # leak icon
    HLS_LEAK_ICON = (By.XPATH, "//*[contains(@content-desc,'LEAK_SENSOR')]")
    HLS_DEVICELIST_STATUS = (By.XPATH,
                             '//android.widget.LinearLayout[index]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[2]')

    # Leak Notifications
    HLS_NOTIFICATIONS = (By.ID, 'android:id/title')
    HLS_ANDROID_STATUSBAR = (By.ID, 'android:id/statusBarBackground')
    HLS_CLEARTEXT = (By.ID, 'com.android.systemui:id/dismiss_text')
    HLS_CONTENT_TEXT = (By.ID, 'android:id/big_text')

    HLS_MAINCOLUMN = (By.ID, 'notification_main_column')

    # Banner
    HLS_BANNER_TEXT = (By.ID, 'textView2')
    HLS_BANNER_LOW = (By.ID, 'text_low_flow')
    HLS_BANNER_HIGH = (By.ID, 'text_high_flow')
    HLS_LOW_REMINDLATER_BUTTON = (By.ID, 'leak_sensor_control_guide_low_flow_remind_button')
    HLS_LOW_YES_BUTTON = (By.ID, 'leak_sensor_control_guide_low_flow_yes_button')
    HLS_HIGH_NO_BUTTON = (By.ID, 'leak_sensor_control_guide_high_flow_no_button')
    HLS_HIGH_YES_BUTTON = (By.ID, 'leak_sensor_control_guide_high_flow_yes_button')

    # Troubleshooting screen
    HLS_TS_QUESTIONS = (By.ID, 'troubleshooting_question')
    HLS_BUTTON_CONTAINERS = (By.ID, 'troubleshooting_button_container')
    HLS_CLOSE_BUTTON = (By.ID, 'hive_toolbar_button_close')

    # Call a Plumber
    HLS_DONE_BUTTON = (By.ID, 'hive_toolbar_button_done')
    HLS_CALL_EXPERT_TITLE = (By.ID, 'hive_toolbar_text_view_title')


class MimicLocators(object):
    MMC_DEVICE = (By.ID, 'deviceSlot6')
    MMC_ICON = (By.ID, 'light_switcher_mimic')
    MMC_CONTROL = (By.XPATH, "//*[contains(@content-desc,'Control tab')]")
    MMC_POSIIVE = (By.ID, 'positiveBtn')
    MMC_NEGATIVE = (By.ID, 'negativeBtn')
    MMC_STOP_BUTTON = (By.ID, 'button_stop_mimic')
    MMS_START_BUTTON = (By.ID, 'mimic_start_button')
    MMC_SELECTEDDEVICES_BUTTON = (By.ID, 'button_selected_devices')
    MMC_SELECTEDDEVICES_TEXT = (By.ID, 'selected_devices_text')
    MMC_SELECTEDHOURS_BUTTON = (By.ID, 'button_selected_hours')
    MMS_SELECTEDHOURS_TEXT = (By.ID, 'selected_hours_text')
    MMC_ANIMATION = (By.ID, 'mimic_animation')
    MMC_SETUP = (By.ID, 'setup_mimic')
    MMC_LIGHTSTATUS_ICON = (By.ID, 'light_status_icon')  # v
    MMC_LIGHTSTATUS_TITLE = (By.ID, 'light_status_title')  # Mimic active
    MMC_LIGHTSTATUS_SUBTITLE = (By.ID, 'light_status_subtitle')  # Bulb on
    MMC_BACK_BUTTON = (By.ID, 'back_button')
    MMC_SELECT_TITLE = (By.XPATH, "//*[contains(@text,'Select lights')]")
    MMC_SAVE_BUTTON = (By.ID, 'next_save_button')
    MMC_LIGHTS_LAYOUTS = (By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout")
    MMC_LIGHTS_NAME = (By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[index]"
                                 "/android.widget.TextView[1]")
    MMC_LIGHTS_CHECKBOX = (By.XPATH, "//android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[index]"
                                     "/android.widget.CheckBox[1]")
    MMC_TIMES_TITLE = (By.XPATH, "//*[contains(@text,'Set times')]")
    MMC_STARTTIME_BUTTON = (By.ID, 'radio_start_time')
    MMC_ENDTIME_BUTTON = (By.ID, 'radio_end_time')
    MMC_HOUR_SCROLL = (By.ID, 'hour')
    MMC_MINUTE_SCROLL = (By.ID, 'minute')
    MMC_NEXTDAY_TEXT = (By.ID, 'text_next_day')
    MMC_STARTTIME_TEXT = (By.ID, 'text_start_time')
    MMC_ENDTIME_TEXT = (By.ID, 'text_end_time')
    MMC_TITLE = (By.ID, 'title')
    LIGHT_STATUS_TEXT = (By.ID, 'light_status_text')
    LIGHT_OFFLINE = (By.ID, 'node_offline_title')
    LIGHT_MODE_VIEW = (By.ID, 'button_mode_status')
    LIGHT_MODECHANGE_ICON = (By.ID, 'button_mode_right')
