import csv

raw = []
obama = []
others = [] # others 由raw的3000行和obama的3000行组合而成

with open("obama.csv", "r", encoding="utf-8") as obamafile:
    reader = csv.reader(obamafile)
    for i in reader:
        obama.append(i)

with open("training.1600000.processed.noemoticon.csv", "r", encoding="utf-8") as rawfile:
    reader = csv.reader(rawfile)
    count = 6000
    for i in reader:
        raw.append(i)
        count -= 1
        if count <= 0:
            break



for i in range(6000):
    others.append(raw[i])
    if i % 3 != 1:
        others[i][5] = obama[i][5]
    if i == 2037:
        others[i][5] = obama[i][5]


with open("others.csv","w",newline="",encoding="utf-8") as othersfile:
    csvwriter = csv.writer(othersfile, dialect=("excel"))
    for i in raw:
        csvwriter.writerow(i)