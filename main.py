import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import pvporcupine
import queue
import json


# Parameters
fs = 44100  # Sample rate
filename = 'output1.wav'  # Output filename
keywords = ["blueberry"]  # Keyword to say
silence_threshold = 800  # Threshold for silence detection
record_after_stop_seconds = 5  # Duration of silence before stopping the recording

# AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
with open("keys.json") as json_file:
    PVPORCUPINE_ACCESS_KEY = json.load(json_file)["PVPORCUPINE_ACCESS_KEY"]

# Initialize Porcupine
handle = pvporcupine.create(access_key=PVPORCUPINE_ACCESS_KEY, keywords=keywords)
frame_length = handle.frame_length
sample_rate = handle.sample_rate
audio_buffer = np.zeros(handle.frame_length, dtype=np.int16)  # Buffer to hold audio samples
buffer_index = 0  # Index to keep track of the buffer

# Initialize recording state variables
recording = False
silent_frames = 0
max_silent_frames = int(sample_rate * record_after_stop_seconds / frame_length)
audio_data = queue.Queue()  # Queue to store audio data

def callback(indata, frames, time, status):
    """This is called for each audio block."""
    global buffer_index, recording, silent_frames, audio_data

    if status:
        print(status)

    audio_frame = indata[:, 0]  # Single channel
    audio_frame = audio_frame * 32767  # Scale
    audio_frame = audio_frame.astype(np.int16)  # Convert

    # Handle recording state
    if recording:
        audio_data.put(audio_frame.copy())
        
        # Check if the current frame is silent
        print(np.abs(audio_frame).mean())
        is_silent = np.abs(audio_frame).mean() < silence_threshold
        silent_frames = silent_frames + 1 if is_silent else 0
        
        # Stop recording after 5 seconds of silence
        if silent_frames >= max_silent_frames:
            recording = False
            silent_frames = 0
            save_recording()
    
    else:
        # Add new samples to the buffer
        samples_to_copy = min(len(audio_frame), handle.frame_length - buffer_index)
        audio_buffer[buffer_index:buffer_index + samples_to_copy] = audio_frame[:samples_to_copy]
        buffer_index += samples_to_copy
        
        # If the buffer is full, process it for keyword detection
        if buffer_index >= handle.frame_length:
            keyword_index = handle.process(audio_buffer)
            if keyword_index >= 0:
                print(f"Keyword detected! Index: {keyword_index}")
                recording = True
                silent_frames = 0
                audio_data.queue.clear()  # Clear previously stored data
                audio_data.put(audio_buffer.copy())  # Start recording
            buffer_index = 0  # Reset buffer index

def save_recording():
    """Save the recorded audio to a file."""
    recorded_frames = [audio_data.get() for _ in range(audio_data.qsize())]
    recorded_audio = np.concatenate(recorded_frames, axis=0)
    write(filename, sample_rate, recorded_audio)
    print(f"Audio written to {filename}")

# Open a stream with a callback function
with sd.InputStream(callback=callback, channels=1, dtype='float32', samplerate=sample_rate):
    print("Listening for keyword...")
    while True:
        sd.sleep(1000)  # Keep the script running
