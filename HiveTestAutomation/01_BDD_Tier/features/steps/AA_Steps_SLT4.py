from behave import given, when, then
import FF_SLT4
import FF_device_utils as dutils
import time
import FF_OCRUtils as ocr_util


def assert_with_report(statement, reporter, message):
    if statement :
        reporter.ReportEvent('Test Validation : ', message, "PASS")
    else:
        reporter.ReportEvent('Test Validation : ', message, "FAIL")


def log_done(reporter, message):
    reporter.ReportEvent('Test step :' , message , 'DONE')

def log_report(reporter, message):
    reporter.ReportEvent('Report :', message , '')


@given('the TGstick is paired with the SLT4 thermostat and the device is switched to  {temp_scale} scale')
def pair_device(context, temp_scale):
    context.stat = FF_SLT4.SLT4(temp_scale)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('SLT4 Stat validation scenario ')

@when('the ACC wiring configuration is connected')
def check_humidifier_connection(context):
    stat = context.stat
    stat_wiring_state = stat.get_stat_wiring_state()
    if 'Acc' in stat_wiring_state:
        log_report(context.reporter, 'The humidfier wiring configuration is connected')
    else:
        assert_with_report(False, 'The humidifier wiring (Acc) is not connected, The test case configuration has failed')


def check_humidity_device_state(context, expected_value):
    stat = context.stat
    stat_device_state = stat.get_current_humidity_control_type()
    if stat_device_state == expected_value:
        assert_with_report(False, 'The device has {0} on , instead of {1} on '.format(stat_device_state, expected_value))
    else:
        assert_with_report(True, 'The device has {0} on '.format(stat_device_state))

@then('The stat humidity control type should be {expected_value}')
def check_humidity_control_type(context, expected_value):
    stat = context.stat
    reporter = context.reporter
    stat_device_state = stat.get_current_humidity_control_type()
    if stat_device_state == expected_value:
        assert_with_report(True, reporter, 'The device has {0} on (validated via zigbee) '.format(stat_device_state))
    else:
        assert_with_report(False, reporter, 'The device has {0} on , instead of {1} on (validated via zigbee)'.format(stat_device_state, expected_value))

@when('The humidifier is set to {percentage:d} percentage humidity')
def set_humidifier_to_percentage(context, percentage):
    stat = context.stat
    stat.set_humidity_percentage('HUMIDIFIER', percentage)
    log_done(context.reporter, 'Setting the humidifier to {0} percentage  humidity'.format(percentage))
    stat_device_state = stat.get_current_humidity_control_type()
    log_report(context.reporter, 'The {0} is turned on '.format(stat_device_state))


@when('The de-humidifier is set to {percentage:d} percentage humidity')
def set_dehumidifier_to_percentage(context, percentage):
    stat = context.stat
    stat.set_humidity_percentage('DEHUMIDIFIER', percentage)
    log_done(context.reporter, 'Setting the de-humidifier to {0} percentage  humidity'.format(percentage))
    stat_device_state = stat.get_current_humidity_control_type()
    log_report(context.reporter, 'The {0} is turned on '.format(stat_device_state))


@when('the stat is set to mode {device_mode}')
def change_device_mode(context, device_mode):
    stat = context.stat
    log_done(context.reporter, 'The current device mode is {0}'.format(stat.get_current_mode()))
    stat.withMode(device_mode).set()
    log_done(context.reporter, 'Switched the device to mode {0}'.format(device_mode))
    # Store the current state
    previous_stat_state_var = {}
    previous_stat_state_var['stat_mode'] = stat.get_current_mode()
    previous_stat_state_var['stat_heat_temp'] = stat.get_current_set_heat_temp()
    previous_stat_state_var['stat_cool_temp'] = stat.get_current_set_cool_temp()
    context.previous_stat_state_var = previous_stat_state_var

@when('the temperature scale stat is set to {device_scale}')
def switch_device_scale(context, device_scale):
    stat = context.stat
    log_done(context.reporter, 'The current device temperature scale is {0}'.format(stat.get_current_device_scale()))
    stat.set_device_scale(device_scale)
    log_done(context.reporter, 'Switched the temperature scale to {0}'.format(device_scale))

@then('the temperature scale on the stat should be set to {expected_scale}')
def check_device_scale(context, expected_scale):
    stat = context.stat
    current_scale = stat.get_current_device_scale()
    message = 'The device temperature scale should be switched successfully to {0} scale'.format(expected_scale)
    assert_with_report(current_scale == expected_scale, context.reporter, message)


@then('it should be switched to mode {expected_mode}')
def check_device_mode(context, expected_mode):
    current_mode = context.stat.get_current_mode()
    context.current_mode = current_mode
    if current_mode == expected_mode:
        assert_with_report(True, context.reporter, 'The device is successfully switched to mode to {0} (Validated via Zigbee)'.format(expected_mode))
    else :
        assert_with_report(False, context.reporter, 'The device is expected to  switched to mode to {0}, But is in mode {1} (Validated via Zigbee)'.format(expected_mode, current_mode))


@when('The holiday mode ends after {time_duration:d} minutes')
def wait_until_mode_ends(context, time_duration):
    time.sleep(time_duration*60 + 20)
    holiday_mode_state = context.stat.get_current_holiday_mode_state()
    if holiday_mode_state == 'INACTIVE':
        assert_with_report(True, context.reporter, 'The holiday mode is successfully ended after the end time')
    else :
        assert_with_report(False, context.reporter, 'The holiday mode is still active even after the end time has reached')





