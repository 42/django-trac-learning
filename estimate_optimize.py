import math
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn import metrics
from sklearn.svm import SVR

from fun1 import get_data
#from fun2 import get_data
#from fun3 import get_data
#from fun4 import get_data
#from fun5 import get_data
#from fun6 import get_data

def learn(params, kernel='rbf', verbose=True):
    tickets, times = get_data()

    tickets_train, tickets_test, times_train, times_test = \
        cross_validation.train_test_split(tickets, times, 
                                          test_size=0.2, random_state=0)
    clf = SVR(kernel=kernel, verbose=verbose, C=params[0], gamma=params[1])
    print 'For', clf
    clf.fit(tickets_train, times_train)

    times_train_predict = clf.predict(tickets_train)
    times_test_predict = clf.predict(tickets_test)

    train_error = metrics.mean_squared_error(times_train, times_train_predict)
    test_error = metrics.mean_squared_error(times_test, times_test_predict)

    print 'Train error: %.1f Test error: %.1f' % (
        math.sqrt(train_error)/(24*3600), math.sqrt(test_error)/(24*3600))
    return test_error

from scipy.optimize import fmin, fmin_bfgs

print 'RBF'
print fmin(learn, [11e7, 9e7],
           full_output = True,
           disp = True)

# learn('rbf', param_grid=dict(C=np.logspace(6,8,4),
#                              gamma=np.logspace(7,20,4)
#                              ))#, verbose=True)

# print '\nLinear'
# learn('linear', param_grid=dict(C=np.logspace(1,5,5)), verbose=True)

# print '\nSigmoid'
# learn('sigmoid', param_grid=dict(C=np.logspace(-10,1,5)), verbose=True)

# print '\nPoly'
# learn('poly', param_grid=dict(C=np.logspace(-1,10,5)), verbose=True)

# RBF
# Train error: 343.8 Test error: 350.20
# Best C: 5.6e+07
# Best gamma: 1.0e+05
