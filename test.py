from math import sqrt

x = [
    0.008,
    0.022,
    0.036,
    0.052,
    0.067,
    0.082,
    0.096,
    0.111,
    0.125,
    0.275
]
y = [
    0.196,
    0.294,
    0.392,
    0.491,
    0.589,
    0.687,
    0.785,
    0.883,
    0.981,
    1.96
]

def mean(vals):
    return sum(vals)/float(len(vals))

def variance(values, mean):
    return sum([(x-mean)**2 for x in values])

def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

def coefficients(x, y):
    def mean(vals):
        return sum(vals)/float(len(vals))
    def variance(values, mean):
        return sum([(x-mean)**2 for x in values])
    def covariance(x, mean_x, y, mean_y):
        covar = 0.0
        for i in range(len(x)):
            covar += (x[i] - mean_x) * (y[i] - mean_y)
        return covar

    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]


b0, b1 = coefficients(x, y)
print('Coefficients: B0=%.3f, B1=%.3f' % (b0, b1))

def simple_linear_regression(train, test):
    predictions = list()
    train_x = [i[0] for i in train]
    train_y = [i[0] for i in train]
    b0, b1 = coefficients(train_x, train_y)
    for row in test:
        yhat = b0 + b1 * row[0]
        predictions.append(yhat)
    return predictions

def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

def make_test_set(x):
    return [[i, None] for i in x]
 
def evaluate_algorithm(dataset, algorithm):
    x = dataset[0]
    y = dataset[1]
    test_set = make_test_set(x)
    predicted = algorithm(dataset, test_set)
    print(predicted)
    actual = [row[-1] for row in dataset]
    rmse = rmse_metric(actual, predicted)
    return rmse

x = [1, 2, 4, 3, 5]
y = [1, 3, 3, 2, 5]

rmse = evaluate_algorithm([x, y], simple_linear_regression)
print('RMSE: %.3f' % (rmse))