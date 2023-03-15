import numpy as np

def makeTrialParams_HC(subjectId):

    numTrials = 7
    trialParams = []

    # make list of trial durations, starting with practice triall
    practiceTrialDuration_s = 15
    mainTrialDurations_s = np.random.permutation([25, 30, 35, 40, 45, 50])
    trialDurations_s = [practiceTrialDuration_s]
    for dur in mainTrialDurations_s: trialDurations_s.append(dur)

    # generate trial data objects
    for i in range(numTrials):
        trialParams.append({
            'subjectId': subjectId,
            'trialIndex': i,
            'isPracticeTrial': i == 0,
            'duration_s': trialDurations_s[i],
            # init output values
            'numHeartbeatsTracked': 0,
            'numHeartbeatsCounted': 0,
            'confidenceRating': -1,
            'startTime_s': None,
            'endTime_s': None
        })
    
    return trialParams
