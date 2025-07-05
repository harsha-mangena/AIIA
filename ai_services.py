import io
import numpy as np
import whisper
import logging
from typing import Optional
import google.generativeai as genai
from config import *

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.whisper_model = None
        self.genai_client = None
        self.conversation_history = []
        self.is_speaking = False
        self.initialize_services()
        
    def initialize_services(self):
        """Initialize all AI services"""
        try:
            # Initialize Whisper
            self.whisper_model = whisper.load_model(WHISPER_MODEL)
            logger.info(f"Whisper {WHISPER_MODEL} model loaded successfully")
            
            # Initialize Gemini
            genai.configure(api_key=GEMINI_API_KEY)
            self.genai_client = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini client initialized successfully")
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {e}")
            return False
    
    def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio using Whisper"""
        if not self.whisper_model:
            return ""
        
        try:
            # Convert bytes to numpy array. The audio is already 16-bit PCM.
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe with Whisper using supported parameters only
            result = self.whisper_model.transcribe(
                audio_np, 
                language="en", 
                fp16=False,
                temperature=0.0,  # More deterministic output
                condition_on_previous_text=True  # Better context understanding
            )
            text = result["text"].strip()
            
            if text and len(text) > 2:  # Filter out very short/empty transcriptions
                logger.info(f"Transcribed: {text}")
                return text
            return ""
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return ""
    
    def get_response(self, conversation_history: list, user_input: str) -> str:
        """Get response from Gemini API with conversation history"""
        if not self.genai_client:
            return "I'm sorry, AI service is not available."
        
        try:
            # Build conversation context more carefully
            conversation_text = f"{SYSTEM_PROMPT}\n\nConversation:\n"
            
            # Add conversation history (limit to last 8 exchanges to avoid token limits)
            recent_history = conversation_history[-8:] if len(conversation_history) > 8 else conversation_history
            
            for role, content in recent_history:
                if role == "You":
                    conversation_text += f"Candidate: {content}\n"
                elif role == "Agent":
                    conversation_text += f"Interviewer: {content}\n"
            
            # Add current user input if it's substantial
            if user_input.strip() and len(user_input.strip()) > 2:
                conversation_text += f"Candidate: {user_input}\nInterviewer:"
            else:
                conversation_text += "Interviewer:"
            
            # Generate response with safety settings
            response = self.genai_client.generate_content(
                conversation_text,
                generation_config={
                    "max_output_tokens": 150,
                    "temperature": 0.7,
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            
            if response and hasattr(response, 'text') and response.text:
                ai_response = response.text.strip()
                return ai_response
            elif response and hasattr(response, 'candidates') and response.candidates:
                # Try to get text from candidates if direct text access fails
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        return candidate.content.parts[0].text.strip()
                
            # If we still don't have a response, provide a helpful fallback
            return "I see you started to say something. Could you please continue with your thought?"
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return "I'm sorry, I'm having trouble processing that. Could you please try saying it again, perhaps with a bit more detail?"
    
    def get_ai_response(self, user_input: str) -> str:
        """Get response from Gemini API"""
        if not self.genai_client:
            return "I'm sorry, AI service is not available."
        
        try:
            # Build conversation context
            conversation_text = f"{SYSTEM_PROMPT}\n\nConversation History:\n"
            
            # Add conversation history (last 6 exchanges to keep context manageable)
            recent_history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
            
            for role, content in recent_history:
                if role == "user":
                    conversation_text += f"Candidate: {content}\n"
                elif role == "assistant":
                    conversation_text += f"Interviewer: {content}\n"
            
            # Add current user input
            conversation_text += f"Candidate: {user_input}\nInterviewer:"
            
            # Generate response
            response = self.genai_client.generate_content(
                conversation_text,
                generation_config={
                    "max_output_tokens": 150,
                    "temperature": 0.7,
                }
            )
            
            if response and response.text:
                ai_response = response.text.strip()
                
                # Update conversation history
                self.conversation_history.append(("user", user_input))
                self.conversation_history.append(("assistant", ai_response))
                
                return ai_response
            else:
                return "I'm sorry, I didn't catch that. Could you please repeat your answer?"
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI service. Could you please repeat that?"
    
    def get_opening_question(self) -> str:
        """Get the opening interview question"""
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nThis is the start of a technical interview. Please greet the candidate warmly and ask them to introduce themselves - their name, background, experience level, and areas of interest in computer science. Keep it conversational and welcoming."
            
            response = self.genai_client.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 100,
                    "temperature": 0.8,
                }
            )
            
            if response and response.text:
                opening = response.text.strip()
                self.conversation_history.append(("assistant", opening))
                return opening
            else:
                # Fallback opening focused on introduction
                fallback = "Hello! Welcome to your technical interview. I'm excited to learn about you! Could you please start by introducing yourself - your name, background, and experience level with computer science and programming?"
                self.conversation_history.append(("assistant", fallback))
                return fallback
                
        except Exception as e:
            logger.error(f"Failed to get opening question: {e}")
            fallback = "Hello! Welcome to your technical interview. I'm excited to learn about you! Could you please start by introducing yourself - your name, background, and experience level with computer science and programming?"
            self.conversation_history.append(("assistant", fallback))
            return fallback
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
