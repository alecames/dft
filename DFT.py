import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

SAMPLE_RATE = 44100

# a) To convert samples x[k] to harmonics... 
# f(t) 
def f_t (t, x, T, n):
	return sum(a_n(x, n, T) * np.cos(2*np.pi*n*t/T) + b_n(x, n, T) * np.sin(2*math.pi*n*t/T) for n in range(int(T/2)) ) + a_0(x, T)

# a_n
def a_n (x, n, T):
	return 2/T * sum(x[k] * np.cos(2*math.pi*n*k/T) for k in range(T))

# b_n
def b_n (x, n, T):
	return 2/T * sum(x[k] * np.sin(2*math.pi*n*k/T) for k in range(T))

# a_0
def a_0 (x, T):
	return 1/T * sum(x[k] for k in range(T))

# # b) To reconstruct wave from the harmonics...
# def reconstruct(x, T, n):
# 	return sum(a_n(x, n, T) * np.cos(2*np.pi*n*t/T) + b_n(x, n, T) * np.sin(2*np.pi*n*t/T) for t in range(T))

def main ():
	print("\nDiscrete Fourier Transform Tool\n--------------------------------\nThis program will take an input wave plot it's harmonics and reconstruct the wave from the harmonics.\n")
	print(f"Sample rate: {SAMPLE_RATE}Hz")
	# set path of filedialog to current directory
	file_path = filedialog.askopenfilename(initialdir = "./samples/", title = "Select a text file.", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
	# read in file
	with open(file_path, 'r') as f:
		samples = [float(line) for line in f]

	# valid input for harmonic count
	while True:
		try:
			harm_count = int(input("Enter harmonic count: "))
			break
		except ValueError:
			print("Invalid input. Please enter an integer.")

	
	# get time domain
	t = np.linspace(0, len(samples)/SAMPLE_RATE, len(samples))
	t = 5

	# get harmonics
	harmonics = [f_t(t, samples, len(samples), n) for n in range(harm_count)]

	plt.xlabel("Harmonic")
	plt.ylabel("Amplitude")
	plt.plot(range(harm_count), harmonics)
	plt.show()

if __name__ == '__main__':
	main()
	