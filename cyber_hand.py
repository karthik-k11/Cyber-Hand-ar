import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque

# "Cyberpunk" Palette (Darker, grittier colors)
C_VOID = (15, 15, 20)
C_CORE = (0, 255, 255)
C_FLUX = (0, 100, 255)
C_SCAN = (255, 50, 50)
C_TEXT = (200, 200, 200)