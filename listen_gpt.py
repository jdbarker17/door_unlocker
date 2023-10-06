from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import wave
import pyaudio

# Globals
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 500
secret = [0.56655329, 0.55641723, 0.30201814]
#secret = [0.2550794, 0.12126984, 0.2592517,  0.22126984, 0.23764172, 0.14269841, 0.24099773, 0.25594104, 0.26643991, 0.13537415, 0.23557823, 0.54469388, 0.23739229, 0.49097506, 0.2623356, 0.13979592, 0.2624263, 0.49927438]



def main_peak_detection(sound_file, window_size_seconds=0.05):
    fs, data = read(sound_file)
    
    # Detect all peaks
    all_peaks, _ = find_peaks(data, height=5000)
    
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




def is_triggered(data):
    """Check if the audio data exceeds the threshold."""
    THRESHOLD = 500  
    amplitudes = np.frombuffer(data, dtype=np.int16)
    if np.abs(amplitudes).mean() > THRESHOLD:
        return True
    return False

def record_audio(RECORD_SECONDS = 5):
    audio = pyaudio.PyAudio()
    ################################### Audio Recording and Processing ################################################
    # Parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    THRESHOLD = 500  # Adjust this value based on your needs
    # RECORD_SECONDS = 5  # Duration to record after detecting the sound
        # Start streaming from microphone

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Listening...")

    recording_data = []
    while True:
        data = stream.read(CHUNK)
        if is_triggered(data):
            print("Recording...")
            recording_data.append(data)
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                recording_data.append(data)
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(recording_data)
   


def save_wav_file(filename, audio_data):
    """Save audio data to a WAV file."""
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)

def validate(distances):
    
    if len(distances) != len(secret):
        return False
    
    else:
        for i,distance in enumerate(distances):
            #Set tolerance equal to 50% of the value
            tolerance = 0.5
            # If its within upper and lower tolerances
            if (distance  < secret[i] * tolerance + secret[i]) and distance > secret[i] - (tolerance *  secret[i]):
                continue
            else:
                return False
        
        return True


def plot_analysis(focuses,distances,amplitudes):

    #Prints for Distances, Focuses, and Amplitudes
    print(f'Distances = {distances}')
    print(f'Focuses = {focuses}')
    print(f'Amplitudes = {amplitudes}')

    #Plot for Distance Lines
    plt.plot([focuses[0],focuses[0]+distances[0]],[amplitudes[0],amplitudes[0]])

    #Plot for Focus Lines
    plt.plot(focuses, amplitudes, 'o', color='red')
    for i,focus in enumerate(focuses):
        if i > len(distances) - 1:
            break
        #Plots distances on the main graph at desired altitudes
        plt.plot([focus,focus + distances[i]], [amplitudes[i],amplitudes[i]])
    plt.show()


if __name__ == '__main__':
    recorded_audio = record_audio(5)
    save_wav_file("output.wav", recorded_audio)

    focuses, distances, amplitudes = main_peak_detection("output.wav")
    plot_analysis(focuses,distances,amplitudes)
    print(validate(distances))
