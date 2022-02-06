import FF_device_utils as device_utils
import FF_SLT4
import time
import FF_timeClusterTest as timeutil

class ScreenUtil(object):


    SCREEN_PATHS = {
        'HOME_SCREEN': 'MENU;MENU;BACK',
        'MENU_SCREEN': 'MENU;MENU',
        'HEAT_SCREEN': 'MENU;MENU;DIALROTATE-CLOCKWISE-0',
        'COOL_SCREEN': 'MENU;MENU;DIALROTATE-CLOCKWISE-1',
        'DUAL_SCREEN': 'MENU;MENU;DIALROTATE-CLOCKWISE-2',
        'EM_SCREEN'  : 'MENU;MENU;DIALROTATE-CLOCLWISE-3',
        'OFF_SCREEN' : 'MENU;MENU;DIALROTATE-CLOCKWISE-4',
        'MORE_SCREEN': 'MENU;MENU;DIALROTATE-CLOCKWISE-5'
    }


    SUB_MENU_PATHS = {
        'HOLD_SUBMENU' : 'DIAL_PRESS;DIAL_PRESS',
        'SCHEDULE_SUBMENU': 'DIALROTATE-CLOCKWISE-1;DIAL_PRESS',
        'DUAL_HOLD_SUBMENU' : 'DIAL_PRESS',
        'EM_HEAT_ON' : 'DIAL_PRESS',
        'EM_HEAT_OFF':'DIAL_PRESS;DIALROTATE-CLOCKWISE-1',
        'START_OVER_SUBMENU' :'DIALROTATE-CLOCKWISE-1;DIALROTATE-CLOCKWISE-1;DIAL_PRESS'
    }


    MORE_SUBMENU = {
        'FAN'  :'DIAL_PRESS',
        'HUMIDITY': 'DIALROTATE-CLOCKWISE-1',
        'DISPLAY': 'DIALROTATE-CLOCKWISE-2',
        'SETUP': 'DIALROTATE-CLOCKWISE-3'
    }


    SETUP_SUBMENU = {
        'SYSTEM_TYPE' : '',
        'ACC_TYPE' : 'DIALROTATE-CLOCKWISE-1'
    }

    ACC_SUBMENU = {
        'HUMIDIFIER' : '',
        'DEHUMIDIFIER' : 'DIALROTATE-CLOCKWISE-1'
    }

    SCH_SUBMENU = {
        'MON' : '',
        'TUE' : 'DIALROTATE-CLOCKWISE-1',
        'WED': 'DIALROTATE-CLOCKWISE-2',
        'THU': 'DIALROTATE-CLOCKWISE-3',
        'FRI': 'DIALROTATE-CLOCKWISE-4',
        'SAT': 'DIALROTATE-CLOCKWISE-5',
        'SUN': 'DIALROTATE-CLOCKWISE-6'
    }
    SCHEDULE_SLOT={
        'HEAT_C':'21.0;16.0;16.0;16.0;21.0;16.0',
        'COOL_C':'26;30;30;30;26;28',
        'HEAT_F':'70.0;62.0;62.0;62.0;70.0;62.0',
        'COOL_F':'78.0;85.0;85.0;85.0;78.0;82.0'
    }

    CELCIUS_DIAL_FACTOR = 2

    def __init__(self, slt4_instance):
        self.slt4_instance = slt4_instance
        self.node_id = slt4_instance.get_device_node_id()
        self.end_point = slt4_instance.get_device_endpoint()


    def _does_have_em(self):
        has_em = False
        wiring_state = self.slt4_instance.get_stat_wiring_state()
        print('The wiring state is {0}'.format(wiring_state))
        if 'W1' and 'W3' in wiring_state:
            has_em = True
        elif 'W1' and 'O/B' in wiring_state:
            has_em = True
        return has_em



    def _navigate_step(self, navigation_step):
        print('Handling the step {0}'.format(navigation_step))
        if 'DIALROTATE' in navigation_step.upper():
            print('Dial rotate action located')
            split_steps = navigation_step.split('-')
            rotation_direction = split_steps[1]
            rotation_units = split_steps[2]
            if self._does_have_em() == False and int(rotation_units) >= 4:
                rotation_units = int(rotation_units) -1
            device_utils.rotateDial_SLT4(self.node_id, self.end_point,rotation_direction, rotation_units)
            self.slt4_instance.press_dial()
        elif 'DIAL_PRESS' in navigation_step:
            print('Dial press action located')
            self.slt4_instance.press_dial()
        else:
            print('Button action located')
            device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, navigation_step, 'PRESS')


    def navigate_to(self, screen_name):
        stat_mode = self.slt4_instance.get_current_mode()
        if 'BOOST' in stat_mode:
            self.slt4_instance.cancel_boost()
            time.sleep(5)
        navigation_path = self.SCREEN_PATHS[screen_name]
        if navigation_path == None:
            raise Exception('Invalid screen {0}- The screen does not exist'.format(screen_name))
        for navigation_step in navigation_path.split(';'):
            self._navigate_step(navigation_step)



    def navigate_to_submenu(self, submenu_name, submenu_holder = None):
        if submenu_holder == None:
            navigation_path = self.SUB_MENU_PATHS[submenu_name]
        else:
            navigation_path = submenu_holder[submenu_name]
        if navigation_path == None:
            raise Exception('Invalid Submenu {0}- The Submenu does not exist'.format(submenu_name))
        if len(navigation_path) == 0:
            print('Dummy step , Returning')
            return
        for navigation_step in navigation_path.split(';'):
            self._navigate_step(navigation_step)


    def _set_device_temp_using_dial(self, initial_temperature , target_temperature):
        if target_temperature  == -100:
            print('The target is -100, Ignoring the dial turns ')
            return

        print('The initial temperature is {0} and the final temperature is {1}'.format(initial_temperature, target_temperature))
        device_scale = self.slt4_instance.get_current_device_scale()
        if device_scale == 'CELCIUS':
            resolution = 0.5
        else:
            resolution = 1
        temp_to_set = target_temperature - float(initial_temperature)
        print('The temperature to set {0}'.format(temp_to_set))
        if temp_to_set > 0 :
            rotation_direction = 'CLOCKWISE'
        else :
            rotation_direction = 'ANTICLOCKWISE'

        number_of_turns = abs(temp_to_set)/resolution
        print('The number of turns needed is {0}'.format(number_of_turns))
        device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, number_of_turns)


    def _set_device_boost_duration(self, configured_timer_value, needed_time_in_hours):
        rounded_off_value = round(configured_timer_value/60)
        rotation_units = needed_time_in_hours - rounded_off_value
        if rotation_units > 0 :
            rotation_direction = 'CLOCKWISE'
        else:
            rotation_direction = 'ANTICLOCKWISE'

        device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, abs(rotation_units))



    def change_heat_temperature(self, target_temperature):
        self.navigate_to('HOME_SCREEN')
        initial_temperature = self.slt4_instance.get_current_set_heat_temp()
        self._set_device_temp_using_dial(initial_temperature, target_temperature)

    def change_heat_without_cancelling(self, target_temperature):
        initial_temperature = self.slt4_instance.get_current_set_heat_temp()
        self._set_device_temp_using_dial(initial_temperature, target_temperature)

    def change_cool_without_cancelling(self, target_temperature):
        initial_temperature = self.slt4_instance.get_current_set_cool_temp()
        self._set_device_temp_using_dial(initial_temperature, target_temperature)


    def change_cool_temperature(self, target_temperarture):
        self.navigate_to('HOME_SCREEN')
        initial_temperature = self.slt4_instance.get_current_set_cool_temp()
        self._set_device_temp_using_dial(initial_temperature, target_temperarture)



    def find_default_cool_boost_values(self):
        self.navigate_to('HOME_SCREEN')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TOP LEFT', 'PRESS')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')
        time.sleep(5)
        cool_temp = self.slt4_instance.get_current_set_cool_temp()
        timer_value = self.slt4_instance.get_current_device_timer_value()
        self.slt4_instance.cancel_boost()
        return cool_temp, timer_value

    def find_default_heat_boost_values(self):
        self.navigate_to('HOME_SCREEN')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TOP RIGHT', 'PRESS')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')
        time.sleep(5)
        heat_temp = self.slt4_instance.get_current_set_heat_temp()
        timer_value = self.slt4_instance.get_current_device_timer_value()
        self.slt4_instance.cancel_boost()
        return heat_temp, timer_value



    def set_heat_boost(self, target_temperature, target_duration = 0):
        initial_temperature, initial_duration = self.find_default_heat_boost_values()
        print('The initial temp and duration are {0}, {1}'.format(initial_temperature, initial_duration))
        time.sleep(5)
        self.navigate_to('HOME_SCREEN')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TOP RIGHT', 'PRESS')
        self._set_device_temp_using_dial(initial_temperature, target_temperature)
        self.slt4_instance.press_dial()
        self._set_device_boost_duration(initial_duration, target_duration)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')


    def set_cool_boost(self, target_temperature, target_duration = 0):
        initial_temperature, initial_duration = self.find_default_cool_boost_values()
        print('The initial temp and duration are {0}, {1}'.format(initial_temperature, initial_duration))
        time.sleep(5)
        self.navigate_to('HOME_SCREEN')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TOP LEFT', 'PRESS')
        self._set_device_temp_using_dial(initial_temperature, target_temperature)
        self.slt4_instance.press_dial()
        self._set_device_boost_duration(initial_duration, target_duration)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')


    def _determine_heat_hold_point(self):
        self.slt4_instance.withMode('HEAT HOLD').set()
        time.sleep(5)
        return self.slt4_instance.get_current_set_heat_temp()

    def _determine_cool_hold_point(self):
        self.slt4_instance.withMode('COOL HOLD').set()
        time.sleep(5)
        return self.slt4_instance.get_current_set_cool_temp()



    def set_to_heat_hold(self, temperature_value):
        self.navigate_to('HEAT_SCREEN')
        self.navigate_to_submenu('HOLD_SUBMENU')
        current_displayed_value = self._determine_heat_hold_point()
        print('The current temp is {0}'.format(current_displayed_value))
        self._set_device_temp_using_dial(current_displayed_value, temperature_value)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")


    def set_device_off(self):
        print('Turning the device to off')
        self.navigate_to('OFF_SCREEN')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")



    def set_to_cool_hold(self, temperature_value):
        print('Setting the device to cool hold mode')
        self.navigate_to('COOL_SCREEN')
        self.navigate_to_submenu('HOLD_SUBMENU')
        current_displayed_value = self._determine_cool_hold_point()
        print('The current temp is {0}'.format(current_displayed_value))
        self._set_device_temp_using_dial(current_displayed_value, temperature_value)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")

    def set_device_to_heat_schedule(self):
        self.navigate_to('HEAT_SCREEN')
        self.navigate_to_submenu('SCHEDULE_SUBMENU')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")


    def set_device_to_cool_schedule(self):
        self.navigate_to('COOL_SCREEN')
        self.navigate_to_submenu('SCHEDULE_SUBMENU')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")


    def _determine_dual_setpoint(self):
        self.slt4_instance.withMode('DUAL HOLD').set()
        time.sleep(5)
        set_heat_temp = self.slt4_instance.get_current_set_heat_temp()
        set_cool_temp = self.slt4_instance.get_current_set_cool_temp()
        return set_heat_temp, set_cool_temp


    def set_device_dual_hold(self, heat_target_tempetrature, cool_target_temperature):
        heat_setpoint, cool_setpoint = self._determine_dual_setpoint()
        print('The current heat and cool set points are {0}, {1}'.format(heat_setpoint, cool_setpoint))
        self.navigate_to('DUAL_SCREEN')
        self.navigate_to_submenu('DUAL_HOLD_SUBMENU')
        self._set_device_temp_using_dial(heat_setpoint, heat_target_tempetrature)
        self.slt4_instance.press_dial()
        self._set_device_temp_using_dial(cool_setpoint, cool_target_temperature)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")

    def set_device_dual_schedule(self):
        self.navigate_to('DUAL_SCREEN')
        self.navigate_to_submenu('SCHEDULE_SUBMENU')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")



    def set_device_to_mode(self, device_mode, heat_target=0, cool_target=0, duration = 0):
        if device_mode == 'HEAT HOLD':
            self.set_to_heat_hold(heat_target)
        elif device_mode == 'COOL HOLD':
            self.set_to_cool_hold(cool_target)
        elif device_mode == 'HEAT_BOOST':
            self.set_heat_boost(heat_target, duration)
        elif device_mode == 'COOL_BOOST':
            self.set_cool_boost(cool_target, duration)
        elif device_mode == 'HEAT SCHEDULE':
            self.set_device_to_heat_schedule()
        elif device_mode == 'COOL SCHEDULE':
            self.set_device_to_cool_schedule()
        elif device_mode == 'DUAL HOLD':
            self.set_device_dual_hold(heat_target, cool_target)
        elif device_mode == 'DUAL SCHEDULE':
            self.set_device_dual_schedule()
        elif device_mode == 'OFF':
            self.set_device_off()
        else:
            raise Exception('Invalid device mode {0}'.format(device_mode))


    def turn_on_em_heat(self):
        if self.slt4_instance.is_emergency_heat_wired() == False:
            print('The EM is not WIRED , Cannot turn on the emergency mode ')
        temp_scale = self.slt4_instance.get_current_device_scale()
        current_local_temp = int(self.slt4_instance.get_current_temperature())
        if temp_scale == 'CELCIUS' and current_local_temp  >= 25:
            print('THE LOCAL TEMP is MORE THAN 25 degrees {0} , Cannot enable EM '.format(current_local_temp))
            return
        elif current_local_temp >= 77:
            print('THE LOCAL TEMP is MORE THAN 77 degrees {0} , Cannot enable EM '.format(current_local_temp))
            return
        self.navigate_to('EM_SCREEN')
        self.navigate_to_submenu('EM_HEAT_ON')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")




    def turn_off_em_heat(self):
        if self.slt4_instance.is_emergency_heat_wired() == False:
            print('The EM is not WIRED , Cannot turn off the emergency mode ')
        self.navigate_to('EM_SCREEN')
        self.navigate_to_submenu('EM_HEAT_OFF')
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")

    def set_humidity_type(self, humidity_type):
        if humidity_type == 'HUMIDIFIER' or humidity_type == 'DEHUMIDIFIER':
            self.navigate_to('MORE_SCREEN')
            self.navigate_to_submenu('SETUP', self.MORE_SUBMENU)
            self.navigate_to_submenu('ACC_TYPE', self.SETUP_SUBMENU)
            current_humidity_control_type = self.slt4_instance.get_current_humidity_control_type()
            if current_humidity_control_type == 'HUMIDIFIER':
                self.ACC_SUBMENU['HUMIDIFIER']  =''
                self.ACC_SUBMENU['DEHUMIDIFIER'] = 'DIALROTATE-CLOCKWISE-1'
            else:
                self.ACC_SUBMENU['HUMIDIFIER'] = 'DIALROTATE-ANTICLOCKWISE-1'
                self.ACC_SUBMENU['DEHUMIDIFIER'] = ''

            self.navigate_to_submenu(humidity_type, self.ACC_SUBMENU)
        else:
            print('The ACC type should be either humidifier or dehumidifier')



    def set_humidity_percentage_in_dial(self, target_humidity_percent):
        if target_humidity_percent % 5 != 0:
            print('The target humidity percent should be multiples of 5 ')
        self.navigate_to('MORE_SCREEN')
        self.navigate_to_submenu('HUMIDITY', self.MORE_SUBMENU)
        current_humidity_percentage = self.slt4_instance.get_humidity_percentage()
        '''Humidity values start from 30 % and go up '''
        if current_humidity_percentage ==0 :
            device_utils.rotateDial_SLT4(self.node_id, self.end_point, 'CLOCKWISE', 1)
            current_humidity_percentage = 30
        delta = target_humidity_percent - current_humidity_percentage
        print('The current humidity percentage is {0}'.format(current_humidity_percentage))
        print('The delta is {0}'.format(delta))
        resolution = 5
        rotation_direction = 'CLOCKWISE'
        if delta < 0:
            rotation_direction = 'ANTICLOCKWISE'
        delta = abs(delta)
        number_of_turns = delta/resolution
        print('The number of turns needed is {0} in {1}'.format(resolution, rotation_direction))
        device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, number_of_turns)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')



    def _determine_fan_selector_index(self, fan_mode):
        if fan_mode == 'AUTO':
            return 0
        if fan_mode =='ALWAYS_ON':
            return 1
        if fan_mode == 'CIRCULATE':
            return 2
        raise Exception('Invalid fan mode {0}'.format(fan_mode))



    def determine_rot_dir_for_circulation_timer(self, target_value):
        rotation_direction = 'CLOCKWISE'
        current_timer_offset = self.slt4_instance.get_circulation_timer_value()/15
        print('The current timer offset is {0}'.format(current_timer_offset))
        target_timer_offset = target_value/15
        rotation_needed = target_timer_offset - current_timer_offset
        if rotation_needed < 0:
            rotation_direction = 'ANTICLOCKWISE'
        return rotation_direction, abs(rotation_needed)

    def set_device_fan_state(self, target_fan_mode, target_mins = 15):
        print('The target fan mode is {0}'.format(target_fan_mode))
        if target_mins not in [15, 30, 45]:
            raise Exception('The target mins should be in 15 , 30 or 45')
        is_fan_wired = self.slt4_instance.is_fan_wired()
        if is_fan_wired is True:
            if (target_fan_mode == 'AUTO') or (target_fan_mode == 'CIRCULATE') or (target_fan_mode == 'ALWAYS_ON'):
                self.navigate_to('MORE_SCREEN')
                self.navigate_to_submenu('FAN', self.MORE_SUBMENU)
                current_fan_mode = self.slt4_instance.get_fan_mode()
                print('The current fan mode is {0}'.format(current_fan_mode))
                current_fan_selector_index = self._determine_fan_selector_index(current_fan_mode)
                target_fan_selector_index = self._determine_fan_selector_index(target_fan_mode)
                rotation_needed =  target_fan_selector_index - current_fan_selector_index
                rotation_direction = 'CLOCKWISE'
                if rotation_needed < 0:
                    rotation_direction = 'ANTICLOCKWISE'
                rotation_needed = abs(rotation_needed)
                print("The rotation units needed is {0} and is in {1}".format(rotation_needed, rotation_direction))
                device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, rotation_needed)
                self.slt4_instance.press_dial()
                if target_fan_mode is 'CIRCULATE':
                    direction, num_of_rotation = self.determine_rot_dir_for_circulation_timer(target_mins)
                    device_utils.rotateDial_SLT4(self.node_id, self.end_point, direction, num_of_rotation)
                device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, 'TICK', 'PRESS')
                return
            else:
                raise Exception('Invalid target fan mode (only AUTO, ALWAYS_ON and CIRCULATE allowed')


    '''UI Schedule Functions'''

    def set_start_over_schedule(self,device_mode, schedule):
        schedule_slots=''
        temp_scale = self.slt4_instance.get_current_device_scale()
        if str(device_mode).upper() == "HEAT SCHEDULE":
            self.navigate_to('HEAT_SCREEN')
            if temp_scale == 'CELCIUS':
                schedule_slots = self.SCHEDULE_SLOT['HEAT_C'].split(';')
            else:
                schedule_slots = self.SCHEDULE_SLOT['HEAT_F'].split(';')
        elif str(device_mode).upper() == "COOL SCHEDULE":
            self.navigate_to('COOL_SCREEN')
            if temp_scale == 'CELCIUS':
                schedule_slots = self.SCHEDULE_SLOT['COOL_C'].split(';')
            else:
                schedule_slots = self.SCHEDULE_SLOT['COOL_F'].split(';')
        self.navigate_to_submenu('START_OVER_SUBMENU')
        for day in schedule:
            print('initiating pgm to select day')
            self.get_day(day)
            print('day is selected')
        time.sleep(3)
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")
        time.sleep(5)

        for day in schedule:
            print('Initiating to select the timeslot for the day - {0}'.format(day))
            self.generate_schedule_timeslot(schedule[day], schedule_slots)
            if str(device_mode).upper() == "COOL SCHEDULE":
                device_utils.rotateDial_SLT4(self.node_id, self.end_point, 'CLOCKWISE', 1) # Move the cursor to set cool schedule
            self.slt4_instance.press_dial()  # Press Dialer to select Heat / Cool Schedule

            print('Timeslot for the day is set') #There is an issue in selecting the day by dialer press & rotate


    def generate_schedule_timeslot(self,schedule_day,schedule_slots):
        time_pointer = 6 * 4 # Default timeslot to begin is 6 AM - Convert to slot

        print('The current default schedule slot'+str(schedule_slots))

        cntr=0
        for event in schedule_day:
            #Get the schedule slot in sequence
            temp_scale = self.slt4_instance.get_current_device_scale()
            temp_pointer=float(schedule_slots[cntr])
            if temp_scale == 'CELCIUS':
                temp_pointer=float(temp_pointer) * self.CELCIUS_DIAL_FACTOR # For celcius - 2 dial turn require for 1 degree turn

            #Get the user entered timeslot for the day
            timeslot=event[0]
            timeslot=timeutil.timeStringToMinutes(timeslot)
            dial_turn_temp=float(event[1])
            print(event[0], dial_turn_temp)

            dial_turn_time=timeslot/15
            if temp_scale == 'CELCIUS':
                dial_turn_temp=dial_turn_temp * self.CELCIUS_DIAL_FACTOR # For celcius - 2 dial turn require for 1 degree turn
            dial_turn_temp=float(dial_turn_temp)
            time.sleep(3)
            if cntr > 1:
                self.slt4_instance.press_dial() # To select Yes in the dialog to add more time slot

            if cntr!=0: # To remove the default 1 hour time selection for next timeslot
                time_pointer=time_pointer + 4
                print('Increased the time pointer by 4 ~ Default 1 Hr gap for next slot')

            # Set the time slot for the day
            time_rotation_needed = dial_turn_time - time_pointer
            print('The current time pointer is ' + str(time_pointer) + ' and dial turn required is ' + str(dial_turn_time))
            print('The number of dial turns needed to set time to '+ str(event[0]) +' is '+ str(time_rotation_needed))
            rotation_direction = 'CLOCKWISE'
            if time_rotation_needed < 0:
                rotation_direction = 'ANTICLOCKWISE'
            time_pointer = time_pointer + time_rotation_needed
            time_rotation_needed = abs(time_rotation_needed)
            print('The number of dial turns needed to set time to ' + str(event[0]) + ' is ' + str(time_rotation_needed))
            device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, time_rotation_needed - 1)
            self.slt4_instance.press_dial()

            # Set the temp for the time slot
            temp_rotation_needed = dial_turn_temp - temp_pointer
            print('current schedule temp is ' + str(schedule_slots[cntr]) + ' and its temp_pointer= ' + str(temp_pointer))
            print('The number of dial turns needed to set temp to ' + str(event[1]) + ' is ' + str(temp_rotation_needed))
            rotation_direction = 'CLOCKWISE'
            if temp_rotation_needed < 0:
                rotation_direction = 'ANTICLOCKWISE'
            temp_pointer = temp_pointer + temp_rotation_needed
            temp_rotation_needed = abs(temp_rotation_needed)
            print('The number of dial turns needed to set temp to ' + str(event[1]) + ' is ' + str(temp_rotation_needed))
            device_utils.rotateDial_SLT4(self.node_id, self.end_point, rotation_direction, temp_rotation_needed - 1)
            self.slt4_instance.press_dial()
            cntr=cntr+1

        if cntr < 6: # If user exits before 6 time slot - UI need to select NO
            device_utils.rotateDial_SLT4(self.node_id, self.end_point, 'CLOCKWISE', 1)
            self.slt4_instance.press_dial()  # Press Dialer to select  Schedule

        # Press Tick to confirm the schedule for the day
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")
        time.sleep(7)
        self.slt4_instance.press_dial() # Press Dialer to confirm the schedule for all day
        time.sleep(3)
        # Press Tick to confirm the schedule for all 7 day
        device_utils.pressSLT4DeviceButton(self.node_id, self.end_point, "TICK", "PRESS")
        time.sleep(7)

    def get_day(self,val):
        if str(val).upper() == 'MON':
            self.navigate_to_submenu('MON', self.SCH_SUBMENU)
        elif str(val).upper() == 'TUE':
            self.navigate_to_submenu('TUE', self.SCH_SUBMENU)
        elif str(val).upper() == 'WED':
            self.navigate_to_submenu('WED', self.SCH_SUBMENU)
        elif str(val).upper() == 'THU':
            self.navigate_to_submenu('THU', self.SCH_SUBMENU)
        elif str(val).upper() == 'FRI':
            self.navigate_to_submenu('FRI', self.SCH_SUBMENU)
        elif str(val).upper() == 'SAT':
            self.navigate_to_submenu('SAT', self.SCH_SUBMENU)
        elif str(val).upper() == 'SUN':
            self.navigate_to_submenu('SUN', self.SCH_SUBMENU)
        else:
            raise Exception('Invalid date is entered')

'''Sample test scenarios'''
if __name__ == "__main__":
    stat = FF_SLT4.SLT4('FAHRENHEIT')
    print(round(float(stat.get_current_temperature()), 1))
    stat.withMode('DUAL HOLD').set()
    navigator = ScreenUtil(stat)
    navigator.set_device_fan_state('AUTO', target_mins = 15)
    time.sleep(5)
    print(stat.get_fan_mode())










