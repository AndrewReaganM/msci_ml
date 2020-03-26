import os

dir = "Dataset/ETFs"
allfiles = os.listdir(dir)

tickerdict = {}

for file in allfiles:
    tickerdict[file.replace('.us.txt', '')] = "NOT IN SECTOR LIST"


with open("companies.csv", "r") as companyfile:
	lines = companyfile.readlines()

	for i in range(len(lines)):
		lines[i] = lines[i].split(",")

	labels = lines[0]

	sectorindex = labels.index('sector\n')

	companysector = {}

	for company in lines[1:]:

		if company[0].lower() in tickerdict.keys():
			tickerdict[company[0].lower()] = company[sectorindex]
			if tickerdict[company[0].lower()] == '\n':
				tickerdict[company[0].lower()] = 'NO SECTOR LISTED'

# print(tickerdict)
for key in tickerdict.keys():
	print(key + " : " + tickerdict[key])


