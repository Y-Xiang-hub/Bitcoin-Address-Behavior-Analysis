"""
    Format Rules of the Input Data

    col:label
        - instances with the same class label must be adjacent

    col:SW
        - instances with the same SW label must be adjacent
"""

import sys
import pandas as pd
import math

INPUT_DATASET = 'INPUT_FILE_NAME.csv'  # input file name of the original set
OUTPUT_TRAIN_SET = 'TRAINING_SET_NAME.csv'  # output file name of the training set
OUTPUT_TEST_SET = 'TESTING_SET_NAME.csv'  # output file name of the testing set
SPLIT_BY = ['label', 'SW']  # split based on which columns
SPLIT_RATE = 0.8  # the rate of training set


########## Split training and testing sets based on SW and label ##########

data = pd.read_csv(INPUT_DATASET)

data_count = data.groupby(SPLIT_BY).account.count()
data_train = pd.DataFrame(columns=data.columns)
data_test = pd.DataFrame(columns=data.columns)
curr_row = 0

for e in list(data_count.index):
    try:
        count_train = math.floor(data_count[e] * SPLIT_RATE)
        count_test = data_count[e] - count_train

        data_train = pd.concat([data_train, data.iloc[curr_row:curr_row + count_train, :]])
        curr_row = curr_row + count_train

        data_test = pd.concat([data_test, data.iloc[curr_row:curr_row + count_test, :]])
        curr_row = curr_row + count_test

    except KeyError:
        print("Unknown error. Please contact yuexin.xiang@cug.edu.cn")
        sys.exit(1)


########## Shuffle data sets ##########

data_train = data_train.sample(frac=1)
data_test = data_test.sample(frac=1)

data_train.to_csv(OUTPUT_TRAIN_SET, index=False)
data_test.to_csv(OUTPUT_TEST_SET, index=False)


########## Validate data sets ##########

df_o = pd.read_csv(INPUT_DATASET)
label_o = df_o.groupby('label').account.count()
print("----- Instance number summary of the original data set by label -----")
print(label_o, "\n")
print("The total number of instances in the original data set is: ", df_o.account.count(), "\n\n")

df_train = pd.read_csv(OUTPUT_TRAIN_SET)
label_train = df_train.groupby('label').account.count()
print("----- Instance number summary of the training data set by label -----")
print(label_train, "\n")
print("The total number of instances in the training data set is: ", df_train.account.count(), "\n\n")

df_test = pd.read_csv(OUTPUT_TEST_SET)
label_test = df_test.groupby('label').account.count()
print("----- Instance number summary of the testing data set by label -----")
print(label_test, "\n")
print("The total number of instances in the testing data set is: ", df_test.account.count(), "\n\n")
