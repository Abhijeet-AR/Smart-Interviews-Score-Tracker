import sys
from datetime import date

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_row_no(s, gc):
    try:
        r_no = len(s.get_all_records())

    except IndexError:
        r_no = 0

    return r_no


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

file_path = '/Users/AR/Documents/Programming/Python/Pycharm/ScoreTracker/smartinterviewsscores-a81911f5ec09.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
gc = gspread.authorize(credentials)

names = ['Abhijeet Reddy', 'NIKIL REDDY MULAGUNDLA', 'Varagani Hemanth Kumar', 'Garine Akhil',
         'BANDA NIKHIL REDDY', 'DOKURU SUDHAMSH REDDY', 'Kuntla Likith Reddy', 'PALAKURTHY MANI SREEKAR',
         'GOPU M N G RAGHUNADH', 'R Tejaswini', 'Ainesh Phanithi', 'K TARUN BHARGAV', 'B Lekh Raj']

verifier = input('Are you sure you want to delete? : ')

if verifier == '' or verifier.lower() == 'yes':
    print('Deleting')

else:
    sys.exit()

date_today = date.today()
for name in names:
    sheet = gc.open('Smart Interviews Tracker').worksheet(name)

    row_no = get_row_no(sheet, gc)
    date = sheet.cell(row_no, 1).value
    if row_no and date == date_today.strftime("%d %b %y"):
        sheet.delete_row(row_no)
        sheet.delete_row(row_no)
        print('Deleted data of ', name)

print('Successful')
