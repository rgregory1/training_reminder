# python3

import credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import smtplib
import time


scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Mandatory Training Responses 17-18').sheet1

staff_responses = sheet.get_all_records()

gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password

staff_email_list = []
for staff in staff_responses:
    if staff['Staff Member'] != '':     # check to make sure there is a name in the staff column
        na_list = []
        if '#N/A' in staff.values(): # if this appears anywhere in the dict, loop over all the key, value pairs.
            for key, value in staff.items():
                if value == '#N/A':
                    na_list.append(str(key))
            staff_email_list.append({'email' : staff['Staff Member'], 'missing': na_list})
pprint(staff_email_list)


for tardy_staff in staff_email_list:
    sent_from = 'jjennett@fnwsu.org    '
    to = tardy_staff['email']
    subject = 'Mandatory Training Reminder'
    body = 'According to our records, you need to complete the following sections of the Mandatory Trainings \n'
    missing_list = ", ".join(tardy_staff['missing'])
    body2 = 'Please visit the Swanton Mandatory Training site when you can to finish, please have this done by Winter Break! \n \n https://sites.google.com/a/fnwsu.org/swanton-school-mandatory-training-site/ '
    body3 = 'This is an automated message, please DO NOT respond to it!'
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s \n
    %s \n
    %s \v
    %s
    """ % (sent_from, to, subject, body, missing_list, body2, body3)

    print('sending email to ' + tardy_staff['email'])
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('email sent!')
    except:
        print('Something went wrong...')
    time.sleep(5)
print('finished with staff emails')


sent_from = gmail_user
to = ['jjennett@fnwsu.org', 'dstamour@fnwsu.org', 'rgregory@fnwsu.org']
subject = 'Mandatory Trainings Notifications Sent'
body = 'Reminders to complete the Mandatory Trainings have been sent to the followint people'
report = ''
for staff in staff_email_list:
    missing_list = ", ".join(staff['missing'])
    report = report + staff['email'] + ' - ' + missing_list + '\n'


email_text = """\
From: %s
To: %s
Subject: %s

%s \n
%s
""" % (sent_from, ", ".join(to), subject, body, report)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Report email sent!')
except:
    print('Something went wrong...')
