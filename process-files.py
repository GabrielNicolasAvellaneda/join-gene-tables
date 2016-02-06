import sys
import csv
from decimal import Decimal 

def showUsage():
	print('Usage: python process-file.py <master_file> <detail_file> <output_file> [threshold]')

def checkArgs():
	if (len(sys.argv) < 4):
		showUsage()		
		sys.exit(1)

def generate_dict(detail_reader, detail_id_column):
	result = dict()
	for row in detail_reader:
		if (len(row) > 0):
			related_row_id = row[detail_id_column].strip().lower()
			result[related_row_id] = row

	return result

def main():
	try:
		checkArgs()	
		master_file = sys.argv[1]
		detail_file = sys.argv[2]
		output_file = sys.argv[3]
		threshold = None
		if (len(sys.argv) > 4):
			threshold = Decimal(sys.argv[4])

		print('Reading from Master file: ' + master_file)
		print('Reading from Details file: ' + detail_file)
		print('Writing to file: ' + output_file)
		print('Using threshold: ' + str(threshold))

		csv_master = open(master_file) 
		csv_detail = open(detail_file)
		csv_output = open(output_file, 'wb')

		master_reader = csv.reader(csv_master, delimiter=',')
		detail_reader = csv.reader(csv_detail, delimiter='\t')
		output_writer = csv.writer(csv_output, delimiter=',')

		# Skip headers
		master_headers = next(master_reader)
		detail_headers = next(detail_reader)
		# Write output headers
		output_writer.writerow(master_headers + detail_headers)

		master_id_column = 1
		detail_id_column = 0

		detail_dict = generate_dict(detail_reader, detail_id_column)

		master_threshold_column = 6

		for row in master_reader:
			row_threshold = Decimal(row[master_threshold_column])
			row_id = row[master_id_column].strip().lower()
			if (threshold == None) or (row_threshold > threshold):
				related = detail_dict[row_id]
				row_output = row + related
				output_writer.writerow(row_output)

	except (IOError, KeyError) as e:
		print(e)
		sys.exit(1)


if __name__ == "__main__":
	main()
