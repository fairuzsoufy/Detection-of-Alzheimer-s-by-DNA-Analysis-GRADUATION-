from __future__ import division, print_function
import glob
import os
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory
import pandas as pd


def filter(path):
    try:

        x = '0'
        directory = path

        for filename in os.listdir(directory):
            print(filename)
            if filename.endswith(".csv"):
                pdata = pd.read_csv(directory + "\\" + filename)

                pdata = pdata[
                    ((pdata['Chr'] == '1') | (pdata['Chr'] == '14') | (pdata['Chr'] == '19') | (pdata['Chr'] == '21')) &
                    pdata['SNP Name'].str.match('rs')]
                dataFrameOut = pdata[
                    ############################## GRCH 37 ############################################
                    # (((pdata['Chr'] == '1')) & (pdata['Position'].between(227047885, 227093804, inclusive=True))) |
                    # ((pdata['Chr'] == '14') & (pdata['Position'].between(73593143, 73700399, inclusive=True))) |
                    # ((pdata['Chr'] == '19') & (pdata['Position'].between(45399039, 45422650, inclusive=True))) |
                    # ((pdata['Chr'] == '21') & (pdata['Position'].between(27242861, 27553446, inclusive=True)))]

                    ############################## GRCH 36 ############################################
                    (((pdata['Chr'] == '1')) & (pdata['Position'].between(225114896, 225160427, inclusive=True))) |
                    ((pdata['Chr'] == '14') & (pdata['Position'].between(72662932, 72766862, inclusive=True))) |
                    ((pdata['Chr'] == '19') & (pdata['Position'].between(50090879, 50114490, inclusive=True))) |
                    ((pdata['Chr'] == '21') & (pdata['Position'].between(26164732, 26475003, inclusive=True)))]

                z = str(filename)
                dataFrameOut.drop(
                    columns=['GC Score', 'Allele1 - Top', 'Allele2 - Top', 'Allele1 - AB', 'Allele2 - AB', 'Log R Ratio'
                        , 'B Allele Freq', 'Y Raw', 'X Raw', 'Y', 'X', 'R', 'Theta', 'SNP', 'Cluster Sep', 'GT Score'])

                export_csv = dataFrameOut.to_csv(directory + "\\" + "test" + z, header=True)

                print(filename)
                os.remove(directory + "\\" + filename)
    except FileNotFoundError:
        print("Wrong file or file path")
    mergeCsv(path)
def mergeCsv(path):
    try:
        os.chdir(path)
        extension = 'csv'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.to_csv("total.csv", index=False, encoding='utf-8-sig')

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

root = admin()
root.mainloop()