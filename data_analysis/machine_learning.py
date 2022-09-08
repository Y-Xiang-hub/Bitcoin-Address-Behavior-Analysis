import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import neighbors, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


'''
    Splitting the training and testing sets using sklearn train_test_split
'''


data = pd.read_csv('BABD-13.csv')

y = data.label
X = data.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)

# choose features that are used for training
# X_PAI = X.iloc[:, 0:38]       # PAI
# X_PDI = X.iloc[:, 38:52]      # PDI
# X_PTI = X.iloc[:, 52:65]      # PTI
# X_CI = X.iloc[:, 65:132]      # CI
X_SI = X.iloc[:, 0:132]         # SI
X_LSI = X.iloc[:, 132:148]      # LSI

X_KNN = X.iloc[:, np.r_[1:8, 9:11, 13, 15, 26, 38:45, 48:52, 53, 57, 66:68, 72, 132:148]]
X_RF = X.iloc[:, np.r_[1:10, 20:25, 40, 54, 60:62, 91, 96, 105:107, 132:148]]
X_XGB = X.iloc[:, np.r_[1:10, 20:25, 40, 54, 60:62, 91, 96, 105:107, 132:148]]


X_train, X_test, y_train, y_test = train_test_split(X_RF, y, test_size=0.2, random_state=9)


'''
    Splitting the training and testing sets using our designed method
'''

# data_train = pd.read_csv('BABD-13_train.csv')
# data_test = pd.read_csv('BABD-13_test.csv')

# X_train = data_train.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)
# X_test = data_test.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)
# y_train = data_train.label
# y_test = data_test.label


'''
    Normalization / Standardization
'''


normalizer = preprocessing.MinMaxScaler()
X_train = normalizer.fit_transform(X_train)
X_test = normalizer.transform(X_test)

# standardizer = preprocessing.StandardScaler()
# X_train = standardizer.fit_transform(X_train)
# X_test = standardizer.transform(X_test)


'''
    KNN model
'''


knn = neighbors.KNeighborsClassifier(n_neighbors=4,
                                     algorithm='kd_tree',
                                     weights='distance',
                                     n_jobs=-1)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
a = accuracy_score(y_test, y_pred_knn)
print("KNN: " + str(a))
print(precision_score(y_test, y_pred_knn, average='macro', zero_division=0))
print(precision_score(y_test, y_pred_knn, average='micro', zero_division=0))
print(precision_score(y_test, y_pred_knn, average='weighted', zero_division=0))
print(recall_score(y_test, y_pred_knn, average='macro'))
print(recall_score(y_test, y_pred_knn, average='micro'))
print(recall_score(y_test, y_pred_knn, average='weighted'))
print(f1_score(y_test, y_pred_knn, average='macro'))
print(f1_score(y_test, y_pred_knn, average='micro'))
print(f1_score(y_test, y_pred_knn, average='weighted'))


'''
    DT model
'''


dt = tree.DecisionTreeClassifier(random_state=9,
                                 criterion='entropy',
                                 splitter='best')
dt = dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
a = accuracy_score(y_true=y_test, y_pred=y_pred_dt)
print("DT: " + str(a))
print(precision_score(y_test, y_pred_dt, average='macro', zero_division=0))
print(precision_score(y_test, y_pred_dt, average='micro', zero_division=0))
print(precision_score(y_test, y_pred_dt, average='weighted', zero_division=0))
print(recall_score(y_test, y_pred_dt, average='macro'))
print(recall_score(y_test, y_pred_dt, average='micro'))
print(recall_score(y_test, y_pred_dt, average='weighted'))
print(f1_score(y_test, y_pred_dt, average='macro'))
print(f1_score(y_test, y_pred_dt, average='micro'))
print(f1_score(y_test, y_pred_dt, average='weighted'))


'''
    RF model
'''


rfc = RandomForestClassifier(random_state=9,
                             n_estimators=200,
                             n_jobs=-1)
rfc = rfc.fit(X_train, y_train)
y_pred_rf = rfc.predict(X_test)
a = accuracy_score(y_true=y_test, y_pred=y_pred_rf)
print("RF: " + str(a))
print(precision_score(y_test, y_pred_rf, average='macro', zero_division=0))
print(precision_score(y_test, y_pred_rf, average='micro', zero_division=0))
print(precision_score(y_test, y_pred_rf, average='weighted', zero_division=0))
print(recall_score(y_test, y_pred_rf, average='macro'))
print(recall_score(y_test, y_pred_rf, average='micro'))
print(recall_score(y_test, y_pred_rf, average='weighted'))
print(f1_score(y_test, y_pred_rf, average='macro'))
print(f1_score(y_test, y_pred_rf, average='micro'))
print(f1_score(y_test, y_pred_rf, average='weighted'))


'''
    MLP model
'''


mlp = MLPClassifier(random_state=9,
                    max_iter=1000,
                    solver='adam',
                    hidden_layer_sizes=(100, 100, 100))
mlp = mlp.fit(X_train, y_train)
y_pred_mlp = mlp.predict(X_test)
a = accuracy_score(y_true=y_test, y_pred=y_pred_mlp)
print("MLP: " + str(a))
print(precision_score(y_test, y_pred_mlp, average='macro', zero_division=0))
print(precision_score(y_test, y_pred_mlp, average='micro', zero_division=0))
print(precision_score(y_test, y_pred_mlp, average='weighted', zero_division=0))
print(recall_score(y_test, y_pred_mlp, average='macro'))
print(recall_score(y_test, y_pred_mlp, average='micro'))
print(recall_score(y_test, y_pred_mlp, average='weighted'))
print(f1_score(y_test, y_pred_mlp, average='macro'))
print(f1_score(y_test, y_pred_mlp, average='micro'))
print(f1_score(y_test, y_pred_mlp, average='weighted'))


'''
    XGBoost model
'''


xgb = model = XGBClassifier(objective='multi:softmax',
                            num_class=13,
                            eval_metric='mlogloss',
                            learning_rate=0.5,
                            use_label_encoder=False,
                            n_jobs=-1)
xgb = xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
a = accuracy_score(y_true=y_test, y_pred=y_pred_xgb)
print("XGB: " + str(a))
print(precision_score(y_test, y_pred_xgb, average='macro', zero_division=0))
print(precision_score(y_test, y_pred_xgb, average='micro', zero_division=0))
print(precision_score(y_test, y_pred_xgb, average='weighted', zero_division=0))
print(recall_score(y_test, y_pred_xgb, average='macro'))
print(recall_score(y_test, y_pred_xgb, average='micro'))
print(recall_score(y_test, y_pred_xgb, average='weighted'))
print(f1_score(y_test, y_pred_xgb, average='macro'))
print(f1_score(y_test, y_pred_xgb, average='micro'))
print(f1_score(y_test, y_pred_xgb, average='weighted'))
