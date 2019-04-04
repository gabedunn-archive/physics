# Physics
> A repo for my physics 20 & 30 course and the graphs I made with matplotlib for it.

## Usage
```bash
python plotter.py [-h] file [-t/--threshold THRESHOLD] [-s/--save] [-l/--linearize] [-o/--only]
```

## Help
```bash
python ploter.py --help
# ->
usage: plotter.py [-h] file [-t/--threshold THRESHOLD] [-s/--save] [-l/--linearize] [-o/--only]


Plots a graph based on the input file, and can also linearize the graph.

positional arguments:
  file                  a file to pull data from

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        rmse threshold to consider highest good value
  -s, --save            save the graph to a file (default: False)
  -l, --linearize       show a second, linearized graph
  -o, --only            show only the linearized graph
```

## TODO
- Try not use `sqrt(y)` in place of `y^2`.
- Add command overrides for all default graph options.