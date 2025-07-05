# 🚀 CSM Technical Interview Agent

A sophisticated AI-powered technical interview system that conducts real-time voice conversations with candidates. Built as a command-line interface (CLI) application, powered by Google's Gemini AI, OpenAI's Whisper, and Microsoft's SpeechT5 (Sesame) for natural text-to-speech.

## 🎯 Key Features

- **Real-time Voice Conversation**: Natural, flowing conversation through microphone input and AI speech
- **Advanced AI Interviewer**: Powered by Google Gemini for intelligent, contextual questioning
- **Professional Speech Recognition**: Using OpenAI Whisper for accurate transcription
- **High-Quality Text-to-Speech**: SpeechT5 (Sesame) neural TTS for natural-sounding voice
- **Contextual Interview Flow**: Gathers user background before asking tailored technical questions
- **Conversation Logging**: Automatically saves interview transcripts with timestamps
- **Cross-Platform**: Works on any operating system with Python support

## 🛠️ Technical Architecture

### Core Components
- **CLI Interface**: Rich terminal-based interface for smooth user experience
- **Speech Processing**: Energy-based voice detection + Whisper STT (medium model)
- **AI Engine**: Google Gemini 1.5 Flash for conversational responses
- **Audio Output**: SpeechT5 neural TTS with HiFiGAN vocoder
- **Audio Processing**: Direct microphone access with sounddevice library

### Interview Flow
1. **User Introduction**: Agent asks for candidate's background and experience
2. **Context Analysis**: AI analyzes user's profile to tailor questions
3. **Progressive Questioning**: Gradually increases difficulty based on responses
4. **Feedback & Follow-up**: Provides constructive feedback and asks follow-up questions
5. **Conversation Logging**: Saves complete interview transcript

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Microphone-enabled device
- Terminal/Command line access

### Installation

