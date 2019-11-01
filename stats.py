#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:35:29 2019

@author: pi
"""

import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np

df = pd.read_csv("logETH_2019-10-31 16:59:57.376414.txt")

def show_graphs():
    fig = plt.figure(figsize = (12,10))
    ax1 = fig.add_subplot(211)
    
    df.plot(x="time",  y="bal1", ax=ax1, kind="line", label='bal 0.5%')
    df.plot(x="time",  y="bal2", ax=ax1, kind="line", label='bal 1.0%')
    df.plot(x="time",  y="bal3", ax=ax1, kind="line", label='bal 1.5%')
    df.plot(x="time",  y="bal4", ax=ax1, kind="line", label='bal 2.0%')
    df.plot(x="time",  y="bal5", ax=ax1, kind="line", label='bal 2.5%')
    #plt.yticks(0, 4, 1)
    
    ax2 = fig.add_subplot(212)
    ax2 = df.plot(x="time", y="price", ax=ax2, kind="line")


x = df['price']
y = df.loc[3:7,:]

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 100) 
lm = LinearRegression()
lm = lm.fit(x_train,y_train)   #lm.fit(input,output)
print('Coeficient :', lm.coef_)
print('Intercept :', lm.intercept_)

#To predict values
y_pred = lm.predict(x_test)

#Errors are the difference between observed and predicted values.
y_error = y_test - y_pred

#R-square score
r2_score(y_test,y_pred)
print('r2 score :', r2_score)


# -------------------
#using statsmodels
# -------------------

import statsmodels.api as sma
X_train = sma.add_constant(x_train) ## let's add an intercept (beta_0) to our model
X_test = sma.add_constant(x_test) 

#Linear regression can be run by using sm.OLS:
import statsmodels.formula.api as sm
lm2 = sm.OLS(y_train,X_train).fit()

#The summary of our model can be obtained via:
lm2.summary()

#The predicted values for test set are given by:
y_pred2 = lm2.predict(X_test) 

#Guide :
#https://www.listendata.com/2018/01/linear-regression-in-python.html#Difference-between-Simple-and-Multiple-Linear-Regression