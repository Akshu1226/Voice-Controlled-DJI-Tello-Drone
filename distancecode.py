from vosk import Model, KaldiRecognizer
import pyaudio
from djitellopy import Tello
import sys
import cv2
import numpy as np
import scipy.signal
import re
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from word2number import w2n

# Initialize the Vosk model and recognizer
model_path = r"C:\Users\DELL\Downloads\vosk-model-small-en-in-0.4 (2)\vosk-model-small-en-in-0.4"  # Update this with the correct path
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Initialize the Tello drone               #################################################
# tello = Tello()
# tello.connect()

# # Print the initial battery percentage
# print(f"Battery Percent: {tello.get_battery()}%")

# Set up microphone input
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Initialize Sentence Transformer model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a pre-trained model

# List of known commands
known_commands = ["takeoff", "land", "forward", "backward", "left", "right", "up", "down", "rotate", "flip", "end"]


def recognize_command():
    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)  # Output the recognized text
            return result


def get_closest_command(recognized_text, threshold=0.7):
    # Get embeddings for the recognized text
    recognized_embedding = embedding_model.encode([recognized_text])

    # Get embeddings for all known commands
    command_embeddings = embedding_model.encode(known_commands)

    # Calculate cosine similarity
    similarities = cosine_similarity(recognized_embedding, command_embeddings)[0]

    # Find the command with the highest similarity
    closest_command_index = np.argmax(similarities)
    highest_similarity = similarities[closest_command_index]

    # Check if the highest similarity is above the threshold
    if highest_similarity >= threshold:
        closest_command = known_commands[closest_command_index]
    else:
        closest_command = None

    return closest_command


# def parse_command(command):
#     # Extract the distance if mentioned in the command
#     match = re.search(r'(\d+|[a-zA-Z]+)\s*(cm|centimeters|meters|m)?', command)
#     if match:
#         distance_text = match.group(1)
#         unit = match.group(2)

#         # Convert text to number if it's a word
#         try:
#             distance = w2n.word_to_num(distance_text)
#         except ValueError:
#             # If it's not a word, check if it's a valid number
#             try:
#                 distance = int(distance_text)
#             except ValueError:
#                 # Handle cases where distance_text is not a valid number
#                 distance = None  # or set a default value like 40

#         if distance is not None:
#             if unit in ['meters', 'm']:
#                 distance *= 100  # Convert meters to centimeters
#         else:
#             distance = 40  # Default distance if not specified
#     else:
#         distance = 40  # Default distance if not specified

#     # Extract the command part without distance
#     command_part = re.sub(r'(\d+|[a-zA-Z]+)\s*(cm|centimeters|meters|m)?', '', command).strip()

#     return command_part.lower(), distance


def execute_command(command, distance):
    # Execute the recognized command
    if 'takeoff' in command or 'take off' in command:
        print("Command: Tello auto Takeoff")
        # tello.takeoff()                                  ############################################################
    elif 'land' in command:
        print("Command: Tello auto Land")
        # tello.land()
    # elif 'forward' in command or 'for ward' in command:
    elif 'forward' in command:
        print(f"Command: Move forward {distance} cm")
        # tello.move_forward(distance)
    elif 'backward' in command:
        print(f"Command: Move backward {distance} cm")
        # tello.move_back(distance)
    elif 'left' in command:
        print(f"Command: Move left {distance} cm")
        # tello.move_left(distance)
    elif 'right' in command:
        print(f"Command: Move right {distance} cm")
        # tello.move_right(distance)
    elif 'up' in command:
        print(f"Command: Move up {distance} cm")
        # tello.move_up(distance)
    elif 'down' in command:
        print(f"Command: Move down {distance} cm")
        # tello.move_down(distance)
    elif 'rotate' in command:
        print("Command: Rotate 90 degrees")
        # tello.rotate_clockwise(90)
    elif 'flip' in command:
        print("Command: Flip")
        # tello.flip('f')
    elif 'end' in command:
        print('Ending the program...')
        # tello.land()
        sys.exit(0)
    else:
        print("Command not recognized")

    # Print the battery status after executing each command                       ###################################
    # print(f"Battery Percent: {tello.get_battery()}%")


