from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import wave

def main_peak_detection(sound_file, window_size_seconds=0.15):
    fs, data = read(sound_file)
    
    # Detect all peaks
    all_peaks, _ = find_peaks(data, height=1000)
    
    main_peaks = []
    
    # Check each peak to see if it's the main peak within its window
    for peak in all_peaks:
        start = int(max(0, peak - window_size_seconds * fs / 2))
        end = int(min(len(data), peak + window_size_seconds * fs / 2))
        
        # If the current peak is the maximum in its window, keep it
        if data[peak] == max(data[start:end]):
            main_peaks.append(peak)
    
    focuses = np.array(main_peaks) / fs  # Convert peak indices to time
    distances = np.diff(focuses)
    amplitudes = data[main_peaks]
    plot_signal(sound_file)
    
    return focuses, distances, amplitudes

def plot_signal(audio):
    # Preprocessing
    audio_sig = wave.open(audio, "r")
    fs = audio_sig.getframerate()
    n_samples = audio_sig.getnframes()
    signal_wave = audio_sig.readframes(-1)
    duration = n_samples/fs

    # Actual Processing
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    time = np.linspace(0, duration, num=n_samples)

    # Plotting
    plt.figure(figsize=(15, 5))
    plt.plot(time, signal_array)
    plt.title('Audio Plot')
    plt.ylabel('Signal Wave')
    plt.xlabel('Time (s)')
    plt.xlim(time[0], time[-1])

# Main peak detection
focuses, distances, amplitudes = main_peak_detection("band knock.wav")
#plot_signal("snaps.wav")#


# Plot detected main peaks on the waveform
plt.plot(focuses, amplitudes, 'o', color='red')
for i,focus in enumerate(focuses):
    if i > len(distances) - 1:
        break
    #Plots distances on the main graph at desired altitudes
    plt.plot([focus,focus + distances[i]], [amplitudes[i],amplitudes[i]])

# TODO - iomplement system logic

#plt.plot([focuses[0],focuses[0]+distances[0]],[amplitudes[0],amplitudes[0]])


plt.show()

focuses, distances, amplitudes  # Return these values to inspect
print(f'Distances = {distances}')
print(f'Focuses = {focuses}')
print(f'Amplitudes = {amplitudes}')
