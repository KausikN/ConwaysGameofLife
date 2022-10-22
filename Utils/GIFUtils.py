"""
GIF Utils
"""

# Imports
import cv2
import random
import imageio
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from tqdm import tqdm

# Main Functions
def ResizeImage_Pixelate(I, maxSize=512):
    '''
    Resize Image - Pixelate
    '''
    if I.shape[0] > I.shape[1]:
        new_size = (int(I.shape[1] * maxSize / I.shape[0]), maxSize)
    else:
        new_size = (maxSize, int(I.shape[0] * maxSize / I.shape[1]))
    I = cv2.resize(I, new_size, interpolation=cv2.INTER_NEAREST)

    return I

def SaveImageSequence(ImgSeq, path, mode="gif", frameSize=None, fps=25):
    '''
    Save Image Sequence
    '''
    # GIF
    if mode in ["gif", "GIF", "G", "g"]:
        imageio.mimsave(path, ImgSeq)
    # Video
    elif mode in ["V", "v", "Video", "video", "VIDEO", "VID", "vid"]:
        if frameSize == None:
            frameSize = (ImgSeq[0].shape[0], ImgSeq[0].shape[1])
        vid = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"DIVX"), fps, frameSize)
        for i in range(len(ImgSeq)):
            vid.write(ImgSeq[i])
        vid.release()
    # Images
    else:
        for i in range(len(ImgSeq)):
            cv2.imwrite(path + "_" + str(i+1) + ".png", ImgSeq[i])