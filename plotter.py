import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from linearize import coefficients, combine, linearize_complete, rmse_metric
import json, sys, re, os
import argparse

# set up some options and save them to variables.
parser = argparse.ArgumentParser(description='Plot a graph based on the input file.')
parser.add_argument('file', metavar='file', type=str,
                    help='a file to pull data from')
parser.add_argument( '-t', '--threshold', default='0.01', help='rmse threshold to consider highest good value')
parser.add_argument('-s', '--save', dest='save', action='store_const',
                    const=True, default=False,
                    help='save the graph to a file (default: False)')
parser.add_argument('-l', '--linearize', dest='linearize', action='store_const',
                    const=True, default=False,
                    help='show a second, linearized graph')
parser.add_argument('-o', '--only', dest='only', action='store_const',
                    const=True, default=False,
                    help='show only the linearized graph')
args = parser.parse_args()

file = args.file
save = args.save
threshold = float(args.threshold)
linearize = args.linearize
only = args.only

# if the file doesn't exists, exit.
if not Path(file).is_file():
    sys.exit(f'{file} does\'t exist.')
else:
    filename = 'Figure ' + re.sub('\.json$', '.png', os.path.basename(file))

# open the unit file and grab data from it.
with open(file) as json_file:
    # set defaults, and load from data dict if exists.
    data = json.load(json_file)
    xkcd = True if 'xkcd' not in data else data['xkcd']
    grid = True if 'grid' not in data else data['grid']
    line = True if 'line' not in data else data['line']
    trend = True if 'trend' not in data else data['trend']

    # check to make sure plot exists and has x & y.
    if 'plot' not in data:
        sys.exit('no plot specified in the file')
    if 'x' not in data['plot']:
        sys.exit('no x data in the plot')
    if 'y' not in data['plot']:
        sys.exit('no y data in the plot')

    # save plot to variables.
    plot = data['plot']
    x = plot['x']
    y = plot['y']
    dataset = combine(x, y)

    # check that x & y have values.
    if 'values' not in x:
        sys.exit('no x values')
    if 'values' not in y:
        sys.exit('no y values')

def plotter (x, y, linearize):
    # set default titles, and use titles from dict if specified.
    xtitle = 'x' if 'title' not in x else x['title']
    ytitle = 'y' if 'title' not in y else y['title']
    title = f'{ytitle} vs. {xtitle}'

    # set window title, graph title, and adjust whitespace.
    fig = plt.figure()
    fig.canvas.set_window_title(re.sub('(\$)|(\\\)', '', re.sub('(\\\\to)', '→', title)))
    plt.title(title)
    plt.subplots_adjust(left=0.15, bottom=0.15)

    # set x & y axis labels
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    # plot the trend line (if trend is true).
    if trend and not linearize:
        b0, b1 = coefficients(dataset)
        trend_y = np.array(x['values'])*b1 + b0
        rmse = rmse_metric(y['values'], trend_y)
        if rmse > threshold:
            plt.plot(x['values'], trend_y, 'r')
            plt.plot([x['values'][0], x['values'][-1]], [trend_y[0], trend_y[-1]], 'ro')

    # plot the line first so it shows underneath (if line is true).
    if line:
        plt.plot(x['values'], y['values'])

    # plot the data points with blue circles.
    plt.plot(x['values'], y['values'], 'bo')

    # if grid is true, turn on the grid.
    if grid:
        plt.grid(linewidth='1')

    # if specified, save to file.
    if save:
        if linearize:
            plt.savefig(f'Linearized {filename}')
        else:
            plt.savefig(filename)

    # show the graph.
    plt.show()

# display some information about whether the graph needs to be straightened.
b0, b1 = coefficients(dataset)
separator = '+' if b0 >= 0 else '-'
b0 = b0 if b0 >= 0 else -b0
trend_y = np.array(x['values'])*b1 + b0
rmse = rmse_metric(y['values'], trend_y)
straight = True if rmse < threshold else False
y_values, straight_rmse, manipulations, iterations = linearize_complete(x['values'], y['values'], threshold)
manipulations_string = ' → '.join(manipulations)

dash_line = '----------------------------------------'
print(dash_line)
print(f'Trend Line (LBF):   {round(b1, 3)}x {separator} {round(b0, 3)}')
print(f'Trend Line RMSE:    {round(rmse, 4)}%')
print(f'Line is Straight:   {straight}')
if not straight:
    print(f'To Straighten:      {manipulations_string}')
    print(f'Straightened RMSE:  {round(straight_rmse, 4)}%')
    print(f'Iterations:         {iterations}.')
    print('Y Values After Straightening:')
    print(f'    {y_values}')
    if not linearize:
        print(f'To graph the linearized version, run the command with \'-l/--linearize\' appended.')
print(dash_line)


# if xkcd is true, display the graph in xkcd style.
if not (linearize and only):
    if xkcd:
        with plt.xkcd():
            plotter(x, y, False)
    else:
        plotter(x, y, False)

# if linearize is true, display the linearized graph with same xkcd rules.
if linearize and not straight:
    manipulations_string = '$' + ('\ \\to\ '.join(manipulations)) + '$'
    y['title'] = y['title'] + ' $\\to$ ' + manipulations_string
    y['values'] = y_values
    if xkcd:
        with plt.xkcd():
            plotter(x, y, True)
    else:
        plotter(x, y, True)
