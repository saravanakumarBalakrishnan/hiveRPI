"""
Created on 17 Jun 2015

@author: ranganathan.veluswamy
"""

from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    # TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']" )
    TITLE_LABEL = (By.XPATH, ".//*[@class='forms']")
    USERNAME_EDTBOX = (By.ID, 'username')
    PASSWORD_EDTBOX = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, "//*[@type='submit']")
    FORGOTTEN_PASSWORD_LINK = (By.PARTIAL_LINK_TEXT, 'Forgot your password')


class LoginPageLocatorsV3(object):
    TITLE_LABEL = (By.XPATH, '//*[@class="forms"]')
    USERNAME_EDTBOX = (By.ID, 'username')
    PASSWORD_EDTBOX = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, "//*[@type='submit']")
    FORGOTTEN_PASSWORD_LINK = (By.PARTIAL_LINK_TEXT, 'Forgot your password')
    COOKIES_CLOSE_LINK = (By.XPATH, '//*[@class="button-close"]')


class MainMenuLocatorsV3(object):
    SETTINGS_MENU = (By.XPATH, '//*[@class="cldByS kbLQue"]')
    MANAGE_DEVICE = (By.XPATH, '//*[@class="jTruxY"]//*[@href="/devices"]')


class PageHeaderLocators(object):
    DATE_TIME = (By.XPATH, '//*[@class="datetime"]')
    USERNAME_DISPLAY = (By.XPATH, "//*[@ng-if='identity.name']")


class HeatingPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']")
    MY_HIVE_LINK = (By.LINK_TEXT, 'My Hive')
    MY_HIVE_MENU = (By.XPATH, "//*[@data-icon='b']")
    MY_HIVE_LINK_UNDER_MENU = (By.XPATH, "//*[@href='/dashboard']")
    USERNAME_DISPLAY = (By.XPATH, "//*[@ng-if='identity.name']")
    HEAT_MODE_GROUP = (By.XPATH, "//*[@active-item='local.mode']")
    CURRENT_MODE_ITEM = (By.XPATH, "//*[@class='ng-binding active']")
    SCHEDULE_MODE_LINK = (By.LINK_TEXT, 'Schedule')
    MANUAL_MODE_LINK = (By.LINK_TEXT, 'Manual')
    OFF_MODE_LINK = (By.LINK_TEXT, 'Off')
    BOOST_MODE_LINK = (By.XPATH, "//*[@class='boost-on']")
    STOP_BOOST_BUTTON = (By.XPATH, "//*[@class='boost-off']")
    BOOST_TIME_LABE = (By.XPATH, "//*[@class='hours-minutes']")
    SET_BOOST_SCROLL = (By.XPATH, "//*[@data-reactid='.3.0']")
    TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[@throbber-throb-for='heating.temperature']")

    SCHEDULE_TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[@role='spinbutton']")
    SCHEDULE_TARGET_TEMPERATURE_SCROLLV6 = (By.XPATH, "//*[@ng-model='currentTemp']")
    TIME_SCALE_FIRST = (By.XPATH, "//*[@data-reactid='.0.0.0.$0']")
    TIME_SCALE_LAST = (By.XPATH, "//*[@data-reactid='.0.0.0.$24']")
    HEATING_SCHEDULE_TABLE = (By.XPATH, "//*[@data-reactid='.1.2.0.0']//*[canvas[4]]")
    HEATING_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.1.2.0.0']//*[canvas[4]]")
    SAVE_BUTTON = (By.XPATH, "//*[@ng-click='isChanged ? saveNow() : null']")
    SAVE_BUTTONV6 = (By.XPATH, "//*[@data-reactid='.1.3.1']")
    RUNNING_STATE_FLAME_ICON = (By.XPATH, "//*[@ng-show='flameOn']")


class HotWaterPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']")
    HOT_WATER_MODE_GROUP = (By.XPATH, "//*[@active-item='hotwater.mode']")

    CURRENT_MODE_ITEM = (By.XPATH, ".//*[@class='ng-binding active']")
    SCHEDULE_MODE_LINK = (By.LINK_TEXT, 'Schedule')
    MANUAL_MODE_LINK = (By.LINK_TEXT, 'On')
    OFF_MODE_LINK = (By.LINK_TEXT, 'Off')
    BOOST_MODE_LINK = (
        By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']//*[@class='boost-on']")
    STOP_BOOST_BUTTON = (
        By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']//*[@class='boost-off']")
    BOOST_TIME_LABE = (By.XPATH, "//*[@class='hours-minutes']")
    SET_BOOST_SCROLL = (By.XPATH, "//*[@data-reactid='.3.0']")
    # BOOST_MODE_LINK =  (By.LINK_TEXT, 'BOOST')
    HOT_WATER_SCHEDULE_TABLE = (By.XPATH, "//*[@data-reactid='.1.0.1']")
    HOT_WATER_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.3.2.0.0']//*[canvas[4]]")
    SAVE_BUTTON = (By.XPATH, "//*[@ng-click='isChanged ? saveNow() : null']")
    SAVE_BUTTONV6 = (By.XPATH, "//*[@data-reactid='.3.3.1']")
    HOT_WATER_SWITCH = (By.XPATH, "//*[@class='hot-water-switch']")
    HOT_WATER_MODE_MENU = (By.XPATH, "//*[@active-item='hotwater.mode']")
    HOT_WATER_SCHEDULE_GROUP = (By.XPATH, "//*[@ng-controller='HotWaterScheduleController as hotWaterScheduler']")
    HOT_WATER_CONTROLER_GROUP = (By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']")
    HOT_WATER_RUNNING_STATE = (By.XPATH, "//*[contains(@class,'hot-water-off')]")


class ActivePlugPageLocators(object):
    ACTIVE_PLUG_CONTROLER_GROUP = (By.XPATH, ".//*[@class='activeplug-control']")

    ACTIVE_PLUG_RUNNING_STATE = (By.XPATH, "//*[contains(@class,'activeplug-off')]")
    ACTIVE_PLUG_NEXT_EVENT = ["//*[@class ='next-event']"]
    ACTIVE_PLUG_SWITCH = [".//*[@class='activeplug-switch']"]
    ACTIVE_PLUG_SWITCH1 = (By.XPATH, './/*[@class="activeplug-switch"]')
    ACTIVE_PLUG_SCHEDULE = [".//*[@class='scheduled']"]
    ACTIVE_PLUG_LEFT_ARROW = (By.XPATH, './/*[@class="arrow-left"]')
    ACTIVE_PLUG_RIGHT_ARROW = (By.XPATH, './/*[@class="arrow-right"]')
    ACTIVE_PLUG_AREA_HIDDEN = ["aria-hidden"]
    ACTIVE_PLUG_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.0.2.0.0']//*[canvas[4]]")
    SAVE_BUTTONV6 = (By.XPATH, '//button[@class="save"]')


class ActivePlugPageLocators_V3(object):
    ACTIVE_PLUG_CONTROLER_GROUP_V3 = (By.XPATH, './/*[@data-qa="active-plug-base"]')
    ACTIVE_PLUG_SCHEDULE_V3 = [".//*[@data-qa='mode-selector-description']"]
    ACTIVE_PLUG_NEXT_EVENT_V3 = [".//*[@data-qa='mode-selector-description']"]
    ACTIVE_PLUG_MANUAL_MODE_V3 = (By.XPATH, './/*[@data-qa="mode-selector-manual"]')
    ACTIVE_PLUG_SCHEDULE_MODE_V3 = (By.XPATH, './/*[@data-qa="mode-selector-schedule"]')
    ACTIVE_PLUG_STATE_INDICATOR = ['.//*[@data-qa="active-plug-msg"]']
    ACTIVE_PLUG_SCHEDULE_MAIN_V3 = (By.XPATH, '//*[@data-qa="schedule-base"]')
    ACTIVE_PLUG_SCH_WEEKDAYS = '//*[@data-qa="schedule-weekday-'
    ACTIVE_PLUG_SCH_EVENTS = (By.XPATH, './/*[@data-qa="schedule-event"]')
    ACTIVE_PLUG_COOKIES_CLOSE = (By.XPATH, './/*[@class="button-close"]')
    ACTIVE_PLUG_SCH_DAY_CLOSE = ['.//*[@class ="schedule-close-day"]']
    ACTIVE_PLUG_SCH_RESET_SCHEDULE = (By.XPATH, './/*[@data-qa="schedule-reset"]')
    ACTIVE_PLUS_SCH_EVENT_SLIDER = (By.XPATH, './/*[@data-qa ="schedule-slider"]')
    ACTIVE_PLUG_SCH_TIME_FROM_SLIDER = (By.XPATH, './/*[@data-qa="schedule-time-displayed"]')
    ACTIVE_PLUG_SCH_TIME_FROM_SLIDER_PATH = ['.//*[@data-qa="schedule-time-displayed"]']
    ACTIVE_PLUG_SCH_ADD_BUTTON = (By.XPATH, './/*[@data-qa="schedule-plus"]')
    ACTIVE_PLUG_SCH_COPY_BUTTON = (By.XPATH, './/*[@data-qa="schedule-copy"]')
    ACTIVE_PLUG_SCH_DELETE_BUTTON = (By.XPATH, './/*[@data-qa="schedule-minus"]')
    ACTIVE_PLUG_SCH_SAVE_BUTTON = (By.XPATH, './/*[@data-qa="schedule-save"]')

    ACTIVE_PLUG_SCH_PLUS_BUTTONS = ['.//*[@class="sc-bYwvMP kBuujU"]']

    ACTIVE_PLUG_SCHEDULE_MAIN_V3_XPATH = [".//*[@class='sc-dRCTWM eGrexR']"]
    ACTIVE_PLUG_SCHEDULE_SVG_V3 = (By.CSS_SELECTOR, "svg")
    ACTIVE_PLUG_SCHEDULE_SVG_COMPONENTS_V3 = (By.CSS_SELECTOR, "g")
    ACTIVE_PLUG_RUNNING_STATE = (By.XPATH, "//*[contains(@class,'activeplug-off')]")
    ACTIVE_PLUG_SWITCH1 = (By.XPATH, './/*[@class="activeplug-switch"]')
    ACTIVE_PLUG_SCHEDULE = [".//*[@class='scheduled']"]
    ACTIVE_PLUG_AREA_HIDDEN = ["aria-hidden"]
    ACTIVE_PLUG_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.0.2.0.0']//*[canvas[4]]")
    SAVE_BUTTONV6 = (By.XPATH, '//button[@class="save"]')


class MotionSensorPageLocators_V3(object):
    MOTION_SENSOR_STATUS_INDICATOR = (By.XPATH, './/*[@data-qa="motion-sensor-status"]')
    MOTION_SENSOR_STATE = (By.XPATH, './/*[@data-qa="motion-sensor-msg"]')
    MOTION_SENSOR_LAST_DETECTED = ['.//*[@data-qa="motion-sensor-last-detected"]']
    MOTION_SENSOR_LAST_DETECTED_TIME = ['.//*[@data-qa="motion-sensor-last-time"]']
    MOTION_SENSOR_EVENT_LOGS_BASE = (By.XPATH, './/*[@data-qa="motion-sensor-logs-base"]')
    MOTION_SENSOR_PLUS_ZOOM_BUTTON_DISABLED = ['.//*[@class="zoom-controls__plus zoom-controls__plus--disabled"]']
    MOTION_SENSOR_PLUS_ZOOM_BUTTON = (By.XPATH, './/*[@class="zoom-controls__plus"]')
    MOTION_SENSOR_TRIGGERED = (By.XPATH, './/*[@data-qa="sensor-activity-times"]')
    MOTION_SENSOR_BUSIEST_PERIOD = (By.XPATH, './/*[@data-qa="sensor-activity-busiest"]')
    MOTION_SENSOR_DAY_CALENDAR = (By.XPATH, './/*[@data-qa="day-selector-base"]')
    MOTION_SENSOR_CALENDAR_LIST = (By.TAG_NAME, 'li')
    MOTION_SENSOR_TODAY_EVENTS = (By.XPATH, './/*[@class ="logs-timeline-component__info-wrapper"]')


class ForgottenPasswordPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@ng-controller='ForgottenPasswordController']")
    EMAIL_ADDR_FIELD = (By.XPATH, "//input[@name='email']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(.,'Submit')]")
    REMINDER_MESSAGE = (By.XPATH, "//*[@ng-bind-html='message']")
    YOPMAIL_EMAIL_ADDR_FIELD = (By.ID, "login")
    YOPMAIL_CHECK_INBOX = (By.XPATH, "//input[@title='Check inbox @yopmail.com']")
    YOPMAIL_HREF_LINK = (By.LINK_TEXT, 'here')
    PASSWORD_RESET_LABEL = (By.XPATH, "//*[@ng-controller='ResetPasswordController']")
    SUCCESS_MESSAGE = (By.XPATH, '//p[contains(.,"Your password has been updated successfully, you may now login.")]')
    NEW_PASSWORD = (By.ID, "password")
    CONFIRM_PASSWORD = (By.ID, "password2")
    LOGIN_BUTTON = (By.XPATH, '//a[@href="/login"]')
    FRAME_REF = (By.ID, "ifmail")


class HeatingDashboardLocators(object):
    SETTINGS_MENU = (By.XPATH, "//*[@data-icon='i']")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")
    NOTIFICATION_LINK = (By.XPATH, "//a[@href='/notifications']")
    MANAGE_DEVICE = (By.XPATH, "//a[@href='/devices']")


class HeatingNotificationLocators(object):
    TITLE_LABEL = (By.XPATH, '//*[@ng-controller="NotificationsController"]//h2')
    HIGH_TEMP_CHKBOX = (By.XPATH, '//input[@name="aboveActive"]')
    HIGH_TEMP_TT = (By.XPATH, '//*[@name="above"]')
    LOW_TEMP_CHKBOX = (By.XPATH, '//input[@name="belowActive"]')
    LOW_TEMP_TT = (By.XPATH, '//*[@name="below"]')
    WARNINGS_CHKBOX = (By.XPATH, '//*[@ng-model="formData.warningsEmail"]')
    SAVE_BUTTON = (By.XPATH, '//button[contains(.,"Save")]')


class DashboardLocators(object):
    DASHBOARD_CONTENT = (By.XPATH, '//*[@ng-if="products"]')
    HEATING_THUMBNAIL = (By.XPATH, '//*[@class="product heating text-center"]')
    HEATING_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product heating text-center offl"]')
    HOTWATER_THUMBNAIL = (By.XPATH, '//*[@class="product hotwater text-center"]')
    HOTWATER_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product hotwater text-center offl"]')
    ACTIVEPLUG_THUMBNAIL = (By.XPATH, '//*[@class="product activeplug text-center"]')
    ACTIVEPLUG_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product activeplug text-center offl"]')
    WARMWHITE_THUMBNAIL = (By.XPATH, '//*[@class="product activelight text-center"]')
    WARMWHITE_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product activelight text-center offl"]')
    TUNEABLE_THUMBNAIL = (By.XPATH, '//*[@class="product tuneablelight text-center"]')
    TUNEABLE_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product tuneablelight text-center offl"]')
    COLOUR_THUMBNAIL = (By.XPATH, '//*[@class="product colourlight text-center"]')
    COLOUR_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product colourlight text-center offl"]')
    ACTIVEPLUG_THUMBNAIL_V3 = (By.XPATH, "//*[@id='15c5ea04-0cf8-4e37-a80d-bd71ebf37f1e']/span/div/div[2]")
    # ACTIVEPLUG_THUMBNAIL_V3 = (By.XPATH, './/div[2]/div/div[@class="sc-bIKvTM dldcuw"]/div[2]/div[3][@data-drop-position="1:1"]/span')
    # ACTIVEPLUG_THUMBNAIL_V3 = (By.XPATH, '//div[contains(text(), "Plug 2")]')
    # ACTIVEPLUG_THUMBNAIL_V3 = (By.XPATH, ".//*[@id='15c5ea04-0cf8-4e37-a80d-bd71ebf37f1e']/span/div/div[2]/div[2]")


    ACTIVEPLUG_THUMBNAIL_OFFLINE_V3 = (
        By.XPATH, '//*[@href="/products/activeplug/0ddf5aba-7640-4f6b-89cf-17ca063087b5/ASDFASDFASD"]')


class DashboardLocatorsV3(object):
    DATE_AND_TIME = (By.XPATH, '//*[@class="sc-bXGyLb jLdnGn"]')
    DASHBOARD_CONTENT = (By.XPATH, '//*[@class="sc-ckYZGd jQaeVH"]')
    RIGHT_ARROW = (By.XPATH, '//span[.="z"]')
    DASHBOARD_VIEW_SELECTOR = (By.XPATH, '//span[.="c"]')

    @staticmethod
    def dashboard_traverse(a, b):
        DASHBOARD_CELL = (By.XPATH, '//*[@data-drop-position="' + a + ':' + b + '"]')
        return DASHBOARD_CELL


class WarmWhiteLightPageLocators(object):
    PRODUCT_NAME = (By.XPATH, '//*[@class="columns module-heading text-center"]')
    BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="activelight-brightness"]')
    DIMMER_5_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="5%"]')
    DIMMER_10_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="10%"]')
    DIMMER_20_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="20%"]')
    DIMMER_30_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="30%"]')
    DIMMER_40_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="40%"]')
    DIMMER_50_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="50%"]')
    DIMMER_60_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="60%"]')
    DIMMER_70_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="70%"]')
    DIMMER_80_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="80%"]')
    DIMMER_90_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="90%"]')
    DIMMER_100_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="100%"]')
    CENTRAL_STATUS_INDICATOR = (By.XPATH, '//*[@throbber-throb-for="activelight.status"]')
    INDICATOR_OFF = (By.XPATH, '//*[@class="activelight-off"]')
    INDICATOR_ON = (By.XPATH, '//*[@class="activelight-on"]')
    CURRENT_BRIGHTNESS = (By.XPATH, '//*[@ng-bind="status.brightness"]')
    MODE_SELECTOR_TEXT = (By.XPATH, '//*[@aria-label="Light Bulbs"]')
    MANUAL_MODE_SELECTOR = (By.LINK_TEXT, '<')
    SCHEDULE_MODE_SELECTOR = (By.LINK_TEXT, '>')

    SCHEDULE_BRIGHTNESS_PICKER = (By.XPATH, '//*[@status="status"]')
    SCHEDULE_LIGHT_TABLE = (By.XPATH, '//*[@data-reactid=".0.2.0"]//*[canvas[4]]')
    UNDO_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.0"]')
    SAVE_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.1"]')
    SCHEDULE_DIMMER_5_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="5%"]')
    SCHEDULE_DIMMER_10_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="10%"]')
    SCHEDULE_DIMMER_20_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="20%"]')
    SCHEDULE_DIMMER_30_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="30%"]')
    SCHEDULE_DIMMER_40_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="40%"]')
    SCHEDULE_DIMMER_50_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="50%"]')
    SCHEDULE_DIMMER_60_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="60%"]')
    SCHEDULE_DIMMER_70_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="70%"]')
    SCHEDULE_DIMMER_80_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="80%"]')
    SCHEDULE_DIMMER_90_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="90%"]')
    SCHEDULE_DIMMER_100_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="100%"]')