def filter_text_based_distance(command):
    # Define a pattern to match text-based numbers
    number_words_pattern = r'\b(one|two|three|four|five|six|seven|eight|nine|ten|' \
                           r'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|' \
                           r'eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|' \
                           r'eighty|ninety|hundred|thousand)\b'

    # Find all matches of text-based numbers in the command
    text_numbers = re.findall(number_words_pattern, command, flags=re.IGNORECASE)

    # If found, convert each text number to its numeric equivalent
    if text_numbers:
        try:
            # Join the text numbers into a single string and convert
            distance = w2n.word_to_num(" ".join(text_numbers))
        except ValueError:
            distance = None
    else:
        distance = None  # No text-based number found

    return distance


def listen_and_execute():
    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)  # Output the recognized text

            try:
                result_dict = json.loads(result)  # Parse the JSON string
                recognized_text = result_dict.get('text',
                                                  '').strip()  # Safely get the 'text' field and strip any extra spaces
                print(f"You said: '{recognized_text}'")

                # Skip processing if recognized_text is empty
                if not recognized_text:
                    print("No recognizable command detected. Skipping execution.")
                    continue

                # Extract distance from recognized text
                distance = filter_text_based_distance(recognized_text)

                # Remove text-based numbers from the recognized text
                if distance is not None:
                    number_words_pattern = r'\b(one|two|three|four|five|six|seven|eight|nine|ten|' \
                                           r'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|' \
                                           r'eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|' \
                                           r'eighty|ninety|hundred|thousand)\b'
                    recognized_text = re.sub(number_words_pattern, '', recognized_text, flags=re.IGNORECASE).strip()
                    print(f"Remaining text after removing numbers: '{recognized_text}'")

                # Get the closest command using cosine similarity
                closest_command = get_closest_command(recognized_text, threshold=0.7)  # Adjust threshold as needed
                if closest_command:
                    print(f"Interpreted as: {closest_command}")

                    # Execute the command with the extracted distance
                    execute_command(closest_command,
                                    distance if distance is not None else 40)  # Use default distance if not extracted
                else:
                    print("Command not recognized confidently. Skipping execution.")
            except Exception as e:
                print(f"Error: {e}")


# def listen_and_execute():
#     while True:
#         data = stream.read(1024)
#         if recognizer.AcceptWaveform(data):
#             result = recognizer.Result()
#             print(result)  # Output the recognized text

#             try:
#                 result_dict = json.loads(result)  # Parse the JSON string
#                 recognized_text = result_dict.get('text', '').strip()  # Safely get the 'text' field and strip any extra spaces
#                 print(f"You said: '{recognized_text}'")

#                 # Skip processing if recognized_text is empty
#                 if not recognized_text:
#                     print("No recognizable command detected. Skipping execution.")
#                     continue

#                 # Get the closest command using cosine similarity
#                 closest_command = get_closest_command(recognized_text, threshold=0.7)  # Adjust threshold as needed
#                 if closest_command:
#                     print(f"Interpreted as: {closest_command}")

#                     # Parse and execute the command
#                     command, distance = parse_command(closest_command)
#                     print('Command ===== ', command)
#                     print('distance ===== ', distance)
#                     execute_command(command, distance)
#                 else:
#                     print("Command not recognized confidently. Skipping execution.")
#             except Exception as e:
#                 print(f"Error: {e}")


# Main loop
while True:
    listen_and_execute()
    k = cv2.waitKey(1)
    if k == ord('a'):
        # tello.land()                                                 ####################################################
        print("Simulated landing command triggered.")
        break

# Release resources
stream.stop_stream()
stream.close()
cap.terminate()
