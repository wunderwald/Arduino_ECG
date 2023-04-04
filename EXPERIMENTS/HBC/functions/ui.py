from psychopy import gui
import re

def parseNumHeartbeats(numHeartbeats):
    if not numHeartbeats:
        return -1
    try:
        return int(numHeartbeats)
    except:
        return -1


def dialogueNumHeartbeats():
    inputIsValid = False
    numHeartbeats = None
    confidence = None
    failedOnce = False
    while not inputIsValid:
        myDlg = gui.Dlg(title="")
        myDlg.addField(f"How many heartbeats did you count? {'[ enter a positive integer ]' if failedOnce else ''}")
        myDlg.addField('How confident are you about your count?', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], initial=4)
        inputData = myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK: 
            failedOnce = True
            continue
        numHeartbeats = parseNumHeartbeats(inputData[0])
        confidence = inputData[1]
        inputIsValid = numHeartbeats >= 0
        if not inputIsValid:
            failedOnce = True
    return {
        'numHeartbeats': numHeartbeats,
        'confidence': confidence
    }


def testSubjectId(id):
    exp = "^[0-9]{3}"
    match = re.search(exp, str(id))
    return (match != None) and (match.group() == str(id))
    

def dialogueSubjectId():
    inputIsValid = False
    subjectId = None
    failedOnce = False
    while not inputIsValid:
        myDlg = gui.Dlg(title="")
        myDlg.addField(f"Enter subject ID {'[ enter a positive integer with 3 digits ]' if failedOnce else ''}")
        inputData = myDlg.show() 
        if not myDlg.OK: 
            failedOnce = True
            continue
        subjectId = inputData[0]
        inputIsValid = testSubjectId(subjectId)
        if not inputIsValid:
            failedOnce = True
    return subjectId