from behave import given, when, then
import FF_SLT4 as FF_SLT4
import FF_SLT4_ScreenNavigator as navigator
import FF_SLT4_OCRUtil as OCRUtils
import time

EXECUTION_MODE = 'REMOTE'


def assert_with_report(statement, reporter, message):
    if statement :
        reporter.ReportEvent('Test Validation : ', message, "PASS")
    else:
        reporter.ReportEvent('Test Validation : ', message, "FAIL")


def log_done(reporter, message):
    reporter.ReportEvent('Test step :' , message , 'DONE')

def log_report(reporter, message):
    reporter.ReportEvent('Report :', message , '')



@given('the TGstick is paried with the SLT4 thermostat and the device is switched to  {temp_scale} scale for UI based validation')
def pair_device(context, temp_scale):
    context.stat = FF_SLT4.SLT4(temp_scale)
    context.screen_navigator =  navigator.ScreenUtil(context.stat)
    screenshot_folder = context.reporter.strCurrentScreenshotFolder
    print('The current screenshot folder is {0}'.format(screenshot_folder))
    context.ocr_util = OCRUtils.SLT4OCRUtil(screenshot_folder, context.stat, EXECUTION_MODE)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('SLT4 Stat UI/OCR validation scenarios')



def _set_device_hold_mode_via_ui(context, mode_name, target_temp_change_mode, target_temperature_change_points, duration = 0):
    stat = context.stat
    screen_navigator = context.screen_navigator
    stat_scale = stat.get_current_device_scale()
    stat_temp = stat.get_current_temperature()
    reporter = context.reporter
    if stat_scale == 'CELCIUS':
        temperature = float(stat_temp)
        temperature = round(temperature*2)/2
    else:
        temperature = int(stat_temp)
    context.initial_temperature = temperature
    if target_temp_change_mode == 'above':
        target_temp = temperature+ target_temperature_change_points
    elif target_temp_change_mode == 'below':
        target_temp = temperature - target_temperature_change_points
    if 'HEAT' in mode_name.upper():
        screen_navigator.set_device_to_mode(mode_name, heat_target=target_temp, duration=duration)
    elif 'COOL' in mode_name.upper():
        screen_navigator.set_device_to_mode(mode_name, cool_target=target_temp, duration=duration)

    if duration == 0:
        log_done(reporter, 'Set the device to {0} via UI with temperature set to {1} - Initial temperature was {2} - Changed by {3} points'.format(mode_name, target_temp, stat_temp, target_temperature_change_points))
    else:
        log_done(reporter, 'Set the device to {0} via UI  for duration {1} with temperature set to {2} - Initial temperature was {3} - Changed by {4} points '.format(mode_name, duration, target_temp, stat_temp, target_temperature_change_points))


@when('the device is set to mode {mode_name} with {target_temperature_change_points:d} points {target_temp_change_mode} ambient temperature via UI')
def set_device_for_all_modes(context, mode_name, target_temp_change_mode, target_temperature_change_points):
    _set_device_hold_mode_via_ui(context, mode_name, target_temp_change_mode, target_temperature_change_points)

@when('the device is set to  boost mode {mode_name} with {target_temperature_change_points:d} points {target_temp_change_mode} ambient temperature via UI for {duration:d} hours')
def set_device_to_boost_mode(context, mode_name, target_temp_change_mode, target_temperature_change_points, duration):
    _set_device_hold_mode_via_ui(context, mode_name, target_temp_change_mode, target_temperature_change_points, duration)


def validate_timer_value(context, min_hrs_expected, min_mins_expected):
    ocr_util = context.ocr_util
    reporter = context.reporter
    hours, mins = ocr_util.get_screen_timer_value()
    message_success = 'The timer value in ({0}) is {1}'
    message_failure = 'The timer value in ({0}} is {1}, It should have been atleast {2} '
    if hours < min_hrs_expected:
        assert_with_report(False, reporter, message_failure.format('Hours', ))






@then('The device should be successfully switched to {expected_device_mode} in UI')
def validate_device_mode_from_ocr(context, expected_device_mode):
    ocr_util = context.ocr_util
    reporter = context.reporter
    time.sleep(5)
    actual_device_mode = ocr_util.get_current_stat_mode()
    if actual_device_mode == expected_device_mode:
        assert_with_report(True, reporter, 'The device UI displays the device to be in {0} - As expected '.format(expected_device_mode, actual_device_mode))
    else:
        assert_with_report(False, reporter, 'The device UI is expected to be in {0} mode , but was in {1}'.format(expected_device_mode, actual_device_mode))