@then('the humidity should be set to {expected_percentage:d} percentage')
def check_humidity_value(context, expected_percentage):
    stat = context.stat
    current_humidity_value = stat.get_humidity_percentage()
    message = 'The current read humidity value is {0} percent(validated via zigbee)'.format(current_humidity_value)
    assert_with_report(expected_percentage == current_humidity_value, context.reporter, message)


def set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode, duration = None):
    stat = context.stat
    message = 'Current device mode is {0}, Current ambient temperature is {1}, '.format(stat.get_current_mode(), stat.get_current_temperature())
    log_report(context.reporter, message)
    time.sleep(10)
    # Store the current state
    previous_stat_state_var = {}
    previous_stat_state_var['stat_mode'] = stat.get_current_mode()
    previous_stat_state_var['stat_heat_temp'] = stat.get_current_set_heat_temp()
    previous_stat_state_var['stat_cool_temp'] = stat.get_current_set_cool_temp()
    context.previous_stat_state_var = previous_stat_state_var
    print('The previous stat state is {0}'.format(previous_stat_state_var))
    #Get the current temperature
    context.current_temperature = stat.get_current_temperature()
    context.baseline_temp = round(float(context.current_temperature))
    temperature_points = int(temperature_points)

    context.current_temperature = round(float(stat.get_current_temperature()))
    if temp_change_mode == 'above':
        context.target_temperature = context.current_temperature + temperature_points
    if temp_change_mode == 'below':
        context.target_temperature = context.current_temperature - temperature_points

    stat.withMode(device_mode)

    if duration:
        stat.for_time(duration)

    if device_mode.strip() == 'HEAT HOLD' or device_mode == 'HEAT_BOOST':
        print('The device is in heat mode , Setting up the heating temperature')
        stat.with_heat_set_to_temperature(context.target_temperature)
    elif device_mode.strip() == 'COOL HOLD' or device_mode == 'COOL_BOOST' or device_mode.strip() == 'COOL SCHEDULE':
        print('The device is in heat mode , Setting up the Cooling temperature')
        stat.with_cooling_set_to_temperature(context.target_temperature)
    else :
        assert_with_report(False, context.reporter, "Invalid selection mode , HEAT / COOL / HEAT_BOOST and COOL_BOOST Allowed")

    stat.set()
    if duration:
        log_done(context.reporter,
                 "Set the stat to {0} with {1} points {2} the ambient temperature for duration {3}".format(device_mode, temperature_points, temp_change_mode, duration))
    else:
        log_done(context.reporter, "Set the stat to {0} with {1} points {2} the ambient temperature".format(device_mode, temperature_points, temp_change_mode))



@when('the device is in {device_mode} mode and the required temperature is set to {temperature_points:d} points {temp_change_mode} the ambient temperature')
def set_device_mode_temp(context, device_mode, temperature_points, temp_change_mode):
    set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode)
    '''
                 Wait for the protection timer to be off
                 Looks like the value is set to 180 when the device is turned on , which will make these 
                 tests run 180 seconds slower in the initial state as it cannot be reliably determined 
                 if the device was turned on the first time or the protection timer is already running !
          '''
    time.sleep(5)
    current_timer_value = context.stat.get_protection_timer_value()
    # Sleep for an extra 20 seconds
    if current_timer_value > 0:
        print('The protection timer is on for {0} seconds , Sleeping until then'.format(current_timer_value))
        time.sleep(current_timer_value + 20)


@when('the device is in {device_mode} mode and the required temperature is set to {temperature_points:d} points {temp_change_mode} the ambient temperature without protection timer validation')
def set_device_mode_temp_without_timer(context, device_mode, temperature_points, temp_change_mode):
    set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode)


@when('the device is in {device_mode} mode and the required temperature is set to {temperature_points:d} points {temp_change_mode} the ambient temperature for {duration:d} minutes without protection timer validation')
def set_device_mode_temp_with_timer(context, device_mode, temperature_points, temp_change_mode, duration):
    set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode, duration)


@when('the device is set to {device_mode} mode and the required temperature is set to {temperature_points:d} points {temp_change_mode} the ambient temperature {count:d} times')
def set_device_mode_temp_count(context, device_mode, temperature_points, temp_change_mode, count):
    '''Check if the protection timer is on now , Sleep if so '''
    time.sleep(5)
    current_timer_value = context.stat.get_protection_timer_value()
    if current_timer_value > 0:
        print('The protection timer is on for {0} seconds , Sleeping until then'.format(current_timer_value))
        time.sleep(current_timer_value + 5)

    for i in range(count):
        context.stat.withMode('OFF').set()
        time.sleep(5)
        #set the device temp
        set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode)


@when('the device is set to {initial_mode} mode with {initial_temp_points} points {initial_temp_change_mode} the ambient temperature and is set to COOL_BOOST with {final_temp_points} points below the ambient temperature')
def change_device_mode_from(context, initial_mode, initial_temp_points, initial_temp_change_mode, final_temp_points):
    stat = context.stat
    set_heat_cool_with_temp_and_time(context, initial_mode, initial_temp_points, initial_temp_change_mode)
    context.initial_set_cool_temp = stat.get_current_set_cool_temp()
    print('The initial set cool temp is {0}'.format(context.initial_set_cool_temp))
    #Sleep for 20 seconds
    time.sleep(20)
    set_heat_cool_with_temp_and_time(context, 'COOL_BOOST', final_temp_points, 'below')
    context.final_set_cool_temp = stat.get_current_set_cool_temp()
    print('The final set cool temp is {0}'.format(context.final_set_cool_temp))
    time.sleep(20)