class WarmWhiteLightPageLocatorsV3(object):
    # PRODUCT_NAME = (By.XPATH,'//*[@class="columns module-heading text-center"]')
    # BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="activelight-brightness"]')
    CENTRAL_STATUS_INDICATOR = (By.XPATH, '//*[@class="sc-bMVAic cZeerF"]')
    # INDICATOR_OFF = (By.XPATH,'//*[@class="activelight-off"]')
    # INDICATOR_ON = (By.XPATH, '//*[@class="activelight-on"]')
    CURRENT_BRIGHTNESS = (By.XPATH, '//*[@style="background: rgb(255, 255, 255) none repeat scroll 0% 0%;"]')
    MODE_SELECTOR_TEXT = (By.XPATH, '//*[@aria-label="Light Bulbs"]')
    MANUAL_MODE_SELECTOR = (By.XPATH, '//*[@aria-label="Manual"]')
    SCHEDULE_MODE_SELECTOR = (By.XPATH, '//*[@aria-label="Schedule"]')

    SCHEDULE_BRIGHTNESS_PICKER = (By.XPATH, '//*[@status="status"]')
    SCHEDULE_LIGHT_TABLE = (By.XPATH, '//*[@data-reactid=".0.2.0"]//*[canvas[4]]')
    UNDO_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.0"]')
    SAVE_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.1"]')
    SCHEDULE_DIMMER_5_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="5%"]')
    SCHEDULE_DIMMER_10_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="10%"]')
    SCHEDULE_DIMMER_20_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="20%"]')
    SCHEDULE_DIMMER_30_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="30%"]')
    SCHEDULE_DIMMER_40_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="40%"]')
    SCHEDULE_DIMMER_50_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="50%"]')
    SCHEDULE_DIMMER_60_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="60%"]')
    SCHEDULE_DIMMER_70_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="70%"]')
    SCHEDULE_DIMMER_80_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="80%"]')
    SCHEDULE_DIMMER_90_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="90%"]')
    SCHEDULE_DIMMER_100_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="100%"]')

    @staticmethod
    def dimmer_percentage(a):
        DIMMER = (By.XPATH, '//*[@aria-label="' + a + '"]')
        return DIMMER


