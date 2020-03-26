import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

all_x_points = []

with open("2011close.csv", "r", newline='') as datafile:
	csvreader = csv.reader(datafile, delimiter=',')
	prices = []
	index = 0

	for row in csvreader:

		if row[0] == "a":
			for item in row:
				prices.append([])
			continue

		for i in range(len(row)):
			if len(row[i]) > 0:
				prices[i].append(float(row[i]))


		index = index + 1


usable_prices = []

for row in prices:
	if len(row) == 251 and row[0] < 1000:
		usable_prices.append(row)
		all_x_points.append([i for i in range(1, 252)])

print(len(usable_prices))

plt.figure(figsize=(12, 12))

n_samples = 73
random_state = 170
X, y = make_blobs(n_samples=n_samples, random_state=random_state)

# print(X.shape)
# print(y)

# Incorrect number of clusters
y_pred = KMeans(n_clusters=5, random_state=random_state).fit_predict(usable_prices)
y_pred_adj = []
for i in y_pred:
	temp_array = []
	for c in range(251):
		temp_array.append(i)
	y_pred_adj.append(temp_array)

print(y_pred)

plt.subplot(221)
plt.scatter(all_x_points, usable_prices, c=y_pred_adj)

plt.title("Stocks with 251 close prices in 2011")

plt.show()