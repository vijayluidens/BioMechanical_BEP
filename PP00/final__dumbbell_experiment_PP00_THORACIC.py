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

    # Filter ES-T left and right data and calculate RMS
    filtered_rms_left_thoracic = butter_lowpass_filter((transformed_data[:, 0])**2, cutoff, fs, order)
    filtered_rms_right_thoracic = butter_lowpass_filter((transformed_data[:, 2])**2, cutoff, fs, order)

    # Take the square root to get RMS after filtering
    filtered_rms_left_thoracic = np.sqrt(filtered_rms_left_thoracic)
    filtered_rms_right_thoracic = np.sqrt(filtered_rms_right_thoracic)

    # Find the maximum value of the average RMS and its index
    max_rms_left = np.max(filtered_rms_left_thoracic)
    max_rms_index_left = np.argmax(filtered_rms_left_thoracic)
    max_rms_right = np.max(filtered_rms_right_thoracic)
    max_rms_index_right = np.argmax(filtered_rms_right_thoracic)

    # Print the maximum RMS values
    print(f'Max RMS ES-T Left for {file_path}: {max_rms_left:.4f}')
    print(f'Max RMS ES-T Right for {file_path}: {max_rms_right:.4f}')

    # Extract the time indices for the selected range for plotting
    selected_indices = np.where((frequency >= start_freq) & (frequency <= end_freq))[0]

    # Create a time array based on the selected indices
    time = np.arange(len(selected_indices))

    # Plot the selected data
    plt.subplot(3, 1, plot_position)
    plt.plot(time, transformed_data[:, 0], label='ES-T Left')
    plt.plot(time, transformed_data[:, 1], label='ES-T Right')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude (mV)')
    plt.title(f'Erector Spinae Data for {file_path} Specified Frequency Range')

    # Plot filtered RMS of ES-T left and right
    plt.plot(time, filtered_rms_left_thoracic, 'k', label='Filtered RMS of ES-T Left')
    plt.plot(time, filtered_rms_right_thoracic, 'm', label='Filtered RMS of ES-T Right')

    # Plot vertical line at max RMS index
    plt.axvline(x=max_rms_index_left, color='g', linestyle='--', label='Max RMS of ES-T Left')
    plt.axvline(x=max_rms_index_right, color='g', linestyle='--', label='Max RMS of ES-T Right')

    # Plot dot at maximum value ES-T left and right
    plt.scatter(max_rms_index_left, max_rms_left, color='b', zorder=5)
    plt.scatter(max_rms_index_right, max_rms_right, color='cyan', zorder=5)
    plt.text(max_rms_index_left, max_rms_left, f'({max_rms_index_left}, {max_rms_left:.4f})', fontsize=9, verticalalignment='bottom')
    plt.text(max_rms_index_right, max_rms_right, f'({max_rms_index_right}, {max_rms_right:.4f})', fontsize=9, verticalalignment='bottom')

    plt.legend()

# Define file paths and frequency ranges
file_paths = ["PP00/PP00_6kg.txt", "PP00/PP00_8kg.txt", "PP00/PP00_10kg.txt"]
frequency_ranges = [(4000, 7200), (11880, 15800), (4300, 5500)]

# Create a figure for subplots
plt.figure(figsize=(12, 18))

# Process and plot each file
for i, (file_path, freq_range) in enumerate(zip(file_paths, frequency_ranges)):
    process_and_plot(file_path, freq_range[0], freq_range[1], i + 1)

# Show the plots
plt.tight_layout()
plt.show()
