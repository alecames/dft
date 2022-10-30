import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tqdm.auto import tqdm
import multiprocessing as mp

root = tk.Tk()
root.withdraw()


# Alec Ames
# 6843577

# COSC 4P98
# Assignment 2
# 10/26/2022

# Discrete Fourier Transform Tool
# --------------------------------
# This program will take an input wave plot it's harmonics and reconstruct the wave from the harmonics.
#
# variables:
# ----------------------------------------
# t = time in samples (from 0 to T-1)
# T = total number of samples
# f(t) = amplitude of wave at time t
# n = harmonic number
# x = input wave
# x[k] = sample at time k

SAMPLE_RATE = 44100

# ----------------------------------------
# this will calculate a_n
def a_n(x, n, T):
	return 2/T * sum(x[k] * np.cos(2*math.pi*n*k/T) for k in range(T))

# this will calculate b_n
def b_n(x, n, T):
	return 2/T * sum(x[k] * np.sin(2*math.pi*n*k/T) for k in range(T))

# calculates list of coefficients a_n and b_n
def calc_coeffs(h_count, x, T, pool):
	coeff_a = [0 for i in range(h_count)]
	coeff_b = [0 for i in range(h_count)]
	for n in tqdm(range(h_count), bar_format="{l_bar}{bar:40}{r_bar}"):
		coeff_a[n] = a_n(x, n, T)
		coeff_b[n] = b_n(x, n, T)
	return coeff_a, coeff_b

# this will calculate the amplitude of the nth harmonic
def amplitude_n(coeff_a, coeff_b, h_count):
	return [np.sqrt(coeff_a[n]**2 + coeff_b[n]**2) for n in range(h_count)]

# this will calculate the phase of the nth harmonic
def phase_n(coeff_a, coeff_b, h_count):
	phases = [0 for i in range(h_count)]
	for n in range(h_count):
		if coeff_a[n] != 0:
			phases[n] = np.arctan(coeff_b[n]/coeff_a[n])
	return phases

# plots original wave
def plot_wave(wave, title):
	plt.title(title)
	plt.xlabel("Time (samples)")
	plt.ylabel("Amplitude")
	plt.plot(wave)
	plt.show()

# plots harmonic amplitude and phase for all harmonics over the range of 1 to h_count using matplotlib
def plot_harmonics(h_count, harmonics, phases):
	fig, ax1 = plt.subplots()
	fig.suptitle(f"Harmonics of Input Waveform (n = {h_count})")
	ax1.set_xlabel("Harmonic #")
	ax1.set_ylabel("Amplitude")
	ax1.bar(range(h_count), harmonics, 0.9, color="royalblue", label="Amplitude")
	ax2 = ax1.twinx()
	ax1.set_xticks(range(0, h_count, math.ceil(h_count/20)))
	ax2.set_yticks(np.arange(-math.pi/2, (math.pi/2)+0.01, math.pi/16))
	ax2.set_ylabel("Phase (radians)")
	ax2.bar(range(h_count), phases, 0.125, color=(0.5, 0.5, 0.5, 0.5), label="Phase")
	fig.legend()
	plt.show()

# saves harmonic #, coefficient a_n, coefficient b_n, ampltitude and phase to a tab delimited txt file
def save_harmonics(h_count, coeff_a, coeff_b, harmonics, phases, file_path, ): 
	with open(f"out/{getname(file_path)}_{h_count}_harmonics.txt", "w") as f:
		f.write("Harm. #\tCoeff. a\tCoeff. b\tAmplitude\tPhase\n")
		for n in range(h_count):
			f.write(f"{n}\t{coeff_a[n]:.8f}\t{coeff_b[n]:.8f}\t{harmonics[n]:.8f}\t{phases[n]:.8f}\n")

