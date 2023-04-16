import librosa
import numpy as np
import time
import colorsys
import matplotlib.pyplot as plt
import pygame
from collections import deque
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class PumpWidget(QWidget):
    def __init__(self, index):
        super().__init__()

        self.index = index
        self.power = 0
        self.color = (0, 0, 0)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.update_label()

    def update_label(self):
        self.label.setText(f"Pump {self.index + 1}: {int(self.power * 100)}%")
        self.label.setStyleSheet(f"background-color: rgb({int(self.color[0] * 255)}, {int(self.color[1] * 255)}, {int(self.color[2] * 255)});")

    def update_pump_state(self, power, color):
        self.power = power
        self.color = color
        self.update_label()

class WaterLightsShow(QWidget):
    def __init__(self, n_pumps):
        super().__init__()

        self.n_pumps = n_pumps
        self.pump_widgets = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        for i in range(self.n_pumps):
            pump_widget = PumpWidget(i)
            self.pump_widgets.append(pump_widget)
            layout.addWidget(pump_widget)

        self.setLayout(layout)
        self.setWindowTitle("Water and Lights Show")

    def update_pump_states(self, pump_states):
        for i in range(self.n_pumps):
            power = pump_states[f"pump_{i+1}"]["power"]
            color = pump_states[f"pump_{i+1}"]["color"]

            self.pump_widgets[i].update_pump_state(power, color)



class Pump:
    def __init__(self, smoothing_window=10):
        self.smoothing_window = smoothing_window
        self.past_powers = deque(maxlen=smoothing_window)

    def update(self, new_power):
        self.past_powers.append(new_power)
        return np.mean(self.past_powers)


def visualize_show(app, window, pump_states):
    window.update_pump_states(pump_states)
    app.processEvents()


def initialize_pumps(n_pumps, smoothing_window=10):
    return [Pump(smoothing_window) for _ in range(n_pumps)]


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def map_features_to_pump_states(pumps, features, n_pumps , sr):
    """Maps audio features to water pump states.

    Args:
        features (dict): A dictionary of audio features.
        n_pumps (int): The number of water pumps available.

    Returns:
        dict: A dictionary with the water pump states.
    """

    # Normalize the spectral centroid to [0, 1]
    normalized_spectral_centroid = features["spectral_centroid"] / sr

    # Map the spectral centroid to a color in the HSV color space
    hue = normalized_spectral_centroid
    saturation = 1.0
    value = 1.0
    rgb_color = colorsys.hsv_to_rgb(hue, saturation, value)

    # Calculate the power for each pump based on the tempo and beats
    if features["tempo"] != 0:
        beat_duration = 60.0 / features["tempo"]
        beat_fraction = (time.time() % beat_duration) / beat_duration
        raw_pump_powers = [np.sin(2 * np.pi * i * beat_fraction) for i in range(1, n_pumps + 1)]
    else:
        raw_pump_powers = [0] * n_pumps

    # Update the pump powers using the moving average
    pump_powers = [pumps[i].update(raw_pump_powers[i]) for i in range(n_pumps)]

    # Create a dictionary with the water pump states
    pump_states = {}
    for i in range(n_pumps):
        pump_states[f"pump_{i+1}"] = {
            "power": max(pump_powers[i], 0),  # Ensure the power is non-negative
            "color": rgb_color
        }

    return pump_states


def process_audio_in_chunks(file_path, n_pumps, chunk_duration=0.1):
    """Processes an audio file in chunks and updates the pump states.

    Args:
        file_path (str): Path to the audio file.
        n_pumps (int): The number of water pumps available.
        chunk_duration (float): The duration of each chunk in seconds. Default is 0.1 seconds.

    Returns:
        None
    """
    # Load the audio file
    y, sr = librosa.load(file_path)

    # Calculate the number of samples per chunk
    samples_per_chunk = int(chunk_duration * sr)

    # Create the PyQt5 application and the WaterLightsShow instance
    app = QApplication(sys.argv)
    window = WaterLightsShow(n_pumps)
    window.show()

    # Initialize the pumps
    pumps = initialize_pumps(n_pumps)

    # Play the audio
    play_audio(file_path)

    # Iterate over the audio in chunks
    for start_sample in range(0, len(y), samples_per_chunk):
        # Extract the current chunk
        end_sample = start_sample + samples_per_chunk
        y_chunk = y[start_sample:end_sample]

        # Extract features for the current chunk
        features = extract_show_features_from_chunk(y_chunk, sr)

        # Update the pump states based on the features
        pump_states = map_features_to_pump_states(pumps, features, n_pumps, sr)

        # Visualize the water and lights show
        visualize_show(app, window, pump_states)

        # Sleep for the duration of the chunk
        time.sleep(chunk_duration)

    pygame.mixer.music.stop()

    # Close the PyQt5 application
    sys.exit(app.exec_())


def extract_show_features_from_chunk(y_chunk, sr):
    # Extract features for the current chunk
    tempo, beats = librosa.beat.beat_track(y=y_chunk, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y_chunk, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y_chunk, sr=sr)

    features = {
        "tempo": tempo,
        "beats": beats,
        "spectral_centroid": np.mean(spectral_centroid),
        "spectral_contrast": np.mean(spectral_contrast)
    }

    return features


n_pumps = 4
songPath = r"SongPath"
process_audio_in_chunks(songPath, n_pumps)
