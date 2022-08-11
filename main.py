import os
import sys
import math
import gen
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import cv2
import time

resume = False
file = ""
blur = False
detect = False

with open('output/progress.txt') as f:
    progress = f.read().splitlines()
    
    if len(progress) >= 4 and progress[0] and not int(progress[1]) == 0 and not progress[1] == "Finished!":
        resume = input("The last video seems to be unfinished. Continue from where you left off? (Y/N): ").capitalize()
        while not (resume == "Y" or resume == "N"):
            resume = input("The last video seems to be unfinished. Continue from where you left off? (Y/N): ").capitalize()
        resume = resume == "Y"
    
    if resume:
        file = progress[0]
        blur = progress[2] == "True"
        detect = progress[3] == "True"
        
        
    else:
        file = input("File to encode: ")
        while not os.path.isfile(file):
            file = input("File to encode: ")

        blur = input("Blur? (Y/N): ").capitalize()
        while not (blur == "Y" or blur == "N"):
            blur = input("Blur? (Y/N): ").capitalize()
        blur = blur == "Y"

        detect = input("Crop Background? (Y/N): ").capitalize()
        while not (detect == "Y" or detect == "N"):
            detect = input("Crop Background? (Y/N): ").capitalize()
        detect = detect == "Y"

if file.endswith((".jpg", ".png")):
    frame = cv2.imread(file)
    x, y = gen.encode(frame, blur, detect, False)

    repeat = 1000

    wavfile.write("output/sound_wave_x.wav", 44100, np.int16(x * 32767))
    wavfile.write("output/sound_wave_y.wav", 44100, np.int16(y * 32767))

    left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * repeat
    right_channel = AudioSegment.from_wav("output/sound_wave_y.wav") * repeat
    stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
    stereo_sound.export("output/final_sound.wav", format="wav")
    
    print("\nFinished Rendering!")
    with open("output/progress.txt", "w") as f:
        f.write(f"{file}\nFinished!")

elif file.endswith((".mp4", ".avi")):
    
    cap = cv2.VideoCapture(file)
    
    num = gen.count_frames(cap)
    
    cap = cv2.VideoCapture(file)
    
    success, frame = cap.read()
    count = 0
    start_frame = 0
    
    if resume:
        count = int(progress[1])
        start_frame = count
        for i in range(count - 1):
            success, frame = cap.read()
    else:
        success, frame = cap.read()
        count = 0
    
    
    start = time.perf_counter()
    while success:

        try:
            x, y = gen.encode(frame, blur, detect, True)
            wavfile.write("output/sound_wave_x.wav",
                            44100, np.int16(x * 32767))
            wavfile.write("output/sound_wave_y.wav",
                            44100, np.int16(y * 32767))
            left_channel = AudioSegment.from_wav("output/sound_wave_x.wav") * 2
            right_channel = AudioSegment.from_wav(
                "output/sound_wave_y.wav") * 2
            stereo_sound = AudioSegment.from_mono_audiosegments(
                left_channel, right_channel)
            if count == 0:
                stereo_sound.export("output/final_sound.wav", format="wav")
            else:
                old_stereo_sound = AudioSegment.from_wav(
                    "output/final_sound.wav")
                old_stereo_sound += stereo_sound
                old_stereo_sound.export(
                    "output/final_sound.wav", format="wav")
                
        except:
            with open("output/progress.txt", "w") as f:
                f.write(f"{file}\n{count}\n{blur}\n{detect}")
                print(" " * 100, end="\r")
                print(f"The program crashed at frame {count}!")
                sys.exit()
                        
        success, frame = cap.read()

        count += 1
        progress = round(count / num * 20)

        estim = (time.perf_counter() - start) / (count - start_frame) * (num - count)

        if estim >= 7200:
            estim = f"{str(math.floor(estim / 3600))} hrs {str(math.floor((estim % 3600) / 60))} mins"
        elif estim >= 3600:
            estim = f"{str(math.floor(estim / 3600))} hr {str(math.floor((estim % 3600) / 60))} mins"
        elif estim >= 300:
            estim = f"{str(math.floor(estim / 60))} mins"
        elif estim >= 120:
            estim = f"{str(math.floor(estim / 60))} mins {str(round(estim % 60))} s"
        elif estim >= 60:
            estim = f"{str(math.floor(estim / 60))} min {str(round(estim % 60))} s"
        else:
            estim = f"{str(round(estim % 60))} s"

        print(" " * 100, end="\r")
        print(f"Progress: |{'█' * progress}{' ' * (20 - progress)}| {str(round(count / num * 100))}% ({str(count)}/{str(num)}) ...... Estimated Time Remaining: {estim}", end='\r')

    print("\nFinished Rendering!")
    with open("output/progress.txt", "w") as f:
        f.write(f"{file}\nFinished!")

else:
    print("Sorry! File type not supported.")