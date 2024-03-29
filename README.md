# VoiceNote

VoiceNote is a Python application that uses the [Picovoice](https://picovoice.ai/) Porcupine library to detect specific keywords in real-time audio and record the audio after the keyword is detected. The audio is then converted to text through [whisper](https://github.com/openai/whisper). 

The future goal is to have it running in the background of my linux computers via systemcl to be able to take note on the fly.

## Setup

1. Clone the repository.
2. Install the required Python packages:

```sh
pip install sounddevice numpy scipy pvporcupine openai-whisper
```

You may need to install portAudio and ffmeg
```sh
sudo apt install libportaudio2
sudo apt install ffmpeg
```

You will need to provide a [Picovoice](https://picovoice.ai/) access key in a file named keys.json. 

## Usage
```sh
python main.py
```
The script listens for the keyword "blueberry". When it detects the keyword, it starts recording audio. The recording stops after 5 seconds of silence.

The recorded audio is saved in a file named output1.wav.

Configuration
You can customize the application by modifying the parameters in main.py:

fs: The sample rate.
filename: The name of the output file.
keywords: The keywords to detect.
silence_threshold: The threshold for silence detection.
record_after_stop_seconds: The duration of silence before stopping the recording.
You also need to provide a Picovoice access key in a file named keys.json.

License
This project is licensed under the MIT License.

