import FF_device_utils as dutils
import FF_zigbeeClusters as device_clusters
import FF_threadedSerial as AT
import FF_zigbeeToolsConfig as config
import time
import datetime
import FF_timeClusterTest as timeutil
import FF_device_utils as device_utils
from datetime import datetime as dt
import FF_convertTimeTemperature as conv
from datetime import timedelta


"""
    Class representing the SLT4 thermostat . This uses a fluent pattern to enable the user to set the stat to the required values 
    The SLT4 stat has different wiring configurations and also provides the user to set the temperature to Farenheit or celcuis . 
    It is presumed that the user hardwires the configuration and uses this class for reading / writing the stat attributes 

    For example the below sample code illustrates the use ( Assuming that the stat us set in Celcuis mode)  

        stat = SLT4('CELCIUS')
        - To Set the stat to Cool boost (21 degrees) for 2 minutes 
                stat.withMode('COOL_BOOST').for_time(2).with_cooling_set_to_temperature(21).set()
            - It should be noted that the call to set has to be made to execute the zigbee command
        - To read the current temperature 
                stat.get_current_temperature()

    To stop the threads the call to shutdown_device has to be made

    Please note that this is a version in progress and might be updated frequently . 

    Also THIS CLASS IS NOT THREAD SAFE  


     - TODOs 
        - Implement Humidifier measurememt 
        - Implement device schedule and related configurations
        - Implement functionality to read the hardwired device state . Pending with Jira DE-545 


"""


