#!/usr/bin/env python2
import datetime

months = {}
months['January'] = 1
months['February'] = 2
months['March'] = 3
months['April'] = 4
months['May'] = 5
months['June'] = 6
months['July'] = 7
months['August'] = 8
months['September'] = 9
months['October'] = 10
months['November'] = 11
months['December'] = 12

with open("date.txt", "r") as f:
    content = f.read()

lines = content.split('\n')
count = 0
for line in lines:
    parts = line.split(' ')
    month = parts[0]
    day = parts[1][:-1]
    year = parts[2]
    # leap years...
    if month == "February":
        try:
            weekday = datetime.datetime(int(year)+1, months[month], int(day)).weekday()
        except:
            continue
    else:
        weekday = datetime.datetime(int(year)+1, months[month], int(day)).weekday()
    # monday == 0
    if weekday == 4:
        count += 1

print "There are %d Fridays" % count


