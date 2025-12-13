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

class CyberHUD:
    def __init__(self):
        self.ticks = 0
        self.trails = [deque(maxlen=10) for _ in range(5)]
        self.energy_level = 0.0
        
    def _get_dist(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def render_bloom(self, canvas, center, radius, color, intensity=0.5):
        """Creates a soft light diffusion effect"""
        if radius <= 0: return
        overlay = canvas.copy()
        cv2.circle(overlay, center, radius, color, -1)
        cv2.addWeighted(overlay, intensity, canvas, 1 - intensity, 0, canvas)

    def render_orbital_rings(self, canvas, center, radius, color):
        """Draws rotating segmented rings instead of hexagons"""
        for r_offset, speed in [(0, 2), (20, -3), (40, 1)]:
            r = radius + r_offset
            angle_start = (self.ticks * speed) % 360
            # Draw 3 arcs per ring
            for i in range(3):
                start = angle_start + (i * 120)
                end = start + 60
                cv2.ellipse(canvas, center, (r, r), 0, start, end, color, 2)