@when('the device is set to {initial_mode} mode with {initial_temp_points} points {initial_temp_change_mode} the ambient temperature and is set to HEAT_BOOST with {final_temp_points} points above the ambient temperature')
def change_device_mode_from(context, initial_mode, initial_temp_points, initial_temp_change_mode, final_temp_points):
    stat = context.stat
    set_heat_cool_with_temp_and_time(context, initial_mode, initial_temp_points, initial_temp_change_mode)
    context.initial_set_heat_temp = stat.get_current_set_heat_temp()
    print('The initial set heat temp is {0}'.format(context.initial_set_heat_temp))
    #Sleep for 20 seconds
    time.sleep(20)
    set_heat_cool_with_temp_and_time(context, 'HEAT_BOOST', final_temp_points, 'above')
    context.final_set_heat_temp = stat.get_current_set_heat_temp()
    print('The final set heat temp is {0}'.format(context.final_set_heat_temp))
    time.sleep(20)



@then('The set heating temperature should be overridden in the stat')
def check_if_heat_temp_overridden(context):
    message = 'When the device is set to HEAT BOOST mode , The previously set temperature is overridden - (Previously set heat temp was {0} points, Now the heat temperature set to {1} points '
    if context.initial_set_heat_temp != context.final_set_heat_temp:
        assert_with_report(True, context.reporter, message.format(context.initial_set_heat_temp, context.final_set_heat_temp))
    else:
        assert_with_report(False, context.reporter, message.format(context.initial_set_heat_temp, context.final_set_heat_temp))



@then('The set cooling temperature should be overridden in the stat')
def check_if_cool_temp_overridden(context):
    message = 'When the device is set to COOL BOOST mode , The previously set temperature is overridden - (Previously set cool temp was {0} points, Now the cooling temperature set to {1} points '
    if context.initial_set_cool_temp != context.final_set_cool_temp:
        assert_with_report(True, context.reporter, message.format(context.initial_set_cool_temp, context.final_set_cool_temp))
    else:
        assert_with_report(False, context.reporter, message.format(context.initial_set_cool_temp, context.final_set_cool_temp))





@when('the device is in {device_mode} mode and the required temperature is set to {temperature_points:d} points {temp_change_mode} the ambient temperature for {duration:d} minutes')
def set_device_mode_temp_time(context, device_mode, temperature_points, temp_change_mode, duration):
    '''If the current device is in boost mode , Cancel it first '''
    current_mode = context.stat.get_current_mode()
    if current_mode == 'HEAT_BOOST' or current_mode == 'COOL_BOOST':
        print('Boost detected .. Cancelling the same')
        context.stat.cancel_boost()
    set_heat_cool_with_temp_and_time(context, device_mode, temperature_points, temp_change_mode, duration)
    '''
                 Wait for the protection timer to be off
                 Looks like the value is set to 180 when the device is turned on , which will make these 
                 tests run 180 seconds slower in the initial state as it cannot be reliably determined 
                 if the device was turned on the first time or the protection timer is already running !
          '''
    time.sleep(5)
    current_timer_value = context.stat.get_protection_timer_value()
    # Sleep for an extra 5 seconds
    if current_timer_value > 0:
        print('The protection timer is on for {0} seconds , Sleeping until then'.format(current_timer_value))
        time.sleep(current_timer_value + 5)


@when('The heat temperature is overridden by {overide_value:d} points')
def set_heat_temperature(context, overide_value):
    time.sleep(15)
    stat = context.stat
    context.baseline_temp = round(float(stat.get_current_set_heat_temp()))
    log_report(context.reporter, 'The current device set heat temperature is {0}'.format(context.baseline_temp))
    context.set_heat_temp = context.baseline_temp + overide_value
    #Reset the command string
    stat.command_string = ''
    stat.with_heat_set_to_temperature(context.set_heat_temp).set()
    time.sleep(10)
    log_done(context.reporter, "override the heat temperature to {0}. Done. ".format(context.set_heat_temp))

@when('The cool temperature is overridden by {overide_value:d} points')
def set_cooling_temperature(context, overide_value):
    time.sleep(15)
    stat = context.stat
    context.baseline_temp = round(float(stat.get_current_set_cool_temp()))
    log_report(context.reporter, 'The current device set Cooling temperature is {0}'.format(context.baseline_temp))
    context.set_cool_temp = context.baseline_temp - overide_value
    #Reset the command string
    stat.command_string = ''
    stat.with_cooling_set_to_temperature(context.set_cool_temp).set()
    time.sleep(10)
    log_done(context.reporter, "Override the cooling temperature to {0}".format(context.set_cool_temp))

@when('The vacation mode is set for {time_duration_in_minutes:d} minutes from the current stat time')
def set_vacation_mode(context, time_duration_in_minutes):
    time.sleep(20)
    reporter = context.reporter
    stat = context.stat
    log_report(reporter, 'Switching the stat into vacation mode for {0} minutes'.format(time_duration_in_minutes))
    stat.set_holiday_mode(time_duration_in_minutes)
    log_done(reporter, 'The stat is switched to vacation mode')
    #Sleep for 20 seconds
    time.sleep(20)

