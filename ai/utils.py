import numpy as np
import csv

def read_csv(file_path):
    columnNames = None
    matrix = []
    with open(file_path, 'rt') as file:
        reader = csv.reader(file, delimiter=',', quotechar='\\')
        for row in reader:
            matrix.append(np.array(row).astype(float))

    array = np.array(matrix)
    return array, columnNames

def addRows(rowList, file_path):
    with open(file_path, 'wt') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        for row in rowList:
            writer.writerow(row)