@when('the stat UI is set to dual hold mode with heat target set to {heat_target:d} and cool target set to {cool_target:d}')
def set_device_to_dual_hold(context, heat_target, cool_target):
    ocr_util = context.ocr_util
    stat = context.stat
    reporter = context.reporter
    screen_navigator = context.screen_navigator
    screen_navigator.set_device_to_mode('DUAL HOLD', heat_target=heat_target, cool_target=cool_target)
    log_done(reporter, 'Set the stat to dual hold mode with heat target set to {0} and cooling target set to {1}'.format(heat_target, cool_target))



@then('the stat UI should be in {expected_mode} with the target temperature changed {points_changed:d} points {temp_change_mode} the ambient temperature')
def validate_device_mode_temperature(context, expected_mode, points_changed, temp_change_mode):
    validate_device_mode_from_ocr(context, expected_mode)
    ocr_util = context.ocr_util
    stat = context.stat
    reporter = context.reporter
    initial_temperature = round(context.initial_temperature*2)/2
    if temp_change_mode == 'above':
        expected_final_temperature = initial_temperature + points_changed
    elif temp_change_mode == 'below':
        expected_final_temperature = initial_temperature - points_changed
    else:
        raise Exception('only above and below are allowed!')
    context.expected_temperature = expected_final_temperature
    if 'HEAT' in expected_mode.upper():
        current_stat_set_temp = stat.get_current_set_heat_temp()
    if 'COOL' in expected_mode.upper():
        current_stat_set_temp = stat.get_current_set_cool_temp()

    print('The expected temperature is {0} and the current tenperature is {1}'.format(expected_final_temperature, current_stat_set_temp))
    if float(expected_final_temperature) == float(current_stat_set_temp):
        assert_with_report(True, reporter, 'When the stat is switched to {0} and when the target temperature is set to '
                                           '{1} ({2} points change over ambient temperature) via stat UI it is '
                                           'successful'.format(expected_mode, expected_final_temperature, points_changed))

    else:
        assert_with_report(False, reporter, 'When the stat is switched to {0} and when the target temperature is set to {1} '
                                            '({2} points change over the ambient temperature)via UI  ,'
                                            ' The stat is supposed to be changed to temperature {3} , '
                                            'But was found to be at {4}'.format(expected_mode, expected_final_temperature,
                                                                                points_changed, expected_final_temperature, current_stat_set_temp))

@then('the stat should display the expected target temperature value')
def validate_displayed_target_temperature(context):
    expected_temperature = context.expected_temperature
    ocr_util = context.ocr_util
    reporter = context.reporter
    target_temp,_= ocr_util.get_current_temp_and_target_temp()
    if float(target_temp) == float(expected_temperature):
        assert_with_report(True, reporter, 'The current and target temperature shown in the stat UI should match - Value {0}'.format(target_temp))
    else:
        assert_with_report(False, reporter,'The target temperature shown in the stat is {0}, It should have been {1}'.format(target_temp, expected_temperature))


@then('The stat should display the timer value for atleast {expected_hours:d} hours and {expected_mins:d} mins')
def validate_device_timer(context, expected_hours, expected_mins):
    ocr_util = context.ocr_util
    reporter = context.reporter
    actual_timer_hours, actual_timer_mins = ocr_util.get_screen_timer_value()
    log_report(reporter, "The displayed timer hour and mins values are {0} and {1}".format(actual_timer_hours, actual_timer_mins))
    hours_fulfilled = actual_timer_hours >= expected_hours
    mins_fulfilled = actual_timer_mins >= expected_mins
    if hours_fulfilled is True:
        assert_with_report(True, reporter, 'The displayed timer hour value is {0} is matching the expected minimum value {1}'.format(actual_timer_hours, expected_hours))
    else:
        assert_with_report(False, reporter, 'The displayed timer hour {0} is expected atleast to be greater than or equal to {1}'.format( actual_timer_hours, expected_hours))

    if mins_fulfilled is True:
        assert_with_report(True, reporter, 'The displayed timer mins value is {0} is matching the expected minimum value {1}'.format(actual_timer_mins, expected_mins))

    else:
        assert_with_report(False, reporter,'The displayed timer mins {0} is expected atleast to be greater than or equal to {1}'.format(actual_timer_mins, expected_mins))


@then('The protection timer should be on for atleast {expected_mins:d} minutes in the UI')
def check_protection_timer(context, expected_mins):
    ocr_util = context.ocr_util
    reporter = context.reporter
    timer_mins,_ = ocr_util.get_protection_timer_value()
    mins_fulfilled = timer_mins >= expected_mins
    if mins_fulfilled is True:
        assert_with_report(True, reporter, 'The protection timer is on for atleast {0} minutes in the UI '.format(expected_mins))
    else:
        assert_with_report(False, reporter, 'The protection timer is expected to be on for atleast {0} mins in the UI, It was on for {1}'.format(expected_mins, timer_mins))



