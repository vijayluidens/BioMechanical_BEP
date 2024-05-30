import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Weight in kilograms
loads = [6,8,10]

# Normalized data point of each participant: T-L, T-R, L-L, L-R
data_pp00_TL = [0.21333903380098804, 0.26593544679594794, 0.2659808540953603]
data_pp00_TR = [0.23551494851468313, 0.261556607384162, 0.22961731147233577]
data_pp00_LL = [0.21901000822690855, 0.27465000795596134, 0.2676357312443546]
data_pp00_LR = [0.2246945408714792, 0.23187571723597222, 0.2706794741320111]

# Mean values of thoracic and lumbar region: PP00
mean_pp00_thoracic = [(x + y) / 2 for x, y in zip(data_pp00_TL, data_pp00_TR)]
mean_pp00_lumbar = [(x + y) / 2 for x, y in zip(data_pp00_LL, data_pp00_LR)]

# Given data points
data_pp03_TL = [0.10177419830901005, 0.091521716550284]
data_pp03_TR = [0.08106633583443414, 0.12440700761938041]
data_pp03_LL = [0.08315429345883311, 0.08762104669074129]
data_pp03_LR = [0.12715909096481537, 0.14192482103740792]

# Interpolate for each pair of data points at 8 kg
interpolated_values = {}

# Interpolate for data_pp03_TL
interpolated_values['TL'] = np.interp(8, [6, 10], data_pp03_TL)

# Interpolate for data_pp03_TR
interpolated_values['TR'] = np.interp(8, [6, 10], data_pp03_TR)

# Interpolate for data_pp03_LL
interpolated_values['LL'] = np.interp(8, [6, 10], data_pp03_LL)

# Interpolate for data_pp03_LR
interpolated_values['LR'] = np.interp(8, [6, 10], data_pp03_LR)

# Create lists with interpolated values included: PP03
data_pp03_TL_big = [data_pp03_TL[0], interpolated_values['TL'], data_pp03_TL[1]]
data_pp03_TR_big = [data_pp03_TR[0], interpolated_values['TR'], data_pp03_TR[1]]
data_pp03_LL_big = [data_pp03_LL[0], interpolated_values['LL'], data_pp03_LL[1]]
data_pp03_LR_big = [data_pp03_LR[0], interpolated_values['LR'], data_pp03_LR[1]]

# Mean values of thoracic and lumbar region: PP03
mean_pp03_thoracic = [(x + y) / 2 for x, y in zip(data_pp03_TL_big, data_pp03_TR_big)]
mean_pp03_lumbar = [(x + y) / 2 for x, y in zip(data_pp03_LL_big, data_pp03_LR_big)]

# PP04 Data
data_pp04_TL = [0.112263287856807, 0.10128526758809676, 0.09563060116409758]
data_pp04_TR = [0.10776309075431048, 0.12979179481336825, 0.12401269447869485]
data_pp04_LL = [0.09748086906121536, 0.11885247478930842, 0.11527589034165936]
data_pp04_LR = [0.09627550088698694, 0.11245900544323154, 0.08409940845778568]

# Mean values of thoracic and lumbar region: PP03
mean_pp04_thoracic = [(x + y) / 2 for x, y in zip(data_pp04_TL, data_pp04_TR)]
mean_pp04_lumbar = [(x + y) / 2 for x, y in zip(data_pp04_LL, data_pp04_LR)]


#PP05 Data
data_pp05_TL = [0.0903991218702938, 0.08955267810005192, 0.09251656132732143]
data_pp05_TR = [0.10819033128151205, 0.12967595234933912, 0.13525258151258152]
data_pp05_LL = [0.09775345481123927, 0.07813742828682649, 0.09228231977830557]
data_pp05_LR = [0.09429585987062919, 0.10224945681136031, 0.09237418466063049]

mean_pp05_thoracic = [(x + y) / 2 for x, y in zip(data_pp05_TL, data_pp05_TR)]; print(mean_pp05_thoracic)
mean_pp05_lumbar = [(x + y) / 2 for x, y in zip(data_pp05_LL, data_pp05_LR)]

# Plotting
plt.figure(figsize=(10, 6))

# # Plot PP00 data
# plt.plot(mean_pp00_thoracic, loads, 'o', label= 'PP00-T')
# plt.plot(mean_pp00_lumbar, loads, 'o', label= 'PP00-L')

# Plot PP03 data
plt.plot(mean_pp03_thoracic, loads, 'o', label= 'PP03-T')
plt.plot(mean_pp03_lumbar, loads, 'o', label= 'PP03-L')


# Plot PP04 data
plt.plot(mean_pp04_thoracic, loads, 'o', label= 'PP04-T')
plt.plot(mean_pp04_lumbar, loads, 'o', label= 'PP04-L')


# Plot PP05 data
plt.plot(mean_pp05_thoracic, loads, 'o', label= 'PP05-T')
plt.plot(mean_pp05_lumbar, loads, 'o', label= 'PP05-L')


plt.xlabel('Normalized EMG Data (mV/mV)')
plt.ylabel('Loads (kg)')
plt.title('Normalized EMG Data vs Loads')
plt.legend()
plt.grid(False)
plt.show()

# Plotting thoracic mean data
plt.figure(figsize=(10, 6))
# plt.plot(mean_pp00_thoracic, loads, 'o-', label='PP00 Thoracic')
plt.plot(mean_pp03_thoracic, loads, 'o-', label='PP03 Thoracic')
plt.plot(mean_pp04_thoracic, loads, 'o-', label='PP04 Thoracic')
plt.plot(mean_pp05_thoracic, loads, 'o-', label='PP05 Thoracic')

