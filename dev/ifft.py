import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play
import csv
import matplotlib.pyplot as plt


file = open("gen.csv", "r")

csv_reader = csv.reader(file)

data_list = [row for row in csv_reader]
data_list = [list(map(float, lst)) for lst in data_list]

#print(data_list)

data_list_x = [x[0] for x in data_list]
data_list_y = [x[1] for x in data_list]

plt.plot(data_list_x,data_list_y,'mx')
plt.show()

duration = 1
data_length = len(data_list_x)
#N = int(44100 * duration)
N = data_length * duration
NN2 = int(data_length/2)

fft_x = np.fft.fft(data_list_x) / data_length
fft_y = np.fft.fft(data_list_y) / data_length

X0 = np.append(fft_x[range(NN2)], np.zeros([N-data_length],dtype=complex))
X  = np.append(X0, fft_x[range(NN2,data_length)])

Y0 = np.append(fft_y[range(NN2)], np.zeros([N-data_length],dtype=complex))
Y  = np.append(Y0, fft_y[range(NN2,data_length)])

x = np.real(N*np.fft.ifft(X)) # real values taken for plotting
y = np.real(N*np.fft.ifft(Y))

def map_amplitude(x):
    previ = 0
    for i in x:
        if np.abs(i) > np.abs(previ):
            previ = i
    x = x/np.abs(previ)
    print(previ)
    return x

x = map_amplitude(x)
y = map_amplitude(y)

xnn = np.arange(data_length)
xn  = np.arange(N) / 44100

plt.plot(xn,y,'mx')
plt.show()

plt.plot(xn,x,'mx')
plt.show()

print(len(x), len(y))

repeat = 1000

wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x * 32767))
wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y * 32767))

left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * repeat
right_channel = AudioSegment.from_wav("output/sound_wave_y.wav") * repeat
stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
stereo_sound.export("output/final_sound.wav", format="wav")

