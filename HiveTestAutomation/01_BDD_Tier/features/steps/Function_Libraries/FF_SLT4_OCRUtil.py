import pytesseract
import re
import os
import datetime
from PIL import Image, ImageOps, ImageFilter
from subprocess import call
import pexpect
import shutil
from FF_SLT4 import SLT4
import time
from FF_SLT4_ScreenNavigator import ScreenUtil

HOST = 'devices-rpi1.local'
USERNAME = 'pi'
PASSWORD = 'Rathb0n3'

def ssh(host, cmd, user, password, timeout=30):
    ssh_cmd = 'ssh %s@%s "%s"' % (user, host, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.expect(pexpect.EOF)
    child.close()
    if 0 != child.exitstatus:
        raise Exception('Command {0} has failed with status {1}'.format(cmd, child.exitstatus))



def scp(host, file_name, user, password, output_file_path, timeout=30):
    scp_cmd = 'scp ' + USERNAME + '@' + HOST + ':{0} .'
    scp_cmd = scp_cmd.format(file_name)
    print('The scp command is {0}'.format(scp_cmd))
    child = pexpect.spawn(scp_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.expect(pexpect.EOF)
    child.close()
    if 0 != child.exitstatus:
        raise Exception('Command {0} has failed with status {1}'.format(scp_cmd, child.exitstatus))
    path = os.path.abspath(str(output_file_path))
    timestamp = datetime.datetime.today().strftime('%d-%b-%Y %H:%M:%S')
    final_file_path = output_file_path+ '/' + timestamp +'.jpg'
    shutil.move(file_name, final_file_path)
    return final_file_path


class SLT4OCRUtil(object):

    SCREEN_TEXT = {
        'HOME_SCREEN_MESSAGE' : 'dial to change temperature'
    }

    def __init__(self, screenshot_folder, stat_instance, mode):
        print('Initialising the SLT4 display utility')
        self.screenshot_folder = screenshot_folder
        self.stat_instance = stat_instance
        self.mode = mode


    def _capture_remote_image(self, host, user, password):
        '''Login to the raspberry pi , Take a image test.jpg and copy the same to local using a timestamp'''
        command_string = 'rm -f test.jpg;raspistill --timeout 2 -q 100 -br 50 -sh 100 -ex night -awb auto -o test.jpg -ss 10000 -hf'
        ssh(host, command_string, user, password)
        return scp(host, 'test.jpg', user, password, self.screenshot_folder)


    def _capture_local_image(self):
        print('Local mode detected , Capturing the image in local pi')
        path = os.path.abspath(str(self.screenshot_folder))
        timestamp = datetime.datetime.today().strftime('%d-%b-%Y %H:%M:%S')
        image_filename_with_path = path + '/capture' + timestamp + '.jpg'
        call(["raspistill", "--timeout", "2", "-q", "100", "-br", "50", "-sh", "100", "-ex", "night", "-awb", "auto",
              "-o", image_filename_with_path, "-ss", "10000", "-hf"])
        print('Capture Local , The image file path is {0}'.format(image_filename_with_path))
        return image_filename_with_path


    def _load_image(self,file_name):
        # path = os.path.abspath(str(context.reporter.strCurrentScreenshotFolder))
        print('Loading the file {0}'.format(file_name))
        img = Image.open(file_name)
        img = ImageOps.autocontrast(img)
        return img



    def _get_displayed_text_as_array(self, image):
        print('Attempting to get the system mode')
        text = pytesseract.image_to_string(image, lang='eng', boxes=False, config='--psm 6')
        text = str(text).encode('ascii', 'ignore').decode('ascii')
        print('The text is {0}'.format(text))
        lines = []
        for line in text.split('\n'):
            if len(line) > 0:
                lines.append(line.lower())
        return lines



    def _does_display_has_text(self, input_array, text_to_search):
        text_to_search = text_to_search.lower()
        print('The text to search is {0}'.format(text_to_search))
        print('The input array is  {0}'.format(input_array))
        is_text_located = False
        for line in input_array:
            if text_to_search in line:
                is_text_located = True
                break
        return is_text_located


    def _get_digits_new(self, arr):
        stat_scale = self.stat_instance.get_current_device_scale()
        if stat_scale == 'CELCIUS':
            required_len = 6
        else:
            required_len = 4

        print('The input lines are here {0}'.format(arr))
        index = None
        for item in arr:
            if 'ACT' in item.upper():
                index = arr.index(item)
                print('The index is {0}'.format(index))
                break

        if index == None:
            raise 'Unable to search for values , please ensure that a proper image is taken '

        possible_number = re.findall('\d+', arr[index-1])
        possible_number = ''.join(possible_number)
        print('The possible number obtained in the first iteration is {0}'.format(possible_number))
        length_obtained = len(possible_number)
        if length_obtained < required_len:
            remaining_find = required_len - length_obtained
            previous_possible_number = re.findall('\d+', arr[index -2])
            previous_possible_number = ''.join(previous_possible_number)
            previous_possible_number = previous_possible_number[:length_obtained]
            possible_number = previous_possible_number + possible_number
        print('The possible number located is {0}'.format(possible_number))
        if stat_scale == 'CELCIUS':
            target_temp = float(possible_number[0:2] + '.' + possible_number[2:3])
            current_temp = float(possible_number[3:5] + '.' + possible_number[5:6])
        else:
            target_temp = possible_number[:2]
            current_temp = possible_number[2:4]
        return target_temp,current_temp






    def _get_digits_for_dual(self, s):
        s = ''.join(s)
        s = re.findall('\d+', s)
        s = ''.join(s)
        if len(s) < 8:
            raise Exception(
                'Cannot determine the temperature , Please ensure that the image is correctly captured, The located digit is {0}'.format(
                    s))
        cool_hold_temp = float(s[0:2] + '.' + s[2:3])
        actual_temp = float(s[3:5] + '.' + s[5:6])
        heat_hold_temp = float(s[6:8] + '.' + s[8:9])
        print('The values are {0}, {1}, {2}'.format(cool_hold_temp, actual_temp, heat_hold_temp))
        return cool_hold_temp, actual_temp, heat_hold_temp


    def capture(self):
        if self.mode == 'REMOTE':
            file_name = self._capture_remote_image(HOST, USERNAME, PASSWORD)
        else:
            file_name = self._capture_local_image()
            '''Allow the image to be transferred completely '''
        time.sleep(5)
        return file_name


    def get_weighted_color_average(self, img):
        val = img.histogram()
        red_count = 0
        blue_count = 0
        green_count = 0
        for red_index in range(0, 256):
            red_count += val[red_index]*red_index
        for green_index in range(256, 512):
            green_count += val[green_index]*(green_index-256)
        for blue_index in range(512, 768):
            blue_count += val[blue_index]*(blue_index-512)
        total_values = red_count+ blue_count + green_count
        red_percent = red_count / total_values*100
        blue_percent = blue_count / total_values*100
        green_percent = green_count / total_values*100
        print('The overall percent is R:{0}, G:{1}, B:{2}'.format(red_percent, green_percent, blue_percent))
        return red_percent, green_percent, blue_percent,


    def _determine_op_mode(self, image_lines):
        ''' AT times we dont get reliable output from the OCR , Just determine if the outout has a
            K followed by cool or heat for heat / cool boost'''
        print('The input lines are {0}'.format(image_lines))
        operation_mode = ''
        if self._does_display_has_text(image_lines, 'CK HEAT'):
            operation_mode = 'HEAT_BOOST'

        elif self._does_display_has_text(image_lines, 'CK COOL'):
            operation_mode =  'COOL_BOOST'

        elif self._does_display_has_text(image_lines, 'OFF'):
            operation_mode =  'OFF'

        elif self._does_display_has_text(image_lines, 'VACATION'):
            operation_mode =  'VACATION MODE'

        elif self._does_display_has_text(image_lines, 'HOLD'):
            operation_mode = 'HOLD'

        elif self._does_display_has_text(image_lines, 'SCHEDULE'):
            operation_mode = 'SCHEDULE'

        elif self._does_display_has_text(image_lines, 'OFF'):
            operation_mode = 'OFF'

        return operation_mode


    def get_current_stat_mode(self, image=None):
        operation_mode = ''
        self.stat_instance.press_dial()
        retry_count = 0
        if image is None:
            image = self._load_image(self.capture())

        image_lines = self._get_displayed_text_as_array(image)
        # Check if System mode is off

        operation_mode = self._determine_op_mode(image_lines)



        '''Retry one more time When there is an issue in getting operation mode '''
        if len(operation_mode) == 0:
                self.stat_instance.press_dial()
                image = self._load_image(self.capture())
                image_lines = self._get_displayed_text_as_array(image)
                operation_mode = self._determine_op_mode(image_lines)


        if 'BOOST' in operation_mode or 'OFF' in operation_mode or 'VACATION' in operation_mode:
            return operation_mode

        _r,_g,_b = self.get_weighted_color_average(image)

        does_have_target = self._does_display_has_text(image_lines, 'ARGE') or self._does_display_has_text(image_lines, 'TA')

        if does_have_target == False:
            return 'DUAL ' + operation_mode

        if _r > _b and _r > _g:
            return 'HEAT ' + operation_mode

        if _b > _r and _b > _g:
            return 'COOL ' + operation_mode

        if _g > _r and _g > _b:
            return 'COOL ' + operation_mode

        ''' Dual mode does not have a taget string '''


        return 'UNKNOWN'


    def get_current_humidity_value(self):
        try:
            wiring_state = self.stat_instance.get_stat_wiring_state()
            if 'Acc' not in wiring_state:
                raise Exception('The device is not wired for humidity control , Cannot get the humidity percentage')
        except(Exception):
            print(' An error occurred while getting the device wiring state , Making a best possible guess')
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        for line in image_lines:
            if '%' in line:
                print('The line is {0}'.format(line))
                return line[-3:-1]

        raise Exception('Unable to get the humidity percentage from the UI , POssibly the image is not clear')


    def get_current_temp_and_target_temp(self):
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        print('The image lines are {0}'.format(image_lines))
        current_stat_mode = self.stat_instance.get_current_mode()
        print('The current stat mode is {0}'.format(current_stat_mode))
        possible_number_text = ''

        if 'DUAL' in current_stat_mode:
            possible_number_text = self._get_digits_for_dual(image_lines[3:])
        else:
            possible_number_text = self._get_digits_new(image_lines)
        return possible_number_text



    def get_screen_timer_value(self, retry_count = 2):
        attempt = 0
        while attempt < retry_count:
            image = self._load_image(self.capture())
            image_lines = self._get_displayed_text_as_array(image)
            '''Remove the first item in the index'''
            match = None
            image_lines.pop(0)
            for line in image_lines:
                match = re.search('[0-9]{1,2}:[0-9]{2}:[0-9]{1,2}', line)
                if match != None:
                    timer_values = match.group(0).split(':')
                    return int(timer_values[0]), int(timer_values[1])
            else:
                ++attempt
                continue
        ''' If we dont find a match , then report the values seperately'''
        return -1, -1


    def get_protection_timer_value(self):
        self.stat_instance.press_dial()
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        '''Remove the first item in the index'''
        match = None
        image_lines.pop(0)
        for line in image_lines:
            match = re.search('[0-9]{1}:[0-9]{1,2}', line)
            if match != None:
                break
        if match == None:
            ''' If we dont find a match , then report the values seperately'''
            return -1, -1
        timer_values = match.group(0).split(':')
        return int(timer_values[0]), int(timer_values[1])


    def is_protection_timer_on(self):
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        return self._does_display_has_text(image_lines, 'ON IN')


    def is_device_name_is_displayed(self, expected_name):
        self.stat_instance.press_dial()
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        return self._does_display_has_text(image_lines, expected_name)



    def is_em_heat_on(self):
        if self.stat_instance.is_emergency_heat_wired()  == False:
            return False
        self.stat_instance.press_dial()
        image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)
        return self._does_display_has_text(image_lines, 'emergency') or self._does_display_has_text(image_lines, 'EM')



    ''' Get the current displayed humidity percentage '''
    def get_set_humidity_percent(self):
        wiring_state = self.stat_instance.get_stat_wiring_state()
        if 'Acc' not in wiring_state:
            print('The device is not wired for humidity ')
            return -100
        retry = 0
        while retry < 3:
            self.stat_instance.press_dial()
            image = self._load_image(self.capture())
            image_lines = self._get_displayed_text_as_array(image)
            print('The image lines are {0}'.format(image_lines))
            possible_number = image_lines[3]
            merged_num = ''
            for element in possible_number.split():
                merged_num+=str(element)
            match = re.search('[0-9]{2}', merged_num)
            if match != None:
                return match.group(0)
            ++retry
        return -1

    '''UI Schedule Functions'''


    def get_schedule_details(self, image=None):
        operation_mode = ''
        # self.stat_instance.press_dial()
        retry_count = 0
        if image is None:
            image = self._load_image(self.capture())
        image_lines = self._get_displayed_text_as_array(image)

        print(image_lines)
        # operation_mode = self._determine_op_mode(image_lines)


if __name__ == "__main__":
    #slt4 = SLT4('FAHRENHEIT')
    slt4 = SLT4('FAHRENHEIT')
    navigator = ScreenUtil(slt4)
    navigator.navigate_to('MORE_SCREEN')
    navigator.navigate_to_submenu('HUMIDITY', navigator.MORE_SUBMENU)
    ocrUtil = SLT4OCRUtil('/Users/bharath.gopalan/test-dir', slt4, 'REMOTE')
    print(ocrUtil.get_set_humidity_percent())
    #print('The device mode is {0}'.format(ocrUtil.get_current_stat_mode()))
    #print('The temps are {0}'.format(ocrUtil.get_screen_timer_value()))

    #print(ocrUtil.get_current_temp_and_target_temp())




    '''slt4.withMode('HEAT HOLD').with_heat_set_to_temperature(30).set()
    slt4.press_dial()
    current_temp, target_temp = ocrUtil.get_current_temp_and_target_temp()
    print('The current and target temp is {0}, {1}'.format(current_temp, target_temp))

    slt4.withMode('COOL HOLD').with_cooling_set_to_temperature(20).set()
    slt4.press_dial()
    current_temp, target_temp = ocrUtil.get_current_temp_and_target_temp()
    print('The current and target temp is {0}, {1}'.format(current_temp, target_temp))

    slt4.withMode('HEAT_BOOST').with_heat_set_to_temperature(31).set()
    slt4.press_dial()
    current_temp, target_temp = ocrUtil.get_current_temp_and_target_temp()
    print('The current and target temp is {0}, {1}'.format(current_temp, target_temp))

    slt4.withMode('COOL_BOOST').with_cooling_set_to_temperature(19).set()
    slt4.press_dial()
    current_temp, target_temp = ocrUtil.get_current_temp_and_target_temp()
    print('The current and target temp is {0}, {1}'.format(current_temp, target_temp))'''





    #slt4.press_dial()
    #slt4.press_dial()
    #print('The humidity percentage is {0}'.format(ocrUtil.get_humidity_percentage()))


    #print(ocrUtil._get_displayed_text_as_array('/Users/bharath.gopalan/screenshots/dual-hold.jpg'))
    #print(ocrUtil.get_current_temp_and_target_temp('/Users/bharath.gopalan/screenshots/heat-hold.jpg'))
