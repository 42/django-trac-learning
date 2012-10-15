import math
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor

from fun6 import get_data

def learn(param_grid=None,):
    tickets, times = get_data()

    tickets_train, tickets_test, times_train, times_test = \
        cross_validation.train_test_split(tickets, times, 
                                          test_size=0.2, random_state=0)
    clf = GridSearchCV(estimator=KNeighborsRegressor(),
                       param_grid=param_grid,
                       n_jobs=1)
    clf.fit(tickets_train, times_train)

    times_train_predict = clf.predict(tickets_train)
    times_test_predict = clf.predict(tickets_test)

    train_error = metrics.mean_squared_error(times_train, times_train_predict)
    test_error = metrics.mean_squared_error(times_test, times_test_predict)

    print 'Train error: %.1f Test error: %.2f' % (
        math.sqrt(train_error)/(24*3600), math.sqrt(test_error)/(24*3600))
    print 'Best # of neighbors: %.1e' % clf.best_estimator_.n_neighbors

learn(param_grid=dict(n_neighbors=range(3,11)))
