import csv
import datetime as dt
import numpy as np
import scipy.sparse as sp
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer, \
        TfidfTransformer
import time

def total_seconds(dt):
    return dt.days*24*3600 + dt.seconds

def get_data():
    tickets_file = csv.reader(open('2012-10-09.close.csv'))

    time_format = '%Y-%m-%d %H:%M:%S'
    tickets = []
    times = []
    reporters = []
    subjects = []
    components = []

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
        reporters.append(reporter)
        subjects.append(summary)
        components.append(component)

    scaler = preprocessing.Scaler().fit(np.array(tickets))
    tickets = sp.csr_matrix(scaler.transform(tickets))
    tickets = sp.hstack((tickets, TfidfTransformer().fit_transform(
                CountVectorizer().fit_transform(reporters))))
    tickets = sp.hstack((tickets, TfidfTransformer().fit_transform(
                CountVectorizer(ngram_range=(1,3)).fit_transform(subjects))))
    tickets = sp.hstack((tickets, TfidfTransformer().fit_transform(
                CountVectorizer().fit_transform(components))))

    scaler = preprocessing.Scaler(with_mean=False).fit(tickets)
    tickets = scaler.transform(tickets)
    return tickets, times