@then('The vacation mode must be enabled')
def validate_vacation_mode_enabled(context):
    reporter = context.reporter
    stat = context.stat
    current_holiday_mode = stat.get_current_holiday_mode_state()
    if current_holiday_mode == 'ACTIVE':
        assert_with_report(True, reporter, 'The holiday mode is successfully enabled in the stat ')
        stat.cancel_holiday_mode()
    else:
        assert_with_report(False, reporter, 'The device is not successfully toggled into holiday mode')


@when('The vacation mode is cancelled')
def cancel_vacation_mode(context):
    reporter = context.reporter
    stat = context.stat
    current_holiday_mode = stat.get_current_holiday_mode_state()
    if current_holiday_mode == 'ACTIVE':
        log_report(reporter, 'The Holiday mode is active , Attempting to cancel the same ')
        stat.cancel_holiday_mode()
        log_done(reporter, 'Cancelled the holiday mode')
    else :
        log_report(reporter, 'The vacation mode is already inactive , Nothing to be done')



@then('The vacation mode must be disabled')
def validate_vacation_mode_enabled(context):
    reporter = context.reporter
    stat = context.stat
    current_holiday_mode = stat.get_current_holiday_mode_state()
    if current_holiday_mode == 'INACTIVE':
        assert_with_report(True, reporter, 'The holiday mode is disabled in the stat(validated via Zigbee) ')
    else:
        assert_with_report(False, reporter, 'The device is still in holiday mode(Validated via zigbee)')


@then('The cool temperature should be changed by {change_points:d} points')
def check_current_temp(context, change_points):
    current_temperature = round(float(context.stat.get_current_set_cool_temp()))
    message = 'The cooling temperature is overridden by {0} points - From {1} to {2}'.format(change_points ,context.baseline_temp ,context.baseline_temp - change_points)
    current_mode = context.stat.get_current_mode()
    log_report(context.reporter, 'The current device mode is {0} and the current set cooling  temperature is is {1}'.format(current_mode, current_temperature))
    assert_with_report(abs(current_temperature-context.baseline_temp) == change_points, context.reporter, message);


@then('The heat temperature should be changed by {change_points:d} points')
def check_current_heat_temp(context, change_points):
    if change_points == 0:
        log_done(context.reporter, 'Zero change point . Nothing to be done')
        return
    current_temperature = round(float(context.stat.get_current_set_heat_temp()))
    message = 'The temperature is expected to be set to change by {0} point - from {1} to {2}, It was {3}'.format(change_points ,context.baseline_temp ,context.baseline_temp + change_points, current_temperature)
    current_mode = context.stat.get_current_mode()
    log_report(context.reporter, 'The current device mode is {0} and the current set heating temperature is {1}'.format(current_mode, current_temperature))
    if current_mode == 'HEAT_BOOST' or current_mode == 'COOL_BOOST':
        print('Boost detected .. Cancelling the same')
        context.stat.cancel_boost()
    assert_with_report(abs(current_temperature-context.baseline_temp) == change_points, context.reporter, message);

@then('The {heater_cooler_device_state} should be on')
def get_stat_status(context, heater_cooler_device_state):
    time.sleep(15)
    current_stat_state = context.stat.get_stat_state()
    message = "The device state should be {0}".format(heater_cooler_device_state)
    log_report(context.reporter, 'The current state is {0}'.format(current_stat_state.strip()))
    assert_with_report(current_stat_state.strip() == heater_cooler_device_state.strip(), context.reporter, message)
    current_mode = context.stat.get_current_mode()
    if current_mode == 'HEAT_BOOST' or current_mode == 'COOL_BOOST':
        print('Boost detected .. Cancelling the same')
        context.stat.cancel_boost()
    time.sleep(10)

@when('the device is set to dual mode {mode} , with heating set to {heat_temp_points:d} and cooling set to {cool_temp_points:d}')
def set_stat_in_dual_mode(context, mode, heat_temp_points, cool_temp_points):
    if mode != 'DUAL HOLD' and mode != 'DUAL SCHEDULE':
        raise Exception('invalid dual mode {0} only DUAL HOLD or DUAL SCHEDULE allowed'.format(mode))
    stat = context.stat
    log_report(context.reporter, 'The current stat mode is {0} with current heat temperature set to {1}, current cooling temperature set to {2}'.format(stat.get_current_mode(), stat.get_current_set_heat_temp(), stat.get_current_set_cool_temp()))
    stat.withMode(mode).with_heat_set_to_temperature(heat_temp_points).with_cooling_set_to_temperature(cool_temp_points).set()
    log_done(context.reporter, 'Set the stat to {0} with heat temp set to {1}, with cool temp set to {2}'.format(stat.get_current_mode(), stat.get_current_set_heat_temp(), stat.get_current_set_cool_temp()))


@then('the heater should be off')
def check_heater_off(context):
    time.sleep(10)
    current_stat_state = context.stat.get_stat_state()
    message = "The  heater should be off"
    if len(current_stat_state) == 0:
        stat_state_str = 'OFF'
    else:
        stat_state_str = current_stat_state
    log_report(context.reporter, 'The current heater state is {0}'.format(stat_state_str))
    assert_with_report('HEAT' not in current_stat_state , context.reporter, message)

