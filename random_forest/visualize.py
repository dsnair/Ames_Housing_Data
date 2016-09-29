import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

# Since there are 81 variables, set the display size to be 90 variables
pd.set_option('display.max_columns', 90)
pd.set_option('display.max_rows', 90)

train = pd.read_csv("train.csv")

# Find missing values
train.head()		# notice NaN
train.describe()	# notice different counts due to NaN
train.dtypes		# variable data types
train.shape		# data dimension = # rows, # columns

# Drop these variables due to lots of missing values; also drop Id
train.count()		# count NaN
train = train.drop(['Id', 'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature'], axis = 1)  # 1 = columns, 0 = rows
train.count()


### VISUALIZE ###


# SalePrice: The property's sale price in dollars
hist = [go.Histogram(x = train['SalePrice'])]
layout = go.Layout(title = "The property's sale price in dollars",
				xaxis = dict(title = "SalePrice (dollars)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# SalePrice: log base 10 transform
hist = [go.Histogram(x = np.log10(train['SalePrice']))]
layout = go.Layout(title = "The property's sale price in dollars (log base 10)",
				xaxis = dict(title = "SalePrice (dollars in log base 10)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)


# Plot top variables as seen in variable importance plot

# GrLivArea: Above grade (ground) living area square feet
hist = [go.Histogram(x = train['GrLivArea'])]
layout = go.Layout(title = "Above grade (ground) living area square feet",
				xaxis = dict(title = "GrLivArea (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# Neighborhood: Physical locations within Ames city limits
nghdTab = train['Neighborhood'].value_counts()	# frequency table
nghdTab
frqDict = nghdTab.to_dict()			# convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Physical locations within Ames city limits", 
				xaxis = dict(title = "Neighborhood"), 
				yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.plot(fig)

# OverallQual: Overall material and finish quality
qualTab = train['OverallQual'].value_counts()	# frequency table
qualTab
frqDict = qualTab.to_dict()			# convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Overall material and finish quality", 
				xaxis = dict(title = "OverallQual"), 
				yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.plot(fig)

# 1stFlrSF: First Floor square feet
hist = [go.Histogram(x = train['1stFlrSF'])]
layout = go.Layout(title = "First Floor square feet",
				xaxis = dict(title = "1stFlrSF (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# 2ndFlrSF: Second Floor square feet
hist = [go.Histogram(x = train['2ndFlrSF'])]
layout = go.Layout(title = "Second Floor square feet",
				xaxis = dict(title = "2ndFlrSF (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# TotalBsmtSF: Total square feet of basement area
hist = [go.Histogram(x = train['TotalBsmtSF'])]
layout = go.Layout(title = "Total square feet of basement area",
				xaxis = dict(title = "TotalBsmtSF (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# BsmtFinSF1: Type 1 finished square feet
hist = [go.Histogram(x = train['BsmtFinSF1'])]
layout = go.Layout(title = "Type 1 finished square feet",
				xaxis = dict(title = "BsmtFinSF1 (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# GarageCars: Size of garage in car capacity
carsTab = train['GarageCars'].value_counts()	# frequency table
carsTab
frqDict = carsTab.to_dict()			# convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Size of garage in car capacity", 
				xaxis = dict(title = "GarageCars (# of cars)"), 
				yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.plot(fig)

# LotArea: Lot size in square feet; log base 10 transform
hist = [go.Histogram(x = np.log10(train['LotArea']))]
layout = go.Layout(title = "Lot size in square feet (log base 10)",
				xaxis = dict(title = "LotArea (square feet)"),
				yaxis = dict(title = "Frequency"),
				bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.plot(fig)

# OverallCond: Overall condition rating
condTab = train['OverallCond'].value_counts()	# frequency table
condTab
frqDict = condTab.to_dict()			# convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Overall condition rating", 
				xaxis = dict(title = "OverallCond"), 
				yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.plot(fig)
