import csv
import numpy as np
import pandas as pd
import glob
import os


'''Process Bitcoin data from original .csv file:
    step1: delete empty rows
    step2: delete S6 col
    step3: change header S7->S6, S8->S7, S9->S8, S10->S9
    step4: split tuples in S5 into S5 and S6
    step5: process tuples S2-1, S2-2, S2-3 (find the maximum degree)
    step6: process missing values (using 0 for all according to the definitions)
    step7: add the label to each row at the last col
    step8: Merge all .csv files 
'''


def delete_empty_address(csv_file_1):
    lines = list()
    with open(csv_file_1, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            flag = 0
            for i in range(2, 117):
                if row[i]:
                    flag = 1
                    break
                else:
                    print(row[0])
                    break
            if flag == 1:
                lines.append(row)
            else:
                continue

    with open(csv_file_1, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    print("1-Empty Bitcoin addresses have been deleted!")


def delete_empty_col(csv_file_2):
    df = pd.read_csv(csv_file_2)
    keep_col = ['account', 'SW', 'PAIa11-1', 'PAIa11-2', 'PAIa12', 'PAIa13', 'PAIa14-1', 'PAIa14-2', 'PAIa14-3',
                'PAIa14-4', 'PAIa14-R1', 'PAIa14-R2', 'PAIa14-R3', 'PAIa14-R4', 'PAIa15-1', 'PAIa15-2', 'PAIa15-R1',
                'PAIa15-R2', 'PAIa16-1', 'PAIa16-2', 'PAIa16-R1', 'PAIa16-R2', 'PAIa17-1', 'PAIa17-2', 'PAIa17-3',
                'PAIa17-R1', 'PAIa17-R2', 'PAIa17-R3', 'PAIa21-1', 'PAIa21-2', 'PAIa21-3', 'PAIa21-4', 'PAIa21-R1',
                'PAIa21-R2', 'PAIa21-R3', 'PAIa21-R4', 'PAIa22-1', 'PAIa22-2', 'PAIa22-R1', 'PAIa22-R2', 'PDIa1-1',
                'PDIa1-2', 'PDIa1-3', 'PDIa1-R1', 'PDIa1-R2', 'PDIa1-R3', 'PDIa11-1', 'PDIa11-2', 'PDIa11-R1',
                'PDIa11-R2', 'PDIa12', 'PDIa12-R', 'PDIa13', 'PDIa13-R', 'PTIa1', 'PTIa2', 'PTIa21', 'PTIa31-1',
                'PTIa31-2', 'PTIa31-3', 'PTIa32', 'PTIa33', 'PTIa41-1', 'PTIa41-2', 'PTIa41-3', 'PTIa42', 'PTIa43',
                'CI1a1-1', 'CI1a1-2', 'CI1a2', 'CI2a11-1', 'CI2a11-2', 'CI2a12-1', 'CI2a12-2', 'CI2a12-3', 'CI2a12-4',
                'CI2a21-1', 'CI2a21-2', 'CI2a22-1', 'CI2a22-2', 'CI2a22-3', 'CI2a22-4', 'CI2a23-1', 'CI2a23-2',
                'CI2a31-1', 'CI2a31-2', 'CI2a32-1', 'CI2a32-2', 'CI2a32-3', 'CI2a32-4', 'CI2a33-1', 'CI2a33-2',
                'CI3a11-1', 'CI3a11-2', 'CI3a12-1', 'CI3a12-2', 'CI3a12-3', 'CI3a12-4', 'CI3a21-1', 'CI3a21-2',
                'CI3a21-3', 'CI3a22-1', 'CI3a22-2', 'CI3a22-3', 'CI3a22-4', 'CI3a22-5', 'CI3a22-6', 'CI3a23-1',
                'CI3a23-2', 'CI3a23-3', 'CI3a31-1', 'CI3a31-2', 'CI3a32-1', 'CI3a32-2', 'CI3a32-3', 'CI3a32-4',
                'CI3a33-1', 'CI3a33-2', 'CI4a11', 'CI4a12-1', 'CI4a12-2', 'CI4a13', 'CI4a21', 'CI4a22-1', 'CI4a22-2',
                'CI4a23', 'CI4a31', 'CI4a32-1', 'CI4a32-2', 'CI4a33', 'CI4a41', 'CI4a42-1', 'CI4a42-2', 'CI4a43',
                'S1-1', 'S1-2', 'S1-3', 'S1-4', 'S1-5', 'S1-6', 'S2-1', 'S2-2', 'S2-3', 'S3', 'S4', 'S5', 'S7', 'S8',
                'S9', 'S10']
    new_df = df[keep_col]
    new_df.to_csv(csv_file_2, index=False)
    print("2-Empty col has been deleted!")


def change_header(csv_file_3):
    df = pd.read_csv(csv_file_3)
    correct_df = df.copy()
    correct_df.rename(columns={'S7': 'S6', 'S8': 'S7', 'S9': 'S8', 'S10': 'S9'}, inplace=True)
    correct_df.to_csv(csv_file_3, index=False, header=True)
    print("3-Header has been changed!")


def split_tuple(csv_file_4):
    S5_list = []
    S6_list = []
    df = pd.read_csv(csv_file_4)
    for i in df["S5"]:
        new_S5 = i.split(', ')[0][1:]
        S5_list.append(new_S5)
        new_S6 = i.split(', ')[1][:-1]
        S6_list.append(new_S6)

    se1 = pd.Series(S5_list)
    se2 = pd.Series(S6_list)
    df['S5'] = se1.values
    df['S6'] = se2.values
    df.to_csv(csv_file_4, index=False)
    print("4-S5 has been split into S5 and S6!")


def process_tuple_maximum(csv_file_5):
    S2_1_list = []
    S2_2_list = []
    S2_3_list = []
    df = pd.read_csv(csv_file_5)
    for i in df["S2-1"]:
        max_len = len(i.split(', '))
        if max_len == 2:
            max_degree = i.split(', ')[max_len - 2][2:]
        else:
            max_degree = i.split(', ')[max_len - 2][1:]
        S2_1_list.append(max_degree)

    for i in df["S2-2"]:
        max_len = len(i.split(', '))
        if max_len == 2:
            max_degree = i.split(', ')[max_len - 2][2:]
        else:
            max_degree = i.split(', ')[max_len - 2][1:]
        S2_2_list.append(max_degree)

    for i in df["S2-3"]:
        max_len = len(i.split(', '))
        if max_len == 2:
            max_degree = i.split(', ')[max_len - 2][2:]
        else:
            max_degree = i.split(', ')[max_len - 2][1:]
        S2_3_list.append(max_degree)

    se1 = pd.Series(S2_1_list)
    se2 = pd.Series(S2_2_list)
    se3 = pd.Series(S2_3_list)
    df['S2-1'] = se1.values
    df['S2-2'] = se2.values
    df['S2-3'] = se3.values
    df.to_csv(csv_file_5, index=False)
    print("5-Maximum values of S2 have been done!")


def process_missing_value(file_6):
    df = pd.read_csv(file_6, na_values='-')
    df.fillna(0, inplace=True)
    df.to_csv(file_6, index=False)
    print("6-Missing values are filled!")


def add_address_label(csv_file_7, label_name):
    df = pd.read_csv(csv_file_7)
    df["label"] = label_name
    df.to_csv(csv_file_7, index=False)
    print("7-Labels have been added!")


def merge_csv_file(folder_path, file_1):
    os.chdir(folder_path)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])  # combine all files in the list
    combined_csv.to_csv(file_1, index=False, encoding='utf-8')  # export to csv
    print("0-Files with the same type have been merged!")


if __name__ == '__main__':

    '''
        1. Delete empty Bitcoin address in a csv file
        2. Delete empty (S6) cols
        3. Change header (S7->S6, S8->S7 and S9->S8) # S10->S9
        4. Split tuples (S5->[S5 and S6])
        5. Process tuple (find maximum degree in S2-1, S2-2, and S2-3)
        6. Process missing values (using 0 for all)
        7. Add labels to Bitcoin address
        8. Merge all .csv files 
    '''

    csv_files = []
    for file in glob.glob("*.csv"):
        csv_files.append(file)
    print(csv_files)

    prev_file = " "
    for file in csv_files:
        print('"' + file + '"')
        delete_empty_address(file)
        delete_empty_col(file)
        change_header(file)
        split_tuple(file)
        process_tuple_maximum(file)
        process_missing_value(file)

    # add the label
    # file = "fileaname.csv"
    # label = 0
    # add_address_label(file, label)

    # merge .csv files
    # path = r"C:\Users\24563\Desktop\Paper\Bitcoin paper\MLcode"
    # file = "BABD_raw.csv"
    # merge_csv_file(path, file)