@then('the cooler should be off')
def check_cooler_off(context):
    time.sleep(10)
    current_stat_state = context.stat.get_stat_state()
    message = "The cooler should be off "
    if len(current_stat_state) == 0:
        stat_state_str = 'OFF'
    else:
        stat_state_str = current_stat_state
    log_report(context.reporter, 'The cooler heater state is {0}'.format(stat_state_str))
    assert_with_report('COOL' not in current_stat_state , context.reporter, message)

@then('the protection timer should be on for {value:d} seconds')
def validate_protection_timer_value(context, value):
    protection_timer_value = context.stat.get_protection_timer_value()
    message = "The protection timer should be on for {0} seconds".format(value)
    # The current timer value should be atleast 175 seconds
    log_report(context.reporter, 'The protection timer value is {0}'.format(protection_timer_value))
    assert_with_report(protection_timer_value > value, context.reporter, message)


@then("the device timer should be on for {duration:d} minutes")
def validate_timer_value(context, duration):
    #Sleep for two seconds, There is a time lag for the value to be rendered in the screen
    time.sleep(10)
    timer_value = context.stat.get_current_device_timer_value()
    log_report(context.reporter, 'The device timer value is {0} '.format(timer_value))
    message = "The device timer should atleast be on for {0} minutes ".format(duration)
    assert_with_report(timer_value >= duration, context.reporter, message)

@when("the user cancels quick mode")
def cancel_quick_mode(context):
    stat = context.stat
    current_mode = stat.get_current_mode()
    if current_mode == 'HEAT_BOOST' or current_mode == 'COOL_BOOST':
        stat.cancel_boost()
        log_done(context.reporter, "Cancelled the stat boost mode ")
        #Sleep for a couple of seconds
        time.sleep(2)
    else :
        assert_with_report(False, context.reporter, "Device is not in quick heat/cool mode , Cannot cancel the same")

@then("the {mode} mode should be cancelled")
def check_cancelled_boost_mode(context, mode):
    current_mode = context.stat.get_current_mode()
    assert_with_report((current_mode != 'HEAT_BOOST' or current_mode != 'COOL_BOOST'), context.reporter, "The boost should be cancelled")

@then("the stat should return to the previous state")
def compare_previous_state(context):
    stat = context.stat
    previous_stat_values = context.previous_stat_state_var
    stat_current_mode = stat.get_current_mode()

    log_report(context.reporter, 'The stat previous mode was {0} and the current mode is {1}'.format(previous_stat_values['stat_mode'], stat_current_mode))
    assert_with_report(stat.get_current_mode() == previous_stat_values['stat_mode'], context.reporter,"The stat previous mode is restored once the BOOST is cancelled or completed  ")

    log_report(context.reporter, 'The stat previous heat temp was {0} and the current set heat temp is is {1}'.format(previous_stat_values['stat_heat_temp'], stat.get_current_set_heat_temp()))
    assert_with_report(stat.get_current_set_heat_temp() == previous_stat_values['stat_heat_temp'], context.reporter, "The stat previously set heat temperature is restored when BOOST is cancelled or completed")

    log_report(context.reporter, 'The stat previous cool temp was {0} and the current set cool temp is is {1}'.format(previous_stat_values['stat_cool_temp'], stat.get_current_set_cool_temp()))
    assert_with_report(stat.get_current_set_cool_temp() == previous_stat_values['stat_cool_temp'], context.reporter, "The stat previously set cool temperature is restored when BOOST is cancelled or completed")

@when("the device switches from {initial_mode} to {final_mode}")
def change_device_mode(context, initial_mode, final_mode):
    stat = context.stat
    log_report(context.reporter, 'The device is now in {0}'.format(stat.get_current_mode()))
    context.initial_mode = initial_mode
    context.final_mode = final_mode
    stat.withMode(initial_mode).set()
    stat.withMode(final_mode).set()
    log_done(context.reporter, "Set the stat from {0} to {1}".format(initial_mode, final_mode))

@then("the change to {final_mode} should be successful")
def validate_mode_change(context, final_mode):
    stat = context.stat
    assert_with_report(stat.get_current_mode() == final_mode, context.reporter, "Was able to switch the stat from {0} mode to {1}".format(context.initial_mode, final_mode))

@then('The heat temperature should be {heat_temperature:d}')
def validate_heat_temp(context, heat_temperature):
    stat = context.stat
    stat_temp = round(float(stat.get_current_set_heat_temp()))
    assert_with_report(stat_temp == heat_temperature, context.reporter, 'The current set heat temp is {0}, Expected {1}'.format(stat_temp, heat_temperature))

@then('The cool temperature should be {cool_temperature:d}')
def validate_cool_temp(context, cool_temperature):
    stat = context.stat
    stat_temp = round(float(stat.get_current_set_cool_temp()))
    assert_with_report(stat_temp == cool_temperature, context.reporter, 'The current set cool temp is {0}, Expected {1}'.format(stat_temp, cool_temperature))

@then('the device should be in {expected_mode} mode')
def validate_device_mode(context, expected_mode):
    stat = context.stat
    current_device_mode = stat.get_current_mode()
    assert_with_report(stat.get_current_mode() == expected_mode, context.reporter, 'The current device mode should be {0} , but was {1}'.format(expected_mode, current_device_mode))


