import torch
import sounddevice as sd
import numpy as np
import threading
import logging
from typing import Optional
import time
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import librosa

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.is_speaking = False
        self.speech_lock = threading.Lock()
        self.processor = None
        self.model = None
        self.vocoder = None
        self.speaker_embeddings = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.initialize_tts()
        
    def initialize_tts(self):
        """Initialize SpeechT5 (Sesame) Text-to-Speech model"""
        try:
            logger.info("Loading SpeechT5 model...")
            
            # Load processor, model, and vocoder
            self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
            self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
            self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
            
            # Move models to device
            self.model = self.model.to(self.device)
            self.vocoder = self.vocoder.to(self.device)
            
            # Load speaker embeddings from dataset
            embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
            self.speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0).to(self.device)
            
            logger.info(f"SpeechT5 TTS initialized successfully on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize SpeechT5 TTS: {e}")
            return False
    
    def speak_text(self, text: str, callback: Optional[callable] = None):
        """Convert text to speech and play it using SpeechT5"""
        if not text.strip():
            if callback:
                callback()
            return
        
        # If already speaking, just ignore the new request to prevent queue buildup
        with self.speech_lock:
            if self.is_speaking:
                logger.info("TTS busy, ignoring new speech request to prevent queue buildup")
                if callback:
                    callback()
                return
            self.is_speaking = True
        
        def speak_thread():
            try:
                logger.info(f"Speaking with SpeechT5: {text[:50]}...")
                
                if not self.model or not self.processor or not self.vocoder:
                    logger.error("SpeechT5 models not initialized")
                    return
                
                # Process text
                inputs = self.processor(text=text, return_tensors="pt").to(self.device)
                
                # Generate speech
                with torch.no_grad():
                    speech = self.model.generate_speech(
                        inputs["input_ids"], 
                        self.speaker_embeddings, 
                        vocoder=self.vocoder
                    )
                
                # Convert to numpy and ensure correct format
                audio_np = speech.cpu().numpy()
                
                # Resample if needed (SpeechT5 outputs at 16kHz)
                target_sample_rate = 16000
                
                # Normalize audio
                audio_np = audio_np / np.max(np.abs(audio_np))
                
                # Play audio using sounddevice
                sd.play(audio_np, samplerate=target_sample_rate)
                sd.wait()  # Wait until audio finishes playing
                
                logger.info("Finished speaking with SpeechT5")
                        
            except Exception as e:
                logger.error(f"SpeechT5 TTS failed: {e}")
            finally:
                with self.speech_lock:
                    self.is_speaking = False
                if callback:
                    callback()
        
        # Run TTS in a separate thread to avoid blocking
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def stop_speaking(self):
        """Stop current speech"""
        with self.speech_lock:
            try:
                sd.stop()  # Stop sounddevice playback
                self.is_speaking = False
                logger.info("TTS stopped")
            except Exception as e:
                logger.error(f"Failed to stop TTS: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if TTS is currently speaking"""
        return self.is_speaking
