import os
import cv2
import glob

def rescale_frame(frame, shape, percent=50):
    width = int(shape[1] * percent/ 100)
    height = int(shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

for f in glob.glob("*.png"):
    frame = cv2.imread(f)
    shape = frame.shape
    frame = cv2.UMat(frame)
    frame = rescale_frame(frame,shape,20)
    frame = rescale_frame(frame,shape,100)
    cv2.imwrite(f, frame,[int(cv2.IMWRITE_PNG_COMPRESSION), 30])
