# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>


from psychopy import gui

from parameters import getParameters
from task import run

# Create a GUI and ask for high-evel experiment parameters
g = gui.Dlg()
g.addField("participant", initial="Participant")
g.addField("session", initial="HBD")
g.show()

# Set global task parameters here
parameters = getParameters(
    participant=g.data[0],
    session=g.data[1],
    screenNb=0,
)

# Run task
run(parameters, runTutorial=True)

parameters["win"].close()