class TuneableLightPageLocatorsV3(object):
    # PRODUCT_NAME = (By.XPATH,'//*[@class="columns module-heading text-center"]')
    # BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="activelight-brightness"]')
    CENTRAL_STATUS_INDICATOR = (By.XPATH, '//*[@class="sc-gqPbQI cUFgHe"]')
    DIMMER_VIEW_SELECTOR = (By.XPATH, '//span[.="dimmer"]')
    # INDICATOR_OFF = (By.XPATH,'//*[@class="activelight-off"]')
    # INDICATOR_ON = (By.XPATH, '//*[@class="activelight-on"]')
    CURRENT_BRIGHTNESS = (By.XPATH, '//*[@style="background: rgb(255, 255, 255) none repeat scroll 0% 0%;"]')
    MODE_SELECTOR_TEXT = (By.XPATH, '//*[@aria-label="Light Bulbs"]')
    MANUAL_MODE_SELECTOR = (By.XPATH, '//*[@aria-label="Manual"]')
    SCHEDULE_MODE_SELECTOR = (By.XPATH, '//*[@aria-label="Schedule"]')

    SCHEDULE_BRIGHTNESS_PICKER = (By.XPATH, '//*[@status="status"]')
    SCHEDULE_LIGHT_TABLE = (By.XPATH, '//*[@data-reactid=".0.2.0"]//*[canvas[4]]')
    UNDO_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.0"]')
    SAVE_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.1"]')
    SCHEDULE_DIMMER_5_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="5%"]')
    SCHEDULE_DIMMER_10_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="10%"]')
    SCHEDULE_DIMMER_20_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="20%"]')
    SCHEDULE_DIMMER_30_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="30%"]')
    SCHEDULE_DIMMER_40_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="40%"]')
    SCHEDULE_DIMMER_50_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="50%"]')
    SCHEDULE_DIMMER_60_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="60%"]')
    SCHEDULE_DIMMER_70_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="70%"]')
    SCHEDULE_DIMMER_80_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="80%"]')
    SCHEDULE_DIMMER_90_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="90%"]')
    SCHEDULE_DIMMER_100_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="100%"]')

    @staticmethod
    def dimmer_percentage(a):
        DIMMER = (By.XPATH, '//*[@aria-label="' + a + '"]')
        return DIMMER


