from vosk import Model, KaldiRecognizer
import pyaudio
from djitellopy import Tello
import sys
import cv2
import numpy as np
import scipy.signal
import re
import json

# Initialize the Vosk model and recognizer
model_path = r"C:\Users\poojitha\Downloads\vosk-model-small-en-in-0.4 (1)\vosk-model-small-en-in-0.4"  # Update this with the correct path
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Initialize the Tello drone
tello = Tello()
tello.connect()

# Print the initial battery percentage
print(f"Battery Percent: {tello.get_battery()}%")

# Set up microphone input
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()


def recognize_command():
    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)  # Output the recognized text
            return result


def spectral_subtraction(noisy_signal, sr):
    # Short-Time Fourier Transform
    f, t, Zxx = scipy.signal.stft(noisy_signal, fs=sr, nperseg=1024)

    # Estimate noise spectrum (e.g., average of first few frames)
    noise_spectrum = np.mean(np.abs(Zxx[:, :5]) ** 2, axis=1)

    # Subtract noise spectrum
    magnitude_spectrum = np.abs(Zxx) - noise_spectrum[:, None]
    magnitude_spectrum = np.maximum(magnitude_spectrum, 0)

    # Reconstruct the signal
    Zxx_clean = magnitude_spectrum * np.exp(1j * np.angle(Zxx))
    _, clean_signal = scipy.signal.istft(Zxx_clean, fs=sr)

    return clean_signal


def parse_command(command):
    # Extract the distance if mentioned in the command
    match = re.search(r'(\d+)\s*(cm|centimeters|meters|m)?', command)
    if match:
        distance = int(match.group(1))
        if match.group(2) in ['meters', 'm']:
            distance *= 100
    else:
        distance = 40
    return command.lower(), distance


def execute_command(command, distance):
    # Execute the recognized command
    if 'takeoff' in command or 'take off' in command:
        print("Command: Tello auto Takeoff")
        tello.takeoff()
    elif 'land' in command:
        print("Command: Tello auto Land")
        tello.land()
    elif 'forward' in command or 'for ward' in command:
        print(f"Command: Move forward {distance} cm")
        tello.move_forward(distance)
    elif 'backward' in command:
        print(f"Command: Move backward {distance} cm")
        tello.move_back(distance)
    elif 'left' in command:
        print(f"Command: Move left {distance} cm")
        tello.move_left(distance)
    elif 'right' in command:
        print(f"Command: Move right {distance} cm")
        tello.move_right(distance)
    elif 'up' in command:
        print(f"Command: Move up {distance} cm")
        tello.move_up(distance)
    elif 'down' in command:
        print(f"Command: Move down {distance} cm")
        tello.move_down(distance)
    elif 'rotate' in command:
        print("Command: Rotate 90 degrees")
        tello.rotate_clockwise(90)
    elif 'flip' in command:
        print("Command: Flip")
        tello.flip('f')
    elif 'end' in command:
        print('Ending the program...')
        tello.land()
        sys.exit(0)
    else:
        print("Command not recognized")

    # Print the battery status after executing each command
    print(f"Battery Percent: {tello.get_battery()}%")


def listen_and_execute():
    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)  # Output the recognized text

            try:
                result_dict = json.loads(result)  # Parse the JSON string
                command = result_dict.get('text', '')  # Safely get the 'text' field
                print(f"You said: {command}")

                # Parse and execute the command
                command, distance = parse_command(command)
                execute_command(command, distance)

            except Exception as e:
                print(f"Error: {e}")


# Main loop
while True:
    listen_and_execute()
    k = cv2.waitKey(1)
    if k == ord('a'):
        tello.land()
        break

# Release resources
stream.stop_stream()
stream.close()
cap.terminate()