@when('The device fan mode is set to {fan_mode}')
def set_stat_fan_mode(context, fan_mode):
    stat = context.stat
    log_report(context.reporter, "The current fan mode is {0}".format(stat.get_fan_mode()))
    stat.set_fan_mode(fan_mode)
    log_done(context.reporter, "set the fan mode to {0}".format(fan_mode))

@when("After the duration of {duration:d} minutes")
def wait_for_duration(context, duration):
    print('Sleeping for {0} minutes'.format(duration))
    log_report(context.reporter, 'The boost has completed ')
    time.sleep(duration*60)
    print('Sleeping completed..')



@then('the device fan should be successfuly set to {expected_mode}')
def validate_fan_mode(context, expected_mode):
    time.sleep(5)
    stat = context.stat
    current_fan_mode = stat.get_fan_mode()
    assert_with_report(current_fan_mode == expected_mode, context.reporter, 'The current fan mode is {0}, expected mode is {1}'
                                                                            ' (validated via Zigbee)'.format(current_fan_mode, expected_mode))



@then('the fan circulate timer should be set to {expected_timer_value:d} mins')
def fan_timer_value(context, expected_timer_value):
    time.sleep(5)
    stat = context.stat
    actual_timer_value = stat.get_circulation_timer_value()
    if int(actual_timer_value) == int(expected_timer_value):
        assert_with_report(True, context.reporter, 'The fan timer is set to {0} mins as expected(validated in Zigbee)'.format(expected_timer_value))
    else:
        assert_with_report(False, context.reporter, 'The fan timer should have been set to {0} mins , but'
                                                    ' was set for {1} mins(validated in zigbee) '.format(expected_timer_value, actual_timer_value))



@then('the device should be switched to emergency mode')
def check_emergency_mode(context):
    stat = context.stat
    current_mode = stat.get_stat_state()
    in_emergency_mode = 'EMERGENCY_HEAT' in current_mode
    stat.cancel_boost()
    assert_with_report(in_emergency_mode, context.reporter, 'The device is triggered to emergency mode {0}'.format(in_emergency_mode))

@when('the device name is set to {device_name}')
def set_stat_name(context, device_name):
    log_report(context.reporter, "the current device name is {0}".format(context.stat.get_device_name()))
    context.stat.set_device_name(device_name)
    log_done(context.reporter, 'Set the device name to {0}'.format(device_name))


@then('the device name should be set to {expected_device_name}')
def validate_device_name(context, expected_device_name):
    time.sleep(5)
    actual_device_name = context.stat.get_device_name()
    assert_with_report(actual_device_name == expected_device_name, context.reporter, 'The device name now is {1}'.format(expected_device_name, actual_device_name))


@then('The device fan should be turned on')
def validate_fan_on(context):
    time.sleep(5)
    current_device_state = context.stat.get_stat_state()
    if 'FAN' in current_device_state:
        assert_with_report(True, context.reporter, 'The device fan is ON')
    else:
        assert_with_report(False, context.reporter, 'The device fan is OFF')



@then('The device fan should be turned off')
def validate_fan_off(context):
    time.sleep(5)
    current_device_state = context.stat.get_stat_state()
    if 'FAN' in current_device_state:
        assert_with_report(False, context.reporter, 'The device fan is ON')
    else:
        assert_with_report(True, context.reporter, 'The device fan is OFF')


@when('The emergency heat precondition has been met')
def check_emergency_precondition(context):
    reporter = context.reporter
    current_device_scale = context.stat.get_current_device_scale()
    log_report(reporter, 'The current device scale is {0}'.format(current_device_scale))
    current_stat_temperature = int(float(context.stat.get_current_temperature()))
    log_report(reporter, 'The ambient temperature is {0}'.format(current_stat_temperature))
    if current_device_scale == 'FAHRENHEIT':
        print('The current decice scale is FAHRENHEIT')
        has_preconditon_met = current_stat_temperature < 77
    else:
        print('The current decice scale is CELCIUS')
        has_preconditon_met = current_stat_temperature < 25

    context.em_heat_precondition = has_preconditon_met

    if has_preconditon_met:
        assert_with_report(True, reporter, 'The device will be able to switch to emergency heat')
        current_system_mode = context.stat.get_current_mode()
        if 'EMERGENCY_HEAT' in current_system_mode:
            log_report(reporter, 'Disabling a previously set emergency heat')
            context.stat.cancel_boost()
    else :
        assert_with_report(False, reporter, 'The device will not be able to switch to emergency heat')

@when('The emergency heat is turned on')
def turn_on_emergency_mode(context):
    reporter = context.reporter
    stat = context.stat
    if context.em_heat_precondition == False:
        log_report(reporter, 'The emergency heat precondition is not met , Cannot turn on the EM heat , Cases may fail')
        return
    stat.enable_emergency_heat()
    log_done(reporter, 'Turned on emergency heat in the stat')


@then('The emergency heat should be enabled')
def check_if_emergency_mode_enabled(context):
    reporter = context.reporter
    current_system_mode = context.stat.get_current_mode()
    log_report(reporter, 'The current system mode is {0}'.format(current_system_mode))
    emergency_heat_enabled = ('EMERGENCY_HEAT' in current_system_mode)
    if emergency_heat_enabled :
        assert_with_report(True, reporter, 'The emergency heat is successfully enabled')
    else:
        assert_with_report(False, reporter, 'The emergency heat is NOT Enabled')


