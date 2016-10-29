# Pandas documentation: http://pandas.pydata.org/pandas-docs/stable/api.html#attributes
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

train = pd.read_csv("../data/train.csv")
test = pd.read_csv("../data/test.csv")
data = pd.concat([train, test])

# data dimensions: # rows, # columns
train.shape
test.shape
data.shape

data = data.drop(["Id", "SalePrice"], axis = 1) # drop these variables
data.columns.values  # print all column names

# find variables with missing values
data.isnull().sum().sort_values(ascending = False)

# Explore variables one at a time
# -------------------------------

# MSSubClass
data["MSSubClass"].isnull().sum()
freq = data["MSSubClass"].value_counts()  # frequency table
freq
    # MSSubClass is categorical, though coded as numeric
plt.bar(range(len(freq)), freq.values, align = "center")  # bar graph
plt.xticks(range(len(freq)), freq.keys())
plt.xlabel("MSSubClass")
plt.ylabel("Frequency")
#plt.show()
    # \ wraps long code to next line
    # create 3 types of dwelling
MSSubClass = data["MSSubClass"].replace([20, 60], 1) \
.replace([50, 120, 30, 160, 70, 80, 90], 2) \
.replace([190, 85, 75, 45, 180, 40, 150], 3)
new = pd.DataFrame({"MSSubClass": MSSubClass})  # create new dataframe
new["MSSubClass"].value_counts()
new.head()

# MSZoning
train["MSZoning"].value_counts()
test["MSZoning"].value_counts()
data["MSZoning"].isnull().sum()
    # low residential density?: Y (1) or N (0)
new["MSZoning"] = data["MSZoning"].map(lambda x: 1 if (x == "RL") or (x == "RM") else 0)
new["MSZoning"] = new["MSZoning"].fillna(0)
data["MSZoning"].value_counts()
new["MSZoning"].value_counts()  # NOT enough variety!
new.head()

# LotFrontage

# LotArea

# Street
data["Street"].isnull().sum()
data["Street"].value_counts()
    # paved street?: Y (1) or No (0)
new["Street"] = np.where(data["Street"] == "Pave", 1, 0)
new["Street"].value_counts()  # NOT enough variety!
new.head()

# Alley
data["Alley"].isnull().sum()
new["Alley"] = data["Alley"].fillna("None")  # NA doesn't mean missing
    # alley access?: Y (1) or N (0)
new["Alley"] = new["Alley"].map(lambda x: 0 if (x == "None") else 1)
new["Alley"].value_counts()  # NOT enough variety!
new.head()

# LotShape ???
data["LotShape"].isnull().sum()
data["LotShape"].value_counts()
    # regular lot shape?: Y (1) or No (0)
new["LotShape"] = np.where(data["LotShape"] == "Reg", 1, 0) # ????
new["LotShape"].value_counts()
new.head()

# LandContour
data["LandContour"].isnull().sum()
data["LandContour"].value_counts()
    # flat lot?: Y (1) or N (0)
new["LandContour"] = np.where(data["LandContour"] == "Lvl", 1, 0)
new["LandContour"].value_counts()  # NOT enough variety!
new.head()

# Utilities: NOT enough variety! Drop this variable
data["Utilities"].value_counts()

# LotConfig
data["LotConfig"].isnull().sum()
data["LotConfig"].value_counts()
new["LotConfig"] = data["LotConfig"].replace(["FR2", "FR3"], "FR")
new["LotConfig"].value_counts()  # NOT enough variety!
new.head()

# LandSlope
data["LandSlope"].isnull().sum()
data["LandSlope"].value_counts()
    # gentle slope?: Y (1) or No (0)
new["LandSlope"] = np.where(data["LandSlope"] == "Gtl", 1, 0)
new["LandSlope"].value_counts()  # NOT enough variety!
new.head()

# Neighborhood

# Condition1 and Condition2
data["Condition1"].value_counts()
data["Condition2"].value_counts()
    # Most houses have normal condition. If either conditions are normal, combine them
Condition = np.logical_or(data["Condition1"] == "Norm", data["Condition2"] == "Norm")
Condition.value_counts()  # NOT enough variety! Drop this variable

# BldgType
data["BldgType"].isnull().sum()
data["BldgType"].value_counts()
    # single-family detached?: Y (1) or N (0)
new["BldgType"] = np.where(data["BldgType"] == "1Fam", 1, 0)
new["BldgType"].value_counts()  # NOT enough variety!
new.head()

