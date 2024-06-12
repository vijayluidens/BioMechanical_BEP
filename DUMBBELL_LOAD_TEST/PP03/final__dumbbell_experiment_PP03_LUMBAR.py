import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def transform_mV(emg_data):
    transformed_data = (emg_data - ((2**16 - 1) / 2)) / 32768
    return transformed_data

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

def process_and_plot(file_path, start_freq, end_freq, plot_position):
    # Load the data from the file
    data = np.loadtxt(file_path)

    # Extract the relevant columns (5th to 8th) for the specified frequency range
    frequency = data[:, 0]  
    relevant_data = data[(frequency >= start_freq) & (frequency <= end_freq), 4:8]

    # Transform values to millivolt
    transformed_data = transform_mV(relevant_data)

    cutoff = 10  # Define the cutoff frequency
    fs = 1000   # Define the sampling frequency
    order = 4   # Define the filter order

    # Filter ES-L left and right data and calculate RMS
    filtered_rms_left = butter_lowpass_filter((transformed_data[:, 1])**2, cutoff, fs, order)
    filtered_rms_right = butter_lowpass_filter((transformed_data[:, 3])**2, cutoff, fs, order)

    # Clip negative values to zero
    filtered_rms_left = np.clip(filtered_rms_left, 0, None)
    filtered_rms_right = np.clip(filtered_rms_right, 0, None)

    # Take the square root to get RMS after filtering
    filtered_rms_left = np.sqrt(filtered_rms_left)
    filtered_rms_right = np.sqrt(filtered_rms_right)

    # Calculate the average RMS
    average_rms = (filtered_rms_left + filtered_rms_right) / 2

    # Find the maximum value of the average RMS and its index
    max_avg_rms = np.max(average_rms)
    max_avg_rms_index = np.argmax(average_rms)

    # Extract the time indices for the selected range for plotting
    selected_indices = np.where((frequency >= start_freq) & (frequency <= end_freq))[0]

    # Create a time array based on the selected indices
    time = np.arange(len(selected_indices))

    # Plot the selected data
    plt.subplot(3, 1, plot_position)
    plt.plot(time, transformed_data[:, 1], label='ES-L Left')
    plt.plot(time, transformed_data[:, 3], label='ES-L Right')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude (mV)')
    plt.title(f'Erector Spinae Data for {file_path} Specified Frequency Range')

    # Plot filtered RMS of ES-L left and right
    plt.plot(time, filtered_rms_left, 'k', label='Filtered RMS of ES-L Left')
    plt.plot(time, filtered_rms_right, 'm', label='Filtered RMS of ES-L Right')

    # Plot average RMS
    plt.plot(time, average_rms, 'r', label='Average RMS')

    # Plot vertical line at max average RMS index
    plt.axvline(x=max_avg_rms_index, color='g', linestyle='--', label='Max Avg RMS')

    # Plot dot at maximum value of the mean
    plt.scatter(max_avg_rms_index, max_avg_rms, color='b', zorder=5)
    plt.text(max_avg_rms_index, max_avg_rms, f'({max_avg_rms_index}, {max_avg_rms:.4f})', fontsize=9, verticalalignment='bottom')

    plt.legend()

    return max_avg_rms

# Define file paths and frequency ranges
file_paths = ["DUMBBELL_LOAD_TEST/PP03/PP03_6kg.txt", "DUMBBELL_LOAD_TEST/PP03/PP03_10kg.txt"]
frequency_ranges = [(5200, 7100), (4100, 5500)]
loads = [6, 10]  # Corresponding loads in kg

# Create a figure for subplots
plt.figure(figsize=(12, 18))

max_rms_values = []

# Process and plot each file
for i, (file_path, freq_range, load) in enumerate(zip(file_paths, frequency_ranges, loads)):
    max_rms = process_and_plot(file_path, freq_range[0], freq_range[1], i + 1)
    max_rms_values.append(max_rms)

# Show the plots
plt.tight_layout()
plt.show()

mvc_pp03 = 0.0941

norm_max_rms_values = np.divide(max_rms_values, mvc_pp03)

# Plot maximum average RMS against load
plt.figure()
plt.plot(norm_max_rms_values, loads, marker='o')
plt.xlabel('Load (kg)')
plt.ylabel('Maximum Average RMS (mV)')
plt.title('Maximum Average RMS vs. Load')
plt.grid(True)
plt.show()
