import matplotlib.pyplot as plt
import json, sys

if len(sys.argv) < 2:
    sys.exit('specify the unit number (eg. 28.1)')

unit = sys.argv[1]

file = 'unit' + unit + '.json'

with open(file) as json_file:
    unit_data = json.load(json_file)
    title = unit_data['title']
    xkcd = unit_data['xkcd']
    grid = unit_data['grid']
    plots = unit_data['plots']

def plotter ():
    if len(plots) != 1:
        sys.exit('not one plot')
    else:
        n = 0
    # set up the plot stuff
    plt.title(title)
    plt.subplots_adjust(left=0.15, bottom=0.15)
    # grab data from dictionary and add it to the plot
    plot = plots[n]
    x = plot['x']
    y = plot['y']

    # set x & y axis labels
    plt.xlabel(x['title'])
    plt.ylabel(y['title'])

    # actually do the plotting
    plt.plot(x['values'], y['values'], x['values'], y['values'], 'bo')

    # if grid is true, turn on the grid
    if grid:
        plt.grid()

    # show the grid
    plt.show()

# if xkcd is true, display the graph in xkcd style
if xkcd:
    with plt.xkcd():
        plotter()
# otherwise, display it normally
else:
    plotter()