# HouseStyle
data["HouseStyle"].isnull().sum()
data["HouseStyle"].value_counts()
    # combine 1 and 1.5 story, 2 and 2.5 story, rest as other
new["HouseStyle"] = data["HouseStyle"].replace(["1Story", "1.5Fin", "1.5Unf"], 1) \
.replace(["2Story", "2.5Fin", "2.5Unf"], 2) \
.replace(["SFoyer", "SLvl"], 0)
new["HouseStyle"].value_counts()
new.head()

# OverallQual
data["OverallQual"].isnull().sum()
data["OverallQual"].value_counts()
    # combine v.poor/poor/fair/<avg (-1), avg/>avg/good (0), v.good/excel/v.excel (1)
new["OverallQual"] = data["OverallQual"].map(lambda x: -1 if x < 4 else 0 if x < 8 else 1)
new["OverallQual"].value_counts()
new.head()

# OverallCond
data["OverallCond"].isnull().sum()
data["OverallCond"].value_counts()
    # combine v.poor/poor/fair/<avg (-1), avg/>avg/good (0), v.good/excel/v.excel (1)
new["OverallCond"] = data["OverallCond"].map(lambda x: -1 if x < 4 else 0 if x < 8 else 1)
new["OverallCond"].value_counts()  # NOT enough variety!
new.head()

# YearBuilt
data["YearBuilt"].describe()
    # years usually needs to be binned
new["YearBuilt"] = pd.qcut(data["YearBuilt"], q = 4, labels = ["ancient", "older", "newer", "modern"])
pd.concat((new["YearBuilt"], data["YearBuilt"]), axis = 1).head()
new["YearBuilt"].value_counts()
new.head()

# YearRemodAdd
data["YearRemodAdd"].describe()
remodel = np.subtract(data["YearRemodAdd"], data["YearBuilt"])
remodel.describe()
remodel.value_counts()  # years since remodeled, # houses
new["YearRemodAdd"] = pd.Series(remodel.map(lambda x: "Never" if x <= 0 else "recent" if x <= 10 else "long ago"))
new["YearRemodAdd"].value_counts()
new.head()

# RoofStyle
data["RoofStyle"].isnull().sum()
data["RoofStyle"].value_counts()
new["RoofStyle"] = data["RoofStyle"].replace(["Gambrel", "Flat", "Mansard", "Shed"], "Other")
new["RoofStyle"].value_counts()  # NOT enough variety!
new.head()

# RoofMatl
data["RoofMatl"].isnull().sum()
data["RoofMatl"].value_counts()
    # standard shingle?: Y (1) or N (0)
new["RoofMatl"] = np.where(data["RoofMatl"] == "CompShg", 1, 0)
new["RoofMatl"].value_counts()  # NOT enough variety!

# Exterior1st and Exterior2nd
data["Exterior1st"].isnull().sum()
data["Exterior2nd"].isnull().sum()

data["Exterior1st"].fillna("Other").value_counts()
Exterior1st = data["Exterior1st"] \
.replace(["BrkFace", "WdShing", "AsbShng", "Stucco", "BrkComm", "AsphShn", "Stone", "CBlock", "ImStucc"], "Other")
Exterior1st.value_counts()

data["Exterior2nd"].fillna("Other").value_counts()
Exterior2nd = data["Exterior2nd"] \
.replace(["Wd Shng", "BrkFace", "Stucco", "AsbShng", "Brk Cmn", "ImStucc", "Stone", "AsphShn", "CBlock", "Other"], "Other")
Exterior2nd.value_counts()

np.equal(Exterior1st, Exterior2nd).value_counts()  # check if both columns are same
    # since both variables roughly have the same distribution
    # and most houses have only one exterior material, keep only one of them
new["Exterior"] = Exterior1st
new["Exterior"].value_counts()
new.head()

# MasVnrType
data["MasVnrType"].isnull().sum()
data["MasVnrType"].value_counts()
new["MasVnrType"] = data["MasVnrType"].fillna("None")
new["MasVnrType"].value_counts()
new.head()

# MasVnrArea

