import matplotlib.pyplot as plt

# x variables
x_title = 'Displacement (m)'
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

# y variables
y_title = 'Force (N)'
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

with plt.xkcd():
    plt.plot(x, y, 'bo', x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.grid()
    plt.show()
