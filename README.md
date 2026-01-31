# GrayMatter Interview Coach Pro 🏭

An AI-powered interview coaching tool designed to help candidates prepare for the **Engineer I (Development Program)** role at GrayMatter Systems. This application provides real-time feedback on interview answers using OpenAI's API and speech recognition.

## Features

- **Speech Recognition**: Record your answers directly via microphone
- **AI-Powered Feedback**: Get structured, actionable feedback using OpenAI's GPT models
- **Markdown-Formatted Output**: Clear feedback with highlighted strengths, areas for improvement, and professional phrasing suggestions
- **Interactive Streamlit UI**: User-friendly web interface for a seamless coaching experience
- **Specific Company Context**: Tailored coaching for GrayMatter Systems culture and values

## Prerequisites

- Python 3.8+
- Microphone (for speech recognition)
- OpenAI API key

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ../GrayMatterSystemsInterviewPrep
   ```

2. **Create and activate the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note for macOS users**: If you encounter issues installing `pyaudio`, run:
   ```bash
   CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio
   ```
   (Requires `portaudio` installed via Homebrew: `brew install portaudio`)

## Setup

## Usage

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run interview_coach.py
   ```

3. **Open your browser** to the local URL (typically `http://localhost:8501`)

4. **Interact with the coach**:
   - Use the microphone button to record your answer
   - Or type your answer directly
   - Get AI-powered feedback with professional suggestions

## Project Structure

```
GrayMatterSystemsInterviewPrep/
├── interview_coach.py          # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── venv/                       # Virtual environment (created on setup)
```

## Dependencies

- **streamlit**: Web app framework for building interactive interfaces
- **openai**: Official OpenAI Python client library
- **SpeechRecognition**: Speech-to-text conversion using Google's API
- **pyaudio**: Audio I/O support for microphone input

## API Keys & Authentication

This application uses the OpenAI API. You'll need:
1. An OpenAI account (https://openai.com)
2. An API key from your account settings
3. Set the `OPENAI_API_KEY` environment variable

## Troubleshooting

### "No module named 'speech_recognition'"
Ensure all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### PyAudio Installation Issues (macOS)
```bash
brew install portaudio
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio
```

### Microphone Not Working
- Ensure your microphone is properly connected
- Check system audio settings allow microphone access
- Try increasing the timeout in `recognize_speech()` for slower systems

## Features in Detail

### Interview Feedback Structure

The coach provides feedback organized into three sections:

1. **🟢 What You Did Well**: Highlights strengths and alignment with GrayMatter values
2. **🟡 Areas for Improvement**: Constructive critique on structure, tone, and completeness
3. **💡 Suggested Phrasing**: Two professional variations of your response (Confident/Direct and Thoughtful/Collaborative)

### GrayMatter Systems Context

The coach is specialized for the Engineer I role with knowledge of:
- Company values: Accountability, Integrity, Respect, Innovation, Teamwork
- Program details: 2-year mentorship, hands-on field work, industrial automation
- Key traits: "Thinking and Doing" mentality, owning mistakes, learning agility

## Contributing

Suggestions for improvements are welcome! Consider:
- Adding more question templates for different interview scenarios
- Expanding company context for other roles
- Improving speech recognition accuracy
- Adding answer history/progress tracking

## License

This project is for educational and interview preparation purposes.

## Support

For issues or questions about the application, refer to the troubleshooting section above or check the official documentation for:
- [Streamlit](https://docs.streamlit.io/)
- [OpenAI API](https://platform.openai.com/docs/)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition#readme)
