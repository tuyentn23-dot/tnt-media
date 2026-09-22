
"""
TNT Media v2 - Audio Visualizer Engine
Tao video visualizer chuyen nghiep tu audio
"""

import numpy as np
import cv2
import wave
from pathlib import Path
import math

class AudioVisualizerEngine:
    """Audio Visualizer Engine - tao video visualizer dep"""
    
    def __init__(self, width=1280, height=720, fps=15):
        self.width = width
        self.height = height
        self.fps = fps
        self.spectrum_data = None
        
    def analyze_audio(self, audio_path):
        """Phan tich audio thanh spectrum data"""
        with wave.open(str(audio_path), 'rb') as wav:
            framerate = wav.getframerate()
            n_frames = wav.getnframes()
            
            audio_data = wav.readframes(n_frames)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            if wav.getnchannels() == 2:
                audio_array = audio_array.reshape(-1, 2)
                left = audio_array[:, 0].astype(float)
            else:
                left = audio_array.astype(float)
            
            left = left / 32768.0
        
        # Tao spectrum data
        frame_samples = framerate // self.fps
        n_visual_frames = len(left) // frame_samples
        
        bins = 48
        spectrum_data = []
        
        for i in range(n_visual_frames):
            chunk = left[i*frame_samples:(i+1)*frame_samples]
            fft_data = np.fft.fft(chunk)
            magnitudes = np.abs(fft_data[:len(fft_data)//2])
            
            spectrum = []
            for b in range(bins):
                s = int(b * len(magnitudes) / bins)
                e = int((b + 1) * len(magnitudes) / bins)
                if e > len(magnitudes):
                    e = len(magnitudes)
                if s < e:
                    spectrum.append(np.mean(magnitudes[s:e]))
                else:
                    spectrum.append(0)
            spectrum_data.append(spectrum)
        
        self.spectrum_data = np.array(spectrum_data)
        self.spectrum_norm = (self.spectrum_data - self.spectrum_data.min()) /                             (self.spectrum_data.max() - self.spectrum_data.min() + 1e-8)
        return self.spectrum_data
    
    def create_visualizer_video(self, audio_path, output_path, title, artist, duration=None):
        """Tao video visualizer tu audio"""
        self.analyze_audio(audio_path)
        
        if duration is None:
            duration = len(self.spectrum_norm) / self.fps
        
        total_frames = int(duration * self.fps)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        for i in range(total_frames):
            spec_idx = i % len(self.spectrum_norm)
            spec = self.spectrum_norm[spec_idx]
            
            frame = self._create_frame(spec, title, artist)
            out.write(frame)
        
        out.release()
        return output_path
    
    def _create_frame(self, spec, title, artist):
        """Tao mot frame visualizer"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Background gradient
        for y in range(0, self.height, 3):
            ratio = y / self.height
            frame[y:y+3, :] = (int(30+25*ratio), int(10+20*ratio), int(30+30*ratio))
        
        # Spectrum bars
        n_bars = len(spec)
        bar_w = self.width // n_bars
        center_y = self.height // 2
        
        for bi in range(n_bars):
            bh = int(spec[bi] * self.height * 0.3)
            hue = bi / n_bars
            b = int(100 + 100 * hue)
            g = int(50 + 100 * (1 - abs(hue - 0.5) * 2))
            r = int(150 + 80 * (1 - hue))
            
            x = bi * bar_w
            cv2.rectangle(frame, (x, center_y-bh), (x+bar_w-2, center_y), (b, g, r), -1)
            cv2.rectangle(frame, (x, center_y), (x+bar_w-2, center_y+bh), (b//2, g//2, r//2), -1)
        
        cv2.line(frame, (0, center_y), (self.width, center_y), (255, 255, 255), 2)
        
        # Title text
        font = cv2.FONT_HERSHEY_SIMPLEX
        ts = cv2.getTextSize(title, font, 1.5, 4)[0]
        tx = (self.width - ts[0]) // 2
        ty = self.height - 100
        cv2.putText(frame, title, (tx+3, ty+3), font, 1.5, (0,0,0), 6)
        cv2.putText(frame, title, (tx, ty), font, 1.5, (0, 200, 255), 4)
        
        # Artist text
        asize = cv2.getTextSize(artist, font, 0.8, 2)[0]
        ax = (self.width - asize[0]) // 2
        ay = self.height - 50
        cv2.putText(frame, artist, (ax+2, ay+2), font, 0.8, (0,0,0), 3)
        cv2.putText(frame, artist, (ax, ay), font, 0.8, (180, 180, 180), 2)
        
        return frame