@when('The stat heat temperature is overridden by {override_points:d} degrees via UI')
def override_heat_temperature(context, override_points):
    time.sleep(5)
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    context.current_heat_temp = float(stat.get_current_set_heat_temp())
    log_report(reporter, 'The current set heating temperature is {0}'.format(stat.get_current_set_heat_temp()))
    context.target_temperature = context.current_heat_temp + override_points
    log_report(reporter, ' The override temperature point is {0}'.format(context.target_temperature))
    screen_navigator.change_heat_without_cancelling(context.target_temperature)
    time.sleep(5)
    log_done(reporter, 'The heat temperature is changed by points {0} to {1}'.format(override_points, context.target_temperature))


@when('The stat cool temperature is overridden by {override_points:d} degrees via UI')
def override_cool_temperature(context, override_points):
    time.sleep(5)
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    context.current_cool_temp = float(stat.get_current_set_cool_temp())
    log_report(reporter, 'The current set Cooling temperature is {0}'.format(stat.get_current_set_heat_temp()))
    context.target_cooling_temperature = context.current_cool_temp + override_points
    log_report(reporter, ' The override temperature point is {0}'.format(context.target_cooling_temperature))
    screen_navigator.change_cool_without_cancelling(context.target_cooling_temperature)
    time.sleep(5)
    log_done(reporter, 'The Cool temperature is changed by points {0} to {1}'.format(override_points, context.target_cooling_temperature))


@then('The cool temperature should be overridden in UI by {override_points:d} points')
def check_cool_override_temp(context, override_points):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    stat_current_temp = float(stat.get_current_set_cool_temp())
    stat_initial_temperature = context.current_cool_temp
    expected_temperature = stat_initial_temperature + override_points
    actual_temp, _ = ocr_util.get_current_temp_and_target_temp()
    if float(stat_current_temp) == float(actual_temp):
        assert_with_report(True, reporter,
                           'When the cool temperature is overridden by {0} points, The target temperature is changed correctly'.format(
                               override_points))
    else:
        assert_with_report(False, reporter, 'When the cool temperature is overridden by {0} points, '
                                            'The stat target temperature is supposed to have been {0} from {1} , '
                                            'but was {2}'.format(override_points, expected_temperature,
                                                                 stat_initial_temperature, actual_temp))


@when('The device is switched to mode {mode_name}  with  {change:d} points {change_mode} ambient temperature and OFF {number_of_times:d} times via UI')
def toggle_device_to_mode_and_off(context, mode_name, change, change_mode, number_of_times):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    protection_timer_value = stat.get_protection_timer_value()
    if protection_timer_value > 0:
        print('The protection timer is on before starting the test , Sleeping until it is zero {0}'.format(protection_timer_value))
        time.sleep(protection_timer_value + 10)
    for i in range(number_of_times):
        log_done(reporter, 'Setting the stat to the mode {0} for {1} times'.format(mode_name, number_of_times))
        _set_device_hold_mode_via_ui(context, mode_name, change_mode, change)
        time.sleep(5)
        screen_navigator.set_device_to_mode('OFF')
        time.sleep(5)
        log_done(reporter, 'Set the device to OFF')


@then('The protection timer should be ON in UI')
def check_if_protection_timer_is_on(context):
    ocr_util = context.ocr_util
    reporter = context.reporter
    is_timer_on = ocr_util.is_protection_timer_on()
    if is_timer_on == True:
        assert_with_report(True, reporter, 'The protection timer is ON')
    else:
        assert_with_report(False, reporter, 'The protection timer is OFF , It was expected to be on ')


@then('The heat temperature should be overridden in UI by {override_points:d} points')
def check_heat_override_temp(context, override_points):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    stat_current_temp = float(stat.get_current_set_heat_temp())
    stat_initial_temperature = context.current_heat_temp
    expected_temperature = stat_initial_temperature + override_points
    actual_temp,_ = ocr_util.get_current_temp_and_target_temp()
    if float(stat_current_temp) == float(actual_temp):
        assert_with_report(True, reporter, 'When the heat temperature is overridden by {0} points, The target temperature is changed correctly'.format(override_points))
    else:
        assert_with_report(False, reporter, 'When the heat temperature is overridden by {0} points, '
                                            'The stat target temperature is supposed to have been {0} from {1} , '
                                            'but was {2}'.format(override_points, expected_temperature, stat_initial_temperature, actual_temp))


@when('the stat is switched to the mode {target_mode} in UI')
def switch_stat_mode(context, target_mode):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    log_report(reporter, 'Setting the device to mode {0}'.format(target_mode))
    screen_navigator.set_device_to_mode(target_mode, heat_target=-100, cool_target=-100)
    log_done(reporter, 'The device is successfully toggled to mode {0}'.format(target_mode))


