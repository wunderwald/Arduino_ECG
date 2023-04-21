import serial
import queue
import threading
from psychopy import core, visual
from psychopy.hardware import keyboard
from functions.trialParams import makeTrialParams_HC
from functions.write import makeSubjectCsv, makeEcgCsv, csvToFile
from functions.ui import dialogueNumHeartbeats, dialogueSubjectId
from functions.ecg import EcgMonitorThread
from functions.audio import playSound

# !!!
# use "python3 -m heartbeatCounting" to run this script
# !!!

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


if __name__ == "__main__":
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

    # set up peak queue
    log("# initializing peak queue and ecg recording signal...")
    peakQueue = queue.Queue()
    ecgSignal = queue.Queue()

    # set up ecg monitor thread
    log("# initializing threading...")
    monitorThread = EcgMonitorThread(ard=ard, peakQueue=peakQueue, ecgSignal=ecgSignal)
    monitorThread.start()

    # init subject and trial data
    log("# Initializing subject and trial data...")
    subjectId = dialogueSubjectId()
    trialData = makeTrialParams_HC(subjectId=subjectId)
    log("# ... subject and trial data ready")

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

            log("# Start trial " + str(trial['trialIndex']))
            drawText(win=win, txt="Count your heartbeats until you hear the sound again...")

            # timing
            trial['startTime_s'] = timer.getTime()

            # mark trial start w sound
            playSound()

            # mark trial start in ecg data
            if ecgSignal.qsize() <= 0:
                ecgSignal.put({'millis': -1, 'peakDetected': False, 'ecgLevel': -1, 'trialStart': True, 'trialEnd': False})
            else:
                lastEcgSample = ecgSignal.get(block=False)
                lastEcgSample['trialStart'] = True
                ecgSignal.put(lastEcgSample)

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
            playSound()

            # mark trial start in ecg data
            lastEcgSample = ecgSignal.get(block=False)
            lastEcgSample['trialEnd'] = True
            ecgSignal.put(lastEcgSample)
            

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
        log("Writing subject data to file...")
        outputCsv = makeSubjectCsv(trialData)
        csvToFile(csv=outputCsv, dir=OUTPUT_DIR, filename = "" + str(subjectId) + ".csv")
        ecgCsv = makeEcgCsv(list(ecgSignal.queue))
        csvToFile(csv=ecgCsv, dir=OUTPUT_DIR, filename = "ecg_" + str(subjectId) + ".csv")

    finally:
        # close thread
        log("Closing monitor thread.")
        monitorThread.stop()
        log("Terminated successfully.")




            





