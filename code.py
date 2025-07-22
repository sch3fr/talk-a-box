# code.py (for CircuitPython) - Randomized Playback - Fix for missing shuffle/sample

import board
import digitalio
import audiocore
import audiobusio
import time
import random # Import the random module

# --- Configuration ---
# I2S Pin assignments for MAX98357A
BCLK_PIN = board.GP0
LRCLK_PIN = board.GP1
DATA_PIN = board.GP2

# Pushbutton pin
BUTTON_PIN = board.GP3

# --- Audio File Management ---
AUDIO_FOLDER = "/audio/" # Adjust this if your files are in a subfolder

NUM_AUDIO_FILES = 41 # Your total count

# Create the initial list of all possible file paths (this is our master list)
MASTER_AUDIO_FILE_PATHS = []
for i in range(1, NUM_AUDIO_FILES + 1):
    MASTER_AUDIO_FILE_PATHS.append(f"{AUDIO_FOLDER}{i:04d}.wav")

print(f"Discovered {len(MASTER_AUDIO_FILE_PATHS)} audio file names.")

# --- Setup I2S ---
try:
    audio_out = audiobusio.I2SOut(
        bit_clock=BCLK_PIN,
        word_select=LRCLK_PIN,
        data=DATA_PIN
    )
    print("I2S initialized successfully.")
except Exception as e:
    print(f"Error initializing I2S: {e}")
    print("Please check I2S pin assignments in code and physical wiring.")
    while True:
        time.sleep(1)

# Initialize the pushbutton
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# --- State Variables for Randomized Playback ---
# This list will hold the files that are still available to play in the current cycle
files_remaining_to_play = []

def refill_files_remaining():
    global files_remaining_to_play
    # Copy all paths from the master list to the 'remaining' list
    files_remaining_to_play = MASTER_AUDIO_FILE_PATHS[:]
    print("Refilled files for new playback cycle.")

# Refill the list when the code starts
refill_files_remaining()

print("Setup complete. Press the button to play a random audio file.")

# --- Main Loop ---
last_button_state = True # True means button is not pressed (due to PULL_UP)

while True:
    current_button_state = button.value

    # Detect a falling edge (button pressed)
    if current_button_state == False and last_button_state == True:
        print("Button pressed!")

        # If we've played all files in the current cycle, refill the list
        if not files_remaining_to_play: # Checks if the list is empty
            print("All files played in this cycle. Starting a new random cycle.")
            refill_files_remaining()

        if files_remaining_to_play: # Ensure the list is not empty after refill
            # Pick a random index from the files that are still remaining
            random_index = random.randrange(len(files_remaining_to_play)) # random.randrange(stop)

            # Get the file path from the randomly chosen index
            file_to_play_name = files_remaining_to_play[random_index]
            print(f"Playing: {file_to_play_name}")

            try:
                with open(file_to_play_name, "rb") as audio_file:
                    wav = audiocore.WaveFile(audio_file)
                    audio_out.play(wav)
                    while audio_out.playing:
                        pass

            except OSError as e:
                print(f"Error opening or playing file {file_to_play_name}: {e}")
                print(f"Make sure '{file_to_play_name}' exists on your CIRCUITPY drive at the correct path.")
            except Exception as e:
                print(f"An unexpected error occurred during playback: {e}")
            finally:
                if audio_out.playing:
                    audio_out.stop()
                time.sleep(0.1)
                print(f"Finished playing {file_to_play_name}.")

            # --- CRITICAL CHANGE: Remove the played file from the remaining list ---
            files_remaining_to_play.pop(random_index)
            print(f"{len(files_remaining_to_play)} files remaining in this cycle.")

        else:
            print("Error: No audio files available to play after refill attempt.")

        time.sleep(0.3) # Debounce delay for button press

    last_button_state = current_button_state
    time.sleep(0.01) # Short delay to reduce CPU usage