@then('The emergency heat should be disabled')
def check_if_emergency_mode_disabled(context):
    time.sleep(10)
    reporter = context.reporter
    current_system_mode = context.stat.get_current_mode()
    log_report(reporter, 'The current system mode is {0}'.format(current_system_mode))
    emergency_heat_enabled = ('EMERGENCY_HEAT' in current_system_mode)
    if emergency_heat_enabled :
        assert_with_report(False, reporter, 'The emergency heat is Still on !')
    else:
        assert_with_report(True, reporter, 'The  emergency heat is successfully disabled')


@when('The emergency heat is turned off')
def turn_off_em_heat(context):
    stat = context.stat
    current_mode = stat.get_current_mode()
    if 'EMERGENCY_HEAT' in current_mode:
        stat.cancel_boost()
        log_done(context.reporter, "Cancelled the Emergency heat mode")
        # Sleep for a couple of seconds
        time.sleep(2)
    else:
        assert_with_report(False, context.reporter, "Device is not in emergency heat mode , Cannot cancel the same")

@when('The device is rebooted')
def reboot_device(context):
    stat = context.stat
    stat.reboot_device()
    log_done(context.reporter, 'Device is powercycled successfully')


@then('The vacation mode should be shown in the display')
def ocr_check_vacation_mode(context):
    stat = context.stat
    print('The path is {0}'.format(context.reporter.strCurrentScreenshotFolder))
    #Wake up the device
    stat.press_dial()
    #Set the device in heat hold mode and
    #img = ocr_util.captureOriginal()
    img = ocr_util.loadImage('test.jpg', context)
    text = ocr_util.getText(img, context)
    text_values = text.split('\n')
    for i in text_values:
        print('the pbtained text is {0}'.format(i))





@when('The Below {device_mode} is set in {mode} mode')
def set_week_schedule(context, device_mode, mode):
    stat = context.stat
    stat.device_mode=device_mode

    # Get the schedule details in a table
    oSchedDict,boolStandaloneMode=stat.create_week_schdule_table(context, mode)
    # Schedule the events
    stat.set_schedule(oSchedDict, stat.device_mode, boolStandaloneMode)
    # Activate the schedule
    stat.withMode(str(device_mode).upper()).set()
    log_done(context.reporter, "Schedule is set for the mode " + str(device_mode).upper())
    time.sleep(5)

    current_timer_value = context.stat.get_protection_timer_value()
    # Sleep for an extra 20 seconds
    if current_timer_value > 0:
        print('The protection timer is on for {0} seconds , Sleeping until then'.format(current_timer_value))
        time.sleep(current_timer_value + 20)


@then('Verify if the Schedule is set for the whole week in SLT4')
def validate_set_week_schedule(context):
    stat = context.stat
    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Verify the Given Schedule is Set in SLT4")
    stat.validate_week_schedule(context,context.oSchedDict,stat.device_mode)

@then('Verify if the Schedule is set in SLT4')
def validate_schedule(context):
    stat = context.stat

    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Verify the Given Schedule is Set in SLT4")
    current_mode = context.stat.get_current_mode()
    time.sleep(5)
    if current_mode == "HEAT SCHEDULE":
        current_temperature = round(float(context.stat.get_current_set_heat_temp()))
        print('The current target temp is  ' + stat.get_current_set_heat_temp())
    else:
        current_temperature = round(float(context.stat.get_current_set_cool_temp()))
        print('The current target temp is  ' + stat.get_current_set_cool_temp())

    strLog, strStatus=stat.get_schdule_log('Test',stat.device_mode,current_temperature)
    context.reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
    # stat.validate_week_schedule(context,context.oSchedDict,stat.device_mode)

@when('The temperature is overridden by {overide_value:d} points')
def set_override_temperature(context, overide_value):
    time.sleep(15)
    stat = context.stat
    device_mode = stat.device_mode
    context.baseline_cool_temp = round(float(stat.get_current_set_cool_temp()))
    context.baseline_heat_temp = round(float(stat.get_current_set_heat_temp()))

    # Reset the command string
    stat.command_string = ''
    if str(device_mode).upper() == "COOL SCHEDULE":
        log_report(context.reporter, 'The current device set Cool temperature is {0}'.format(context.baseline_cool_temp))
        context.set_cool_temp = context.baseline_cool_temp - overide_value
        stat.with_cooling_set_to_temperature(context.set_cool_temp).set()
        time.sleep(5)
        log_done(context.reporter, "Override the temperature to {0}".format(context.set_cool_temp))

    if str(device_mode).upper() == "HEAT SCHEDULE":
        log_report(context.reporter, 'The current device set Heat temperature is {0}'.format(context.baseline_heat_temp))
        context.set_heat_temp = context.baseline_heat_temp + overide_value
        stat.with_heat_set_to_temperature(context.set_heat_temp).set()
        time.sleep(5)
        log_done(context.reporter, "Override the temperature to {0}".format(context.set_heat_temp))

    elif str(device_mode).upper() == "DUAL SCHEDULE":
        log_report(context.reporter,
                   'The current device set Heat temperature is {0} and Cool temperature is {1}'.format(
                       context.baseline_heat_temp, context.baseline_cool_temp))
        context.set_heat_temp = context.baseline_heat_temp - overide_value
        context.set_cool_temp = context.baseline_cool_temp - overide_value
        stat.withMode(device_mode).with_heat_set_to_temperature(context.set_heat_temp).with_cooling_set_to_temperature(
            context.set_cool_temp).set()
        # stat.with_heat_set_to_temperature(context.set_heat_temp).with_cooling_set_to_temperature(context.set_cool_temp).set()

        log_done(context.reporter, "Override the heat temperature to {0} and Cool temperature to {1} ".format(context.set_heat_temp, context.set_cool_temp))

