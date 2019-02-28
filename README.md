# Reeds-Shepp Curves

A simple Python implementation of the Reeds-Shepp curves formulas provided in the following paper:

Reeds, J. A.; Shepp, L. A. Optimal paths for a car that goes both forwards and backwards. Pacific J. Math. 145 (1990), no. 2, 367-393.
https://projecteuclid.org/euclid.pjm/1102645450

### Requirements

You will need the `turtle` module to run the demo and draw the generated paths, but you can also use the functions provided in `reeds_shepp.py` without drawing anything.

I have only tested the code under Python 3.7.1. It uses the `enum` module so it will not run on a version below 3.4, but one could easily adapt the code to make it work with Python 2 by replacing the `enum`s by global constants.

### Examples

Draw all the paths going through all the vectors as well as the shortest one (each vector represents a position and an angle, its length does not represent anything).

```
$ python3 demo.py
```

![Reeds-Shepp curves implementation example](demo.gif)

Another example without drawing:

```python
import reeds_shepp as rs
import utils
import math

# a list of "vectors" (x, y, angle in degrees)
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
    # e.steering (LEFT/RIGHT/STRAIGHT), e.gear (FORWARD/BACKWARD), e.param (distance)
```

Output:

```
Shortest path length: 29.53

{ Steering: straight    Gear: backward  distance: 2.0 }
{ Steering: left        Gear: backward  distance: 1.57 }
{ Steering: right       Gear: forward   distance: 1.57 }
{ Steering: left        Gear: forward   distance: 0.13 }
{ Steering: right       Gear: backward  distance: 1.57 }
{ Steering: straight    Gear: backward  distance: 5.81 }
{ Steering: left        Gear: backward  distance: 0.13 }
{ Steering: right       Gear: backward  distance: 0.46 }
{ Steering: left        Gear: forward   distance: 1.57 }
{ Steering: straight    Gear: forward   distance: 5.95 }
{ Steering: left        Gear: forward   distance: 0.59 }
{ Steering: left        Gear: forward   distance: 0.25 }
{ Steering: right       Gear: forward   distance: 1.44 }
{ Steering: left        Gear: backward  distance: 0.21 }
{ Steering: right       Gear: forward   distance: 1.15 }
{ Steering: straight    Gear: forward   distance: 4.9 }
{ Steering: right       Gear: forward   distance: 0.25 }
```