@then('the device name {expected_name} should be set on the stat UI')
def check_device_name_in_ui(context, expected_name):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    log_report(reporter, 'Checking to see if the device has the name {0}'.format(expected_name))
    is_name_on_screen = ocr_util.is_device_name_is_displayed(expected_name)
    #Reset the device name
    stat.set_device_name('')
    if is_name_on_screen is True:
        assert_with_report(True, reporter, 'The device name {0} is displayed on the screen when set'.format(expected_name))
    else:
        assert_with_report(False, reporter, 'The device name {0} is Not displayed on the screen when set, Please check the screenshot'.format(expected_name))

@then('The vacation mode should be disabled in UI')
def check_if_device_not_in_vacation(context):
    time.sleep(5)
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    stat_current_mode = ocr_util.get_current_stat_mode()
    if stat_current_mode != 'VACATION MODE':
        assert_with_report(True, reporter, 'The vacation mode in disabled in the UI ')
    else:
        assert_with_report(True, reporter, 'The vacation mode was expected to be cancelled, The stat is still in vacation mode')

@when('The vacation mode ends after {time_duration:d} minutes in the UI')
def validate_vacation_mode_end(context, time_duration):
    time.sleep(time_duration*60 + 10)
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    stat_current_mode = ocr_util.get_current_stat_mode()
    if stat_current_mode != 'VACATION MODE':
        assert_with_report(True, reporter, 'The vacation mode has ended successfully after {0} minutes in the UI'.format(time_duration))
    else:
        assert_with_report(False, reporter, 'The vacation mode is supposed to have ended successfully after {0} minutes in the UI, However the vacation mode is still on '.format(time_duration))


@when('The stat {humidity_control_type} is set to {percentage:d} percent via UI')
def set_humidifier_to_percent(context, humidity_control_type, percentage):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    screen_navigator.set_humidity_type(humidity_control_type)
    log_done(reporter, 'Set the {0} on '.format(humidity_control_type))
    screen_navigator.set_humidity_percentage_in_dial(percentage)
    log_done(reporter, 'Set the humidity level to {0} percentage'.format(percentage))


@then('The stat humidity percent should be {expected_percentage:d} in the UI')
def validate_humidity_percentage(context, expected_percentage):
    ocr_util = context.ocr_util
    reporter = context.reporter
    stat = context.stat
    screen_navigator = context.screen_navigator
    screen_navigator.navigate_to('MORE_SCREEN')
    screen_navigator.navigate_to_submenu('HUMIDITY', screen_navigator.MORE_SUBMENU)
    actual_ui_humidity_percent = ocr_util.get_set_humidity_percent()
    if int(actual_ui_humidity_percent) == expected_percentage:
        assert_with_report(True, reporter, 'The humidity is set to {0} percent as expected in the UI '.format(expected_percentage))
    else:
        assert_with_report(False, reporter, 'The humidity is expected to be set to {0} percent , But was {1} percent in the '
                                            'UI'.format(expected_percentage, actual_ui_humidity_percent))

@when('The device fan is set to {fan_state} MODE in the UI')
def set_fan_to_on_and_auto(context, fan_state):
    print('The length is {0}'.format(len(fan_state)))
    reporter = context.reporter
    screen_navigator = context.screen_navigator
    log_done(reporter, 'Attempting to set the devcice fan state to {0}'.format(fan_state))
    screen_navigator.set_device_fan_state(fan_state)
    log_done(reporter, 'Set the devcice fan state to {0}'.format(fan_state))

@when('The device fan is set to CIRCULATE_MODE for {duration:d} mins in the UI')
def set_circulate_duration(context, duration):
    reporter = context.reporter
    screen_navigator = context.screen_navigator
    log_done(reporter, 'Attempting to set the devcice fan state to CIRCULATE for {0} mins'.format(duration))
    screen_navigator.set_device_fan_state('CIRCULATE', target_mins=duration)
    log_done(reporter, 'Set the devcice fan state to CIRCULATE for {0} mins'.format(duration))



''' UI Schedule Functions'''
@when('The Below {device_mode} is set in the UI')
def set_schedule_UI(context,device_mode):
    ocr_util = context.ocr_util
    reporter = context.reporter
    screen_navigator = context.screen_navigator
    log_done(reporter, 'Attempting to set the devcice to {0} mode'.format(device_mode))
    # Get the schdule details in a table
    oSchedule,_=context.stat.create_week_schdule_table(context)
    context.oSchedule=oSchedule
    screen_navigator.set_start_over_schedule(device_mode, oSchedule)
    # ocr_util.get_schedule_details()
    log_done(reporter, 'Set the devcice to {0} mode'.format(device_mode))


