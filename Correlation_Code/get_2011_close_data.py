import csv
import os

def main():
    dir = "Dataset/Stocks"
    allfiles = os.listdir(dir)

    tickerdict = {}

    for file in allfiles:
        tickerdict[file.replace('.us.txt', '')] = []
        with open(dir+"/"+file) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in readcsv:
                if row[0][0:4] == '2011':
                    tickerdict[file.replace('.us.txt', '')].append(row[4])

    largest = -1

    correctdict = {}

    for key in tickerdict.keys():
        if largest < len(tickerdict[key]):
            largest = len(tickerdict[key])
        if len(tickerdict[key]) > 0:
            correctdict[key] = tickerdict[key]

    with open('2011close.csv', 'w', newline = '') as outputcsv:
         csvwriter = csv.writer(outputcsv, delimiter=',')
         csvwriter.writerow(correctdict.keys())

         for i in range(0, largest):
            rowtowrite = []
            for key in correctdict.keys():
                
                if i < len(correctdict[key]):
                    rowtowrite.append(correctdict[key][i])
                else:
                    rowtowrite.append(None)

            csvwriter.writerow(rowtowrite)



if __name__ == '__main__':
    main()