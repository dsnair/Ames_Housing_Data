library(randomForest)


# training data
train = read.csv("trainImp.csv", header = TRUE)
head(train)
summary(train)
dim(train)

# testing data
test = read.csv("testImp.csv", header = TRUE)
head(test)
summary(test)
dim(test)


# handle test data having different levels than the training data for factor variables
# ------------------------------------------------------------------------------------

# variables with different levels are: 
# Utilities, Condition2, RoofMatl, Exterior1st, Exterior2nd, Heating, Electrical, GarageQual
lapply(train, levels)
lapply(test, levels)

facVars = names(train[, sapply(train, is.factor)])	# factor variables from train data

# append levels of train data to test data
for (i in facVars) {
	levels = unique(c(levels(train[[i]]), levels(test[[i]])))
	train[[i]] = factor(train[[i]], levels = levels)
	test[[i]] = factor(test[[i]], levels = levels)
}

lapply(train, levels)
lapply(test, levels)


# fit random forest for SalesPrice
# --------------------------------

train = within(train, rm(Id))	# drop Id
test = within(test, rm(Id))

# ?randomForest
fitRF = randomForest(SalePrice ~ ., data = train, importance = TRUE)  # For regression, state variables as formula
fitRF

# training error
trainRF = predict(fitRF, newdata = train, type = "response")
mean((trainRF - train[["SalePrice"]])^2)			# MSE; difficult to understand


# fit random forest for log10(SalesPrice)
# ---------------------------------------

# SalePrice is skewed to the right, so take its log base 10
fitLogRF = randomForest(log10(train[, 1]) ~ ., data = train[, 2:80], importance = TRUE)
fitLogRF

trainLogRF = predict(fitLogRF, newdata = train, type = "response")
mean((trainLogRF - log10(train[, 1]))^2)			# MSE; easy to understand


# make predictions from random forests
# ------------------------------------

predRF = predict(fitRF, newdata = test, type = "response")
predLogRF = predict(fitLogRF, newdata = test, type = "response")
10^predLogRF

write.csv(data.frame(Id = 1461:2919, SalePrice = predRF), "submission.csv", row.names = FALSE)


# feature extraction
# ------------------

# cross-validation
result = rfcv(train[, 2:80], train[, 1], cv.fold = 5, step = 0.9)
result

	# With step=0.9, the 1st row of results$error.cv is the number of predictors used, which is obtained as follows:
	# 80-1=79, round(79*0.9)=71, round(71*0.9)=64, etc.
	# The 2nd row is the cross-validation error for each of the models fit.

	# error decreases as number of predictors increases. 
	# The error stabilizes after 4 predictors, indicating that the rest are extraneous predictors
png("CVerror_RF.png")
with(result, plot(n.var, error.cv, type = "o", lwd = 2))
dev.off()


# variable importance
round(importance(fitRF), 2)			# higher the %IncMSE, more important the variable
round(importance(fitLogRF), 2)

	# GrLvArea, Neighborhood, TotalBsmtSF, OverallQual are the most important predictors
png("variable_importance_plot_fitRF.png")
varImpPlot(fitRF)				# variable importance plot
dev.off()

png("variable_importance_plot_fitLogRF.png")
varImpPlot(fitLogRF)
dev.off()

	# find number of times the variables were used in a forest. Important variables will be used more frequently
freqRF = data.frame(names(train), freq = varUsed(fitRF, by.tree = FALSE, count = TRUE))
freqRF[order(freqRF$freq, decreasing = TRUE), ]

freqLogRF = data.frame(names(train), freq = varUsed(fitLogRF, by.tree = FALSE, count = TRUE))
freqLogRF[order(freqLogRF$freq, decreasing = TRUE), ]