class SLT4(object):
    ''' The Global device ID '''
    device_id = 'SLT4_1'
    ''' The device end point '''
    DEVICE_ENDPOINT = '05'
    '''The stat cluser'''
    THERMOSTAT_CLUSTER = '0201'
    '''The mcode used to read the manufacturer attribute'''
    MANUFACTURER_CODE = '1039'
    ''' The custom cluster for SLT4'''
    MANUFACTURER_CUSTOM_CLUSTER = 'FD01'
    ''' The stat UI cluster '''
    STAT_UI_CLUSTER = '0204'
    STAT_HUMIDIFIER_CLUSTER = '0203'

    MANUFACTURER_CLUSTER_ATTRIBUTES = {
        'PROTECTION_TIMER': '0021',
        'WIRING_CONNECTION': '0036',
        'HUMIDIFICATION_CONTROL': '0032'
    }

    ''' The user modes that will be used to interact with the stat in the test cases'''
    USER_MODES = {
        'OFF': 0,
        'HEAT HOLD': 1,
        'HEAT SCHEDULE': 2,
        'COOL HOLD': 3,
        'COOL SCHEDULE': 4,
        'DUAL HOLD': 5,
        'DUAL SCHEDULE': 6,
        'HEAT_BOOST': 7,
        'COOL_BOOST': 8
    }

    '''Constants for various mode switch '''
    DEVICE_MODE = {
        "OFF": "00",
        "DUAL": "01",
        "COOL": "03",
        "HEAT": "04",
        "EMERGENCY_HEAT": "05",
        "HEAT_BOOST": "14",
        "COOL_BOOST": "13"
    }

    '''Fan Modes'''
    FAN_MODE = {
        'AUTO': '05',
        'ALWAYS_ON': '04',
        'CIRCULATE': '07'
    }

    ''' Constants indicating the device Schedule type and mode '''
    DEVICE_SCHEDULE_TYPE = {
        'HOLD': '01',
        'SCHEDULE': '00'
    }

    DEVICE_CLUSTER_ATTRIBUTES = {
        'MODE': '001C',
        'SCHEDULE_OR_HOLD': '0023',
        'DURATION': '0024',
        'HEAT_TEMP': '0012',
        'COOL_TEMP': '0011',
        'LOCAL_TEMP': '0000',
        'STAT_RUNNING_STATE': '0029',
        'MIN_COOL_TEMP': '0005',
        'MAX_COOL_TEMP': '0006',
        'MIN_HEATING_TEMP': '0003',
        'MAX_HEATING_TEMP': '0004'

    }

    TEMPERATURE_MODE = {
        'FAHRENHEIT': 0,
        'CELCIUS': 1
    }

    DEVICE_UI_ATTRIBUTES = {
        'TEMPERATURE_SCALE': '0000'
    }
    sch_days = {'sun': '01', 'mon': '02', 'tue': '04', 'wed': '08', 'thu': '10', 'fri': '20', 'sat': '40'}
    oWeekDay = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

    def __init__(self, temperature_mode):
        deviceNodeInfo = dutils.getDeviceNode(self.device_id)
        if deviceNodeInfo == None:
            raise Exception(
                'Unable to locate an SLT4 device paired with the node , Please verify if the device is paired')
        self.deviceNodeId = deviceNodeInfo['nodeID']
        self.device_macId = deviceNodeInfo['macID']
        self.command_string = ''
        self.prior_command_string = ''
        print("Identified the device {} at the endpoint {}".format(self.deviceNodeId, self.device_macId))
        self.AT = AT
        ''' Start the threads '''
        try:
            self.AT.stopThreads()
            self.AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
        except:
            self.AT.startSerialThreads(config.PORT, config.BAUD, printStatus=AT.debug, rxQ=True, listenerQ=True)
        self.set_device_scale(temperature_mode)



    ''' Private / internal methods'''

    def _build_command(self):
        return "at+writeatr:{0},{1},{2},{3}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', self.command_string)

    def set_device_scale(self, temperature_mode):
        self.device_temp_scale = self.TEMPERATURE_MODE[temperature_mode]
        if self.device_temp_scale is None:
            raise Exception('Please select if the device is set in Farenheit or degree celcuis')
        command_string = '{0},{1},{2}'
        temp_cluster_attr = self.DEVICE_UI_ATTRIBUTES['TEMPERATURE_SCALE']
        attribute_type = device_clusters.thermostatUiClusterAttrs[temp_cluster_attr]['type']
        if self.device_temp_scale == 0:
            command_string = command_string.format(temp_cluster_attr, attribute_type, '01')
        else:
            command_string = command_string.format(temp_cluster_attr, attribute_type, '00')
        command_string = "at+writeatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                  self.STAT_UI_CLUSTER, command_string)
        expectedResponse = [
            'WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.STAT_UI_CLUSTER)]
        self.AT.sendCommand(command_string, expectedResponse)

    def _get_thermostat_cluster_attr(self, attribute_identifier, attribute_name):
        return device_clusters.thermostatClusterAttrs[attribute_identifier][attribute_name]

    def _get_command_string(self, cluster_attribute_id, value):
        command_string = '{0},{1},{2}'
        attribute_type = device_clusters.thermostatClusterAttrs[cluster_attribute_id]['type']
        return command_string.format(cluster_attribute_id, attribute_type, value)

    def _convert_to_farenheit(self, celcuis):
        return str(round((celcuis * 9 / 5) + 32))

    def _convert_to_celcius(self, farenheit):
        return str(round((farenheit - 32) * 5 / 9))

    def convert_to_packed_hex(self, celcius):
        celcius_str_array = str(celcius).split('.')
        celcius_int_part = celcius_str_array[0]
        celcius_dec_part = None
        if len(celcius_str_array) == 2:
            celcius_dec_part = celcius_str_array[1]
        if len(celcius_int_part) == 1:
            celcius_int_part = '0' + celcius_int_part

        if celcius_dec_part != None and len(celcius_dec_part) == 1:
            celcius_dec_part = celcius_dec_part + '0'
        else:
            celcius_dec_part = '00'
        return "0x{:04x}".format(int(celcius_int_part + celcius_dec_part)).replace('0x', '')

    def convert_to_decimal(self, packed_hex_string):
        string_val = format(int(packed_hex_string, 16), '04d')
        decimal_string = string_val[0:2] + '.' + string_val[2:]
        return decimal_string

    def _format_time(self, minutes):
        return "0x{:04x}".format(minutes).replace('0x', '')

    def _build_device_mode_command_string(self, mode):
        device_mode_value = self.DEVICE_MODE.get(mode)
        if device_mode_value is None:
            raise Exception('Invalid mode identifier {0}, Allowed modes are (OFF,DUAL,COLD,HEAT,BOOST)'.format(mode))
        device_mode_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['MODE']
        return self._get_command_string(device_mode_cluster_attr, device_mode_value)

    def _build_device_schedule_command_string(self, device_schedule):
        device_schedule_type_value = self.DEVICE_SCHEDULE_TYPE[device_schedule]
        if device_schedule_type_value is None:
            raise Exception('Invalid device mode shcedule (HOLD|SCHEDULE) is allowed')
        device_schedule_cluser_attr = self.DEVICE_CLUSTER_ATTRIBUTES['SCHEDULE_OR_HOLD']
        return self._get_command_string(device_schedule_cluser_attr, device_schedule_type_value)

    def _build_time_duration_command_string(self, time_duration_in_mins):
        formatted_time = self._format_time(time_duration_in_mins)
        device_time_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['DURATION']
        return self._get_command_string(device_time_cluster_attr, formatted_time)

    def _build_temp_heat_command_string(self, temperature):
        if self.device_temp_scale == 0:
            temp_in_degrees = self._convert_to_celcius(temperature)
        else:
            temp_in_degrees = temperature
        temp_in_hex = self.convert_to_packed_hex(temp_in_degrees)
        device_heat_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['HEAT_TEMP']
        return self._get_command_string(device_heat_cluster_attr, temp_in_hex)

    def _build_temp_cool_command_string(self, temperature):
        if self.device_temp_scale == 0:
            temp_in_degrees = self._convert_to_celcius(temperature)
        else:
            temp_in_degrees = temperature
        temp_in_hex = self.convert_to_packed_hex(temp_in_degrees)
        device_heat_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['COOL_TEMP']
        return self._get_command_string(device_heat_cluster_attr, temp_in_hex)


    def get_current_stat_time(self):
        get_command_string = 'AT+READATR:{0},{1},0,000A,0000'.format(self.deviceNodeId,self.DEVICE_ENDPOINT)
        print(get_command_string)
        get_expected_response = "RESPATTR:{0},{1},{2}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '000A')
        _,_,response = AT.sendCommand(get_command_string, get_expected_response)
        device_time = response.split(',')[5]
        print('The device time is ', device_time)
        print('Shown time is {0}'.format(timeutil.zbHexToDateString(device_time)))
        return datetime.datetime.strptime(str(timeutil.zbHexToDateString(device_time)), '%Y-%m-%d %H:%M:%S')


    def get_current_holiday_mode_state(self):
        command_string = 'AT+READMATR:{0},{1},0,1039,FD01,0015'.format(self.deviceNodeId, self.DEVICE_ENDPOINT)
        get_expected_response = "RESPATTR:{0},{1},{2}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, 'FD01')
        _,_,response = AT.sendCommand(command_string, get_expected_response)
        enabled_flag = response.split(',')[6]
        print('The enabled flag is {0}'.format(enabled_flag))
        if enabled_flag =='00':
            return 'INACTIVE'
        else:
            return 'ACTIVE'


    def set_holiday_mode(self, offset_in_mins):
        command_string = "AT+WRITEMATR:{0},{1},{2},{3},{4},{5},{6},{7}"
        expectedResponse = ['WRITEMATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.MANUFACTURER_CODE)]
        current_stat_time = self.get_current_stat_time()
        start_zigbee_time = timeutil.utcDatetimeToZbHexTimestamp(current_stat_time)
        current_end_time = current_stat_time  + datetime.timedelta(minutes = offset_in_mins)
        end_zigbee_time = timeutil.utcDatetimeToZbHexTimestamp(current_end_time)

        print("The start time and end times are {0}, {1}",start_zigbee_time, end_zigbee_time)
        start_time_set_str = command_string.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '1039', self.MANUFACTURER_CUSTOM_CLUSTER,'0010', '23', start_zigbee_time)
        print('The command string is {0}'.format(start_time_set_str))
        self.AT.sendCommand(start_time_set_str, expectedResponse)
        print('Setting the end time ')
        end_time_str = command_string.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '1039', self.MANUFACTURER_CUSTOM_CLUSTER, '0011', '23', end_zigbee_time)
        print('The end command string is {0}'.format(end_time_str))
        self.AT.sendCommand(end_time_str, expectedResponse)
        print('Setting the holiday mode ')
        holiday_mode_settings = command_string.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '1039', self.MANUFACTURER_CUSTOM_CLUSTER, '0013', '25', '0FFFFFFFFFFFF')
        self.AT.sendCommand(holiday_mode_settings, expectedResponse)
        enable_holiday_mode_str = command_string.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '1039', self.MANUFACTURER_CUSTOM_CLUSTER, '0012', '30', '01')
        print('The command string is {0}'.format(enable_holiday_mode_str))
        self.AT.sendCommand(enable_holiday_mode_str, expectedResponse)

    def cancel_holiday_mode(self):
        current_mode = self.get_current_holiday_mode_state()
        print('The current mode is {0}'.format(current_mode))
        if current_mode == 'ACTIVE':
            self.command_string = 'at+rawzcl:{0},{1},FD01,053910000001'.format(self.deviceNodeId, self.DEVICE_ENDPOINT)
            self._send_at_command('OK')
            print('Cancelled the holiday mode ')



    def _look_key_by_value(self, dict, dict_value):
        for key, value in dict.items():
            if value == dict_value:
                return key
        raise Exception('The value {0} is not found in the dictionary{1}'.format(dict_value, dict))

    def _send_at_command(self, expected_response):
        response_status, response_code, response_value = self.AT.sendCommand(self.command_string, expected_response)
        return response_status, response_code, response_value

    ''' Public API'''

    def withMode(self, mode):
        self.command_string = ''
        print("The mode id is " + mode)
        mode_id = self.USER_MODES[mode]
        if mode_id is None:
            raise Exception('Invalid Mode {0}, Please select a valid option'.format(mode))
        device_mode = ''
        # The Device is set to off
        if mode_id == 0:
            self.command_string = self._build_device_mode_command_string('OFF')
        # Heat Hold mode
        elif mode_id == 1:
            self.command_string = self._build_device_mode_command_string(
                'HEAT') + ',' + self._build_device_schedule_command_string('HOLD')
        # Heat schedule mode
        elif mode_id == 2:
            self.command_string = self._build_device_mode_command_string(
                'HEAT') + ',' + self._build_device_schedule_command_string('SCHEDULE')
        # Cool hold mode
        elif mode_id == 3:
            self.command_string = self._build_device_mode_command_string(
                'COOL') + ',' + self._build_device_schedule_command_string('HOLD')
        # Cool Schedule
        elif mode_id == 4:
            self.command_string = self._build_device_mode_command_string(
                'COOL') + ',' + self._build_device_schedule_command_string('SCHEDULE')
        elif mode_id == 5:
            self.command_string = self._build_device_mode_command_string(
                'DUAL') + ',' + self._build_device_schedule_command_string('HOLD')
        elif mode_id == 6:
            self.command_string = self._build_device_mode_command_string(
                'DUAL') + ',' + self._build_device_schedule_command_string('SCHEDULE')
        elif mode_id == 7:
            self.command_string = self._build_device_mode_command_string(
                'HEAT_BOOST') + ',' + self._build_device_schedule_command_string('HOLD')
        elif mode_id == 8:
            self.command_string = self._build_device_mode_command_string(
                'COOL_BOOST') + ',' + self._build_device_schedule_command_string('HOLD')

        return self

    def for_time(self, duration_in_mins):
        self.command_string += "," + self._build_time_duration_command_string(duration_in_mins)
        return self

    def with_heat_set_to_temperature(self, temperature):
        self.command_string += "," + self._build_temp_heat_command_string(temperature)
        return self

    def with_cooling_set_to_temperature(self, temp_in_farenheit):
        self.command_string += "," + self._build_temp_cool_command_string(temp_in_farenheit)
        print('The command string is {0}'.format(self.command_string))
        return self

    def set(self):
        print('The command string is ' + self.command_string)
        self.command_string = self.command_string.strip(',')
        self.command_string = "AT+WRITEATR:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                       self.THERMOSTAT_CLUSTER, self.command_string)
        print(self.command_string)
        expectedResponse = [
            'WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.THERMOSTAT_CLUSTER)]
        self.AT.sendCommand(self.command_string, expectedResponse)
        self.prior_command_string = self.command_string
        self.command_string = ''

    def _read_stat_cluster_attr(self, cluster_atribute):
        self.command_string = "AT+READATR:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                      self.THERMOSTAT_CLUSTER, cluster_atribute)
        print('::' + self.command_string)
        expected_response = [
            'RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.THERMOSTAT_CLUSTER)]
        return self._send_at_command(expected_response)

    def get_current_mode(self):
        mode_cluster_attribute = self.DEVICE_CLUSTER_ATTRIBUTES['MODE']
        _, _, mode_resp_value = self._read_stat_cluster_attr(mode_cluster_attribute)
        device_mode = None
        device_mode = self._look_key_by_value(self.DEVICE_MODE, mode_resp_value.split(',')[5])
        if device_mode == 'HEAT_BOOST' or device_mode == 'COOL_BOOST' or device_mode == 'OFF':
            return device_mode
        print('The device mode is {0}'.format(device_mode))

        # Here check and get the device schedule( Hold / Schedule)
        schedule_culster_attribute = self.DEVICE_CLUSTER_ATTRIBUTES['SCHEDULE_OR_HOLD']
        _, _, schedule_resp_value = self._read_stat_cluster_attr(schedule_culster_attribute)
        schedule_mode = self._look_key_by_value(self.DEVICE_SCHEDULE_TYPE, schedule_resp_value.split(',')[5])
        return device_mode + ' ' + schedule_mode

    def _read_and_convert_temp(self, temp_cluster_attr):
        _, _, temp_value = self._read_stat_cluster_attr(temp_cluster_attr)
        temp_string_value = temp_value.split(',')[5]
        actual_temp = float(self.convert_to_decimal(temp_string_value))
        if self.device_temp_scale == 0:
            actual_temp = self._convert_to_farenheit(actual_temp)
        else:
            actual_temp = str(actual_temp)
        return actual_temp

    def get_current_set_heat_temp(self):
        device_temp_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['HEAT_TEMP']
        return self._read_and_convert_temp(device_temp_cluster_attr)

    def get_current_set_cool_temp(self):
        device_temp_cluster_attr = self.DEVICE_CLUSTER_ATTRIBUTES['COOL_TEMP']
        return self._read_and_convert_temp(device_temp_cluster_attr)

    def get_current_temperature(self):
        current_temp_attr = self.DEVICE_CLUSTER_ATTRIBUTES['LOCAL_TEMP']
        return self._read_and_convert_temp(current_temp_attr)

    def _get_manufacturer_attribute(self, attribute_key):
        self.command_string = "AT+READMATR:{0},{1},{2},{3},{4},{5}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                           self.MANUFACTURER_CODE,
                                                                           self.MANUFACTURER_CUSTOM_CLUSTER,
                                                                           attribute_key)
        print(self.command_string)
        expected_response = [
            'RESPMATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.MANUFACTURER_CODE)]
        return self._send_at_command(expected_response)

    def get_protection_timer_value(self):
        timer_attribute_key = self.MANUFACTURER_CLUSTER_ATTRIBUTES['PROTECTION_TIMER']
        _, _, value = self._get_manufacturer_attribute(timer_attribute_key)
        return int(value.split(',')[6], 16)

    def get_stat_state(self):
        '''Verify the stat mode (Fan on / Off / cooler on / Off etc '''
        stat_runningstate_attr = self.DEVICE_CLUSTER_ATTRIBUTES['STAT_RUNNING_STATE']
        _, _, value = self._read_stat_cluster_attr(stat_runningstate_attr)
        value = int(value.split(',')[5], 16)
        print('The value is {0}'.format(value))
        device_mode = ''
        if value & 1 != 0:
            device_mode += 'HEAT_STAGE_1 '
        if value & 2 != 0:
            device_mode += 'COOL_STAGE_1 '
        if value & 4 != 0:
            device_mode += 'FAN_STAGE_1 '
        if value & 8 != 0:
            device_mode += 'HEAT_STAGE_2 '
        if value & 16 != 0:
            device_mode += 'COOL_STAGE_2 '
        if value & 32 != 0:
            device_mode += 'FAN_STAGE_2 '
        if value & 64 != 0:
            device_mode += 'FAN_STAGE_3 '
        if value & 128 != 0:
            device_mode += 'HEAT_STAGE_3 '
        if value & 256 != 0:
            device_mode += 'EMERGENCY_HEAT '
        if value & 256 != 0:
            device_mode += 'ACC '
        if len(device_mode) == 0:
            device_mode = 'OFF'

        return device_mode

    def get_stat_wiring_state(self):
        stat_wiring_config_attr = self.MANUFACTURER_CLUSTER_ATTRIBUTES['WIRING_CONNECTION']
        _, _, value = self._get_manufacturer_attribute(stat_wiring_config_attr)
        value = int(value.split(',')[6], 16)
        print('The value is {0}'.format(value))
        device_wiring_config_array = []
        if value & 1 != 0:
            device_wiring_config_array.append('Rh')
        if value & 2 != 0:
            device_wiring_config_array.append('Rc')
        if value & 4 != 0:
            device_wiring_config_array.append('C')
        if value & 8 != 0:
            device_wiring_config_array.append('W1')
        if value & 16 != 0:
            device_wiring_config_array.append('W2')
        if value & 32 != 0:
            device_wiring_config_array.append('W3')
        if value & 64 != 0:
            device_wiring_config_array.append('Y1')
        if value & 128 != 0:
            device_wiring_config_array.append('Y2')
        if value & 256 != 0:
            device_wiring_config_array.append('O/B')
        if value & 512 != 0:
            device_wiring_config_array.append('G')
        if value & 1024 != 0:
            device_wiring_config_array.append('Acc')

        return device_wiring_config_array

    def set_humidity_percentage(self, humidity_type, percentage):
        stat_wiring_config_attr = self.MANUFACTURER_CLUSTER_ATTRIBUTES['HUMIDIFICATION_CONTROL']
        if humidity_type == 'HUMIDIFIER':
            value = '01'
        elif humidity_type == 'DEHUMIDIFIER':
            value = '10'
        else:
            raise Exception('To set the humidification control , Please  use HUMIDFIER or DEHUMIDIFIER option')

        # Set the humidifier / Dehumidifier
        self.command_string = "AT+WRITEMATR:{0},{1},{2},{3},{4},{5},{6},{7}".format(self.deviceNodeId,
                                                                                    self.DEVICE_ENDPOINT, '0', '1039',
                                                                                    self.MANUFACTURER_CUSTOM_CLUSTER,
                                                                                    stat_wiring_config_attr, '30',
                                                                                    value)
        print('Sending the command {0}'.format(self.command_string))
        expectedResponse = ['WRITEMATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '1039')]
        self.AT.sendCommand(self.command_string, expectedResponse)

        humidity_percentage = str(hex(percentage)).replace('0x', '')
        print('Setting the humidity value to {0}'.format(humidity_percentage))

        # Set the humidity mode
        self.command_string = "AT+WRITEATR:{0},{1},{2},{3},{4},{5},{6}".format(self.deviceNodeId, self.DEVICE_ENDPOINT,
                                                                               '0',
                                                                               self.STAT_HUMIDIFIER_CLUSTER, '0010',
                                                                               '20', humidity_percentage.upper())
        print(self.command_string)
        expectedResponse = [
            'WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.STAT_HUMIDIFIER_CLUSTER)]
        self.AT.sendCommand(self.command_string, expectedResponse)
        self.prior_command_string = self.command_string
        self.command_string = ''

    def get_current_humidity_control_type(self):
        stat_wiring_config_attr = self.MANUFACTURER_CLUSTER_ATTRIBUTES['HUMIDIFICATION_CONTROL']
        command_string = "at+readmatr:{0},{1},{2},{3},{4},{5}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                      '1039', self.MANUFACTURER_CUSTOM_CLUSTER,
                                                                      stat_wiring_config_attr)
        print('Sending {0}'.format(command_string))
        expectedResponse = ['RESPMATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '1039')]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        print('The response is {0}'.format(resp_value))
        stat_humidification_state = resp_value.split(',')[6]
        if stat_humidification_state == '01':
            return 'HUMIDIFIER'
        elif stat_humidification_state == '10':
            return 'DEHUMIDIFIER'

        return 'UNKNOWN'

    def get_humidity_percentage(self):
        command_string = "at+readatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                 self.STAT_HUMIDIFIER_CLUSTER, '0010')
        expectedResponse = [
            'RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.STAT_HUMIDIFIER_CLUSTER)]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        humidity = '0x' + resp_value.split(',')[5]
        return int(humidity, 16)


    def get_current_displayed_humidity_value(self):
        stat_wiring_state = self.get_stat_wiring_state()
        if 'Acc' not in stat_wiring_state:
            print('Looks like humidifier wire is not connected!')
            return -1

        command_string = "at+readatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                 self.STAT_HUMIDIFIER_CLUSTER, '0000')
        expectedResponse = [
            'RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.STAT_HUMIDIFIER_CLUSTER)]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        humidity = '0x' + resp_value.split(',')[5]
        return int(humidity, 16)


    def set_emergency_heat(self):
        command_string = "at+writeatr:{0},{1},{2},{3},{4},{5},{6}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                          self.THERMOSTAT_CLUSTER, '001C', '30', '05')
        expectedResponse = [
            'WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.THERMOSTAT_CLUSTER)]
        self.AT.sendCommand(command_string, expectedResponse)
        time.sleep(10)

    def cancel_boost(self):
        current_mode = self.get_current_mode().strip()
        print("The current mode is " + current_mode)
        if 'BOOST' in current_mode or 'EMERGENCY_HEAT' in current_mode:
            self.command_string = 'at+rawzcl:{0},{1},FD01,053910000001'.format(self.deviceNodeId, self.DEVICE_ENDPOINT)
            self._send_at_command('OK')
            return
        print(' Cannot cancel boost (The device is not in boost/emergency heat mode)')




    def get_configured_temperature(self, mode, range):
        attribute = ''
        if mode == 'HEAT':
            if range == 'MIN':
                attribute = self.DEVICE_CLUSTER_ATTRIBUTES['MIN_HEATING_TEMP']
            elif range == 'MAX':
                attribute = self.DEVICE_CLUSTER_ATTRIBUTES['MAX_HEATING_TEMP']
            else:
                raise Exception('In-valid range selection (either min or max allowed')
        elif mode == 'COOL':
            if range == 'MIN':
                attribute = self.DEVICE_CLUSTER_ATTRIBUTES['MIN_COOL_TEMP']
            elif range == 'MAX':
                attribute = self.DEVICE_CLUSTER_ATTRIBUTES['MAX_COOL_TEMP']
            else:
                raise Exception('In-valid range selection (either min or max allowed')
        else:
            raise Exception('Invalid mode , ONly heat or cool is allowed')
        value = self._read_and_convert_temp(attribute)
        return value

    def get_current_device_timer_value(self):
        time.sleep(20)
        duration_attribute = self.DEVICE_CLUSTER_ATTRIBUTES['DURATION']
        _, _, value = self._read_stat_cluster_attr(duration_attribute)
        print("The read timer value is {0}".format(value))
        return int(value.split(',')[5], 16)

    def get_current_device_scale(self):
        command_string = "at+readatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                 self.STAT_UI_CLUSTER, '0000')
        expectedResponse = [
            'RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.STAT_UI_CLUSTER)]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        temp_code = resp_value.split(',')[5]
        if temp_code == '00':
            return 'CELCIUS'
        elif temp_code == '01':
            return 'FAHRENHEIT'

    def set_fan_mode(self, mode):
        fan_mode = self.FAN_MODE[mode]
        print('Setting the fan mode to {0}'.format(fan_mode))
        if fan_mode is None:
            raise Exception('Invalid mode {0}'.format(mode))
        command_string = "at+writeatr:{0},{1},{2},{3},{4},{5},{6}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                          '0202', '0000', '30', fan_mode)
        expectedResponse = ['WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0202')]
        self.AT.sendCommand(command_string, expectedResponse)


    def get_fan_mode(self):
        command_string = "at+readatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '0202',
                                                                 '0000')
        expectedResponse = ['RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0202')]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        device_mode = resp_value.split(',')[5]
        return self._look_key_by_value(self.FAN_MODE, device_mode)

    def get_circulation_timer_value(self):
        command_string = 'at+readmatr:{0},{1},{2},{3},{4},{5}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', self.MANUFACTURER_CODE,
                                                                      self.MANUFACTURER_CUSTOM_CLUSTER, '0022')
        expectedResponse = ['RESPMATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, self.MANUFACTURER_CODE)]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        circulation_timer = resp_value.split(',')[6]
        return int(circulation_timer, 16)

    def set_device_name(self, device_name):
        command_string = "at+writeatr:{0},{1},{2},{3},{4},{5},{6}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0',
                                                                          '0000', '0010', '42', device_name)
        expectedResponse = ['WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0000')]
        self.AT.sendCommand(command_string, expectedResponse)

    def get_device_name(self):
        command_string = "at+readatr:{0},{1},{2},{3},{4}".format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0', '0000',
                                                                 '0010')
        expectedResponse = ['RESPATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0000')]
        _, _, resp_value = self.AT.sendCommand(command_string, expectedResponse)
        return resp_value.split(',')[5]

    def enable_emergency_heat(self):
        print('Enabling the emergency heat')
        command_string = "AT+WRITEATR:{0},{1},0,0201,001C,30,05".format(self.deviceNodeId, self.DEVICE_ENDPOINT)
        expectedResponse = ['WRITEATTR:{0},{1},{2}'.format(self.deviceNodeId, self.DEVICE_ENDPOINT, '0201')]
        self.AT.sendCommand(command_string, expectedResponse)
        time.sleep(10)


    def reboot_device(self):
        print('Rebooting the device .. Stand by')
        command_string = "at+rawzcl:{0},05,0000,0539100000".format(self.deviceNodeId)
        expected_reponse = ['OK']
        self.AT.sendCommand(command_string, expected_reponse)
        time.sleep(15)

    def press_menu(self):
        print('Accessing the menu button')
        device_utils.pressSLT4DeviceButton(self.deviceNodeId, self.DEVICE_ENDPOINT, "MENU", "PRESS")

    def press_dial(self):
        print('Pressing the device dial')
        device_utils.pressSLT4DeviceButton(self.deviceNodeId, self.DEVICE_ENDPOINT, "DIAL", "PRESS")

    def shutdown_device(self):
        self.AT.stopThreads()

    def get_device_node_id(self):
        return self.deviceNodeId

    def get_device_endpoint(self):
        return self.DEVICE_ENDPOINT

    def is_emergency_heat_wired(self):
        has_em = False
        wiring_state = self.get_stat_wiring_state()
        print('The wiring state is {0}'.format(wiring_state))
        if 'W1' and 'W3' in wiring_state:
            has_em = True
        elif 'W1' and 'O/B' in wiring_state:
            has_em = True
        return has_em


    def is_fan_wired(self):
        has_fan = False
        wiring_state = self.get_stat_wiring_state()
        if 'G' in wiring_state:
            has_fan = True
        return has_fan








    '''Set Schedule for Heat/Cool/Dual'''

    def set_schedule(self,schedule, device_mode, boolStandaloneMode=False):

        for val in schedule:
            payload=self.generate_schedule_payload(schedule[val], device_mode)
            respState, _, respVal = self.setWeeklyScheduleSLT4(self.deviceNodeId, self.DEVICE_ENDPOINT, self.THERMOSTAT_CLUSTER, self.sch_days[val], payload, device_mode, boolStandaloneMode)
            if not respState:
                print('ERROR: setWeeklySchedule() has failed. {}'.format(respVal))
                return respVal

        for day in self.sch_days:
            respState, _, respValue = self.getWeeklyScheduleSLT4(self.deviceNodeId, self.DEVICE_ENDPOINT, self.THERMOSTAT_CLUSTER, self.sch_days[day],device_mode)
            if not respState:
                print("ERROR: getWeeklySchedule(), {}".format(respValue))
                return respValue


    def generate_schedule_payload(self,schedule, device_mode):

        cmd=''
        for event in schedule:
            minutes=timeutil.timeStringToMinutes(event[0])
            time_format =timeutil.utcTimeToZbHexTimestamp(minutes)
            time_in_hex=timeutil.byteSwap(time_format)
            if self.device_temp_scale == 0:  # need to check if conversion required or not
                temp_in_degrees = self._convert_to_celcius(float(event[1]))
            else:
                temp_in_degrees = event[1]
            temp_in_hex = self.convert_to_packed_hex(temp_in_degrees)
            temp_in_hex = timeutil.byteSwap(temp_in_hex)

            if str(device_mode).upper() != "DUAL SCHEDULE":
                cmd = cmd + time_in_hex + temp_in_hex
            else:
                temp_in_hex_dual = self.convert_to_packed_hex(float(temp_in_degrees) - 4.5)  # only for dual mode schdule
                temp_in_hex_dual = timeutil.byteSwap(temp_in_hex_dual)  # only for dual mode schdule
                cmd = cmd + time_in_hex + temp_in_hex_dual + temp_in_hex

        return cmd

    def setWeeklyScheduleSLT4(self,myNodeId, myEp, myCluster, myDayBitmap, myPayload, device_mode, boolStandaloneMode=False):

        frameType = '01'  # 0x01 = Command specific to cluster
        seqNumber = '00'
        commandId = '01'  # 0x01 = setWeeklySchedule

        numberOfEvents = '06'
        if "HEAT" in str(device_mode).upper():
            modeForSequence = '01'  # 0x01 = Heat Mode
        elif "COOL" in str(device_mode).upper():
            modeForSequence = '02'  # 0x02 = Cool Mode
        elif "DUAL" in str(device_mode).upper():
            modeForSequence = '03'  # 0x03 = Dual Mode
        else:
            raise Exception('Unable to locate the selected mode, Please verify if the mode is set as HEAT or COLD or DUAL')

        header = "{0}{1}{2}{3}{4}{5}".format(frameType, seqNumber, commandId, numberOfEvents, myDayBitmap, modeForSequence)

        myMsg = 'AT+RAWZCL:{0},{1},{2},{3}{4}'.format(myNodeId, myEp, myCluster, header, myPayload)
        expectedResponse = ['CWSCHEDULE:{0},{1}'.format(myNodeId, myEp)]
        # respState, respCode, respValue = sendCommand(myMsg, expectedResponse)
        respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)
        if respState and respCode == device_clusters.statusCodes['SUCCESS']:
            respValue = respValue.split(',')[5:]
        return respState, respCode, respValue


    def getWeeklyScheduleSLT4(self,myNodeId, myEp, myCluster, myDayBitmap, device_mode):
        """ Get the schedule for the given day.

        """
        frameType = '01'  # 0x01 = Command specific to cluster
        seqNumber = '00'
        commandId = '02'  # 0x01 = getWeeklySchedule
        if "HEAT" in str(device_mode).upper():
            modeForSequence = '01'  # 0x01 = Heat Mode
        elif "COOL" in str(device_mode).upper():
            modeForSequence = '02'  # 0x02 = Cool Mode
        elif "DUAL" in str(device_mode).upper():
            modeForSequence = '03'  # 0x03 = Dual Mode
        else:
            raise Exception('Unable to locate the selected mode, Please verify if the mode is set as HEAT or COLD or DUAL')


        payload = "{0}{1}{2}{3}{4}".format(frameType, seqNumber, commandId,
                                           myDayBitmap, modeForSequence)
        myMsg = 'AT+RAWZCL:{0},{1},{2},{3}'.format(myNodeId, myEp, myCluster, payload)

        # at+rawzcl:FDDF,05,0201,0100020401
        # CWSCHEDULE:FDDF,05,06,04,01,0186,07D0,01FE,0064,02D0,0064,0348,0064,03DE,07D0,0528,0064
        expectedResponse = ['CWSCHEDULE:{0},{1},06,{2},{3}'.format(myNodeId, myEp, myDayBitmap,modeForSequence)]
        respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)

        if respState and respCode == device_clusters.statusCodes['SUCCESS']:
            respValue = respValue.split(',')[5:]
        return respState, respCode, respValue

    def create_week_schdule_table(self,context, mode=""):
        stat = context.stat
        oSchedDict = {}
        oSchedDict.clear()
        for oRow in context.table:
            if oRow['Day'].upper() == 'TODAY':
                strDay = dt.today().strftime("%a").lower()
                strDay = strDay[:3].lower()
            else:
                strDay = oRow['Day'][:3].lower()
            context.strDay=strDay
            tempSchdlList = []
            oSchedList = []
            for intColCntr in range(1, len(oRow.cells)):
                if not oRow.cells[intColCntr].strip() == "":
                    strTime = oRow.cells[intColCntr].split(',')[0].strip()
                    strHeatState = oRow.cells[intColCntr].split(',')[1].strip().upper()
                    tempSchdlList = tempSchdlList + [(strTime, strHeatState)]

            # if 'UI' not in mode.upper():
            for intTmpCntr in range(6 - len(tempSchdlList)):
                oSchedList = oSchedList + [tempSchdlList[0]]

            for oEvent in tempSchdlList:
                oSchedList = oSchedList + [oEvent]

            oSchedDict[strDay] = oSchedList
        context.oSchedDict = oSchedDict

        if 'STAND' in mode.upper() and 'ALONE' in mode.upper():
            boolStandaloneMode = True
        else:
            boolStandaloneMode = False

        # Set and report schedule
        return oSchedDict,boolStandaloneMode

    def validate_week_schedule(self,context,oSchedDict,device_mode):
        strMode = str(device_mode).upper()
        intGaurdTime = 30
        intChekInterval = 120
        reporter = context.reporter
        while True:
            fltCurrentTargTemp, intDuration, nextEventStartTime, nextEventDay = self.get_current_temp_and_next_event_time(
                oSchedDict)
            print(fltCurrentTargTemp, intDuration, nextEventStartTime,nextEventDay)
            self.validate_sys_mode(reporter, True, strMode, fltCurrentTargTemp,
                                        intDuration * 60, intChekInterval, nextEventStartTime=nextEventStartTime,
                                        nextEventDay=nextEventDay)



    # Gets the current Target temperature from the given schedule dictionary object
    def get_current_temp_and_next_event_time(self,oSchedule):
        fltTemp = 'NO-TEMP'
        intLeftDurarionMin = 15

        intToday = int(dt.today().strftime("%w"))
        intYesterday = int(dt.today().strftime("%w")) - 1
        if intYesterday == -1: intYesterday = 6
        intTomorrow = int(dt.today().strftime("%w")) + 1
        if intTomorrow == 7: intTomorrow = 0
        strToday = self.oWeekDay[intToday]
        strYesterday = self.oWeekDay[intYesterday]
        strTomorrow = self.oWeekDay[intTomorrow]

        intCurrentMin = timeutil.timeStringToMinutes(dt.today().strftime("%H:%M"))
        if strToday in oSchedule:
            oScheduleList = self.remove_duplicates(oSchedule[strToday])
            for intCntr in range(len(oScheduleList)):
                intEventStartMin = timeutil.timeStringToMinutes(oScheduleList[intCntr][0])
                if intCntr == 0 and intCurrentMin < intEventStartMin:
                    if strYesterday in oSchedule:
                        oYestScheduleList = oSchedule[strYesterday]
                        fltTemp = oYestScheduleList[len(oYestScheduleList) - 1][1]
                        intLeftDurarionMin = intEventStartMin - intCurrentMin
                        return fltTemp, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
                    else:
                        return 0.0, 0, '0:00', 'Today'
                if intCntr == len(oScheduleList) - 1:
                    fltTemp = oScheduleList[intCntr][1]
                    if strTomorrow in oSchedule:
                        oTomoScheduleList = oSchedule[strTomorrow]
                        intEventStartMin = timeutil.timeStringToMinutes(oTomoScheduleList[0][0])
                        intLeftDurarionMin = intEventStartMin - intCurrentMin + 1440
                        return fltTemp, intLeftDurarionMin, oTomoScheduleList[0][0], 'Tomorrow'
                    return fltTemp, intLeftDurarionMin, oScheduleList[intCntr][0], 'Today'
                elif (intCurrentMin >= intEventStartMin) and (
                            intCurrentMin < timeutil.timeStringToMinutes(oScheduleList[intCntr + 1][0])):
                    fltTemp = oScheduleList[intCntr][1]
                    intLeftDurarionMin = timeutil.timeStringToMinutes(oScheduleList[intCntr + 1][0]) - intCurrentMin
                    return fltTemp, intLeftDurarionMin, oScheduleList[intCntr + 1][0], 'Today'
        else:
            return 0.0, 0, '0:00', 'Today'
        return fltTemp, intLeftDurarionMin

    def remove_duplicates(self,values):
        output = []
        seen = set()
        for value in values:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    # Validates the system mode for the given duration and logs the validation in check interval time
    def validate_sys_mode(self, reporter, boolAutoMode, strSysMode, strExpectedTemperature,
                          intCheckDuration=600, intCheckTImeInterval=30,
                          nextEventStartTime=None, nextEventDay='Today'):

        # strSysMode = str(strSysMode).split(" ")[0-1]
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')
        strTarg = 'Target Temperature'
        reporter.ReportEvent('Test Validation',
                             'Validating <B>' + strSysMode + ' </B>Mode with ' + strTarg + ' as <B>' + str(
                                 strExpectedTemperature) + \
                             '</B> for every <B>' + str(
                                 intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(
                                 round(intCheckDuration / 60, 2)) + ' minute(s)', 'Done')

        # Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration / intCheckTImeInterval)):
            # Log the Validation of current attributes with Expected Test and Model Attribute values

            # self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strSysMode, strExpectedTemperature,
            #                          strExpextedHolidayStart, strExpectedHolidayEnd)

            strLog, strStatus = self.get_schdule_log( 'Test', strSysMode, strExpectedTemperature)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')

            # Wait for the Check Time interval
            print('sleeping for ' + str(intCheckTImeInterval) + ' sec')
            time.sleep(intCheckTImeInterval)

            if intCntr == int(intCheckDuration / intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration % intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not self.check_guard_time(nextEventStartTime, nextEventDay): return

    def check_guard_time(nextEventStartTime, nextEventDay):
        strCurrentTime = datetime.today().strftime("%H:%M")
        intCurrentMin = timeutil.timeStringToMinutes(strCurrentTime)
        intNextEventStartTimeMinute = timeutil.timeStringToMinutes(nextEventStartTime)
        if 'TOMO' in nextEventDay.upper(): intNextEventStartTimeMinute = intNextEventStartTimeMinute + 1440
        if intCurrentMin > intNextEventStartTimeMinute:
            if intNextEventStartTimeMinute - intCurrentMin < 2:
                time.sleep(60)
            return False
        else:
            if abs(intNextEventStartTimeMinute - intCurrentMin) < 2:
                time.sleep(60)
                return False
            return True

    def get_schdule_log(self, strValidationType, strExpectedMode='', strExpectedSPTemp=1.0):

        strLocalTemperature = 0.0
        strActualTSEPSPTemp = 0.0
        strExpectedTHRunState = ''
        strExpectedSPTemp=float(strExpectedSPTemp)
        current_timer_value = self.get_protection_timer_value()
        # Sleep for an extra 20 seconds
        if current_timer_value > 0:
            print('The protection timer is on for {0} seconds , Sleeping until then'.format(current_timer_value))
            time.sleep(current_timer_value + 20)

        print(self.get_current_mode() + "===========\n")
        strActualTSEPMode = self.get_current_mode()

        if strActualTSEPMode.upper()=="HEAT SCHEDULE":
            occupiedSetpoint= self.DEVICE_CLUSTER_ATTRIBUTES['HEAT_TEMP']
        else:
            occupiedSetpoint = self.DEVICE_CLUSTER_ATTRIBUTES['COOL_TEMP']
        _, _,strActualTSEPSPTemp = self._read_stat_cluster_attr(occupiedSetpoint)
        strActualTSEPSPTemp=timeutil.convertHexTemp(strActualTSEPSPTemp.split(',')[5])

        # Convert strActualTSEPSPTemp to farenheit if device is in farenheit mode
        if self.device_temp_scale==0:
            strActualTSEPSPTemp = self._convert_to_farenheit(float(strActualTSEPSPTemp))
            strActualTSEPSPTemp=float(strActualTSEPSPTemp)
            # strActualTSEPSPTemp=float(strActualTSEPSPTemp) + 1.0

        localtemperature = self.DEVICE_CLUSTER_ATTRIBUTES['LOCAL_TEMP']
        _, _,strLocalTemperature = self._read_stat_cluster_attr(localtemperature)
        strLocalTemperature=timeutil.convertHexTemp(strLocalTemperature.split(',')[5])
        # Convert strLocalTemperature to farenheit if device is in farenheit mode
        if self.device_temp_scale == 0:
            strLocalTemperature = self._convert_to_farenheit(float(strLocalTemperature))
        thermostatRunningState = self.DEVICE_CLUSTER_ATTRIBUTES['STAT_RUNNING_STATE']
        _, _,strActualTSRunState = self._read_stat_cluster_attr(thermostatRunningState)
        strActualTSRunState = strActualTSRunState.split(',')[5]
        if strActualTSRunState == '0000':
            strActualTSRunState = 'OFF'
        else:
            strActualTSRunState = 'ON'

        # Setting Expected Thermostat run state for Test Validation
        if strActualTSEPMode.upper() == "HEAT SCHEDULE":
            if float(strLocalTemperature) < float(strActualTSEPSPTemp):
                strExpectedTHRunState = 'ON'
            else:
                strExpectedTHRunState = 'OFF'
        else:
            if float(strLocalTemperature) > float(strActualTSEPSPTemp):
                strExpectedTHRunState = 'ON'
            else:
                strExpectedTHRunState = 'OFF'

        strTempCompLog = ''
        boolStatus = 'PASS'

        if str(strExpectedMode).upper() == str(strActualTSEPMode):
            strActualTSEPMode = '$$' + str(strActualTSEPMode)
        else:
            strActualTSEPMode = '$$||' + strActualTSEPMode
            boolStatus = 'FAIL'

        if str(strExpectedSPTemp) == str(strActualTSEPSPTemp):
            strActualTSEPSPTemp = '$$' + str(strActualTSEPSPTemp)
        else:
            strActualTSEPSPTemp = '$$||' + str(strActualTSEPSPTemp)
            boolStatus = 'FAIL'
        # Running State

        if strExpectedTHRunState == strActualTSRunState:
            strActualTSRunState = '$$' + strActualTSRunState
        else:
            strActualTSRunState = '$$||' + strActualTSRunState
            boolStatus = 'FAIL'

        # Adding C
        if self.device_temp_scale == 0:
            strExpectedSPTemp = str(strExpectedSPTemp) + 'F'
            strActualTSEPSPTemp = str(strActualTSEPSPTemp) + 'F'
        else:
            strExpectedSPTemp = str(strExpectedSPTemp) + 'C'
            strActualTSEPSPTemp = str(strActualTSEPSPTemp) + 'C'

        # Setting the Header for Pass and Fail
        if boolStatus == 'PASS':
            strHeader = "Attributes$$" + "Expected-" + strValidationType + "  and Actual-Thermostat Values" + "@@@"
            strActualTSEPMode = ''
            strActualTSEPSPTemp = ''
            strActualTSRunState = ''
            strActualHolidayStart = ''
            strActualHolidayEnd = ''
        else:
            strHeader = "Attributes$$" + "Expected-" + strValidationType + " Values$$" + "Actual-Thermostat Values" + "@@@"

        strLog = ''
        if strExpectedMode is not None:
            strTempCompLog = '$~Current Setpoint Temperature$$' + strExpectedSPTemp + strActualTSEPSPTemp
            strLog = strHeader + \
                         'Current System mode$$' + strExpectedMode + strActualTSEPMode + strTempCompLog + \
                         '$~Current Thermostat Running State$$' + strExpectedTHRunState + strActualTSRunState

        return strLog, boolStatus


    def set_n_event_schedule(self, context, strEvent, strDay,device_mode):
        strDay = strDay.split()[0]
        oSchedDict = {}
        oSchedDict.clear()
        if strDay.upper() == 'TODAY': strDay = dt.today().strftime("%a").lower()
        strDay = strDay[:3].lower()
        # if strDay.upper() in oSchdUtil.oWeekDayDict: strDay = oSchdUtil.oWeekDayDict[strDay.upper()]
        context.strDay = strDay

        if strEvent.isnumeric():
            intEvent = int(strEvent)
        else:
            intEvent = 0
        oSheduleList=self.create_schedule_with_events(intEvent,device_mode)
        oSchList=self.makeSixEventSceduleFormat(oSheduleList)
        if not oSheduleList: return False
        oSchedDict = {strDay: oSchList}
        context.oSchedDict = oSchedDict

        print(oSchedDict)
        return oSchedDict

    def create_schedule_with_events(self,numberOfEvents,device_mode):

        currentTime = datetime.datetime.now()
        nextEventTime = conv.roundTimeUp(currentTime, 15 * 60)
        # if time has rolled into next day then subract a day to bring it back.
        if nextEventTime.day > currentTime.day:
            nextEventTime = nextEventTime.replace(day=currentTime.day)

        # Now make the real setpoint list.
        setpoints = []
        intMinLeftForTheDay = (24 * 60) - 1

        if str(device_mode).upper()=="HEAT SCHEDULE":
            minSetTempattr= self.DEVICE_CLUSTER_ATTRIBUTES['MIN_HEATING_TEMP']
        else:
            minSetTempattr = self.DEVICE_CLUSTER_ATTRIBUTES['MIN_COOL_TEMP']
        _, _,minSetTemp = self._read_stat_cluster_attr(minSetTempattr)
        Setpoint=timeutil.convertHexTemp(minSetTemp.split(',')[5])

        if self.device_temp_scale==0:
            Setpoint = self._convert_to_farenheit(float(Setpoint))


        Setpoint = float(Setpoint) + 5
        for i in range(0, numberOfEvents):
            if str(device_mode).upper() == "HEAT SCHEDULE":
                Setpoint = Setpoint + 3
            else:
                Setpoint = Setpoint + 3
            setpoints.append((nextEventTime, Setpoint))
            # Increment nextEventTime by 15mins.
            intMinLeftForTheDay = intMinLeftForTheDay - int(nextEventTime.strftime("%M"))
            if intMinLeftForTheDay > 0:
                nextEventTime = (nextEventTime + timedelta(minutes=15)).replace(day=currentTime.day)
            else:
                return False
        setpoints = sorted(setpoints)
        setpointsStr = []
        for sp in setpoints:
            setpointsStr.append(("{:02}:{:02}".format(sp[0].hour, sp[0].minute), sp[1]))

        return setpointsStr

    def makeSixEventSceduleFormat(self,oSchedList):
        oNewSchedList = []
        intRowCount = len(oSchedList)
        for intTmp in range(6 - intRowCount):
            oNewSchedList.append(oSchedList[0])
        for oEvent in oSchedList:
            oNewSchedList.append(oEvent)
        return oNewSchedList

    def delete_add_event_schedule(self,context,strOpr):
        SchList=context.oSchedDict
        context.beforeChange=context.oSchedDict
        oDelSchedList = []

        for oRow in context.table:
            tempSchdlList = []

            for intColCntr in range(0, len(oRow.cells)):
                if not oRow.cells[intColCntr].strip() == "":
                    strTime = oRow.cells[intColCntr].split(',')[0].strip()
                    strHeatState = oRow.cells[intColCntr].split(',')[1].strip().upper()
                    tempSchdlList = tempSchdlList + [(strTime, strHeatState)]

            for oEvent in tempSchdlList:
                oDelSchedList = oDelSchedList + [oEvent]

        context.oDelSchedList = oDelSchedList
        newList = {}
        newList.clear()
        strDay = dt.today().strftime("%a").lower()
        strDay = strDay[:3].lower()
        Listcheck = self.remove_duplicates(SchList[strDay])
        context.beforeChange=Listcheck
        # Listcheck=SchList[strDay]
        for event in oDelSchedList:
            tempList = []
            for oEvent in Listcheck:
                if not(oEvent== event):
                    tempList=tempList+[oEvent]

            if str(strOpr).upper() == "ADDED":
                tempList = tempList + [event]
            Listcheck=tempList

        Listcheck = sorted(Listcheck, key=lambda Listcheck:Listcheck[0])
        context.newList = Listcheck
        Listcheck = self.makeSixEventSceduleFormat(Listcheck)

        if not Listcheck: return False
        oSchList = {strDay: Listcheck}
        context.oSchedDict = oSchList
        context.afterChange = context.oSchedDict
        return SchList

    def copy_event_schedule(self,context,days):
        copy_days=days.split(',')
        print ('To be copied days are' + str(copy_days))
        SchList=context.oSchedDict
        context.beforeCopy = context.oSchedDict
        strDay=context.strDay
        SchEvent=SchList[strDay]
        for day in copy_days:
            if strDay!= day:
                strCpyDay = day[:3].lower()
                SchList[strCpyDay] = SchEvent
        context.oSchedDict = SchList
        context.afterCopy = context.oSchedDict
        return SchList


'''Sample test scenarios'''
if __name__ == "__main__":
    stat = SLT4('CELCIUS')
    #stat.withMode('HEAT HOLD').set()
    #print(stat.get_stat_state())
    print(stat.get_circulation_timer_value())
    '''stat.withMode('DUAL HOLD').with_heat_set_to_temperature(30).set()
    #stat.withMode('COOL SCHEDULE').with_cooling_set_to_temperature(19.5).set()
    stat.press_dial()
    print("The temp is {0}".format(stat.get_current_temperature()))


    #stat.enable_emergency_heat();
    print('The current mode is {0}'.format(stat.get_current_mode()))
    stat.reboot_device()

    # print(stat.get_stat_wiring_state())
    #stat.set_holiday_mode(1)
    # print(stat.get_stat_wiring_state())

    
    stat.withMode('HEAT HOLD').with_heat_set_to_temperature(29).set()
    time.sleep(5)
    stat.withMode('COOL_BOOST').for_time(2).with_cooling_set_to_temperature(82).set()
    time.sleep(5)
    print('The current device mode is ' + stat.get_current_mode())
    print('The current heat temp is  ' + stat.get_current_set_heat_temp())
    print('The current device temp is  ' + stat.get_current_temperature())
    print("The time is {0}".format(stat.get_protection_timer_value()))
    stat.cancel_boost()
    print(stat.get_configured_temperature('COOL', 'MAX'))
    stat.get
    stat.shutdown_device()'''

    # stat = SLT4('CELCIUS')
    # print(stat.convert_to_packed_hex(80))
    # stat.set_emergency_heat()
    '''print('The mode is {0}'.format(stat.get_stat_state()));
    stat.set_device_name('test')
    print('The device name is {0}'.format(stat.get_device_name()))

    #current_temp = round(float(stat.get_current_temperature()))
    #stat.withMode('HEAT_BOOST').with_heat_set_to_temperature(current_temp + 1).for_time(30).set()
    #time.sleep(15)
    #current_set_heat_temp =round(float(stat.get_current_set_heat_temp()))
    #print('The current temp is {0}'.format(current_set_heat_temp))
    #target_temp = current_set_heat_temp + 1;
    #print('the target temp is {0}'.format(target_temp))
    #stat.command_string = ''
    #stat.for_time(3).set()


    #stat.with_cooling_set_to_temperature(24).set();

    #stat.withMode('DUAL HOLD').with_heat_set_to_temperature(55).with_cooling_set_to_temperature(75).set()
    #print('The stat status is ' + stat.get_stat_state())
    #stat.set_device_scale('CELCIUS')
    #stat.set_device_scale('FARENHEIT')
    #print(stat.get_current_temperature())
    #ssstat.shutdown_device();
    #print(stat.get_protection_timer_value())
    #stat.withMode('COOL_BOOST').for_time(2).with_cooling_set_to_temperature(21).set()
    #print("The timer is {0}".format(stat.get_current_device_timer()))
    #stat.shutdown_device()
    #stat.withMode('OFF').set()
    #stat.for_time()
    #print(stat.get_protection_timer_value())
    #stat.withMode('COOL_BOOST').for_time(2).with_cooling_set_to_temperature(21).set()

    





    #expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,myCluster)]
'''

