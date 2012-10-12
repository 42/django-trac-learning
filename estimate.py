import math
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
from sklearn.svm import SVR

#from fun1 import get_data
#from fun2 import get_data
from fun3 import get_data

def learn(kernel='rbf', param_grid=None):
    tickets, times = get_data()

    tickets_train, tickets_test, times_train, times_test = \
        cross_validation.train_test_split(tickets, times, 
                                          test_size=0.2, random_state=0)
    clf = GridSearchCV(estimator=SVR(kernel=kernel), 
                       param_grid=param_grid,
                       n_jobs=-1)
    clf.fit(tickets_train, times_train)

    times_train_predict = clf.predict(tickets_train)
    times_test_predict = clf.predict(tickets_test)

    train_error = metrics.mean_squared_error(times_train, times_train_predict)
    test_error = metrics.mean_squared_error(times_test, times_test_predict)

    print 'Train error: %.1f Test error: %.2f' % (
        math.sqrt(train_error)/(24*3600), math.sqrt(test_error)/(24*3600))
    print 'Best C: %.1e' % clf.best_estimator_.C

learn('rbf', param_grid=dict(C=np.logspace(-1,10,5)))
