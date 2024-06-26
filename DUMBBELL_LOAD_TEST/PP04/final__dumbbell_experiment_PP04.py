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

def process_and_plot(file_path, start_freq, end_freq, MVC_values):
    # Load the data from the file
    data = np.loadtxt(file_path)

    # Extract the relevant columns (5th to 8th) for the specified frequency range
    frequency = data[:, 0]
    relevant_data = data[(frequency >= start_freq) & (frequency <= end_freq), 4:8]

    print(relevant_data)

    # Transform values to millivolt
    transformed_data = transform_mV(relevant_data)

    # Check for any invalid values
    if np.any(np.isnan(transformed_data)) or np.any(np.isinf(transformed_data)):
        print(f"Invalid values found in transformed data for {file_path}")
        return None, None, None, None

    cutoff = 10  # Define the cutoff frequency
    fs = 1000   # Define the sampling frequency
    order = 4   # Define the filter order

    # Filter ES-T thoracic data and calculate RMS
    filtered_rms_left_thoracic = butter_lowpass_filter((transformed_data[:, 0])**2, cutoff, fs, order)
    filtered_rms_right_thoracic = butter_lowpass_filter((transformed_data[:, 2])**2, cutoff, fs, order)
    filtered_rms_left_thoracic = np.sqrt(np.abs(filtered_rms_left_thoracic))
    filtered_rms_right_thoracic = np.sqrt(np.abs(filtered_rms_right_thoracic))

    # Filter ES-T lumbar data and calculate RMS
    filtered_rms_left_lumbar = butter_lowpass_filter((transformed_data[:, 1])**2, cutoff, fs, order)
    filtered_rms_right_lumbar = butter_lowpass_filter((transformed_data[:, 3])**2, cutoff, fs, order)
    filtered_rms_left_lumbar = np.sqrt(np.abs(filtered_rms_left_lumbar))
    filtered_rms_right_lumbar = np.sqrt(np.abs(filtered_rms_right_lumbar))

    # Calculate the average of the maximum and minimum RMS values for thoracic and lumbar regions
    avg_rms_left_thoracic = (np.max(filtered_rms_left_thoracic) + np.min(filtered_rms_left_thoracic)) / 2
    avg_rms_right_thoracic = (np.max(filtered_rms_right_thoracic) + np.min(filtered_rms_right_thoracic)) / 2
    avg_rms_left_lumbar = (np.max(filtered_rms_left_lumbar) + np.min(filtered_rms_left_lumbar)) / 2
    avg_rms_right_lumbar = (np.max(filtered_rms_right_lumbar) + np.min(filtered_rms_right_lumbar)) / 2

    # Normalize the RMS values using the provided MVC values
    normalized_rms_left_thoracic = avg_rms_left_thoracic / MVC_values[0]
    normalized_rms_right_thoracic = avg_rms_right_thoracic / MVC_values[1]
    normalized_rms_left_lumbar = avg_rms_left_lumbar / MVC_values[2]
    normalized_rms_right_lumbar = avg_rms_right_lumbar / MVC_values[3]

    # Check for any invalid values after normalization
    if np.any(np.isnan([normalized_rms_left_thoracic, normalized_rms_right_thoracic, normalized_rms_left_lumbar, normalized_rms_right_lumbar])) or np.any(np.isinf([normalized_rms_left_thoracic, normalized_rms_right_thoracic, normalized_rms_left_lumbar, normalized_rms_right_lumbar])):
        print(f"Invalid values found in normalized data for {file_path}")
        return None, None, None, None

    # Return the normalized values for plotting
    return normalized_rms_left_thoracic, normalized_rms_right_thoracic, normalized_rms_left_lumbar, normalized_rms_right_lumbar

# Define file paths and frequency ranges
file_paths = ["DUMBBELL_LOAD_TEST/PP04/PP04_6kg.txt", "DUMBBELL_LOAD_TEST/PP04/PP04_8kg.txt", "DUMBBELL_LOAD_TEST/PP04/PP04_10kg.txt"]
frequency_ranges = [(1500, 3200), (12000, 13100), (14400, 15500)]
MVC_values = [0.1507, 0.1171, 0.3325, 0.1404]
loads = [6, 8, 10]

# Collect normalized values for each load
normalized_values_thoracic_left = []
normalized_values_thoracic_right = []
normalized_values_lumbar_left = []
normalized_values_lumbar_right = []

# Process each file and collect the normalized values
for file_path, freq_range in zip(file_paths, frequency_ranges):
    normalized_rms_left_thoracic, normalized_rms_right_thoracic, normalized_rms_left_lumbar, normalized_rms_right_lumbar = process_and_plot(file_path, freq_range[0], freq_range[1], MVC_values)
    if normalized_rms_left_thoracic is not None:
        normalized_values_thoracic_left.append(normalized_rms_left_thoracic)
        normalized_values_thoracic_right.append(normalized_rms_right_thoracic)
        normalized_values_lumbar_left.append(normalized_rms_left_lumbar)
        normalized_values_lumbar_right.append(normalized_rms_right_lumbar)

# Collect the data points into arrays
data_points = [loads,normalized_values_thoracic_left,normalized_values_thoracic_right,normalized_values_lumbar_left,normalized_values_lumbar_right]

# Print the collected data points
print("Collected Data Points:")
print(data_points)

# Plot the normalized RMS values against the loads
plt.figure(figsize=(12, 8))

plt.plot(normalized_values_thoracic_left, loads, 'bo-', label='Normalized Thoracic ES-T Left')
plt.plot(normalized_values_thoracic_right, loads, 'go-', label='Normalized Thoracic ES-T Right')
plt.plot(normalized_values_lumbar_left, loads,  'ro-', label='Normalized Lumbar ES-T Left')
plt.plot(normalized_values_lumbar_right, loads,  'mo-', label='Normalized Lumbar ES-T Right')

plt.ylabel('Load (kg)')
plt.xlabel('Normalized EMG (mV/mV)')
plt.title('Load against Normalized EMG')
plt.legend()
plt.grid(True)
plt.show()
