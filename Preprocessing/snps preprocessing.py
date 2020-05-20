from __future__ import division, print_function
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
import glob
import pandas as pd
from matplotlib import style
import time
low_memory=False
start_time = time.time()
style.use('ggplot')
label_encoder = LabelEncoder()
label_encoder.fit(np.array(['a', 'c', 'g', 't', 'z']))


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
                # dataFrameOut.drop(
                #     columns=['GC Score', 'Allele1 - Top', 'Allele2 - Top', 'Allele1 - AB', 'Allele2 - AB', 'Log R Ratio'
                #         , 'B Allele Freq', 'Y Raw', 'X Raw', 'Y', 'X', 'R', 'Theta', 'SNP', 'Cluster Sep', 'GT Score'])

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

    score("total.csv", r'C:\Users\user\Desktop\project\New folder\sara.csv', r'C:\Users\user\Desktop\project\New folder\Normal.csv')


def score(path1, path2, path3):
    df1 = pd.read_csv(path1)
    df1 = df1.drop(
        columns=['Chr', 'Position','GC Score', 'SNP Index',
                 'Sample Index', 'Allele1 - Top', 'Allele2 - Top', 'Allele1 - AB', 'Allele2 - AB', 'Log R Ratio'
            , 'B Allele Freq', 'Y Raw', 'X Raw', 'Y', 'X', 'R', 'Theta', 'SNP', 'Cluster Sep', 'GT Score'])


    try:
        df1 = df1.drop(
            columns=['Allele2 - Plus', 'Allele1 - Plus'])
    except KeyError:
        print ("adni 2")
    try:
        df1 = df1.drop(
            columns=['Unnamed: 0'])
    except KeyError:
        print ("u")
    
#     df1 = df1.drop(
#         columns=['Allele2 - Plus', 'Allele1 - Plus', 'Chr', 'Position', 'Unnamed: 0', 'GC Score', 'SNP Index',
#                  'Sample Index', 'Allele1 - Top', 'Allele2 - Top', 'Allele1 - AB', 'Allele2 - AB', 'Log R Ratio'
#             , 'B Allele Freq', 'Y Raw', 'X Raw', 'Y', 'X', 'R', 'Theta', 'SNP', 'Cluster Sep', 'GT Score'])
    # df.head()
    df1["Score 1"] = ""
    # df1["Score 2"] = ""
    df2 = pd.read_csv(path2)
    df2 = df2.drop(columns=['Unnamed: 0'])
    df2 = df2.dropna()
    merge = pd.merge(df2, df1, on=['SNP Name'])
    merge.to_csv("Omar.csv")

    df = pd.read_csv("omar.csv")

    conditions = [((df['Allele1 - Forward'] == df['REF']) & (df['Allele2 - Forward'] == df['REF'])),
                  ((df['Allele1 - Forward'] != df['REF']) & (df['Allele2 - Forward'] == df['REF'])),

                  ((df['Allele1 - Forward'] == df['REF']) & (df['Allele2 - Forward'] != df['REF'])),

                  ((df['Allele1 - Forward'] != df['REF']) & (df['Allele2 - Forward'] != df['REF']))]
    values = [0, 1, 1, 2]

    df['Score 1'] = np.select(conditions, values, 3)
    export_csv = df.to_csv(r'1st.csv', header=True,index=False)
    dfOriginal = pd.read_csv("1st.csv")

    snps = dfOriginal['SNP Name'].unique()

    id = dfOriginal['Sample ID'].unique()

    df = pd.DataFrame(columns=snps)
    df['id'] = id
    df.set_index('id', inplace=True)

    for i in range(len(dfOriginal) - 1):
        df[dfOriginal['SNP Name'][i]][dfOriginal['Sample ID'][i]] = dfOriginal['Score 1'][i]
    df.insert(0, 'Status', 'Diseased')
    export_csv = df.to_csv(r'lastOne.csv', index=False, header=True)
    df1 = pd.read_csv("lastOne.csv")
    df2 = pd.read_csv(path3)
    dfAll = pd.concat((df1, df2), sort=False).reindex(columns=df1.columns)
    export_csv = dfAll.to_csv(r'Total_Scored.csv', header=True,index=False)
    df=pd.read_csv('Total_Scored.csv')
#     df = df.drop(columns=['Unnamed: 0'])
#     df.to_csv("Total_Scored2.csv")    

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


# root = admin()
# root.mainloop()
