import os
import smtplib
import time as t
from datetime import date

import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


def send_mail(success, names, error_msg):
    print('sending email')
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(os.environ.get("g_mail"), os.environ.get("g_pass"))

    if success:
        subject = 'Scores - Success'
        body = 'Scores of\n\n'

        for name in names:
            body += (name + '\n')

        body += '\nupdated Successfully.'

    else:
        subject = 'Scores - Failure'
        body = error_msg

    message = f'Subject : {subject}\n\n{body}\n'

    server.sendmail('abhijeet-ar@whatsapp.com', [os.environ.get("o_mail")],
                    message)

    print('email sent')


def check_first(rows, s):
    if rows == 2:
        s.insert_row([0] * 12, 5)

    else:
        col_ord = ord('B')

        t_data = ['']
        for i in range(12):
            col_alph = chr(col_ord + i)

            a = col_alph + str(rows + 2)
            b = col_alph + str(rows)

            if i == 0:
                t_data.append('=' + b + '-' + a)
                continue

            t_data.append('=' + a + '-' + b)

        s.insert_row(t_data, rows + 3, value_input_option='USER_ENTERED')


def get_row_no(s, gc, name):
    try:
        r_no = len(s.get_all_records())

    except IndexError:
        temp_sheet = gc.open('Smart Interviews Tracker').worksheet(name)

        for i in range(1, 4):
            temp = temp_sheet.row_values(i)
            s.insert_row(temp, i)

        r_no = len(s.get_all_records())

    return r_no


def process(names):
    date_today = date.today()

    useful_cols = [7, 8, 9, 12, 13, 16, 17, 20, 23, 24, 28]
    insert_data = {}

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    file_path = '/Users/AR/Documents/Programming/Python/Pycharm/ScoreTracker/smartinterviewsscores-a81911f5ec09.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
    gc = gspread.authorize(credentials)

    smart_interviews_url = os.environ.get('sm_url')
    smart_interviews_sheet = gc.open_by_url(smart_interviews_url).sheet1

    print('Retrieving Data')
    for name in names:
        row = smart_interviews_sheet.find(name).row
        data = smart_interviews_sheet.row_values(row)

        temp_data = [date_today.strftime("%d %b %y"), str(row - 2)]
        for col in useful_cols:
            temp_data.append(data[col])

        insert_data[name] = temp_data

    print('Data Retrieved')

    ind = 0
    for _ in range(10):
        try:
            for name in names[ind:]:
                sheet = gc.open('Smart Interviews Tracker').worksheet(name)

                row_no = get_row_no(sheet, gc, names[0])

                last_rank = sheet.cell(row_no, 2).value
                total_score = sheet.cell(row_no, 13).value
                data = insert_data[name]
                if last_rank != data[1] or total_score != data[-1]:
                    sheet.insert_row(data, row_no + 2)
                    check_first(row_no, sheet)

                ind += 1
                print('Updated data of ' + name)

        except gspread.exceptions.APIError:
            print('Request Limit Exceeded')
            t.sleep(100)


def main():
    names = list(os.environ.get('names').split(','))

    success = True
    error_msg = ''

    for i in range(15):
        try:
            process(names)
            error_msg = ''
            success = True
            break

        except httplib2.ServerNotFoundError:
            print('waiting for internet(3s)')
            error_msg = 'No Internet'
            success = False
            t.sleep(3)
            continue

        except gspread.exceptions.APIError:
            print('Request Limit Exceeded')
            t.sleep(100)
            continue

        except Exception as e:
            print(e)
            error_msg = e
            success = False
            break

    for i in range(1000):
        try:
            send_mail(success, names, error_msg)
            break

        except:
            print('failed')
            if i < 60:
                t.sleep(1)

            elif i < 70:
                print('waiting 1 min')
                t.sleep(60)

            else:
                print('waiting 1 hr')
                t.sleep(3600)

    print('Operations Completed')


if __name__ == '__main__':
    main()
