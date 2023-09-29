from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import wave
import numpy as np


def calc_distances(sound_file):
    #The minimun value for the sound to be recognized as a knock
    min_val = 5000
    
    fs, data = read(sound_file)
    data_size = len(data)
    
    #The number of indexes on 0.15 seconds
    focus_size = int(0.15 * fs)
    
    focuses = []
    distances = []
    amplitudes =[]
    idx = 0
    
    # Initialize the distances list to store distances between consecutive focuses


    # Loop through the data array
    while idx < len(data):
        # Check if the current data value is above the volume threshold
        if data[idx] > min_val:
            # Calculate the center index of the region of interest
            mean_idx = idx + focus_size // 2
            # Append the normalized center index to the focuses list
            focuses.append(float(mean_idx) / data_size)
            
            # If there's more than one focus point, calculate the distance
            # between the current and the previous focus points
            if len(focuses) > 1:
                last_focus = focuses[-2]
                actual_focus = focuses[-1]
                distances.append(actual_focus - last_focus)
                amplitudes.append(data[mean_idx])
            
            # Skip the current region by increasing the index by the window size
            idx += focus_size
        else:
            # If the current value is not above the threshold, move to the next data point
            idx += 1

    # Return the list of distances between consecutive regions of interest
    return focuses,distances,amplitudes
 
#Preprocessing
audio_sig = wave.open("snaps.wav", "r")
print('Parameters:', audio_sig.getparams())
fs = audio_sig.getframerate()
n_samples = audio_sig.getnframes()
signal_wave = audio_sig.readframes(-1)
duration = n_samples/fs

#Actual Processing
signal_array = np.frombuffer(signal_wave, dtype=np.int16)
time = np.linspace(0, duration, num=n_samples)
print(f'sig_array  = {signal_array}')

#Plotting
plt.figure(figsize=(15, 5))
plt.plot(time, signal_array)
plt.title('Audio Plot')
plt.ylabel(' signal wave')
plt.xlabel('time (s)')
plt.xlim(time[0], time[-1]) #limiting the x axis to the audio time
#plt.show()


#Knock processing
#The minimum value for the sound to be recognized as a knock
min_val = 5000
#The number of indexes on 0.15 seconds
focus_size = int(0.15 * fs)

focuses = []
distances = []
idx = 0
distances,focuses,amplitudes = calc_distances('snaps.wav')
print(f'Focuses = {focuses}')
print(f'Distances = {distances}')
print(f'Amplitudes = {amplitudes}')
plt.plot(distances[0:4], amplitudes, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
plt.show()