# saves the reconstructed wave to a file titled {filename}_{harmonic count}_reconstructed.txt into 'out' folder
def save_wave(h_count, wave, file_path):
	with open(f"out/{getname(file_path)}_{h_count}_reconstructed.txt", "w") as f:
		for t in range(len(wave)):
			f.write(f"{wave[t]}\n")

# loads file from .txt 
def load_file(file_path):
	with open(file_path, "r") as f:
		samples = [float(line) for line in f]
	return samples

# get the name of the file for saving
def getname(file_path):
	return file_path.split("/")[-1].split(".")[0]

# reconstruct the wave 
def reconstruct_wave(h_count, harmonics, phases, T):
	wave = [0 for i in range(T)]
	for n in tqdm(range(h_count), bar_format="{l_bar}{bar:40}{r_bar}"):
		for t in range(T):
			wave[t] += harmonics[n] * np.cos(2*math.pi*n*t/T + phases[n])
			# clipping to prevent overflow
			if wave[t] > 1: wave[t] = 1
			elif wave[t] < -1: wave[t] = -1
	return wave

# ================================ = ================================ = ================================
def main():
	pool = mp.Pool(mp.cpu_count())

	print("\nDiscrete Fourier Transform Tool\n-------------------------------\nThis program will take an input wave plot it's harmonics and reconstruct the wave from the harmonics.")
	print(f"Sample rate: {SAMPLE_RATE}Hz")
	# read in the file
	file_path = filedialog.askopenfilename(
		initialdir="./samples/", title="Select a text file.", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
	# read in file
	samples = load_file(file_path)

	# sample info
	T = len(samples)
	x = samples
	a_0 = 1/T * sum(x[k] for k in range(T))

	print(f"File selected: {file_path}\nNumber of samples: {T}\nLength in milliseconds: {(T/SAMPLE_RATE * 1000):.3f}ms")

	# input check loop
	while True:
		try:
			harmonic_count = int(
				input(f"Enter the number of harmonics ({int(T/2)} max): "))
			if harmonic_count > T/2:
				print(f"Error: Harmonic count must be {int(T/2)} or less.")
				continue
			break
		except ValueError:
			print("Error: Harmonic count must be a positive integer.")
			continue
	
	# print info to console
	print("1. Plotting time-amplitude graph of original wave...\n   Close graph to continue to harmonics...")
	plot_wave(x, "Original Wave")

	print("2. Performing Discrete Fourier Transform...")
	coeffs_a, coeffs_b = calc_coeffs(harmonic_count, x, T, pool)
	harmonics = amplitude_n(coeffs_a, coeffs_b, harmonic_count)
	phases = phase_n(coeffs_a, coeffs_b, harmonic_count)

	print(f"3. Plotting graph of {harmonic_count} harmonics...\n   Close graph to continue to reconstruction...")
	plot_harmonics(harmonic_count, harmonics, phases)
	
	print("4. Reconstructing wave...")
	reconstructed_wave = reconstruct_wave(harmonic_count, harmonics, phases, T)
	print("Close graph to save harmonics data to file...")
	plot_wave(reconstructed_wave, "Reconstructed Wave")
	print("------------------------------------------------\n")

	# saves harmonics to file
	while True:
		save = input("Save harmonics to file? (y/n): ")
		if save == "y":
			save_harmonics(harmonic_count, coeffs_a, coeffs_b, harmonics, phases, file_path)
			print(f"Saved harmonics to \".../out/{getname(file_path)}_{harmonic_count}_harmonics.txt\".")
			break
		elif save == "n":
			break
		else:
			print("Error: Invalid input.")
			continue

	# saves reconstructed wave to file
	while True:
		save = input("Save reconstructed wave to file? (y/n): ")
		if save == "y":
			save_wave(harmonic_count, reconstructed_wave, file_path)
			print(f"Saved reconstructed wave to \".../out/{getname(file_path)}_{harmonic_count}_reconstructed.txt\".")
			break
		elif save == "n":
			break
		else:
			print("Error: Invalid input.")
	# 		continue

if __name__ == "__main__":
	main()
