# Reeds-Shepp Curves

A simple implementation of the Reeds-Shepp curves formulas provided in the following research paper:

Reeds, J. A.; Shepp, L. A. Optimal paths for a car that goes both forwards and backwards. Pacific J. Math. 145 (1990), no. 2, 367-393.
https://projecteuclid.org/euclid.pjm/1102645450

### Requirements

You will need the `turtle` module to run the demo and draw the generated paths, but you can also use the functions provided in `reeds_shepp.py` without drawing anything.

I have only tested the code under Python 3.7.1. It uses the `enum` module so it will not run on a version lower than 3.4, but the code could easily be modified to make it work with Python 2 by using custom enumerations.

### Examples

Draw all the paths going through all the vectors as well as the shortest one (each vector represents a position and an angle):

```
$ python3 demo.py
```

![Reeds-Shepp curves implementation example](demo1.gif)

Another example without drawing:

```python
import reeds_shepp as rs
import utils
import math

# a list of vectors
ROUTE = [(-2,4,180), (2,4,0), (2,-3,90), (-5,-6,240), (-6, -7, 160), (-7,-1,80)]

full_path = []
total_length = 0

for i in range(len(ROUTE) - 1):
    path = rs.get_optimal_path(ROUTE[i], ROUTE[i+1])
    full_path += path
    total_length += rs.path_length(path)

print("Shortest path length: {}".format(round(total_length, 2)))

for e in full_path:
    print(e)
```

Output:

```
Shortest path length: 33.94

{ Steering: left        Gear: backward  distance: 0.0 }
{ Steering: straight    Gear: backward  distance: 2.0 }
{ Steering: left        Gear: backward  distance: 1.57 }
{ Steering: right       Gear: forward   distance: 1.57 }
{ Steering: right       Gear: forward   distance: 1.74 }
{ Steering: straight    Gear: forward   distance: 4.08 }
{ Steering: right       Gear: forward   distance: 1.57 }
{ Steering: left        Gear: backward  distance: 1.41 }
{ Steering: right       Gear: backward  distance: 0.46 }
{ Steering: left        Gear: forward   distance: 1.57 }
{ Steering: straight    Gear: forward   distance: 5.95 }
{ Steering: left        Gear: forward   distance: 0.59 }
{ Steering: left        Gear: backward  distance: 0.22 }
{ Steering: right       Gear: backward  distance: 0.46 }
{ Steering: left        Gear: forward   distance: 0.46 }
{ Steering: right       Gear: forward   distance: 2.1 }
{ Steering: left        Gear: forward   distance: 0.6 }
{ Steering: right       Gear: backward  distance: 1.57 }
{ Steering: straight    Gear: backward  distance: 2.47 }
{ Steering: left        Gear: backward  distance: 1.57 }
{ Steering: right       Gear: forward   distance: 2.0 }
```
