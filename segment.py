# as explained by chatgpt
'''
In this modified code, we first import the necessary modules, then define the input file path, output directory path, 
and parameters for the double threshold method. 
We then load the MP3 file using librosa.load() and extract the mel spectrogram using librosa.feature.melspectrogram().

Next, we calculate the mean and standard deviation of the mel spectrogram and use these values to calculate 
the lower and upper thresholds. We then create the output directory if it doesn't exist.

We use librosa.util.frame() to iterate through each frame of the MP3 file, a
nd for each frame, we calculate the mel spectrogram and its energy. 
If the energy is above the upper threshold, we start a new bird sound activation. 
If the energy is below the lower threshold and a bird sound activation has already started, 
we end the current activation and save it as a mel-spectrogram image using librosa.display.specshow() and plt.savefig().

Note that this code saves the mel-spectrogram images as PNG files, 
but you can change the format by modifying the file extension in os.path.join() and plt.savefig(). 
You can also adjust the parameters in plt.figure() to change the size of the images.
'''



import librosa
import librosa.display
import numpy as np
import os
import matplotlib.pyplot as plt

# Define the input MP3 file path
input_file = "input.mp3"

# Define the output directory path
output_dir = "output"

# Define the parameters for the double threshold method
frame_length = 2048
hop_length = 512
n_mels = 128
threshold_low = 0.1
threshold_high = 0.2

# Load the MP3 file and extract the mel spectrogram
y, sr = librosa.load(input_file)
S = librosa.feature.melspectrogram(y, sr=sr, n_fft=frame_length, hop_length=hop_length, n_mels=n_mels)

# Calculate the mean and standard deviation of the mel spectrogram
S_mean = np.mean(S)
S_std = np.std(S)

# Calculate the lower and upper thresholds
threshold_lower = S_mean + threshold_low * S_std
threshold_upper = S_mean + threshold_high * S_std

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Segment the MP3 file using the double threshold method and save each segment as a mel-spectrogram image
for i, frame in enumerate(librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)):
    frame_S = librosa.feature.melspectrogram(frame, sr=sr, n_fft=frame_length, hop_length=hop_length, n_mels=n_mels)
    frame_energy = np.mean(frame_S)
    if frame_energy > threshold_upper:
        # Start of a bird sound activation
        start = i * hop_length
    elif frame_energy < threshold_lower and start is not None:
        # End of a bird sound activation
        end = i * hop_length
        segment = y[start:end]
        S_segment = librosa.feature.melspectrogram(segment, sr=sr, n_fft=frame_length, hop_length=hop_length, n_mels=n_mels)
        plt.figure(figsize=(2, 2))
        librosa.display.specshow(librosa.power_to_db(S_segment, ref=np.max), y_axis='mel', fmax=sr/2, x_axis='time')
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, f"segment{i}.png"), bbox_inches='tight', pad_inches=0)
        plt.close()
        start = None

        