@then('The temperature should be changed by {change_points:d} points')
def check_current_override_temp(context, change_points):
    time.sleep(5)
    if change_points == 0:
        log_done(context.reporter, 'Zero change point . Nothing to be done')
        return

    current_heat_temperature = round(float(context.stat.get_current_set_heat_temp()))
    current_cool_temperature = round(float(context.stat.get_current_set_cool_temp()))
    current_mode = context.stat.get_current_mode()

    if "HEAT" in current_mode:
        message = 'The heat temperature is expected to be set to change by {0} point - from {1} to {2}, It was {3}'.format(change_points , context.baseline_heat_temp,context.baseline_heat_temp + change_points, current_heat_temperature)
        log_report(context.reporter, 'The current device mode is {0} and the current set heat temperature is {1}'.format(current_mode, current_heat_temperature))
        assert_with_report(abs(current_heat_temperature - context.baseline_heat_temp) == change_points, context.reporter,message)
    elif "COOL" in current_mode:
        message = 'The cool temperature is expected to be set to change by {0} point - from {1} to {2}, It was {3}'.format(change_points, context.baseline_cool_temp, context.baseline_cool_temp - change_points, current_cool_temperature)
        log_report(context.reporter,'The current device mode is {0} and the current set cool temperature is {1}'.format(current_mode,current_cool_temperature))
        assert_with_report(abs(current_cool_temperature - context.baseline_cool_temp) == change_points, context.reporter,message)
    elif "DUAL" in current_mode:
        message1 = 'The heat temperature is expected to be set to change by {0} point - from {1} to {2}, It was {3}'.format(change_points, context.baseline_heat_temp, context.baseline_heat_temp - change_points,current_heat_temperature)
        message2 = 'The cool temperature is expected to be set to change by {0} point - from {1} to {2}, It was {3}'.format(change_points, context.baseline_cool_temp, context.baseline_cool_temp - change_points, current_cool_temperature)
        log_report(context.reporter,'The current device mode is {0} and the current set heat temperature is {1}'.format(current_mode,current_heat_temperature))
        log_report(context.reporter,'The current device mode is {0} and the current set cool temperature is {1}'.format(current_mode,current_cool_temperature))
        assert_with_report(abs(current_heat_temperature - context.baseline_heat_temp) == change_points,context.reporter, message1)
        assert_with_report(abs(current_cool_temperature - context.baseline_cool_temp) == change_points, context.reporter,message2)


@when('Below events are {strOpr} from the schedule')
def delete_add_events(context,strOpr):
    stat=context.stat
    device_mode=stat.get_current_mode()
    oSchedDict=stat.delete_add_event_schedule(context,strOpr)
    if str(strOpr).upper()=="ADDED":
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Below events are added from the schedule")
    elif str(strOpr).upper() == "DELETED":
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Below events are deleted from the schedule")
    stat.set_schedule(oSchedDict, device_mode)
    # Activate the schedule
    stat.withMode(str(device_mode).upper()).set()
    log_done(context.reporter, "Events "+ strOpr +" and schedule is updated successfully " + str(device_mode).upper())
    time.sleep(5)

@then('Verify the events before and after change')
def check_schedule_before_after(context):

    strDay = context.strDay
    beforeChange=context.beforeChange
    afterChange = context.newList
    log_done(context.reporter, "The total timeslot of schedule before change is " + str(len(beforeChange)))
    log_done(context.reporter, "The timeslot of schedule before change are " + str(beforeChange))

    log_done(context.reporter, "The total timeslot of schedule after change is " + str(len(afterChange)))
    log_done(context.reporter, "The timeslot of schedule after change are " + str(afterChange))
    log_done(context.reporter, "The change in timeslot of schedule are " + str(context.oDelSchedList))

@when('Above events are to be copied for {days}')
def copy_schedule_to_other_days(context,days):
    stat=context.stat
    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Above events are to be copied for" + days)
    oSchedDict=stat.copy_event_schedule(context,days)

    stat.set_schedule(oSchedDict, stat.device_mode)
    # Activate the schedule
    stat.withMode(str(stat.device_mode).upper()).set()
    log_done(context.reporter, "Schedule is set for the mode " + str(stat.device_mode).upper())
    time.sleep(5)


@then('Verify the schedule is copied to the mentioned days')
def verify_schedule_after_copy(context):
    strDay = context.strDay
    beforeCopy = context.beforeCopy[strDay]
    afterCopy = context.oSchedDict
    context.reporter.HTML_TC_BusFlowKeyword_Initialize("Verify the schedule is copied to the mentioned days")
    log_done(context.reporter, "Schedule is set as below before copy")
    log_done(context.reporter, "For " + str(strDay).upper() +' , The Events are'+str(beforeCopy))
    log_done(context.reporter, "Schedule is set as below after copy & No of Days are " + str(len(afterCopy)))
    for val in afterCopy:
        log_done(context.reporter, "For " + str(val).upper() +' , The Events are '+str(afterCopy[val]))

