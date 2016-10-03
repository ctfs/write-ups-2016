from scipy.io.wavfile import read
import matplotlib.pyplot as plt

# read audio samples
input_data = read("chiptune-bin-part.wav")
audio = input_data[1]
thingy = {}

start = 0
end = len(audio)
thing_len = 5000

list_thing = []
in_thing = False
for n, x in enumerate(range(start, end)):
    data = audio[x]
    data_thing = abs(data)

    if len(list_thing) < thing_len:
        list_thing.append(data_thing)
        continue
    else:
        if max(list_thing) > 2000:
            print "1",
        else:
            print "0",
        list_thing = []

"""
    if data_thing > 1600 and data_thing < 1700:
        print "0", n, x
        in_thing = True

    if data_thing > 2200:
        print "1", n, x
        in_thing = True
"""
