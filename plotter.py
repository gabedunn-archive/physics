import matplotlib.pyplot as plt
import json, sys, re

# grab course level from args
if len(sys.argv) < 2:
    sys.exit('specify the course level (eg. 30)')
else:
    level = sys.argv[1]

# grab unit number from args
if len(sys.argv) < 3:
    sys.exit('specify the unit number (eg. 28.1)')
else:
    unit = sys.argv[2]

# grab whether to save as a file from args. '1' and 'true' will save an image.
if len(sys.argv) == 4:
    save = True if (sys.argv[3] == '1' or sys.argv[3] =='true') else False
else:
    save = False

file = f'units/{level}/{unit}.json'

with open(file) as json_file:
    unit_data = json.load(json_file)
    xkcd = unit_data['xkcd']
    grid = unit_data['grid']
    trend = unit_data['trend']
    plots = unit_data['plots']
    xtitle = plots[0]['x']['title']
    ytitle = plots[0]['y']['title']
    title = f'{ytitle} vs. {xtitle}'

def plotter ():
    if len(plots) != 1:
        sys.exit('not one plot')
    else:
        n = 0
    # set up the plot stuff
    fig = plt.figure()
    fig.canvas.set_window_title(re.sub('\$', '', title)) 
    plt.title(title)
    plt.subplots_adjust(left=0.15, bottom=0.15)
    # grab data from dictionary and add it to the plot
    plot = plots[n]
    x = plot['x']
    y = plot['y']

    # set x & y axis labels
    plt.xlabel(x['title'])
    plt.ylabel(y['title'])

    # plot the trend line first so it shows underneath (if trend is true)
    if trend:
        plt.plot(x['values'], y['values'])
    # plot the data points with blue circles
    plt.plot(x['values'], y['values'], 'bo')

    # if grid is true, turn on the grid
    if grid:
        plt.grid()

    # if specified, save to file
    if save:
        plt.savefig(f'Physics {level} Figure {unit}.png')

    # show the grid
    plt.show()

# if xkcd is true, display the graph in xkcd style
if xkcd:
    with plt.xkcd():
        plotter()
# otherwise, display it normally
else:
    plotter()