# 🚀 CSM Technical Interview Agent

A sophisticated AI-powered technical interview system that conducts real-time voice conversations with candidates. Built with Streamlit, powered by Google's Gemini AI, OpenAI's Whisper, and advanced Text-to-Speech technology.

## 🎯 Key Features

- **Real-time Voice Conversation**: Natural, flowing conversation through microphone input and AI speech
- **Advanced AI Interviewer**: Powered by Google Gemini for intelligent, contextual questioning
- **Professional Speech Recognition**: Using OpenAI Whisper for accurate transcription
- **High-Quality Text-to-Speech**: Natural-sounding AI voice responses
- **Persistent State Management**: Maintains conversation across browser refreshes
- **Health Monitoring**: Built-in system health checks and diagnostics
- **WebRTC Integration**: Low-latency audio processing for seamless interaction

## 🛠️ Technical Architecture

### Core Components
- **Frontend**: Streamlit web interface with WebRTC audio streaming
- **Speech Processing**: Voice Activity Detection (VAD) + Whisper STT
- **AI Engine**: Google Gemini 1.5 Flash for conversational responses
- **Audio Output**: Cross-platform TTS with threading safety
- **State Management**: Thread-safe global state for real-time updates

### Recent Fixes (v2.0)
✅ **Fixed TTS Engine Run Loop Conflicts** - Resolved "run loop already started" errors
✅ **Thread-Safe State Management** - Eliminated session state access issues in background threads  
✅ **Improved Audio Processing** - Enhanced VAD configuration and audio frame handling
✅ **Microphone Access Recovery** - Better WebRTC integration and permission handling
✅ **Conversation Persistence** - Maintains interview state across page refreshes
✅ **Error Recovery** - Robust error handling and automatic recovery mechanisms

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Microphone-enabled device
- Modern web browser (Chrome/Firefox recommended)

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
Edit `config.py` with your API keys:
```python
HF_TOKEN = "your_huggingface_token"
GEMINI_API_KEY = "your_gemini_api_key"
```

3. **Run System Test**
```bash
python system_test.py
```

4. **Start the Application**
```bash
./start.sh
# OR manually:
streamlit run app.py
```

5. **Open Browser**
Navigate to `http://localhost:8501`

## 💡 Usage Instructions

### Starting an Interview
1. Click **"🎙️ Start Interview"**
2. **Allow microphone permissions** when prompted
3. Wait for the AI greeting
4. **Speak clearly** when the status shows "Interview is ACTIVE"

### During the Interview
- **Green Status**: Ready to listen - speak now
- **Yellow Status**: AI is speaking - please wait
- **Conversation History**: Real-time display of the dialogue

### Best Practices
- **Speak clearly** and at normal volume
- **Wait for AI responses** before speaking again
- **Use Chrome/Firefox** for best WebRTC support
- **Ensure stable internet** for AI API calls

## 🔧 System Requirements

### Minimum Requirements
- **OS**: macOS, Windows 10+, or Linux
- **Python**: 3.8+
- **RAM**: 4GB
- **Internet**: Stable broadband connection
- **Browser**: Chrome 88+, Firefox 85+, or Safari 14+

### Recommended Setup
- **RAM**: 8GB+
- **CPU**: Multi-core processor
- **Audio**: Quality USB microphone
- **Network**: Low-latency internet connection

## 🧪 Testing & Debugging

### Health Check
```bash
python system_test.py
```

### Component Testing
The system includes built-in health monitoring:
- **AI Services**: Whisper + Gemini connectivity
- **Audio Processor**: VAD initialization
- **TTS Engine**: Speech synthesis capability

### Common Issues

**Microphone Not Working**
- Ensure browser permissions are granted
- Check system microphone settings
- Try refreshing the page

**AI Not Responding**
- Verify API keys in `config.py`
- Check internet connectivity
- Review logs in terminal

**TTS Issues**
- Restart the application
- Check system audio settings
- Verify TTS engine initialization

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
