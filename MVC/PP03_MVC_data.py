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

# Load the data from the file
data = np.loadtxt("MVC/PP03_MVC.txt")

# Define the frequency range to extract data from
start_freq = 5600
end_freq = 18700

# Extract the relevant columns (5th to 8th) for the specified frequency range
frequency = data[:, 0]  
relevant_data = data[(frequency >= start_freq) & (frequency <= end_freq), 4:8]

# Transform values to millivolt
transformed_data = transform_mV(relevant_data)

cutoff = 10  # Define the cutoff frequency
fs = 1000   # Define the sampling frequency
order = 4   # Define the filter order

# Filter ES-T left and right data and calculate RMS
filtered_rms_left = butter_lowpass_filter((transformed_data[:, 1])**2, cutoff, fs, order)
filtered_rms_right = butter_lowpass_filter((transformed_data[:, 3])**2, cutoff, fs, order)

# Ensure no negative or NaN values
filtered_rms_left[filtered_rms_left < 0] = 0
filtered_rms_left = np.nan_to_num(filtered_rms_left)
filtered_rms_right[filtered_rms_right < 0] = 0
filtered_rms_right = np.nan_to_num(filtered_rms_right)

# Take the square root to get RMS after filtering
filtered_rms_left = np.sqrt(filtered_rms_left)
filtered_rms_right = np.sqrt(filtered_rms_right)

# Calculate the average RMS
average_rms = (filtered_rms_left + filtered_rms_right) / 2

# Find the maximum value of the average RMS and its index
max_avg_rms = np.max(average_rms)
max_avg_rms_index = np.argmax(average_rms)

# Print the maximum value of the average RMS
print(f'Maximum Average RMS: {max_avg_rms:.4f} at index {max_avg_rms_index}')

# Extract the time indices for the selected range for plotting
selected_indices = np.where((frequency >= start_freq) & (frequency <= end_freq))[0]

# Create a time array based on the selected indices
time = np.arange(len(selected_indices))

# Plot the selected data
plt.figure(figsize=(12, 6))
plt.plot(time, transformed_data[:, 1], label='ES-T Left')
plt.plot(time, transformed_data[:, 3], label='ES-T Right')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude (mV)')
plt.title('Erector Spinae Data for Specified Frequency Range')

# Plot filtered RMS of ES-T left and right
plt.plot(time, filtered_rms_left, 'lime', label='Filtered RMS of ES-T Left')
plt.plot(time, filtered_rms_right, 'cyan', label='Filtered RMS of ES-T Right')

# Plot average RMS
plt.plot(time, average_rms, 'purple', label='Average RMS')

# Plot vertical line at max average RMS index
plt.axvline(x=max_avg_rms_index, color='g', linestyle='--', label='Max Avg RMS')

# Plot dot at maximum value of the mean
plt.scatter(max_avg_rms_index, max_avg_rms, color='red', zorder=5)
plt.text(max_avg_rms_index, max_avg_rms, f'({max_avg_rms_index}, {max_avg_rms:.4f})', fontsize=9, verticalalignment='bottom')

plt.legend()
plt.show()