# ExterQual and ExterCond
data["ExterQual"].isnull().sum()
data["ExterCond"].isnull().sum()
original = data["ExterQual"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
current = data["ExterCond"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
original.value_counts()
current.value_counts()
cond = np.subtract(current, original)
cond.value_counts()
new["ExterCond"] = pd.Series(cond.map(lambda x: "depreciated" if x < 0 else "improved" if x > 0 else "no change"))
new["ExterCond"].value_counts()
new.head()

# Foundation
data["Foundation"].isnull().sum()
data["Foundation"].value_counts()
new["Foundation"] = data["Foundation"].replace(["BrkTil", "Slab", "Stone", "Wood"], "Other")
new["Foundation"].value_counts()
new.head()

# BsmtQual
data["BsmtQual"].isnull().sum()  # NA is not missing
data["BsmtQual"].value_counts()
new["BsmtQual"] = data["BsmtQual"].fillna("None") \
.map({"Ex": 4, "Gd": 3, "TA": 2, "Fa": 1, "Po": 1, "None": 0})
new["BsmtQual"].value_counts()
new.head()

# BsmtCond
data["BsmtCond"].isnull().sum()  # NA is not missing
data["BsmtCond"].value_counts()
new["BsmtCond"] = data["BsmtCond"].fillna("None") \
.map({"Ex": 4, "Gd": 3, "TA": 2, "Fa": 1, "Po": 1, "None": 0})
new["BsmtCond"].value_counts()  # NOT enough variety!
new.head()

# BsmtExposure
data["BsmtExposure"].isnull().sum()  # NA is not missing
data["BsmtExposure"].value_counts()
new["BsmtExposure"] = data["BsmtExposure"].fillna("None") \
.map({"Gd": 3, "Av": 2, "Mn": 1, "No": 0, "None": 0})
new["BsmtExposure"].value_counts()
new.head()

# BsmtFinType1 and BsmtFinType2
data["BsmtFinType1"].isnull().sum()  # NA is not missing
data["BsmtFinType2"].isnull().sum()  # NA is not missing
data["BsmtFinType1"].value_counts()
data["BsmtFinType2"].value_counts()
type1 = data["BsmtFinType1"].fillna("None") \
.map({"GLQ": 3, "ALQ": 2, "Rec": 2, "BLQ": 1, "LwQ": 1, "Unf": 0, "None": 0})
type2 = data["BsmtFinType2"].fillna("None") \
.map({"GLQ": 3, "ALQ": 2, "Rec": 2, "BLQ": 1, "LwQ": 1, "Unf": 0, "None": 0})
type1.value_counts()
type2.value_counts()
np.equal(type1, type2).value_counts()  # most houses have 2nd rating
    # basement unfinished?: Y (1) or No (0)
new["BsmtFinType"] = pd.Series(np.logical_or(type1 == 0.0, type2 == 0.0))
new["BsmtFinType"] = np.where(new["BsmtFinType"] == True, 1, 0)
new["BsmtFinType"].value_counts()  # NOT enough variety!
new.head()

# BsmtFinSF1 and BsmtFinSF2

# BsmtUnfSF

# TotalBsmtSF

# Heating

# HeatingQC

# CentralAir
data["CentralAir"].isnull().sum()
data["CentralAir"].value_counts()
new["CentralAir"] = np.where(data["CentralAir"] == "Y", 1, 0)
new["CentralAir"].value_counts()  # NOT enough variety!
new.head()

# Electrical

# 1stFlrSF and 2ndFlrSF

# LowQualFinSF

# GrLivArea

# BsmtFullBath, BsmtHalfBath, FullBath, HalfBath

# Bedroom

# Kitchen

# KitchenQual

# TotRmsAbvGrd

# Functional

# Fireplaces
data["Fireplaces"].isnull().sum()
data["Fireplaces"].value_counts()
    # has fireplace?: Y (1) or No (0)
new["Fireplaces"] = np.where(data["Fireplaces"] > 0, 1, 0)
print new["Fireplaces"].value_counts()
new.head()

# FireplaceQu
data["FireplaceQu"].isnull().sum()
data["FireplaceQu"].value_counts()  # NA isn't missing
new["FireplaceQu"] = data["FireplaceQu"].fillna("None") \
.map({"Ex": 3, "Gd": 3, "TA": 2, "Fa": 1, "Po": 1, "None": 0})
print new["FireplaceQu"].value_counts()
new.head()

# GarageType

# GarageYrBlt

# GarageFinish

# GarageCars and GarageArea

# GarageQual and GarageCond

# PavedDrive

# WoodDeckSF

# OpenPorchSF, EnclosedPorch, 3SsnPorch, ScreenPorch

# PoolArea

# PoolQC

# Fence

# MiscFeature

# MiscVal

# MoSold and YrSold

# SaleType

# SaleCondition
