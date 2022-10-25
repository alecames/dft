# discrete fourier transform formula

import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import scipy.io.wavfile as wav
import scipy.fftpack as fft

root = tk.Tk()
root.withdraw()

SAMPLE_RATE = 44100

# load in wav file
def load_wav ():
	file_path = filedialog.askopenfilename(initialdir = "./samples/", title = "Select a text file.", filetypes = (("WAV files", "*.wav"), ("All files", "*.*")))
	# read in file
	sample_rate, samples = wav.read(file_path)
	return samples

# perform discrete fourier transform
def dft (samples):
	# get length of samples
	T = len(samples)
	# get array of harmonics
	harmonics = [sum(samples[k] * np.exp(-2j * np.pi * k * n / T) for k in range(T)) for n in range(T)]
	# get array of frequencies
	freq = np.linspace(0, SAMPLE_RATE, T)
	return freq, harmonics

# plot harmonics as amplitude histogram
def plot_harmonics (freq, harmonics):
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Amplitude")
	plt.plot(freq, np.abs(harmonics))
	plt.show()

def main ():
	print("\nDiscrete Fourier Transform Tool\n--------------------------------\nThis program will take an input wave plot it's harmonics and reconstruct the wave from the harmonics.\n")
	print(f"Sample rate: {SAMPLE_RATE}Hz")
	samples = load_wav()
	freq, harmonics = dft(samples)
	plot_harmonics(freq, harmonics)

if __name__ == "__main__":
	main()
