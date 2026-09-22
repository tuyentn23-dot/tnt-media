
"""
TNT Media v2 - Thumbnail Generator
Tao thumbnail chuyen nghiep cho YouTube
"""

import numpy as np
import cv2
from pathlib import Path

class ThumbnailGenerator:
    """Tao thumbnail dep cho YouTube"""
    
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        
    def create_music_thumbnail(self, title, artist, output_path, bg_color=None):
        """Tao thumbnail cho video nhac"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background gradient
        if bg_color is None:
            bg_color = (40, 30, 50)  # Dark purple
        
        for y in range(self.height):
            ratio = y / self.height
            color = tuple(int(c * (1 - ratio * 0.5)) for c in bg_color)
            frame[y, :] = color
        
        # Decor circle (nhac not)
        center_x = self.width // 4
        center_y = self.height // 2
        cv2.circle(frame, (center_x, center_y), 200, (60, 50, 80), -1)
        cv2.circle(frame, (center_x, center_y), 180, (80, 60, 100), 3)
        
        # Music note symbol
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "J", (center_x - 30, center_y + 60), font, 5, (0, 200, 255), 10)
        
        # Title text
        title_scale = 2.0
        title_thickness = 6
        ts = cv2.getTextSize(title, font, title_scale, title_thickness)[0]
        tx = self.width // 2
        ty = self.height // 2 - 50
        
        cv2.putText(frame, title, (tx + 4, ty + 4), font, title_scale, (0, 0, 0), title_thickness + 4)
        cv2.putText(frame, title, (tx, ty), font, title_scale, (0, 220, 255), title_thickness)
        
        # Artist
        artist_scale = 1.0
        asize = cv2.getTextSize(artist, font, artist_scale, 2)[0]
        ax = self.width // 2
        ay = ty + 80
        cv2.putText(frame, artist, (ax + 2, ay + 2), font, artist_scale, (0, 0, 0), 4)
        cv2.putText(frame, artist, (ax, ay), font, artist_scale, (200, 200, 200), 2)
        
        cv2.imwrite(output_path, frame)
        return output_path
