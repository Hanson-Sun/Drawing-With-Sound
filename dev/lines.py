# import necessary packages
import os
import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import NearestNeighbors
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# initialize mediapipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1)

frame = cv2.imread('input/4ktest.jpg')
bg_image = cv2.imread('input/white.jpg')
height, width, channel = frame.shape

RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# get the result
results = selfie_segmentation.process(RGB)
# extract segmented mask
mask = results.segmentation_mask

# it returns true or false where the condition applies in the mask
# it returns true or false where the condition applies in the mask
condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
# resize the background image to the same size of the original frame
bg_image = cv2.resize(bg_image, (width, height))

# combine frame and background image using the condition
output_image = np.where(condition, frame, bg_image)

edges = cv2.Canny(cv2.GaussianBlur(output_image, [0, 0], 1, 1), 100, 150)

# Prints coordinates of white pixels
y, x = np.where(edges == [255])

points = np.c_[x, y]
clf = NearestNeighbors(n_neighbors=20).fit(points)
G = clf.kneighbors_graph()

T = nx.from_scipy_sparse_array(G)

order = list(nx.dfs_preorder_nodes(T, 0))

xx = x[order]
yy = frame.shape[0] - y[order]

plt.plot(xx, yy)
plt.show()

coord = np.column_stack([xx, yy])

with open("gen.csv", 'w') as file:
    for c in coord:    
        file.write(str(c[0]) +", " + str(c[1]) + "\n")

cv2.imshow("Frame", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
