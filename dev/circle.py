import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play
import csv
import matplotlib.pyplot as plt


s_rate = 44100
T = 1/s_rate
t = 5
N = s_rate * t 

freq = 440
omega = 2*np.pi*freq

t_seq = np.arange(N)*T
y_sin = np.sin(omega*t_seq)
x_sin = np.cos(omega*t_seq)

wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x_sin * 32767))
wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y_sin * 32767))

left_channel = AudioSegment.from_wav("output/sound_wave_x.wav")
right_channel = AudioSegment.from_wav("output/sound_wave_y.wav")
stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
stereo_sound.export("output/circle.wav", format="wav")
