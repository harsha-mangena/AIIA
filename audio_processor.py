import queue
import threading
import numpy as np
import logging
from config import *
import time

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.audio_buffer = []
        self.is_recording = False
        self.last_audio_time = time.time()
        self.silence_threshold = 0.01  # Adjust this threshold as needed
        self.min_audio_length = 5.0  # Minimum 2 seconds of audio for complete sentences
        self.max_audio_length = 20.0  # Maximum 15 seconds of audio
        self.silence_duration = 5.0  # Wait 5 seconds of silence before stopping
        
    def process_audio_chunk(self, audio_data: np.ndarray) -> bytes:
        """Process audio chunk using simple energy-based detection"""
        try:
            # Calculate the energy/volume of the audio chunk
            audio_energy = np.sqrt(np.mean(audio_data ** 2))
            
            current_time = time.time()
            
            # Check if there's sound (above threshold)
            if audio_energy > self.silence_threshold:
                if not self.is_recording:
                    # Start recording
                    self.is_recording = True
                    self.audio_buffer = []
                    logger.info("Started recording audio...")
                
                # Add audio to buffer
                self.audio_buffer.append(audio_data)
                self.last_audio_time = current_time
                
            else:
                # Silent audio
                if self.is_recording:
                    # Check if we should stop recording (silence for 2 seconds)
                    if current_time - self.last_audio_time > self.silence_duration:
                        # Stop recording and process
                        self.is_recording = False
                        
                        if len(self.audio_buffer) > 0:
                            # Convert buffer to bytes
                            full_audio = np.concatenate(self.audio_buffer)
                            audio_duration = len(full_audio) / RATE
                            
                            logger.info(f"Audio captured: {audio_duration:.2f} seconds")
                            
                            # Only process if audio is long enough
                            if audio_duration >= self.min_audio_length:
                                # Convert to 16-bit PCM
                                audio_int16 = (full_audio * 32767).astype(np.int16)
                                audio_bytes = audio_int16.tobytes()
                                
                                logger.info(f"Returning audio segment: {len(audio_bytes)} bytes")
                                return audio_bytes
                            else:
                                logger.info("Audio too short, discarding")
                        
                        self.audio_buffer = []
                    else:
                        # Still in recording mode, add silent audio to buffer
                        if self.is_recording:
                            self.audio_buffer.append(audio_data)
            
            # Safety check - don't let recordings get too long
            if self.is_recording and len(self.audio_buffer) > 0:
                audio_duration = len(np.concatenate(self.audio_buffer)) / RATE
                if audio_duration > self.max_audio_length:
                    # Force stop recording
                    self.is_recording = False
                    full_audio = np.concatenate(self.audio_buffer)
                    audio_int16 = (full_audio * 32767).astype(np.int16)
                    audio_bytes = audio_int16.tobytes()
                    logger.info(f"Max length reached, returning audio: {len(audio_bytes)} bytes")
                    self.audio_buffer = []
                    return audio_bytes
                    
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
        
        return None
    
    def get_audio_queue(self):
        """Get the audio queue for processing"""
        return self.audio_queue


