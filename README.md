# ScaleModel
Python script to rescale Rhino files
Written by Graham Knapp
Ironpython 2.7
Tested under Mcneel Rhino version 5 for windows
Hello all,
I have written a python script to help when working with scale models, specifically it helps when switching regularly between full-scale and model scale. You can download it here : [ModelScale.py](https://raw.githubusercontent.com/dancergraham/ScaleModel/master/ScaleModel.py)
I would be grateful for any comments, feedback, feature requests (but I make no promises) or any examples of similar (better ?!?) scripts.
## Features
* Remembers the model scale, e.g. 1:200
* Permits easy switching between full and model scale
* Permits changes to model scale

## Known issues
* Can enter the wrong state on undo (e.g. thinks it is still in model scale)

## Installation
Follow the instructions [here](https://developer.rhino3d.com/guides/rhinopython/python-running-scripts/)

## Contributing
You can help by commenting here or on the [Github repo](https://github.com/dancergraham/ScaleModel).  In particular I will accept pull requests adding the undo facility, rescaling units or improving the gui.  I would also like to know whether it works in v6 and on mac ?