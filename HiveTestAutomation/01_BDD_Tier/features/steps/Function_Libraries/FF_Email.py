import email
import imaplib
import time
import FF_utils as utils


def findEmail(dict, notificationType):
    blnFlag = False
    intTime = 0
    emailFound = ''
    emailSubject = ''
    emailSubjectResp = ''
    blnSubject = False
    emailContents = ''
    blnContent = False

    if notificationType in dict.keys():
        emailSubject = dict[notificationType][0]
        emailContents = dict[notificationType][1]
        while not blnFlag and intTime < 6:
            emailSubjectResp = ''
            emailFound = loop()
            if emailFound is not '':
                blnFlag = True
                emailHeaders = emailFound.items()
                for eachHeader in emailHeaders:
                    if eachHeader[0] == 'Subject': emailSubjectResp = eachHeader[1]
                    if emailSubject == emailSubjectResp:
                        blnSubject = True
                        if emailFound.is_multipart():
                            emailContentResp = emailFound.get_payload()[0].get_payload()
                        else:
                            emailContentResp = emailFound.get_payload()
                        print(emailContentResp)
                        for emailContent in emailContents:
                            if emailContent in emailContentResp:
                                blnContent = True
                            else:
                                blnContent = False

            time.sleep(10)
            intTime = intTime + 1

    return blnFlag, blnSubject, blnContent


def loop():
    emailProtocol = utils.getAttribute('', 'EMAIL_PROTOCOL')
    mail = imaplib.IMAP4_SSL(emailProtocol, 993)
    unm = utils.getAttribute('', 'Email_ID')
    pwd = utils.getAttribute('', 'Email_Password')
    mail.login(unm, pwd)
    mail.select('INBOX')

    (retcode, messages) = mail.search(None, '(UNSEEN)')
    emailFrom = ''
    emailFound = ''
    if retcode == 'OK':

        for num in messages[0].split():

            typ, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    original = email.message_from_bytes(response_part[1])
                    mailHeaders = original.items()
                    for eachHeader in mailHeaders:
                        if eachHeader[0] == 'From':
                            emailFrom = eachHeader[1]
                            if 'Hive' in emailFrom:
                                emailFound = original
                                break
    mail.logout()
    return emailFound


def readAllExistingEmails():
    emailProtocol = utils.getAttribute('', 'EMAIL_PROTOCOL')
    mail = imaplib.IMAP4_SSL(emailProtocol, 993)
    unm = utils.getAttribute('', 'Email_ID')
    pwd = utils.getAttribute('', 'Email_Password')
    mail.login(unm, pwd)
    mail.select('INBOX')

    (retcode, messages) = mail.search(None, '(UNSEEN)')
    emailFrom = ''
    emailFound = ''
    if retcode == 'OK':

        for num in messages[0].split():

            typ, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    original = email.message_from_bytes(response_part[1])
                    mailHeaders = original.items()
                    for eachHeader in mailHeaders:
                        if eachHeader[0] == 'From':
                            emailFrom = eachHeader[1]
                            if 'Hive' in emailFrom:
                                emailFound = original
    mail.logout()
