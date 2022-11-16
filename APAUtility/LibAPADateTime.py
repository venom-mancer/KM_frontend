import jdatetime

import datetime


def get_persian_date():
    """تاریخ جلالی"""
    return convert_gregorian2jalili(datetime.datetime.now())


def convert_gregorian2jalili(date_in_gregorian):
    """تبدیل تاریخ میلادی به جلالی"""
    jalai_date = str(jdatetime.date.fromgregorian(day=date_in_gregorian.day, month=date_in_gregorian.month,
                                                  year=date_in_gregorian.year)).replace("-", "/")
    return jalai_date


def remove_slash_mark(normal_perian_date):
    """حذف کردن اسلش های تاریخ"""
    return normal_perian_date.replace("/", "")


def get_persian_date_normalized():
    return int(remove_slash_mark(get_persian_date()))

def get_persian_year_normalized():
    full_date = int(remove_slash_mark(get_persian_date()))
    return int(str(full_date)[:4])


def read_date(str2):
    strread = str(str2)
    mm = strread[4:6]
    dd = strread[6:8]
    if mm[0] == '0':
        mm2 = mm[1]
    else:
        mm2 = mm
    if dd[0] == '0':
        dd2 = dd[1]
    else:
        dd2 = dd
    outstr = strread[0:4] + "/" + mm2 + "/" + dd2
    return outstr


def check_date(str2):
    strread = str(str2)
    yy = strread[0:4]
    mm = strread[4:6]
    dd = strread[6:8]
    outd = True
    if int(yy) < 1300 or int(yy) > 1500:
        print('year is not range')
        outd = False
    if (int(mm) <= 0) or (int(mm) > 12):
        print('month is not range')
        outd = False
    if int(mm) <= 6 and (int(dd) > 31) or (int(dd) <= 0):
        print('day is not range')
        outd = False
    if ((int(mm) > 6) and (int(mm) <= 12)) and ((int(dd) > 30) or (int(dd) <= 0)):
        print('day is not range')
        outd = False
    if int(dd) > 31:
        print('day is not range')
        outd = False

    return outd
