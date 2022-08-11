import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import imutils


"""
Function returning list of pixel positions of the edge of an image
This list is ordered to form a path
"""


def get_edges(frame, blur, detect, resize):
    # initialize mediapipe
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
        model_selection=1)
    
    height, width, channel = frame.shape
    if resize:
        frame = cv2.resize(frame, [70, int(70/width*height)])
    height, width, channel = frame.shape

    if detect:
        bg_image = cv2.imread('input/white.jpg')

        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # get the result
        results = selfie_segmentation.process(RGB)
        # extract segmented mask
        mask = results.segmentation_mask

        # it returns true or false where the condition applies in the mask
        # it returns true or false where the condition applies in the mask
        condition = np.stack((mask,) * 3, axis=-1) > 0.5
        # resize the background image to the same size of the original frame
        bg_image = cv2.resize(bg_image, (width, height))

        # combine frame and background image using the condition
        frame = np.where(condition, frame, bg_image)

    if blur:
        frame = cv2.GaussianBlur(frame, [0, 0], 1)
    
    edges = imutils.auto_canny(frame)

    # Prints coordinates of white pixels
    y, x = np.where(edges == [255])

    points = np.c_[x, y]

    if len(points) <= 18:
        return []
    
    clf = NearestNeighbors(n_neighbors=21).fit(points)
    G = clf.kneighbors_graph()

    T = nx.from_scipy_sparse_array(G)

    order = list(nx.dfs_preorder_nodes(T, 0))

    xx = x[order] - width / 2
    yy = height / 2 - y[order]

    coord = np.column_stack([xx, yy])

    return coord

"""
Inverse Fourier Transform
"""


def ifft(data_list):
    if len(data_list) > 0:
        data_list = [list(map(float, lst)) for lst in data_list]

        # print(data_list)

        data_list_x = [x[0] for x in data_list]
        data_list_y = [x[1] for x in data_list]

        duration = 0.033333
        data_length = len(data_list_x)
        if int(44100 * duration) > data_length:
            N = int(44100 * duration)
        else:
            N = data_length
        
        NN2 = int(data_length/2)

        fft_x = np.fft.fft(data_list_x) / data_length
        fft_y = np.fft.fft(data_list_y) / data_length

        X0 = np.append(fft_x[range(NN2)], np.zeros([N-data_length], dtype=complex))
        X = np.append(X0, fft_x[range(NN2, data_length)])

        Y0 = np.append(fft_y[range(NN2)], np.zeros([N-data_length], dtype=complex))
        Y = np.append(Y0, fft_y[range(NN2, data_length)])

        x = np.real(N*np.fft.ifft(X))  # real values taken for plotting
        y = np.real(N*np.fft.ifft(Y))

        x = map_amplitude(x)
        y = map_amplitude(y)

        return x, y
    return [0], [0]

"""
Amplitude Mapper
"""


def map_amplitude(x):
    previ = 0
    for i in x:
        if np.abs(i) > np.abs(previ):
            previ = i
    x = x/np.abs(previ)
    return x

def encode(frame, blur, detect, resize):
    return ifft(get_edges(frame, blur, detect, resize))


def count_frames_manual(video):
    total = 0
    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
            break
        total += 1
    return total

def count_frames(cap, override=False):
    total = 0
    if override:
        total = count_frames_manual(cap)
    else:
        try:
            total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        except:
            total = count_frames_manual(cap)
    cap.release()
    return total