import datetime as dt
import numpy as np
import csv
from sklearn import preprocessing
import time

def total_seconds(dt):
    return dt.days*24*3600 + dt.seconds

def get_data():
    tickets_file = csv.reader(open('2012-10-09.close.csv'))

    tickets = []
    times = []
    time_format = '%Y-%m-%d %H:%M:%S'

    for number, created, changetime, closetime, reporter, summary, status, \
            owner, tkt_type, component, description in tickets_file:
        row = []
        created = dt.datetime.strptime(created, time_format)
        closetime = dt.datetime.strptime(closetime, time_format)
        changetime = dt.datetime.strptime(changetime, time_format)
        time_to_fix = closetime - created

        row.append(float(number))
        row.append(float(time.mktime(created.timetuple())))

        tickets.append(row)
        times.append(total_seconds(time_to_fix))

    scaler = preprocessing.Scaler().fit(np.array(tickets))
    tickets = scaler.transform(tickets)

    return tickets, times