class TuneableLightPageLocators(object):
    PRODUCT_NAME = (By.XPATH, '//*[@class="columns module-heading text-center"]')
    BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="tuneablelight-brightness"]')
    TONE_DIMMER_SWITCH = (By.XPATH, '//*[@ng-click="toggleSettingState()"]//*[@class="general-icon__"]')
    TONE_DIMMER_TEXT = (By.XPATH, '//*[@ng-click="toggleSettingState()"]//*[@class="ng-binding"]')
    DIMMER_5_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="5%"]')
    DIMMER_10_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="10%"]')
    DIMMER_20_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="20%"]')
    DIMMER_30_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="30%"]')
    DIMMER_40_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="40%"]')
    DIMMER_50_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="50%"]')
    DIMMER_60_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="60%"]')
    DIMMER_70_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="70%"]')
    DIMMER_80_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="80%"]')
    DIMMER_90_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="90%"]')
    DIMMER_100_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="100%"]')

    WARMEST_WHITE = (
        By.XPATH, '//*[@status="tuneablelight.status"]//*[@class="tuneablelight-colourtemp"]//*[@title="2700K"]')
    WARM_WHITE = (
        By.XPATH, '//*[@status="tuneablelight.status"]//*[@class="tuneablelight-colourtemp"]//*[@title="3850.5K"]')
    MID_WHITE = (
        By.XPATH, '//*[@status="tuneablelight.status"]//*[@class="tuneablelight-colourtemp"]//*[@title="4617.5K"]')
    COOL_WHITE = (
        By.XPATH, '//*[@status="tuneablelight.status"]//*[@class="tuneablelight-colourtemp"]//*[@title="5384.5K"]')
    COOLEST_WHITE = (
        By.XPATH, '//*[@status="tuneablelight.status"]//*[@class="tuneablelight-colourtemp"]//*[@title="6535K"]')
    CURRENT_TONE = (By.XPATH, '//*[@class="warmcool ng-binding"]')
    SCHEDULE_WARMEST_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-colourtemp"]//*[@title="2700K"]')
    SCHEDULE_WARM_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-colourtemp"]//*[@title="3850.5K"]')
    SCHEDULE_MID_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-colourtemp"]//*[@title="4617.5K"]')
    SCHEDULE_COOL_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-colourtemp"]//*[@title="5384.5K"]')
    SCHEDULE_COOLEST_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-colourtemp"]//*[@title="6535K"]')

    CENTRAL_STATUS_INDICATOR = (By.XPATH, '//*[@throbber-throb-for="tuneablelight.status"]')
    INDICATOR_OFF = (By.XPATH, '//*[@class="tuneablelight-off"]')
    INDICATOR_ON = (By.XPATH, '//*[@class="tuneablelight-on"]')
    CURRENT_BRIGHTNESS = (By.XPATH, '//*[@ng-bind="status.brightness"]')
    MODE_SELECTOR_TEXT = (By.XPATH, '//*[@class="viewport"]')
    MANUAL_MODE_SELECTOR = (By.LINK_TEXT, '<')
    SCHEDULE_MODE_SELECTOR = (By.LINK_TEXT, '>')

    SCHEDULE_BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="konva-scheduler"]//*[@class="tuneablelight-switch-container"]')
    SCHEDULE_TONE_PICKER = (By.XPATH, '//*[@class="konva-scheduler"]//*[@ng-click="toggleState()"]')
    SCHEDULE_LIGHT_TABLE = (By.XPATH, '//*[@class="konva-scheduler"]//*[canvas[4]]')
    UNDO_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.0"]')
    SAVE_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.1"]')
    SCHEDULE_TONE_DIMMER_TEXT = (
        By.XPATH, '//*[@data-reactid=".0.2.0"]//*[@ng-click="toggleSettingState()"]//*[@class="ng-binding"]')
    SCHEDULE_TONE_DIMMER_SWITCH = (
        By.XPATH, '//*[@data-reactid=".0.2.0"]//*[@ng-click="toggleSettingState()"]//*[@class="general-icon__"]')
    SCHEDULE_DIMMER_5_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="5%"]')
    SCHEDULE_DIMMER_10_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="10%"]')
    SCHEDULE_DIMMER_20_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="20%"]')
    SCHEDULE_DIMMER_30_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="30%"]')
    SCHEDULE_DIMMER_40_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="40%"]')
    SCHEDULE_DIMMER_50_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="50%"]')
    SCHEDULE_DIMMER_60_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="60%"]')
    SCHEDULE_DIMMER_70_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="70%"]')
    SCHEDULE_DIMMER_80_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="80%"]')
    SCHEDULE_DIMMER_90_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="90%"]')
    SCHEDULE_DIMMER_100_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="100%"]')

    def dimmer_percentage(a):
        DIMMER = (By.XPATH, '//*[@aria-label="' + a + '"]')
        return DIMMER


