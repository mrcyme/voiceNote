import argparse
import os
import struct
import wave
from datetime import datetime
import json
import pvporcupine
from pvrecorder import PvRecorder
import pvcheetah

KEYWORDS  = ["blueberry"]
with open("keys.json") as json_file:
    PVPORCUPINE_ACCESS_KEY = json.load(json_file)["PVPORCUPINE_ACCESS_KEY"]

def save_text_to_file(text, folderpath, filename):
    # Expands the ~ to the user's home directory
    folderpath = os.path.expanduser(folderpath)
    
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        
    # Use "a" mode to append, and prepend a newline to the text
    with open(os.path.join(folderpath, filename), "a") as file:
        # Prepend a newline to the text to ensure it starts on a new line
        file.write(f"\n{text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', help='Absolute path folder to recorded texte notes', default="~/Documents/digitalFabrication/voiceNote")

    parser.add_argument(
        '--endpoint_duration_sec',
        type=float,
        default=10.,
        help='Duration in seconds for speechless audio to be considered an endpoint')

    args = parser.parse_args()


    keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in KEYWORDS]

    try:
        porcupine = pvporcupine.create(
        access_key=PVPORCUPINE_ACCESS_KEY,
        keyword_paths=keyword_paths,)
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print("One or more arguments provided to Porcupine is invalid: ", args)
        print(e)
        raise e
    except pvporcupine.PorcupineActivationError as e:
        print("AccessKey activation error")
        raise e
    except pvporcupine.PorcupineActivationLimitError as e:
        print("AccessKey '%s' has reached it's temporary device limit" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationRefusedError as e:
        print("AccessKey '%s' refused" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationThrottledError as e:
        print("AccessKey '%s' has been throttled" % args.access_key)
        raise e
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e
    
    cheetah = pvcheetah.create(
        access_key=PVPORCUPINE_ACCESS_KEY,
        endpoint_duration_sec=args.endpoint_duration_sec)

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])


    recorder = PvRecorder(
        frame_length=porcupine.frame_length)
    recorder.start()


    print('Listening ... (press Ctrl+C to exit)')

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"recording_{current_date}.txt"

    transcript = ""
    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            if result >= 0:
                print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                try:
                    while True:
                        partial_transcript, is_endpoint = cheetah.process(recorder.read())
                        transcript += partial_transcript
                        print(partial_transcript, end='', flush=True)
                        if is_endpoint:
                            end_of_transcript = cheetah.flush()
                            print(end_of_transcript)
                            transcript += end_of_transcript
                            print("transcipt ended, waiting for keyword")
                            save_text_to_file(transcript, args.output_path, filename)
                            break
                finally:
                    
                    pass
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()


if __name__ == '__main__':
    main()