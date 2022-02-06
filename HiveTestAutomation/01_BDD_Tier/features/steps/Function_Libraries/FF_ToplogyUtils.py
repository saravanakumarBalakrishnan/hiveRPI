"""
Created on 06 Dec 2016

@author: Kingston.SamSelwyn
"""

import requests
import nmap

attenList = {"1_2": "192.168.130.220",
             "1_3": "192.168.130.55",
             "2_4": "192.168.130.225",
             "3_4": "192.168.130.225",
             "1_4": "192.168.130.225",
             "2_3": "192.168.130.225"}


def setTopology(strAtten, db):
    if 0 <= int(db) <= 90:
        url = 'http://' + strAtten + '/SETATT=' + str(db)
        resp = requests.get(url)
        if str(resp.text) == "1":
            return resp.text
        else:
            return 0
    else:
        return 0


def getAttenuatorsIP(context):
    context.attenList = attenList
    oNm = nmap.PortScanner()
    oNm.scan('10.19.0-3.0-255', '23', '-open')
    oNm.command_line()
    oNm.scaninfo()
    for oIP in oNm.all_hosts():
        if str(oNm[oIP].tcp(23)['state']).upper() == "OPEN":
            print('\n ' + str(oIP))
            url = 'http://' + oIP
            try:
                r = requests.get(url)
                if "RCDAT" in str(r.text):
                    strSN = str(r.text).replace('-99 Unrecognized Command. Model: RCDAT-6000-90   		 SN=', '')
                    strSN = strSN.replace('-99 Unrecognized Command. MN:RCDAT-6000-90 SN:', '')
                    if "11407310057" in strSN:
                        Route = "2_4"
                        attenList[Route] = oIP
                    if "11407310041" in strSN:
                        Route = "2_3"
                        attenList[Route] = oIP
                    if "11407310058" in strSN:
                        Route = "1_2"
                        attenList[Route] = oIP
                    if "11407310038" in strSN:
                        Route = "1_3"
                        attenList[Route] = oIP
                    if "11705210026" in strSN:
                        Route = "1_4"
                        attenList[Route] = oIP
                    if "11705210027" in strSN:
                        Route = "3_4"
                        attenList[Route] = oIP
            except:
                print("error occured")
    print(str(attenList))
    return attenList
