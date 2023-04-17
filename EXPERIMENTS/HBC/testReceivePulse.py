import serial
import queue
import threading
from psychopy import core
from psychopy.hardware import keyboard
from functions.ecg import EcgMonitorThread
#

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




if __name__ == "__main__":
    
    # init arduino
    log("# Initializing arduino...")
    ard = serial.Serial(port=ARD_PORT, baudrate=BAUD)
    log("# ... arduino ready")

    # set up arduino thread & lock / peak queue
    log("# initializing peak queue...")
    peakQueue = queue.Queue()

    # set up arduino thread & lock / peak queue
    log("# initializing threading...")
    monitorThread = EcgMonitorThread(ard=ard, peakQueue=peakQueue)
    monitorThread.start()

    # set up timer and keyboard
    log("# Initializing timer, keyboard...")
    timer = core.Clock()
    kb = keyboard.Keyboard()
    log("# ... timer, keyboard ready")


    # ----------
    # EXPERIMENT
    peakDetected = False
    # ----------
    try:

        startTime = timer.getTime()
        
        while timer.getTime() - startTime < 10:

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
                log("Peakdetected")
            
            # test for ecc press
            if 'escape' in pressedKeys:
                endExperiment = True
                break

            # wait
            core.wait(.1)
                    


    finally:
        # close thread
        log("Closing monitor thread.")
        monitorThread.stop()
        log("Terminated successfully.")


            





