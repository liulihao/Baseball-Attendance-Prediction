# Date: transform date formate to YYYY-MM-dd
# Weekend: check weekday/weekend
# Promotion: for combining with promotion data, create value 0 first
# Substract information for predictive analytics
import csv
from datetime import datetime

inflielist = ['data.csv']
outflielist = ['dataProcessed.csv']
date = ''
weekend = 0

for i in range(len(inflielist)):
	with open(inflielist[i], 'rb') as infile, open(outflielist[i], 'wb') as outfile:
		writer = csv.writer(outfile)
		reader = csv.reader(infile, delimiter=',')
		rows = list(reader)

		# write header (can only concatenate list (not "string") to list, so need to transform to [list])
		writer.writerow(['Date'] + ['Weekend'] + ['Promotion'] + [rows[0][1]] + [rows[0][4]] + [rows[0][6]] + [rows[0][11]] + [rows[0][12]] + [rows[0][13]] + [rows[0][18]] + [rows[0][19]] + [rows[0][20]])
		
		# write data
		for row in rows[1:]:

			# transform date format
			text = row[2].split(' ')
			date = text[1] +' '+ text[2]
			date = str(i + 2011) + ' ' + date
			date = datetime.strptime(date, '%Y %b %d').strftime('%Y-%-m-%-d')

			# define weekday or weekend
			if (text[0] == 'Saturday') | (text[0] == 'Sunday'):
				weekend = 1
			else:
				weekend = 0
			
			if (row[5] != '@'):
				# can only concatenate list (not "int" or "string") to list, so need to transform to [list]
				writer.writerow([date] + [weekend] + [0] + [row[1]] + [row[4]] + [row[6]] + [row[11]] + [row[12]] + [row[13]] + [row[18]] + [row[19]] + [row[20]])