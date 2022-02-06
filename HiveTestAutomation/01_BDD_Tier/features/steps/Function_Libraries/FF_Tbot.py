import time
import requests


class Tbot:
    def doorClose(self):
        url = 'http://10.19.1.96/doorsensorClose'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(url, headers)
        print(r)
        time.sleep(3)

    def doorOpen(self):
        url = 'http://10.19.1.96/doorsensorOpen'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(url, headers)
        print(r)
        time.sleep(3)

    def MotionSensor(self):
        url = 'http://10.19.1.96/motionsensor'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(url, headers)
        print(r)
        time.sleep(3)

    def resetMotionMotor(self):
        url = 'http://10.19.1.96/resetMotionMotor'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(url, headers)
        print(r)
        time.sleep(3)

    def resetDoorMotor(self):
        url = 'http://10.19.1.96/resetDoorMotor'
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(url, headers)
        print(r)
        time.sleep(3)

    def resetPosition(self):
        url = 'http://10.19.1.92/resetPosition'
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)

    def pressMenuButton(self):
        url = 'http://10.19.1.92/gotoPosition/?x=8&y=7&z=23'
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)

    def pressBackButton(self):
        url = 'http://10.19.1.92/gotoPosition/?x=8&y=15&z=23'
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)

    def pressTickButton(self):
        url = 'http://10.19.1.92/gotoPosition/?x=8&y=0&z=24'
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)

    def spinClockWise(self, intUnit):
        url = 'http://10.19.1.92/rotary/?move=clockwise&units=' + str(intUnit)
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)

    def spinAntiClockWise(self, intUnit):
        url = 'http://10.19.1.92/rotary/?move=anticlockwise&units=' + str(intUnit)
        '''headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': '10.19.1.37',
                   'Upgrade-Insecure-Requests': '1'}'''
        r = requests.get(url)
        print(r)
        time.sleep(3)
