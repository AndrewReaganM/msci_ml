import csv

with open("correlation2011.csv", "r") as csvfile:
	lines = csvfile.readlines()
	labels = lines[0].split(",")

	strongcorrelations = {}
	for label in labels:
		strongcorrelations[label] = []

	for i in range(1, len(lines)):
		lines[i] = lines[i].split(",")
		for j in range(len(lines[i])):		
			# print(str(i) + " " + str(j))	
			if lines[i][j] != "NA\n" and lines[i][j] != "NA":
				if abs(float(lines[i][j])) > 0.9 and float(lines[i][j]) < 1.0:
					strongcorrelations[labels[i-1]].append(labels[j])



with open("companies.csv", "r") as companyfile:
	lines = companyfile.readlines()

	for i in range(len(lines)):
		lines[i] = lines[i].split(",")

	labels = lines[0]

	sectorindex = labels.index('sector\n')

	companysector = {}

	for company in lines[1:]:

		if sectorindex < len(company):
			companysector[company[0].lower()] = company[sectorindex].replace('\n','')
		else:
			companysector[company[0].lower()] = company[0].lower()

		if companysector[company[0].lower()] == '\n':
			companysector[company[0].lower()] = 'NA'



sectorcorrelations = {}

# print(companysector)

for key in strongcorrelations.keys():
	sectorcorrelations[key] = [] 

	for ticker in strongcorrelations[key]:
		if ticker.lower() in companysector.keys():
			sectorcorrelations[key].append(companysector[ticker.lower()])

for key in sectorcorrelations.keys():
	print(key + " : ", end="")
	print(sectorcorrelations[key], end="\n\n")



	


	