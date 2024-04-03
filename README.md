# Voice Note Recorder

This Python script listens for a specific keyword ("blueberry") and then records speech, converting it to text until a pause in speech is detected. The text is saved in a designated folder with a filename based on the current date. This script utilizes Picovoice's Porcupine for wake word detection and Cheetah for speech-to-text conversion.

## Features

- **Keyword Activation**: Starts recording when the keyword "blueberry" is detected.
- **Speech to Text**: Converts spoken words to text using Picovoice's Cheetah.
- **Automatic Saving**: Saves the transcribed text to a file, appending new text with each activation.

## Requirements

- Python 3.6 or higher
- `pvporcupine` for wake word detection
- `pvcheetah` for speech-to-text conversion
- `pvrecorder` for audio recording

## Installation

1. Ensure Python 3.6 or higher is installed on your system.
2. Install the required Picovoice packages using pip:

    ```bash
    pip install pvporcupine pvcheetah pvrecorder
    ```

3. Clone this repository or download the script to your local machine.
4. Obtain an AccessKey from Picovoice Console (https://console.picovoice.ai/) and add it to a `keys.json` file in the script's directory:

    ```json
    {
        "PVPORCUPINE_ACCESS_KEY": "Your-Access-Key-Here"
    }
    ```

## Usage

Run the script from the command line, optionally specifying the output path for the text files:

```bash
python voiceNote.py --output_path "the folder where you want to save the notes"
```
The script will continuously listen for the keyword "blueberry". Upon detection, it starts recording speech and transcribes it to text. The text is saved in a designated folder with filenames based on the current date.

## Optional Arguments
- --output_path: The absolute path to the folder where the recorded text notes will be saved. Defaults to "~/Documents/digitalFabrication/voiceNote".
- --endpoint_duration_sec: The duration in seconds for which speechless audio is considered an endpoint, indicating the end of a speech segment. Defaults to 10 seconds.
