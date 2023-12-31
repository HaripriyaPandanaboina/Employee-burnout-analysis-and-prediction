# -*- coding: utf-8 -*-
"""Employee_burnout_analysis_and_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19klRdEAq4UqSAbDIzhc6SPNwlzpgBJ9i

Employees Burnout Analysis and Prediciton
"""

# Commented out IPython magic to ensure Python compatibility.
#importing of libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

from google.colab import drive
drive.mount('/content/drive')

#@title loading of the dataset

burnout=pd.read_excel("/content/drive/MyDrive/employee_burnout_analysis.xlsx")
burnout = pd.DataFrame(burnout)#convert the excel file into the csv file

#printing the top 5 columns of dataset
burnout.head(5)

#Describing the dataset mean,std,mode and count of every attribute
burnout.describe()

#shape of the dataset(rows,columns)
burnout.shape

#Columns
burnout.columns

#Info of datatype and non null count of columns
burnout.info()

#converting the datetime into datatype
burnout['Date of Joining']=pd.to_datetime(burnout['Date of Joining'])
print(type(burnout['Date of Joining']))
print(burnout['Date of Joining'])





#checking null values in dataset

burnout.isnull().sum()

#checking the duplicate values
burnout.duplicated().sum()



#droping the missing values
burnout= burnout.dropna()
#checking is  any null values
burnout.isnull().sum()

#show the number of unique values
burnout.nunique()

burnout["Gender"].unique()

burnout['Company Type'].unique()

burnout['WFH Setup Available'].unique()

#@title Expolartion of data

sns.countplot(data=burnout, x='WFH Setup Available')

sns.barplot(data=burnout,x='Company Type',y='Mental Fatigue Score')

sns.histplot(data=burnout, x='Resource Allocation', bins=10);

sns.histplot(data=burnout, x='Mental Fatigue Score', bins=10);

sns.countplot(data=burnout, x='Designation');

sns.scatterplot(data=burnout, x='Mental Fatigue Score', y='Burn Rate');

sns.pairplot(burnout)

burnout['Gender']              = burnout['Gender'].map({'Female': 1, 'Male': 0})
burnout['Company Type']        = burnout['Company Type'].map({'Service': 1, 'Product': 0})
burnout['WFH Setup Available'] = burnout['WFH Setup Available'].map({'Yes': 1, 'No': 0})

#showing the the unquie values
for i,col in  enumerate(burnout.columns):
  print(f"{burnout[col].unique()}")
  print(f"\n\n{burnout[col].value_counts()}\n\n")

burnout.head()



#droping the irrvelent data
burnout=burnout.drop('Employee ID',axis=1)

burnout.head()





burnout.head(5)

burnout.corr()

import plotly.express as px

corr=burnout.corr()
sns.set(rc={'figure.figsize':(14,12)})
fig=px.imshow(corr,text_auto=True,aspect='auto')
fig.show()

drop_list = ['Date of Joining','Company Type']
burnout_train = burnout.drop(drop_list, axis=1)

burnout_train.head()

#splitin of data for  x and y
X = np.array(burnout_train.drop('Burn Rate', axis=1))
y = np.array(burnout_train['Burn Rate'])

#preprocessing of data
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics

#Standardization of the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

#spliting of the data for train and test
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,shuffle=True,random_state=42)

print('Train shape:', X_train.shape)
print('Test shape:', X_test.shape)







from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('RMSE:', metrics.mean_squared_error(y_test, y_pred))
print('accuracy_score:', metrics.r2_score(y_test, y_pred))

from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


print('MeanAbsoult Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Root MeanSquareError:', metrics.mean_squared_error(y_test, y_pred))
R2_test=metrics.r2_score(y_test, y_pred)*100


print("accuracy_score:",R2_test)









clf = DecisionTreeRegressor(random_state=44,max_depth=3)
model = clf.fit(X_train, y_train)

from sklearn.tree import plot_tree
plt.figure(figsize=(10,8), dpi=150)
plot_tree(model, feature_names=burnout_train.columns)

#Fitting the Multiple Linear Regression model
from sklearn.linear_model import LinearRegression
model= LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Intercept: ", model.intercept_)
print("Coefficients:")
list(zip(burnout_train, model.coef_))

#Prediction of test set
y_pred_model= model.predict(X_test)
#Predicted values
print("Prediction for test set: {}".format(y_pred_model))

mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_model})
mlr_diff.head()

print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
print('RMSE:', metrics.mean_squared_error(y_test, y_pred))
print('accuracy_score:', metrics.r2_score(y_test, y_pred)*100)

import seaborn as sns

sns.regplot(x = y_test, y = y_pred,
            scatter_kws = {"color": "blue", "alpha": 0.5},
            line_kws = {"color": "red"})
plt.title('fitting of the line')
# Set x-axis label
plt.xlabel('actual values')
# Set y-axis label
plt.ylabel('predict values')