class ColourLightPageLocators(object):
    PRODUCT_NAME = (By.XPATH, '//*[@class="columns module-heading text-center"]')
    BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="colourlight-brightness"]')
    DIMMER_SWITCH = (By.XPATH, '//*[@toggle-state="toggleState"]//*[@data-icon="!"]')
    TONE_COLOUR_SWITCH = (By.XPATH, '//*[@class="colourlight-mode text-center row ng-scope"]')
    TONE_SWITCH = (By.XPATH, '//*[@data-icon="4"]')
    COLOUR_SWITCH = (By.XPATH, '//*[@data-icon="#"]')
    DIMMER_5_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="5%"]')
    DIMMER_10_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="10%"]')
    DIMMER_20_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="20%"]')
    DIMMER_30_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="30%"]')
    DIMMER_40_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="40%"]')
    DIMMER_50_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="50%"]')
    DIMMER_60_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="60%"]')
    DIMMER_70_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="70%"]')
    DIMMER_80_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="80%"]')
    DIMMER_90_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="90%"]')
    DIMMER_100_PERCENT = (By.XPATH, '//*[@class="columns small-12 spinner-control"]//*[@title="100%"]')

    WARMEST_WHITE = (
        By.XPATH, '//*[@status="colourlight.status"]//*[@class="colourlight-colourtemp"]//*[@title="2700K"]')
    WARM_WHITE = (
        By.XPATH, '//*[@status="colourlight.status"]//*[@class="colourlight-colourtemp"]//*[@title="3850.5K"]')
    MID_WHITE = (By.XPATH, '//*[@status="colourlight.status"]//*[@class="colourlight-colourtemp"]//*[@title="4617.5K"]')
    COOL_WHITE = (
        By.XPATH, '//*[@status="colourlight.status"]//*[@class="colourlight-colourtemp"]//*[@title="5384.5K"]')
    COOLEST_WHITE = (
        By.XPATH, '//*[@status="colourlight.status"]//*[@class="colourlight-colourtemp"]//*[@title="6535K"]')

    RED_LEFT = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="0, 99, 100"]')
    RED_ORANGE = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="15, 99, 100"]')
    ORANGE = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="30, 99, 100"]')
    ORANGE_YELLOW = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="45, 99, 100"]')
    YELLOW = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="60, 99, 100"]')
    YELLOW_GREEN = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="75, 99, 100"]')
    GREEN = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="90, 99, 100"]')
    GREEN_CYAN = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="150, 99, 100"]')
    CYAN = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="180, 99, 100"]')
    CYAN_BLUE = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="210, 99, 100"]')
    BLUE = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="225, 99, 100"]')
    BLUE_MAGENTA = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="255, 99, 100"]')
    MAGENTA = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="285, 99, 100"]')
    MAGENTA_PINK = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="330, 99, 100"]')
    PINK = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')
    PINK_RED = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')
    RED_RIGHT = (By.XPATH, '//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')

    CENTRAL_STATUS_INDICATOR = (By.XPATH, '//*[@throbber-throb-for="colourlight.status"]')
    INDICATOR_OFF = (By.XPATH, '//*[@class="colourlight-off"]')
    INDICATOR_ON = (By.XPATH, '//*[@class="colourlight-on"]')
    CURRENT_BRIGHTNESS = (By.XPATH, '//*[@ng-bind="status.brightness"]')
    MODE_SELECTOR_TEXT = (By.XPATH, '//*[@class="viewport"]')
    MANUAL_MODE_SELECTOR = (By.LINK_TEXT, '<')
    SCHEDULE_MODE_SELECTOR = (By.LINK_TEXT, '>')
    CURRENT_TONE = (By.XPATH, '//*[@class="warmcool ng-binding"]')

    SCHEDULE_BRIGHTNESS_PICKER = (By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-switch-container"]')
    # SCHEDULE_TONE_PICKER = (By.XPATH, '//*[@class="konva-scheduler"]//*[@ng-click="toggleState()"]')
    SCHEDULE_LIGHT_TABLE = (By.XPATH, '//*[@class="konva-scheduler"]//*[canvas[4]]')
    SCHEDULE_TONE_COLOUR_SWITCH = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="columns small-12 small-text-center ng-scope"]')
    SCHEDULE_TONE_SWITCH = (By.XPATH, '//*[@class="konva-scheduler"]//*[@data-icon="4"]')
    SCHEDULE_COLOUR_SWITCH = (By.XPATH, '//*[@class="konva-scheduler"]//*[@data-icon="#"]')
    UNDO_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.0"]')
    SAVE_BUTTON = (By.XPATH, '//*[@data-reactid=".0.3.1"]')
    SCHEDULE_TONE_DIMMER_TEXT = (
        By.XPATH, '//*[@data-reactid=".0.2.0"]//*[@ng-click="toggleSettingState()"]//*[@class="ng-binding"]')
    SCHEDULE_TONE_DIMMER_SWITCH = (
        By.XPATH, '//*[@data-reactid=".0.2.0"]//*[@ng-click="toggleSettingState()"]//*[@class="general-icon__"]')
    SCHEDULE_DIMMER_5_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="5%"]')
    SCHEDULE_DIMMER_10_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="10%"]')
    SCHEDULE_DIMMER_20_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="20%"]')
    SCHEDULE_DIMMER_30_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="30%"]')
    SCHEDULE_DIMMER_40_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="40%"]')
    SCHEDULE_DIMMER_50_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="50%"]')
    SCHEDULE_DIMMER_60_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="60%"]')
    SCHEDULE_DIMMER_70_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="70%"]')
    SCHEDULE_DIMMER_80_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="80%"]')
    SCHEDULE_DIMMER_90_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="90%"]')
    SCHEDULE_DIMMER_100_PERCENT = (By.XPATH, '//*[@status="status"]//*[@title="100%"]')
    SCHEDULE_WARMEST_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colourtemp"]//*[@title="2700K"]')
    SCHEDULE_WARM_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colourtemp"]//*[@title="3850.5K"]')
    SCHEDULE_MID_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colourtemp"]//*[@title="4617.5K"]')
    SCHEDULE_COOL_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colourtemp"]//*[@title="5384.5K"]')
    SCHEDULE_COOLEST_WHITE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colourtemp"]//*[@title="6535K"]')
    SCHEDULE_RED_LEFT = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="0, 99, 100"]')
    SCHEDULE_RED_ORANGE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="15, 99, 100"]')
    SCHEDULE_ORANGE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="30, 99, 100"]')
    SCHEDULE_ORANGE_YELLOW = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="45, 99, 100"]')
    SCHEDULE_YELLOW = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="60, 99, 100"]')
    SCHEDULE_YELLOW_GREEN = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="75, 99, 100"]')
    SCHEDULE_GREEN = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="90, 99, 100"]')
    SCHEDULE_GREEN_CYAN = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="150, 99, 100"]')
    SCHEDULE_CYAN = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="180, 99, 100"]')
    SCHEDULE_CYAN_BLUE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="210, 99, 100"]')
    SCHEDULE_BLUE = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="225, 99, 100"]')
    SCHEDULE_BLUE_MAGENTA = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="255, 99, 100"]')
    SCHEDULE_MAGENTA = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="285, 99, 100"]')
    SCHEDULE_MAGENTA_PINK = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="330, 99, 100"]')
    SCHEDULE_PINK = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')
    SCHEDULE_PINK_RED = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')
    SCHEDULE_RED_RIGHT = (
        By.XPATH, '//*[@class="konva-scheduler"]//*[@class="colourlight-colour"]//*[@title="345, 99, 100"]')


class HolidayModePageLocators(object):
    HOLIDAY_MENU_OPTION = (By.XPATH, './/*[@href="/holiday-mode"]')
    HOLIDAY_MODE_PAGE_EDIT = './/*[@href="/holiday-mode"]'
    HOLIDAY_MODE_PAGE_EDIT_BUTTON = './/*[@ng-click="editHolidayMode()"]'
