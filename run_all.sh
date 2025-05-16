import matplotlib.pyplot as plt

frequencies = [200, 400, 600, 800, 1000]
latencies = [0.5, 0.4, 0.35, 0.3, 0.25] # can be replaced by your actual measured latencies

plt.plot(frequencies, latencies, marker='o')
plt.title('CPU Frequency vs Latency')
plt.xlabel('CPU Frequency (MHz)')
plt.ylabel('Latency (seconds)')
plt.grid()
plt.show()
