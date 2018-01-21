# VacuumCleanerSim

VacuumCleanerSim is a simulation software for coverage problems in planar environments.
It was originally developed as part of a college project at Hochschule Darmstadt in semester 2017 / 2018.
The simulation allows developers to build arbitrary environments based on rectangular obstacles.
There is a simple possibility to develop new algorithms and run it with the simulator.

## Installation

In order to use this simulation software you need to install [Python3](https://www.python.org/downloads/).

There are some dependencies for this project to install. Just run `pip install` to install them.

## Run the simulation

To start the simulation you can run the following command:
```
python VacuumCleanerSim.py [<algorithm>] [<environment>]
```

Currently there are three possible values for the `algorithm`-parameter:
* `random` (Uses a random bounce walk)
* `spiral` (Uses a spiral walk strategy)
* `swalk` (Uses the "maeander"-walk strategy)

Additionally there are some predefined environments that can be configured in the [configs](conf/config.json)

## Usage

After you start the software, you are in the "build" phase. There you can draw some obstacles and place the vacuum robot.

To use the software you need to know some key assignments:

* `R` - places the robot at the position of your mouse cursor
* `M` - switch the mode to the "simulation" phase. Only possible if there is a robot placed in the environment.
* `P` - toggle display of the coverage path
* `ESC` - exits the software

The result of the simulation will be a folder under /output. There will appear all saved screenshots and a csv-file that contains all data of the simulation.


