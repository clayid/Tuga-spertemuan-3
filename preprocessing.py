# -*- coding: utf-8 -*-
"""preprocessing

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KNhU7avzlZ2_0LjWaCswWkiDgjtQ9nuC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

"""Dataset merupakan data Pima Indian Diabet dari Kaggle"""

#Mengimport data
datmin = pd.read_csv('data.csv',sep=";")
datmin.head(5)

"""#EDA"""

datmin.dtypes

datmin.describe().transpose()

sns.countplot(datmin['Outcome']).set_title('Distribution of Outcome')
plt.show()

"""# Skewness"""

datatr=['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
datmin[datatr].skew(axis=0, skipna=True)

df1=datmin.loc[datmin['Outcome']==0]
df2=datmin.loc[datmin['Outcome']==1]

df1[datatr].skew(axis=0, skipna=True)

df2[datatr].skew(axis=0, skipna=True)

df1[datatr].describe()

df2[datatr].describe()

"""# **Preprocessing**"""

#Mengidentifikasi nilai tak wajar sebagai missing value

datmin['Glucose']=datmin['Glucose'].replace(0,np.nan)
datmin['BloodPressure']=datmin['BloodPressure'].replace(0,np.nan)
datmin['SkinThickness']=datmin['SkinThickness'].replace(0,np.nan)
datmin['Insulin']=datmin['Insulin'].replace(0,np.nan)
datmin['BMI']=datmin['BMI'].replace(0,np.nan)
datmin.head()

"""##Missing Value"""

#cek missing value
total=datmin.isnull().sum().sort_values(ascending = False)
print(total)

"""Sebelum melakukan imputasi pada nilai missing, dicek terlebih dahulu skewness dari data, untuk menentukan imputasi yang tepat

##Imputasi Missing Value
"""

#imputasi class mean pada attribute Glucose dan Insulin
df1['Glucose'].fillna(df1['Glucose'].mean(),inplace=True)
df2['Glucose'].fillna(df2['Glucose'].mean(),inplace=True)

df1['Insulin'].fillna(df1['Insulin'].median(),inplace=True)
df2['Insulin'].fillna(df2['Insulin'].median(),inplace=True)
datmin2=df1.append(df2)
datmin2.head()

#Imputasi Mean pada bloodpressure, skinthickness, dan BMI
mean1=datmin2['BloodPressure'].mean()
datmin2['BloodPressure'].fillna(mean1,inplace=True)
mean2=datmin2['SkinThickness'].mean()
datmin2['SkinThickness'].fillna(mean2,inplace=True)
mean3=datmin2['BMI'].mean()
datmin2['BMI'].fillna(mean3,inplace=True)

datmin2.describe().transpose()

#Ckecking Missing Value
total=datmin2.isnull().sum().sort_values(ascending = False)
print(total)

"""##Outlier"""

#Cek outlier menggunakan boxplot
datat=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
ax = sns.boxplot(data=datmin2[datat], orient="h", palette="Set2")

ax = sns.boxplot(data=datscale[datat], orient="h", palette="Set2")

"""###Univariate"""

#membuat fungsi deteksi outlier univariat
def outlier_treatment(datacolumn):
 sorted(datacolumn)
 Q1,Q3 = np.percentile(datacolumn , [25,75])
 IQR = Q3-Q1
 lower_range = Q1-(1.5 * IQR)
 upper_range = Q3 + (1.5 * IQR)
 return lower_range,upper_range

lowerbound,upperbound = outlier_treatment(datmin2['Pregnancies'])
datmin2[(datmin2['Pregnancies'] < lowerbound) | (datmin2['Pregnancies'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['Glucose'])
datmin2[(datmin2['Glucose'] < lowerbound) | (datmin2['Glucose'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['BloodPressure'])
datmin2[(datmin2['BloodPressure'] < lowerbound) | (datmin2['BloodPressure'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['SkinThickness'])
datmin2[(datmin2['SkinThickness'] < lowerbound) | (datmin2['SkinThickness'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['Insulin'])
datmin2[(datmin2['Insulin'] < lowerbound) | (datmin2['Insulin'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['BMI'])
datmin2[(datmin2['BMI'] < lowerbound) | (datmin2['BMI'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['DiabetesPedigreeFunction'])
datmin2[(datmin2['DiabetesPedigreeFunction'] < lowerbound) | (datmin2['DiabetesPedigreeFunction'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(datmin2['Age'])
datmin2[(datmin2['Age'] < lowerbound) | (datmin2['Age'] > upperbound)].index

"""## Multivariate (Mahalanobis Distance)"""

#mengambil data tanpa kolom target/outcome
datout2=datmin2[['Pregnancies','Glucose','BloodPressure',
                'SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']]

#mengetahui banyak data (n)
df=len(list(datout2.columns.values))

#membuat fungsi mahalanobis distance
def mahalanobis(x=None, data=None, cov=None):
    x_minus_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return mahal.diagonal()

datout2['mahala'] = mahalanobis(x=datout2, data=datout2)
datout2.head()

#membuat fungsi deteksi outlier MD
from scipy.stats import chi2
def MD_detectOutliers(MD,df):
    nilaichi=chi2.isf(0.01, df)
    outliers = []
    for i in range(len(MD)):
        if (MD[i] > nilaichi):
            outliers.append(i)  # index of the outlier
    return np.array(outliers)

outliers_indices = MD_detectOutliers(datout2['mahala'],df)

print("Outliers Indices: {}\n".format(outliers_indices))

len(outliers_indices)

d2=datout2['mahala']
eks = range( len( d2 ))

plt.subplot(111)

plt.scatter( eks, d2 )

plt.hlines( chi2.ppf(0.99, df), 0, len(d2), label ="99% $\chi^2$ quantile", linestyles = "solid" )  

plt.legend()
plt.ylabel("recorded value")
plt.xlabel("observation")
plt.title( 'Mahalanobis detection of outliers at 99% $\chi^2$ quantiles' )

plt.show()

"""## Imputasi Outlier (Lanjutan)"""

out2=datmin2
lowerbound,upperbound = outlier_treatment(datmin2['Pregnancies'])
out2.loc[(out2['Pregnancies'] < lowerbound) | (out2['Pregnancies'] > upperbound),'Pregnancies']=np.NaN

lowerbound1,upperbound1 = outlier_treatment(datmin2['BloodPressure'])
out2.loc[(out2['BloodPressure'] < lowerbound1) | (out2['BloodPressure'] > upperbound1),'BloodPressure']=np.NaN
lowerbound2,upperbound2 = outlier_treatment(datmin2['SkinThickness'])
out2.loc[(out2['SkinThickness'] < lowerbound2) | (out2['SkinThickness'] > upperbound2),'SkinThickness']=np.NaN
lowerbound3,upperbound3 = outlier_treatment(datmin2['Insulin'])
out2.loc[(out2['Insulin'] < lowerbound3) | (out2['Insulin'] > upperbound3),'Insulin']=np.NaN
lowerbound4,upperbound4 = outlier_treatment(datmin2['BMI'])
out2.loc[(out2['BMI'] < lowerbound4) | (out2['BMI'] > upperbound4),'BMI']=np.NaN
lowerbound5,upperbound5 = outlier_treatment(datmin2['DiabetesPedigreeFunction'])
out2.loc[(out2['DiabetesPedigreeFunction'] < lowerbound5) | (out2['DiabetesPedigreeFunction'] > upperbound5),'DiabetesPedigreeFunction']=np.NaN
lowerbound6,upperbound6 = outlier_treatment(datmin2['Age'])
out2.loc[(out2['Age'] < lowerbound6) | (out2['Age'] > upperbound6),'Age']=np.NaN

out2.skew(skipna=True)

out2['Pregnancies'].fillna(out2['Pregnancies'].mean(),inplace=True)
out2['BloodPressure'].fillna(out2['BloodPressure'].mean(),inplace=True)
out2['SkinThickness'].fillna(out2['SkinThickness'].mean(),inplace=True)
out2['Insulin'].fillna(out2['Insulin'].mean(),inplace=True)
out2['BMI'].fillna(out2['BMI'].mean(),inplace=True)
out2['DiabetesPedigreeFunction'].fillna(out2['DiabetesPedigreeFunction'].mean(),inplace=True)
out2['Age'].fillna(out2['Age'].mean(),inplace=True)

lowerbound,upperbound = outlier_treatment(out2['Pregnancies'])
out2[(out2['Pregnancies'] < lowerbound) | (out2['Pregnancies'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(out2['BloodPressure'])
len(out2[(out2['BloodPressure'] < lowerbound) | (out2['BloodPressure'] > upperbound)].index)

lowerbound,upperbound = outlier_treatment(out2['SkinThickness'])
out2[(out2['SkinThickness'] < lowerbound) | (out2['SkinThickness'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(out2['Insulin'])
out2[(out2['Insulin'] < lowerbound) | (out2['Insulin'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(out2['BMI'])
out2[(out2['BMI'] < lowerbound) | (out2['BMI'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(out2['DiabetesPedigreeFunction'])
out2[(out2['DiabetesPedigreeFunction'] < lowerbound) | (out2['DiabetesPedigreeFunction'] > upperbound)].index

lowerbound,upperbound = outlier_treatment(out2['Age'])
out2[(out2['Age'] < lowerbound) | (out2['Age'] > upperbound)].index

"""##After Imputasi Outlier"""

import seaborn as sns
datat=['Pregnancies','Glucose','BloodPressure','SkinThickness',
        'Insulin','BMI','DiabetesPedigreeFunction','Age']
ax = sns.boxplot(data=out2[datat], orient="h", palette="Set2")

out2['mahala'] = mahalanobis(x=out2, data=out2)
out2.head()
outliers_indices = MD_detectOutliers(out2['mahala'],df)

print("Outliers Indices: {}\n".format(outliers_indices))

len(outliers_indices)

"""##Scaling"""

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
datscale=NormalizeData(datmin2)

datscale.describe()

"""##Feature Selection"""

datscale.head()

X=datscale[datat]
y=datscale[['Outcome']]

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
fvalue_selector = SelectKBest(f_classif, k=4)
X_kbest = fvalue_selector.fit_transform(X, y)

X_kbest

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
cor = datscale.corr(method="kendall")
sns.heatmap(cor, annot=True)
plt.show()

"""#Split Training Testing Data"""

from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size = 0.2,random_state=0)