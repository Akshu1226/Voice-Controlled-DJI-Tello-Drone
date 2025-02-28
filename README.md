# Voice-Controlled-DJI-Tello-Drone
This repository provides a Python-based solution to control a DJI Tello drone using voice commands. The system leverages the Vosk speech recognition model to interpret voice commands and the djitellopy library to interface with the Tello drone. The main goal of this project is to create a seamless and interactive way to operate the drone with just your voice.
# Features
## Voice-Controlled Drone: 
Control your DJI Tello drone with simple voice commands.
## Customizable Commands: 
Supports common drone movements (e.g., takeoff, land, forward, backward, rotate) with customizable distances.
## Real-Time Processing: 
Uses the Vosk speech recognition engine for fast and efficient voice command processing.
## Multithreading: 
Allows for simultaneous voice recognition and drone control, improving responsiveness and efficiency.
## Distance Support: 
Supports specifying distances in centimeters or meters for movement commands.
# Prerequisites
DJI Tello Drone: The project is specifically designed to control a DJI Tello drone.
Python 3: Ensure that Python version 3 or later is installed on your system.
Microphone: A working microphone connected to your computer for capturing voice commands or you can even use the microphone present in your laptop.
Internet Connection: Required for installing all the libraries and downloading the Vosk model.
# Install Python Dependencies:
Make sure you have Python 3 installed. You can verify your Python version with:
## python --version
Once Python is installed, you need to install the required libraries for the project.
## pip install libraryname
## This will install the following libraries:
1. Vosk:  A speech recognition library used to convert spoken language into text.
2. PyAudio: For capturing audio input from the microphone.
3. 4. DJITelloPy:  A library that allows interaction with and control over the DJI Tello drone.
5. KaldiRecognizer:  The speech recognition engine within Vosk for real-time processing.
6. NumPy:  For numerical operations, often used with image and audio processing.
7. SciPy: A library for signal processing, which is used in noise reduction and other signal transformations.
8. Threading: A built-in Python module that is used to manage multiple threads for concurrent execution.
## Download the Vosk Model:
Using the following link you can download the required vosk model: ## https://alphacephei.com/vosk/models.
## Connect to DJI Tello:
Power On the Tello Drone: Turn on your DJI Tello drone.
Connect to the Tello Wi-Fi: On your computer, connect to the Tello's Wi-Fi network.
# Running the Script:
Once you have set up the project and installed the dependencies,you can start running the program.
This will start the voice recognition system, and the program will continuously listen for commands to control the drone.
## Verify Connection and Battery Status
Once the script is running, it will Automatically establish a connection with the Tello drone.
Display the current battery percentage in the terminal.
Example output:
Battery Percent: 85%
If the battery percentage is low, charge the drone before proceeding to avoid unexpected disconnections.
## Voice Commands:
Once the program is running, simply speak one of the predefined commands to control the drone. The system will listen for 
  commands such as:
- Takeoff: "Take off" — The drone will take off.
- Land: "Land" — The drone will land.
- Move Commands:
- "Move forward 30 meters"
- "Move backward 10 cm"
- "Move left 20 meters"
- "Move right 15 cm"
- Rotate: "Rotate" — The drone will rotate 90 degrees.
- Flip: "Flip" — The drone will perform a flip.
- End: "End" — The drone will land and the program will exit.
- The distance can be specified in centimeters or meters.
## Stopping the Program
To stop the program, press 'a' in the terminal. This will land the drone and exit the program safely.
## How It Works:
- Voice Command Recognition:
  The system continuously listens for voice commands using the Vosk speech recognition. When a command is detected, it is 
  processed into text.
- Command Parsing:
  The text is parsed to identify the specific action (e.g., "move left") and the corresponding distance (if mentioned).
- Drone Control:
  Based on the parsed command, the system sends appropriate instructions to the DJI Tello drone using the djitellopy 
  library. This allows the drone to perform the specified action (e.g., moving, rotating, flipping).
- Multithreading:
  The voice recognition runs on a separate thread, allowing real-time drone control without delays. The main thread keeps 
  the drone operation active while listening for new commands.
# Common Issues and Troubleshooting Steps:
1. Microphone Not Detected: Check if your microphone is plugged in properly and set as the default input on your system.
2. Tello Not Responding:Ensure your computer is connected to the Tello drone's Wi-Fi and the drone is turned on.
3. Speech Recognition Issues:Make sure the correct Vosk model is downloaded, the model path in the code is correct, and you’re in a quiet place to reduce background noise.
4. Drone Not Moving:Check if the drone has enough battery and ensure there are no obstacles blocking its path.
# Best Practices for Operating the Drone
1. Operate in Open Spaces: 
Always use the drone in a large, open space, free from obstacles like walls, ceilings, and other objects.
2. Monitor Battery Levels:
Regularly check the battery percentage displayed in the terminal to avoid mid-flight disconnections.
3. Avoid Interference:
Ensure there is no interference from other Wi-Fi networks or devices that could disrupt the Tello
Wi-Fi connection.
4. Stay Within Range:
Keep the drone within a 10-meter radius of your computer for optimal connectivity.
# Conclusion and Future Work:
This project successfully implemented a voice-controlled system for the DJI Tello drone, achieving simple and effective human-drone interaction. The system's versatility and performance were enhanced by incorporating distance-based movement commands and threading. Through the integration of a Vosk model and the progression from a custom dataset, the system is now much more usable and can accommodate a diverse range of voices and accents. Future work could focus on:
-	Enhancing speech recognition to handle noisy environments.
-	Adding new commands for more advanced drone movements.
-	Integrating obstacle detection into autonomous navigation.
-	Optimized threading for improved performance and reliability.




