import subprocess

audio_file = './media/bleep.wav'

# command to run ffplay with audio file as input
playAudioFFPlay = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'panic', audio_file]

def playSound():
    # subprocess.call(playAudioFFPlay)
    subprocess.Popen(playAudioFFPlay)