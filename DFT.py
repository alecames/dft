import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

SAMPLE_RATE = 44100

# a) To convert samples x[k] to harmonics... 
# f(t) 
def f_t (t, x, T, n):
	return sum(a_n(x, n, T) * math.cos(2*math.pi*n*t/T) + b_n(x, n, T) * math.sin(2*math.pi*n*t/T) for n in range(int(T/2))) + a_0(x, T)

# a_n
def a_n (x, n, T):
	return 2/T * sum(x[k] * math.cos(2*math.pi*n*k/T) for k in range(T))

# b_n
def b_n (x, n, T):
	return 2/T * sum(x[k] * math.sin(2*math.pi*n*k/T) for k in range(T))

# a_0
def a_0 (x, T):
	return 1/T * sum(x[k] for k in range(T))

# b) To reconstruct wave from the harmonics...
def reconstruct(x, T, n):
	return sum(a_n(x, n, T) * math.cos(2*math.pi*n*t/T) + b_n(x, n, T) * math.sin(2*math.pi*n*t/T) for t in range(T))


if __name__ == '__main__':
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

	# get length of samples
	T = len(samples)

	# get array of time values
	t = np.array([i for i in range(int(T/2))])
	
	# harmonics 
	harmonics = []
	for t in range(T):
		harmonics += [f_t(t, samples, T, n) for n in range(harm_count)]

	# Plot the first 1024 samples
	plt.plot(samples[:1024])
	plt.show()

	plt.plot(harmonics)
	plt.show()