import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

train = pd.read_csv("trainImp.csv")

# SalePrice: The property's sale price in dollars
hist = [go.Histogram(x = train['SalePrice'])]
layout = go.Layout(title = "The property's sale price in dollars",
		   xaxis = dict(title = "SalePrice (dollars)"),
		   yaxis = dict(title = "Frequency"),
		   bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.image.save_as(fig, filename = 'SalePrice.png')

# SalePrice: log base 10 transform
hist = [go.Histogram(x = np.log10(train['SalePrice']))]
layout = go.Layout(title = "The property's sale price in dollars (log base 10)",
		   xaxis = dict(title = "SalePrice (dollars in log base 10)"),
		   yaxis = dict(title = "Frequency"),
		   bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.image.save_as(fig, filename = 'log10SalePrice.png')


# Plot top variables from random forest' variable importance plot

# GrLivArea: Above grade (ground) living area square feet
hist = [go.Histogram(x = train['GrLivArea'])]
layout = go.Layout(title = "Above grade (ground) living area square feet",
		   xaxis = dict(title = "GrLivArea (square feet)"),
		   yaxis = dict(title = "Frequency"),
		   bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.image.save_as(fig, filename = 'GrLivArea.png')

# Neighborhood: Physical locations within Ames city limits
nghdTab = train['Neighborhood'].value_counts()	# frequency table
nghdTab
frqDict = nghdTab.to_dict() # convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Physical locations within Ames city limits", 
		   xaxis = dict(title = "Neighborhood"), 
		   yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.image.save_as(fig, filename = 'Neighborhood.png')

# OverallQual: Overall material and finish quality
qualTab = train['OverallQual'].value_counts()	# frequency table
qualTab
frqDict = qualTab.to_dict() # convert to dictionary
bar = [go.Bar(x = frqDict.keys(), y = frqDict.values())]
layout = go.Layout(title = "Overall material and finish quality", 
		   xaxis = dict(title = "OverallQual"), 
		   yaxis = dict(title = "Frequency"))
fig = go.Figure(data = bar, layout = layout)
py.image.save_as(fig, filename = 'OverallQual.png')

# TotalBsmtSF: Total square feet of basement area
hist = [go.Histogram(x = train['TotalBsmtSF'])]
layout = go.Layout(title = "Total square feet of basement area",
		   xaxis = dict(title = "TotalBsmtSF (square feet)"),
		   yaxis = dict(title = "Frequency"),
		   bargap = 0.01)
fig = go.Figure(data = hist, layout = layout)
py.image.save_as(fig, filename = 'TotalBsmtSF.png')
