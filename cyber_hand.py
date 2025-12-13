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
    
    def render_data_stream(self, canvas, x, y, value):
        """Draws a vertical data bar that reacts to energy"""
        height = 100
        fill = int(height * value)
        cv2.rectangle(canvas, (x, y), (x + 20, y + height), (50, 50, 50), 1)
        color = (0, int(255 * (1-value)), int(255 * value))
        cv2.rectangle(canvas, (x, y + height - fill), (x + 20, y + height), color, -1)

        # Glitch text effect
        txt = f"PWR: {int(value * 100)}%"
        cv2.putText(canvas, txt, (x - 40, y + height + 20), 
                   cv2.FONT_HERSHEY_PLAIN, 1, C_TEXT, 1)
    
    def render_scanner(self, canvas, palm_y, width):
        """Horizontal scanning laser effect"""
        scan_y = (self.ticks * 5) % 480
        cv2.line(canvas, (0, scan_y), (width, scan_y), (0, 50, 0), 1)
        if abs(scan_y - palm_y) < 50:
            cv2.putText(canvas, "TARGET LOCKED", (50, scan_y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, C_SCAN, 1)
    
    def update(self, frame, landmarks):
        h, w, _ = frame.shape
        self.ticks += 1
        
        #Convert landmarks to pixel coords
        coords = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]
        palm = coords[0] # Wrist
        fingers = [coords[4], coords[8], coords[12], coords[16], coords[20]] # Tips
        
        #Update Trails
        for i, tip in enumerate(fingers):
            self.trails[i].append(tip)
            pts = np.array(self.trails[i], np.int32)
            cv2.polylines(frame, [pts], False, C_FLUX, 1 + i)

        #For Calculating Energy
        try:
            poly_area = cv2.contourArea(np.array(fingers + [palm], dtype=np.int32))
            max_area = w * h * 0.08 
            spread = min(poly_area / max_area, 1.0)
            target_energy = 1.0 - spread 
            self.energy_level += (target_energy - self.energy_level) * 0.1
        except:
            pass

        #Render Interface Elements
        
        # Dynamic Pulse Core
        core_size = int(20 + (self.energy_level * 50))
        glow_color = tuple(int(c * self.energy_level) for c in C_SCAN)
        self.render_bloom(frame, palm, core_size + 10, glow_color, 0.4)
        cv2.circle(frame, palm, core_size, C_CORE, 2)
        
        # Orbital Rings
        if self.energy_level > 0.5:
            self.render_orbital_rings(frame, palm, 60, C_FLUX)
            cv2.putText(frame, "SYSTEM ARMED", (palm[0]-60, palm[1]+100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, C_FLUX, 2)
            
        # Connections
        for tip in fingers:
            cv2.line(frame, palm, tip, (50, 50, 50), 1)
            cv2.circle(frame, tip, 4, C_CORE, -1)

        # Scanning Line
        self.render_scanner(frame, palm[1], w)

        # HUD Bars
        self.render_data_stream(frame, 30, h - 150, self.energy_level)

        return frame    