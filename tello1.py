from vosk import Model, KaldiRecognizer
import pyaudio
import sys
import re
import json

# Initialize the Vosk model and recognizer
model_path = r"C:\Users\DELL\Downloads\vosk-model-small-en-in-0.4 (2)\vosk-model-small-en-in-0.4"  # Update this with the correct path
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

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

def parse_command(command):
    # Extract the distance if mentioned in the command
    match = re.search(r'(\d+)\s*(cm|centimeters|meters|m)?', command)
    if match:
        distance = int(match.group(1))
        if match.group(2) in ['meters', 'm']:
            distance *= 100  # Convert meters to centimeters
    else:
        distance = 40  # Default distance if not specified
    return command.lower(), distance

def execute_command(command):
    # Ask for a distance input for specific commands (left or right)
    if 'left' in command or 'right' in command:
        try:
            distance = int(input("Please input the distance in cm: "))  # Request distance from user
        except ValueError:
            print("Invalid input, defaulting to 40 cm")
            distance = 40  # Default to 40 cm if input is invalid
    else:
        distance = 40  # Default distance if the command doesn't require input

    # Execute the recognized command
    if 'takeoff' in command or 'take off' in command:
        print("Command: Simulate Tello auto Takeoff")
    elif 'land' in command:
        print("Command: Simulate Tello auto Land")
    elif 'forward' in command:
        print(f"Command: Simulate moving forward {distance} cm")
    elif 'backward' in command:
        print(f"Command: Simulate moving backward {distance} cm")
    elif 'left' in command:
        print(f"Command: Simulate moving left {distance} cm")
    elif 'right' in command:
        print(f"Command: Simulate moving right {distance} cm")
    elif 'up' in command:
        print(f"Command: Simulate moving up {distance} cm")
    elif 'down' in command:
        print(f"Command: Simulate moving down {distance} cm")
    elif 'rotate' in command:
        print("Command: Simulate rotating 90 degrees")
    elif 'flip' in command:
        print("Command: Simulate flipping")
    elif 'end' in command:
        print('Ending the program...')
        sys.exit(0)
    else:
        print("Command not recognized")

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
                command, _ = parse_command(command)
                execute_command(command)
            except Exception as e:
                print(f"Error: {e}")

# Main loop
while True:
    listen_and_execute()
