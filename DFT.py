from turtle import color
import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

SAMPLE_RATE = 44100

# variables:
# ----------------------------
# t = time in samples (from 0 to T-1)
# T = total number of samples
# f(t) = amplitude of wave at time t
# n = harmonic number 
# x = input wave
# x[k] = sample at time k

def f_t (t, x, T, h_count):
	return sum(((a_n(x, n, T) * np.cos(2*np.pi*n*t/T)) + (b_n(x, n, T) * np.sin(2*math.pi*n*t/T))) for n in range(h_count)) + a_0(x, T)

# this will calculate a_n
def a_n (x, n, T):
	return 2/T * sum(x[k] * np.cos(2*math.pi*n*k/T) for k in range(T))

# this will calculate b_n
def b_n (x, n, T):
	return 2/T * sum(x[k] * np.sin(2*math.pi*n*k/T) for k in range(T))

# this will calculate a_0
def a_0 (x, T):
	return 1/T * sum(x[k] for k in range(T))

# this will calculate the amplitude of the nth harmonic
def amplitude_n (x, n, T):
	return np.sqrt(a_n(x, n, T)**2 + b_n(x, n, T)**2)

# this will calculate the phase of the nth harmonic
def phase_n (x, n, T):
	return np.arctan(b_n(x, n, T)/a_n(x, n, T))

# calculates the amplitude of the harmonics for all harmonics
def calculate_harmonics (input, h_count):
	return [amplitude_n(input, n, len(input)) for n in range(h_count)]

# calculates the phase of the harmonics for all harmonics
def calculate_phases (input, h_count):
	return [phase_n(input, n, len(input)) for n in range(h_count)]

# plots original wave
def plot_wave (wave):
	plt.title("Input Waveform")
	plt.xlabel("Time (samples)")
	plt.ylabel("Amplitude")
	plt.plot(wave)
	plt.show()

# function to plot original wave, amplitude of harmonics, and phase of harmonics in one figure
def plot_graph (h_count, harmonics, phases, wave, file_path):
	# plot original wave
	plt.subplot()
	plt.title("Input Waveform")
	plt.xlabel("Time (samples)")
	plt.ylabel("Amplitude")
	plt.plot(wave)
	plt.show()
	fig, ax1 = plt.subplots()
	fig.suptitle(f"Harmonics of Input Waveform (n = {h_count})")
	ax1.set_xlabel("Harmonic #")
	ax1.set_ylabel("Amplitude")
	ax1.bar(range(h_count), harmonics, 0.9, color = "royalblue")
	ax2 = ax1.twinx()
	ax2.set_ylabel("Phase (radians)")
	ax2.bar(range(h_count), phases, 0.125, color = (0.5, 0.5, 0.5, 0.5))
	plt.show()

# saves the harmonics and phases to a file titled {filename}_{harmonic count}_harmonics.txt into 'out' folder
def save_to_file (h_count, harmonics, phases, file_path):
	with open(f"out/{getname(file_path)}_{h_count}_harmonics.txt", 'w') as f:
		for n in range(h_count):
			f.write(f"{harmonics[n]}\t{phases[n]}\n")

# get the name of the file for saving
def getname (file_path):
	return file_path.split("/")[-1].split(".")[0]

# reconstruct the wave by creating sine waves with the harmonics and phases and adding them together
def reconstruct_wave (h_count, harmonics, phases, T):
	wave = [0 for i in range(T)]
	for n in range(h_count):
		for t in range(T):
			wave[t] += harmonics[n] * np.sin(2*math.pi*n*t/T + phases[n])
	return wave


# ================================ = ================================ = ================================
# main function
def main ():
	print("\nDiscrete Fourier Transform Tool\n--------------------------------\nThis program will take an input wave plot it's harmonics and reconstruct the wave from the harmonics.")
	print(f"Sample rate: {SAMPLE_RATE}Hz")
	# read in the file
	file_path = filedialog.askopenfilename(initialdir = "./samples/", title = "Select a text file.", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
	# read in file
	with open(file_path, 'r') as f:
		samples = [float(line) for line in f]

	print(f"File selected: {file_path}\nNumber of samples: {len(samples)}\nLength in milliseconds: {(len(samples)/SAMPLE_RATE * 1000):.3f}ms")

	# input check loop
	while True:
		try:
			harmonic_count = int(input(f"Enter the number of harmonics ({int(len(samples)/2)} max): "))
			if harmonic_count > len(samples)/2:
				print(f"Error: Harmonic count must be {int(len(samples)/2)} or less.")
				continue
			break
		except ValueError:
			print("Error: Harmonic count must be a positive integer.")
			continue

	harmonics = calculate_harmonics(samples, harmonic_count)
	phases = calculate_phases(samples, harmonic_count)
	plot_graph(harmonic_count, harmonics, phases, samples, file_path)

	reconstructed_wave = reconstruct_wave(harmonic_count, harmonics, phases, len(samples))
	plot_wave(reconstructed_wave)

	# save harmonics to file
	while True:
		save = input("Save to file? (y/n): ")
		if save == "y":
			save_to_file(harmonic_count, harmonics, phases, file_path)
			break
		elif save == "n": break
		else:
			print("Error: Invalid input.")
			continue

if __name__ == '__main__':
	main()
	