import time
import threading
import logging
from rich.console import Console
from rich.panel import Panel
import sounddevice as sd
import numpy as np
import queue

from config import *
from ai_services import AIService
from audio_processor import AudioProcessor
from tts_service import TTSService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

console = Console()

class InterviewManager:
    def __init__(self):
        self.ai_service = AIService()
        self.audio_processor = AudioProcessor()
        self.tts_service = TTSService()
        
        self.conversation_history = []
        self.is_interview_running = False
        self.user_is_speaking = False
        self.audio_queue = queue.Queue()

    def save_conversation(self):
        """Saves the conversation to a text file."""
        filename = f"interview_log_{time.strftime('%Y%m%d-%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write("Interview Conversation Log\n")
            f.write("="*30 + "\n")
            for role, message in self.conversation_history:
                f.write(f"{role}: {message}\n")
        console.print(f"[bold green]Conversation saved to {filename}[/bold green]")

    def record_audio(self):
        """Records audio from the microphone and puts it in a queue."""
        def callback(indata, frames, time, status):
            if status:
                console.print(f"[bold red]Audio Error: {status}[/bold red]")
            # Only process audio if user is supposed to be speaking AND TTS is not active
            if self.user_is_speaking and not self.tts_service.is_currently_speaking():
                audio_bytes = self.audio_processor.process_audio_chunk(indata.flatten())
                if audio_bytes:
                    self.audio_queue.put(audio_bytes)

        try:
            with sd.InputStream(samplerate=RATE, channels=1, dtype='float32', callback=callback):
                while self.is_interview_running:
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error with audio stream: {e}")
            console.print("[bold red]Error: Could not open microphone. Please check your system's audio settings.[/bold red]")

    def start_interview(self):
        """Main loop for the CLI-based interview."""
        self.is_interview_running = True

        # Start audio recording in a background thread
        audio_thread = threading.Thread(target=self.record_audio, daemon=True)
        audio_thread.start()

        console.print(Panel("[bold cyan]🚀 AI Interview Agent Started[/bold cyan]", title="Welcome", expand=False))
        
        # 1. Greeting
        greeting = self.ai_service.get_opening_question()
        self.conversation_history.append(("Agent", greeting))
        console.print(f"\n[bold magenta]Agent:[/bold magenta] {greeting}")
        
        # Wait for TTS to complete before starting to listen
        def on_greeting_complete():
            console.print("\n[bold yellow]You can start speaking now. The interview will end if you say 'goodbye' or 'thank you'.[/bold yellow]")
            console.print("[bold yellow]Please speak for at least 2-3 seconds for better recognition.[/bold yellow]")
        
        self.tts_service.speak_text(greeting, callback=on_greeting_complete)

        while self.is_interview_running:
            try:
                self.user_is_speaking = True
                
                # Wait for audio to be captured
                try:
                    audio_data = self.audio_queue.get(timeout=30) # 30-second timeout
                except queue.Empty:
                    console.print("[bold yellow]No speech detected for a while. Are you still there?[/bold yellow]")
                    continue

                self.user_is_speaking = False # Stop capturing while processing
                console.print("[italic gray]...thinking...[/italic gray]")

                # 2. Transcribe User's Speech
                user_text = self.ai_service.transcribe_audio(audio_data)
                if not user_text:
                    console.print("[bold yellow]Could not understand. Please speak again.[/bold yellow]")
                    continue

                console.print(f"\n[bold cyan]You:[/bold cyan] {user_text}")
                self.conversation_history.append(("You", user_text))

                # Check for end conditions
                if any(phrase in user_text.lower() for phrase in ['goodbye', 'thank you']):
                    self.is_interview_running = False
                    closing_message = "It was a pleasure speaking with you. Goodbye!"
                    console.print(f"\n[bold magenta]Agent:[/bold magenta] {closing_message}")
                    self.tts_service.speak_text(closing_message)
                    continue

                # 3. Get AI Response
                ai_response = self.ai_service.get_response(self.conversation_history, user_text)
                self.conversation_history.append(("Agent", ai_response))

                # 4. Agent Speaks (with callback to control flow)
                console.print(f"\n[bold magenta]Agent:[/bold magenta] {ai_response}")
                
                def on_ai_speech_complete():
                    # Only start listening again after AI finishes speaking
                    pass
                
                self.tts_service.speak_text(ai_response, callback=on_ai_speech_complete)

            except KeyboardInterrupt:
                self.is_interview_running = False
                console.print("\n[bold red]Interview interrupted by user.[/bold red]")
            except Exception as e:
                logger.error(f"An error occurred during the interview: {e}")
                self.is_interview_running = False

        # End of interview
        self.save_conversation()
        console.print(Panel("[bold cyan]✅ Interview Finished[/bold cyan]", expand=False))

if __name__ == "__main__":
    manager = InterviewManager()
    manager.start_interview()