1. **Clone and Setup**
```bash
git clone <repository>
cd AIIA
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

2. **Configure API Keys**
Edit `config.py` and add your API keys:
```python
GEMINI_API_KEY = "your_gemini_api_key_here"
HF_TOKEN = "your_huggingface_token_here"  # Optional for model downloads
```

3. **Run the Interview Agent**
```bash
python cli_app.py
```

### First Time Setup
- The application will download the Whisper medium model (~1.5GB) on first run
- SpeechT5 models will be downloaded automatically from Hugging Face
- Ensure your microphone permissions are enabled for the terminal

## 🎤 How to Use

1. **Start the Interview**: Run `python cli_app.py`
2. **Introduction Phase**: The AI will greet you and ask for your introduction
3. **Background Questions**: AI asks follow-up questions about your experience
4. **Technical Questions**: AI asks tailored technical questions based on your background
5. **Natural Conversation**: Speak naturally - the system handles pauses and incomplete sentences
6. **End Interview**: Say "goodbye" or "thank you" to end the session
7. **Review Transcript**: Check the generated interview log file

## 🔧 Configuration

### Audio Settings (config.py)
- `RATE = 16000` - Audio sample rate (16kHz recommended)
- `WHISPER_MODEL = "medium"` - Whisper model size (tiny/base/small/medium/large)

### AI Settings
- `SYSTEM_PROMPT` - Customizable interviewer personality and behavior
- Temperature and token limits for response generation

## 🏗️ Project Structure

```
AIIA/
├── cli_app.py           # Main CLI application entry point
├── ai_services.py       # AI services (Whisper + Gemini)
├── audio_processor.py   # Audio input processing and voice detection
├── tts_service.py       # SpeechT5 text-to-speech service
├── config.py           # Configuration settings and API keys
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── env/              # Virtual environment
```

## 🔍 Technical Details

### Speech-to-Text Pipeline
1. **Audio Capture**: Direct microphone access via sounddevice
2. **Voice Detection**: Energy-based voice activity detection
3. **Audio Processing**: 16kHz mono audio, normalized amplitude
4. **Transcription**: Whisper medium model with context conditioning

### Text-to-Speech Pipeline
1. **Text Processing**: SpeechT5 processor for input tokenization
2. **Speech Generation**: Neural TTS with speaker embeddings
3. **Vocoding**: HiFiGAN vocoder for high-quality audio output
4. **Audio Playback**: Direct system audio output via sounddevice

### AI Conversation Flow
1. **Context Building**: Conversation history + system prompt
2. **Response Generation**: Gemini 1.5 Flash with safety settings
3. **Content Filtering**: Handles partial inputs and edge cases
4. **Adaptive Questioning**: Tailors difficulty to user's experience level

## 📊 Models Used

- **Speech Recognition**: OpenAI Whisper (medium model)
- **Language Model**: Google Gemini 1.5 Flash
- **Text-to-Speech**: Microsoft SpeechT5 + HiFiGAN vocoder
- **Speaker Embeddings**: CMU Arctic X-vectors dataset

## 🎯 Interview Features

- **Progressive Difficulty**: Questions adapt to candidate's skill level
- **Contextual Follow-ups**: AI remembers and references previous responses
- **Natural Conversation**: Handles interruptions, pauses, and incomplete sentences
- **Professional Feedback**: Constructive evaluation of technical answers
- **Comprehensive Coverage**: Data structures, algorithms, system design, programming concepts

## 🧪 Testing & Troubleshooting

### Health Check
The system includes automatic health monitoring and error recovery:
- **AI Services**: Whisper + Gemini connectivity validation
- **Audio Processor**: Microphone access and voice detection
- **TTS Engine**: SpeechT5 model initialization

### Common Issues

**Microphone Not Working**
- Ensure terminal/Python has microphone permissions
- Check system microphone settings in System Preferences (macOS) or Settings (Windows)
- Test microphone with other applications first

**AI Not Responding**
- Verify API keys in `config.py` are correct
- Check internet connectivity
- Review logs in terminal for specific error messages

**TTS Issues**
- First run downloads models (~2GB) - ensure stable internet
- Check available disk space for model storage
- Restart application if models fail to load

**Transcription Issues**
- Speak clearly and avoid background noise
- Wait for "Started recording audio..." message before speaking
- Ensure minimum 2-3 seconds of speech for better recognition

### Debug Mode
Run with verbose logging:
```bash
python cli_app.py --verbose
```

## � Performance Optimization

### Model Selection
- **Whisper tiny**: Fastest, least accurate
- **Whisper medium**: Recommended balance (current)
- **Whisper large**: Best accuracy, slower processing

### Hardware Recommendations
- **GPU**: CUDA-compatible GPU for faster inference
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB+ for large models
- **Storage**: SSD for faster model loading

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Custom voice training
- [ ] Interview analytics and scoring
- [ ] Video interview capabilities
- [ ] Integration with HR systems
- [ ] Real-time feedback dashboard

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review the logs for error messages
- Create an issue in the repository with detailed information

---

**Built with ❤️ for better technical interviews**

## 📊 Performance Optimization

### Audio Settings
- **Sample Rate**: 16kHz optimized for Whisper
- **Frame Size**: 30ms for low latency
- **VAD Aggressiveness**: Level 3 for accurate speech detection

### AI Configuration
- **Max Response Length**: 150 tokens for concise answers
- **Temperature**: 0.7 for natural conversation
- **Context Window**: Last 6 exchanges for memory efficiency

## 🔒 Security & Privacy

- **API Keys**: Stored locally in config files
- **Audio Data**: Processed in real-time, not stored permanently
- **Conversation**: Maintained only during session
- **Network**: Secure HTTPS connections for all API calls

## 🚀 Advanced Features

### Custom Interview Topics
Modify `SYSTEM_PROMPT` in `config.py` to focus on specific technical areas:
- Data Structures & Algorithms
- System Design
- Programming Languages
- Software Architecture

### Integration Options
- **Webhook Support**: Send interview results to external systems
- **Database Integration**: Store conversation history
- **Analytics**: Track interview metrics and performance

## 📈 Roadmap

- [ ] **Multi-language Support**: Interview in different languages
- [ ] **Video Integration**: Add video chat capabilities  
- [ ] **Advanced Analytics**: Interview scoring and feedback
- [ ] **Custom Voice Models**: Personalized interviewer voices
- [ ] **Integration APIs**: Connect with HR systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly with `python system_test.py`
4. Submit a pull request

## 📞 Support

For technical issues:
1. Check the **Health Status** in the application
2. Review logs in the terminal
3. Run `python system_test.py` for diagnostics
4. Check browser console for WebRTC errors

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for the future of technical interviews**

*Last Updated: January 2025*
