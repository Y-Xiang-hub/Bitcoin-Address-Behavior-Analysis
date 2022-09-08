from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import neighbors
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


'''
    Splitting the training and testing sets using sklearn train_test_split
'''


# using normalized BABD-13_N.csv here to slect the feature
# method 1 and 3 use BABD-13_N and method 2 uses BABD-13
data = pd.read_csv(r'C:\Users\dell\Desktop\Bitcoin_Paper_Code_Data\BitcoinAddressNode\BABD-13_N.csv')

y = data.label
X = data.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=9)


'''
    Splitting the training and testing sets using our designed method
'''


# data_train = pd.read_csv('BABD-13_N.csv')
# data_test = pd.read_csv('BABD-13_N.csv')

# X_train = data_train.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)
# X_test = data_test.drop('label', axis=1).drop('account', axis=1).drop('SW', axis=1)
# y_train = data_train.label
# y_test = data_test.label


'''
    1 Single Feature Selection
'''


# select = SelectKBest(score_func=chi2, k=50)
# fit = select.fit(X_train, y_train)
# dfscores = pd.DataFrame(fit.scores_)
# dfcolumns = pd.DataFrame(X_train.columns)
# featureScores = pd.concat([dfcolumns, dfscores], axis=1)
# featureScores.columns = ['Specs', 'Score']
# print(featureScores.nlargest(50, 'Score'))


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
   2  Feature Importance Measured Method 
'''


model = tree.DecisionTreeClassifier(random_state=9,
                                    criterion='entropy',
                                    splitter='best')
model.fit(X_train, y_train)
plt.figure(figsize=(10, 10))
feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
feat_importances.nlargest(20).plot(kind='barh')
plt.savefig('importance_DT')


'''
    3 Heatmap Generation
'''


# corr = X_train.corr()
# plt.figure(figsize=(80, 80))
# rs = sns.heatmap(corr, linewidths=1, mask=np.zeros_like(corr, dtype=bool), cmap=sns.diverging_palette(220, 10,
#                  as_cmap=True), square=True, xticklabels=True, yticklabels=True, vmin=1, vmax=-1, annot=True, fmt='.2f',
#                  cbar_kws={'shrink': 0.8})
# cbar = rs.collections[0].colorbar
# cbar.ax.tick_params(labelsize=50)
# plt.savefig('heatmap')


'''
    Violin Plots
'''

data = pd.read_csv('BABD-13.csv')
ax = sns.catplot(x="label", y="S2-3", data=data,  # PAIa21-1 PDIa1-2 PTIa41-2 CI3a32-2 S2-2 S2-3
                 kind='violin', 
                 linewidth=0.3,
                 width=0.9,     
                 height=6, palette='hls',
                 scale='width',   
                 gridsize=30,  
                 inner='box',
                 split=True
            )
plt.savefig('test', dpi=500, figsize=(10, 10))
