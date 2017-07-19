import csv

inflielist = ['data.csv']
outflielist = ['dataProcessed.csv']

for i in range(len(inflielist)):
    with open(inflielist[i], 'rb') as infile, open(outflielist[i], 'wb') as outfile:
        writer = csv.writer(outfile)
        reader = csv.reader(infile, delimiter='\t')
        rows = list(reader)
        for row in rows:
            wl = row[12].split('-')
            out = []
            for j in range(len(row)):
                if not j == 12:
                    out = out + [row[j]]
                else:
                    out = out + wl
            writer.writerow(out)
            print(out)