# Plotting lumbar mean data
# plt.plot(mean_pp00_lumbar, loads, 'x-', label='PP00 Lumbar')
plt.plot(mean_pp03_lumbar, loads, 'x-', label='PP03 Lumbar')
plt.plot(mean_pp04_lumbar, loads, 'x-', label='PP04 Lumbar')
plt.plot(mean_pp05_lumbar, loads, 'x-', label='PP05 Lumbar')

plt.xlabel('Mean EMG Data (mV/mV)')
plt.ylabel('Loads (kg)')
plt.title('Loads vs. Mean EMG Data')
plt.legend()
plt.grid(True)
plt.show()

# # Concatenate mean thoracic values from all participants
# all_mean_thoracic = np.concatenate([mean_pp03_thoracic, mean_pp04_thoracic, mean_pp05_thoracic])

# # Concatenate mean lumbar values from all participants
# all_mean_lumbar = np.concatenate([mean_pp03_lumbar, mean_pp04_lumbar, mean_pp05_lumbar])

# # Concatenate loads corresponding to the mean thoracic and lumbar values
# all_loads = np.repeat(loads, 3)

# # Perform linear regression on the concatenated thoracic data
# slope_thoracic, intercept_thoracic, r_value_thoracic, p_value_thoracic, std_err_thoracic = linregress(all_loads, all_mean_thoracic)

# # Perform linear regression on the concatenated lumbar data
# slope_lumbar, intercept_lumbar, r_value_lumbar, p_value_lumbar, std_err_lumbar = linregress(all_loads, all_mean_lumbar)

# # Plotting mean thoracic and lumbar data and linear regression lines
# plt.figure(figsize=(10, 6))

# # Plot mean thoracic data and linear regression line
# plt.plot(all_loads, all_mean_thoracic, 'o', label='Mean Thoracic Data')
# plt.plot(loads, slope_thoracic * np.array(loads) + intercept_thoracic, label=f'Thoracic Linear Regression (R-squared = {r_value_thoracic**2:.2f})')

# # Plot mean lumbar data and linear regression line
# plt.plot(all_loads, all_mean_lumbar, 'o', label='Mean Lumbar Data')
# plt.plot(loads, slope_lumbar * np.array(loads) + intercept_lumbar, label=f'Lumbar Linear Regression (R-squared = {r_value_lumbar**2:.2f})')

# plt.xlabel('Loads (kg)')
# plt.ylabel('Mean EMG Data (mV/mV)')
# plt.title('Mean Thoracic and Lumbar EMG Data vs Loads with Linear Regression')
# plt.legend()
# plt.grid(True)
# plt.show()

# Combine data for all participants
combined_thoracic_means = [x * 100 for x in (mean_pp03_thoracic + mean_pp04_thoracic + mean_pp05_thoracic)]
combined_lumbar_means = [x * 100 for x in (mean_pp03_lumbar + mean_pp04_lumbar + mean_pp05_lumbar)]
combined_loads = loads * 3  # As we have three participants, each with the same load set

# Step 2: Visualize the data
plt.figure(figsize=(10, 6))
plt.scatter(combined_thoracic_means, combined_loads, label='Thoracic Means')
plt.scatter(combined_lumbar_means, combined_loads, label='Lumbar Means', color='red')
plt.xlabel('Mean EMG Data (%)')
plt.ylabel('Loads (kg)')
plt.title('Mean EMG Data vs. Load')
plt.legend()
plt.grid(True)
plt.show()

# Step 3: Perform linear regression for EMG data vs Loads

# Thoracic data regression
slope_thoracic, intercept_thoracic, r_value_thoracic, p_value_thoracic, std_err_thoracic = linregress(combined_thoracic_means, combined_loads)

# Lumbar data regression
slope_lumbar, intercept_lumbar, r_value_lumbar, p_value_lumbar, std_err_lumbar = linregress(combined_lumbar_means, combined_loads)

# Calculate regression lines
regression_line_thoracic = [slope_thoracic * x + intercept_thoracic for x in combined_thoracic_means]
regression_line_lumbar = [slope_lumbar * x + intercept_lumbar for x in combined_lumbar_means]

# Plot EMG data vs. Loads with regression lines
plt.figure(figsize=(10, 6))
plt.scatter(combined_thoracic_means, combined_loads, label='Thoracic Means', color='blue')
plt.plot(combined_thoracic_means, regression_line_thoracic, color='blue', linestyle='dashed', label=f'Thoracic Fit: y={slope_thoracic:.2f}x+{intercept_thoracic:.2f}')
plt.scatter(combined_lumbar_means, combined_loads, label='Lumbar Means', color='red')
plt.plot(combined_lumbar_means, regression_line_lumbar, color='red', linestyle='dashed', label=f'Lumbar Fit: y={slope_lumbar:.2f}x+{intercept_lumbar:.2f}')
plt.xlabel('Normalized Mean EMG Data (%)')
plt.ylabel('Loads (kg)')
plt.title('Load vs. Normalized Mean EMG Data')
plt.legend()
plt.grid(True)
plt.show()

# Print regression statistics
print(f"Thoracic Linear Regression:\n Slope: {slope_thoracic}\n Intercept: {intercept_thoracic}\n R-squared: {r_value_thoracic**2}\n P-value: {p_value_thoracic}")
print(f"Lumbar Linear Regression:\n Slope: {slope_lumbar}\n Intercept: {intercept_lumbar}\n R-squared: {r_value_lumbar**2}\n P-value: {p_value_lumbar}")