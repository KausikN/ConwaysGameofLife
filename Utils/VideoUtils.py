"""
GIF Utils
"""

# Imports
import os
import cv2
import subprocess
import numpy as np
from PIL import Image

from tqdm import tqdm

# Main Functions
def VideoUtils_FixVideo(pathIn, pathOut):
    '''
    VideoUtils - Fix Video File for displaying in streamlit
    '''
    # Init
    COMMAND_VIDEO_CONVERT = 'ffmpeg -i \"{path_in}\" -vcodec libx264 \"{path_out}\"'
    if os.path.exists(pathOut): os.remove(pathOut)
    # Convert
    convert_cmd = COMMAND_VIDEO_CONVERT.format(path_in=pathIn, path_out=pathOut)
    print("Running Conversion Command:")
    print(convert_cmd + "\n")
    ConvertOutput = subprocess.getoutput(convert_cmd)
    # print("Conversion Output:")
    # print(ConvertOutput)

    return ConvertOutput

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

def ResizeImage_Pad(I, size=(480, 640)):
    '''
    Resize Image - Pad
    '''
    ASPECT_RATIO = I.shape[1] / I.shape[0]
    if size[0] < size[1]:
        new_size = (int(size[0] * ASPECT_RATIO), size[0])
    else:
        new_size = (size[1], int(size[1] / ASPECT_RATIO))
    I = cv2.resize(I, new_size, interpolation=cv2.INTER_NEAREST)
    I = cv2.copyMakeBorder(I, 0, size[0] - I.shape[0], 0, size[1] - I.shape[1], cv2.BORDER_CONSTANT, value=(0, 0, 0))

    return I

def VideoUtils_SaveFrames2Video(frames, pathOut, fps=20, size=None):
    '''
    VideoUtils - Save Frames to Video
    '''
    if os.path.splitext(pathOut)[-1] == ".gif":
        
        frames_images = [Image.fromarray(np.array(frame*255, dtype=int)) for frame in frames]
        extraFrames = []
        if len(frames_images) > 1: extraFrames = frames_images[1:]
        frames_images[0].save(pathOut, save_all=True, append_images=extraFrames, format="GIF", loop=0)
    else:
        # if size is None: size = (frames[0].shape[1], frames[0].shape[0])
        if size is None: size = (640, 480)
        frames = [np.array(frame*255, dtype=int) for frame in frames]
        frames = [ResizeImage_Pad(frame, size=size[::-1]) for frame in frames]
        out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'XVID'), fps, size)
        for frame in frames:
            out.write(frame)
        # out.close()
        out.release()