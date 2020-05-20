from __future__ import division, print_function
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory
from itertools import cycle

from qtpy import QtCore
from sklearn.preprocessing import LabelEncoder
import os
import numpy as np
import re
import fileinput
import string
import csv
import distance
import glob
from sklearn import preprocessing
import pandas as pd
from matplotlib import style

style.use('ggplot')



#extract wanted gene from chromosome file
def searcher(start, end, inFile, OFile, path, name):
    try:
        flag = 0
        with open(inFile) as f1:
            with open(OFile, 'w+') as f2:
                lines = f1.readlines()
                for i, line in enumerate(lines):
                    if line.__contains__(start):
                        flag = 1
                    if (flag == 1):
                        f2.write(lines[i])
                        i + 1
                        if (line.__contains__(end)):
                            break
        removing(OFile, path, name)
        os.remove(OFile)
        os.remove(inFile)

    except FileNotFoundError:
        print("Wrong file or file path.")

#Removes all spaces and numbers only keeps the letters
def removing(file, path, name):
    for line in fileinput.input(file, inplace=True):
        print(re.sub("\d+", "", line))
    f = open(file)
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', '').replace(' ', '')
    f = open(path + "\ " + name + ".txt", 'w+')
    # print("f= ",f)
    f.write(new_contents)
    for line in fileinput.input(f, inplace=True):
        print(line.translate(string.digits))
    f.close()
    file = path + "\Stripped " + name + ".txt"


def string_to_array(my_string):
    my_string = my_string.lower()
    my_string = re.sub('[^acgt]', 'z', my_string)
    my_array = np.array(list(my_string))
    return my_array


def remove_newlines(fname):
    flist = open(fname).readlines()
    return [s.rstrip('\n') for s in flist]


def ordinal_encoder(my_array):
    integer_encoded = label_encoder.transform(my_array)
    float_encoded = integer_encoded.astype(float)
    float_encoded[float_encoded == 0] = 0.25  # A
    float_encoded[float_encoded == 1] = 0.50  # C
    float_encoded[float_encoded == 2] = 0.75  # G
    float_encoded[float_encoded == 3] = 1.00  # T
    float_encoded[float_encoded == 4] = 0.00  # anything else, z
    return float_encoded


def next_path(path_pattern):
    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2  # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)

    return path_pattern % b


def divider(file_obj, path, name):
    with open(file_obj, 'r') as file:
        data = file.read()
    string = data
    n = 3
    out = [(string[i:i + n]) for i in range(0, len(string), n)]
    out = str(out).replace('[', '').replace(']', '').replace(',', '').replace("'", '').replace("n", "").replace("\\",
                                                                                                                '')

    # print("Function func")
    with open(path + "\Grouped " + name + ".txt", 'w') as w:
        w.write(str(out))
        w.close()


def readFiles():
    files = []
    for i in os.listdir(r"E:\Users\user\PycharmProjects\untitled1\venv/"):
        if i.endswith('.txt'):
            files.append(open(i))
            f = open(i, 'w')
            print(i)
            f.close()


def hamming_distance(file1, file2):
    # Start with a distance of zero, and count up
    distance = 0
    f = open(file1)
    seq1 = f.readlines()
    f.close()
    f = open(file2)
    seq2 = f.readlines()
    f.close()
    # Loop over the indices of the string
    L = len(seq1)
    for i in range(L):
        # Add 1 to the distance if these two characters are not equal
        if seq1[i] != seq2[i]:
            distance += 1
    # Return the final count of differences
    return distance


def oneHotEncoding():
    with open('GeneGrouped.txt', 'r') as myfile: data = myfile.read().replace('\n', '')
    np.savetxt("array.txt", ordinal_encoder(string_to_array(data)), fmt="%s")
    f = open('array.txt')
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', ' , ')
    f = open('array.txt', 'w')
    f.write(new_contents)
    f.close()
    txtToCsv("array.txt")
    
    
def txtToCsv(file):
    with open(file, 'r') as infile, open("testing.csv", 'w+') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)


def person(path):
    searcher('25870501', '26181121', path + r"\chr21.gb", path + r"\result.txt", path, "app")  # APP
    searcher('44895781', '44919421', path + r"\chr19.gb", path + r"\result.txt", path, "apoe")  # APOE
    searcher('73126441', '73233721', path + r"\chr14.gb", path + r"\result.txt", path, "ps1")  # PSEN1
    searcher('226860541', '226913821', path + r"\chr1.gb", path + r"\result.txt", path, "ps2")  # PSEN2
    toCsv(path)


def toCsv(path):
    try:
        for filename in os.listdir(path):
            # print (filename)
            if filename.endswith(".txt"):
                # print(path + "\\" + filename)
                with open(path + "\\" + filename, 'r') as file:
                    # print("gwa el with")
                    file_obj = open(path + "\\" + "new" + filename, 'w+')
                    # print("gwa el with")
                    data = file.read()
                    string = data
                    n = 3
                    out = [(string[i:i + n]) for i in range(0, len(string), n)]
                    out = str(out).replace('[', '').replace(']', '').replace("'", '')
                    file_obj.write(str(out))
                    # print("gwa el with")
                    file_obj.close()
                with open(path + "\\" + "new" + filename, 'r') as in_file:
                    def trim(line):
                        return line.strip()

                    arr = []
                    for line in in_file:
                        arr.append(list(map(trim, line.split(","))))
                    length = len(arr[0])
                    # print(path)
                    with open(path + "\\" + "new" + os.path.splitext(filename)[0] + ".csv", 'w+',
                              newline='') as out_file:
                        writer = csv.writer(out_file)
                        headers = []
                        for i in range(length):
                            headers.append('Codon' + str(i))
                        # if flag==0:
                        writer.writerow(headers)
                        flag = 1
                        writer.writerows(arr)
                # print(os.path.splitext(filename)[0])
                os.remove(path + "\\" + "new" + filename)
                os.remove(path + "\\" + filename)
    except FileNotFoundError:
        print("Wrong file or file path")

        
class admin(Tk):
    def __init__(self):
        super(admin, self).__init__()
        self.title("Alzheimer's Analysis System")
        self.geometry("538x500+682+227")
        self.labelFrame = ttk.LabelFrame(self, text="Please Select Directory")
        self.labelFrame.grid(column=0, row=1, padx=120, pady=60)
        self.button()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text="Select", command=self.fileDialog)
        self.button.grid(column=1, row=1)

    def fileDialog(self):
        self.filename = askdirectory()
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        way = self.filename
        filter(way)

person(r"C:\Users\user\Desktop\Test") #Whole Genome Preprocessing

############### SNPS Preprocessing ################
# root = admin()
# root.mainloop()
