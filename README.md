# Physics-Capstone (Drawing with Sound)

This project creates the sound waves that draws a 2D image or video (sucession of 2D images) on an oscilloscope in x-y mode.

By Hanson Sun and Leo Tian

Inspiration video: https://www.youtube.com/watch?v=4gibcRfp4zA

## Demo videos
(these videos include the audio that used to generate the images, it may be loud)

My physics teacher : https://youtu.be/_fmOFltRRl8 

Mark : https://youtu.be/VZEjosdaVmU 

A Classic : https://youtu.be/tTSTqkKeNfE

## Description

The main program consists of 2 main parts
- Image processing
- Audio generation

Image processing consists of an edge detection algorithm to convert the pixel image into an image of lines. The lines are then ordered such that everything can be traced in order and only visted once. Optionally, background removal and gaussian blur can be performed before edge detection.

The ordered list of points that form the line image is converted to a list of coordinates. The x and y coordinates are split into two different list. These coordinates are then processed using Discrete Fast Fourier Transform, which prodices a continuous wave form. After scaling and slight numerical processing, the waveform can then be used to create a set of discrete points for a .wav audio file of sampling rate 44100. The audio files from the x and y coordinates form dual channel audio, where the x coordinate corresponds to the left audio and the y-coordinate to the right audio. 

The audio output and by connected to an oscilloscope in x-y mode to draw the final image. To aid testing, a virtual oscillscope was used. However, the final product was tested on an analog oscilloscope with the same sucess. 

## Running the Program

- install all the requirements in requirements.txt through python pip
- run main.py
- input the image or video file as per instruction in console (any assets used should be in the input folder for easy organization)
- wait... it could take very long
- final product should be in the output folder

## Fine tuning

The parameters used for each rendering is largely experimental and will probably require user fine tuning. 
Some paramaters to explore include:
- cv2.resize(frame, [n, int(n/width*height)]) (gen.py line 23) change the value of n for different resize
- cv2.GaussianBlur(frame, [0, 0], 1) (gen.py line 45) change the parameters of gaussian blur for different edge detection results
- clf = NearestNeighbors(n_neighbors=21).fit(points) (gen.py line 57) change the number of n_neighbors to alter complexity of final trace
- duration = 0.033333 (gen.py line 85) change the duration to alter the detail and speed in final result (highly recommended for video inputs)

### have fun!


