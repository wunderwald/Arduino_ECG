import serial
import queue
import threading
from psychopy import core, visual
from psychopy.hardware import keyboard
import simpleaudio as aud
from functions.subjectId import enterSubjectId
from functions.trialParams import makeTrialParams_HC
from functions.write import makeCsvHC, csvToFile
from functions.ui import dialogueNumHeartbeats
from functions.ecg import monitorECG

ARD_PORT = '/dev/cu.usbmodem14101'
BAUD = 115200
LOG = True
OUTPUT_DIR = './subjectData'

def log(txt):
    if not LOG: return
    print(txt)

def drawText(win, txt):
    txtStim = visual.TextStim(win=win, text=txt, pos=(0.0, .5))
    txtStim.draw()
    win.flip()

def kbWaitForKey(kb, keyCode):
    keyPressed = False
    while not keyPressed:
        pressedKeys = kb.getKeys([keyCode], clear=True)
        keyPressed = keyCode in pressedKeys

# --------------
# INITIALIZATION
# --------------
# set up window
log("# Initializing screen...")
winWidth = 1440
winHeight = 800
aspectRatio = winWidth / winHeight
winSize = (winWidth, winHeight)
win = visual.Window(size=winSize, pos=(0, 0))
drawText(win=win, txt="Initializing...")
log("# ... screen ready")

# init arduino
log("# Initializing arduino...")
ard = serial.Serial(port=ARD_PORT, baudrate=BAUD)
log("# ... arduino ready")

# set up arduino thread / peak queue
log("# initializing threading and peak queue...")
peakQueue = queue.Queue()
monitorThread = threading.Thread(target=monitorECG, args=(ard, peakQueue))
monitorThread.start()

# init subject and trial data
log("# Initializing subject and trial data...")
subjectId = enterSubjectId()
trialData = makeTrialParams_HC(subjectId=subjectId)
log("# ... subject and trial data ready")

# init audio
log("# Initializing audio...")
audFile = "./media/rim.wav"
audObj = aud.WaveObject.from_wave_file(audFile)
log("# ... audio ready")

# set up timer and keyboard
log("# Initializing timer, keyboard...")
timer = core.Clock()
kb = keyboard.Keyboard()
log("# ... timer, keyboard ready")


# ----------
# EXPERIMENT
# ----------
try:
    log("# Experiment starts...")
    drawText(win=win, txt="The experiment starts now. The first trial will be a practice trial. Press space to continue...")
    kbWaitForKey(kb=kb, keyCode='space')

    # loop through trials
    endExperiment = False
    peakDetected = False
    for trial in trialData:
        if endExperiment:
            log("# Experiment terminated by experimenter")
            break

        log(f"# Start trial {trial['trialIndex']}")
        drawText(win=win, txt="Count your heartbeats until you hear the sound again...")

        # timing
        trial['startTime_s'] = timer.getTime()

        # mark trial start w sound
        audObj.play()

        # run trial
        peakDetected_last = False
        while timer.getTime() - trial['startTime_s'] < trial['duration_s']:
            if endExperiment: 
                break

            # record keyboard
            pressedKeys = kb.getKeys(['escape'], clear=True)

            # get peak 
            peakDetected_last = peakDetected
            try:
                peakDetected = peakQueue.get(block=False)
            except queue.Empty:
                peakDetected = False
                

            # update tracked peaks
            if peakDetected and not peakDetected_last:
                trial['numHeartbeatsTracked'] += 1
            
            # test for ecc press
            if 'escape' in pressedKeys:
                endExperiment = True
                break

            # wait
            core.wait(.01)
                

        # timing
        trial['endTime_s'] = timer.getTime()

        # mark trial end w sound
        audObj.play()

        # get user input
        if not endExperiment:
            drawText(win=win, txt="Enter how many heartbeats you counted!")
            countData = dialogueNumHeartbeats()
            trial['numHeartbeatsCounted'] = countData['numHeartbeats']
            trial['confidenceRating'] = countData['confidence']
        else:
            drawText(win=win, txt="Experiment over...")
            trial['numHeartbeatsCounted'] = -1
            trial['confidenceRating'] = -1

        # start next trial
        if not endExperiment:
            drawText(win=win, txt="Press space to continue...")
            kbWaitForKey(kb=kb, keyCode='space')

    # write data
    outputCsv = makeCsvHC(trialData)
    csvToFile(csv=outputCsv, dir=OUTPUT_DIR, filename = f"{subjectId}.csv")

finally:
    monitorThread.join()

# TODO:
# - send triggers to labchart on trial start/end
# - fix beat detection


        





