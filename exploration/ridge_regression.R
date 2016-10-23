# install.packages("glmnet")
library(glmnet)


# read train and test data
# ------------------------

train = read.csv("trainImp.csv", header = TRUE)
train = within(train, rm(Id))	# drop Id
head(train)

# testing data
test = read.csv("testImp.csv", header = TRUE)
test = within(test, rm(Id))
head(test)


# prepare data
# ------------

facVars = names(train[, sapply(train, is.factor)])		# factor variables from train data

# append levels of train data to test data
for (i in facVars) {
	levels = unique(c(levels(train[[i]]), levels(test[[i]])))
	train[[i]] = factor(train[[i]], levels = levels)
	test[[i]] = factor(test[[i]], levels = levels)
}

lapply(train, levels)
lapply(test, levels)

# convert data to matrix, and
# convert categorical variables into dummy variables
trainx = model.matrix(SalePrice ~ ., data = train)[, -1]	# remove intercept
trainy = train$SalePrice
testx = model.matrix(~ ., data = test)[, -1]
textx = data.matrix(test)
dim(trainx)
dim(testx)


# fit ridge model
# ---------------

# set a grid of tunning parameter, lambda
grid = 10 ^ seq (from = 10 , to = -2 , length = 100)

# standardize all variables
# alpha = 0 for ridge, alpha = 1 for lasso
model = glmnet(trainx, trainy, alpha = 0, lambda = grid, standardize = TRUE)


# obtain best lambda by cross-validation
# --------------------------------------

set.seed(2016)
cvLambda = cv.glmnet(trainx, trainy, lambda = grid, nfolds = 10, alpha = 0)

cvLambda$lambda 	# lambda values used in model fits
cvLambda$cvm 		# CV error for each lambda
cvLambda$lambda.min	# value of lambda that gives smallest CV error / best lambda

# plot CV error, with upper and lower SD curves, as function of lambda
png("ridge_CVerror.png")
plot.cv.glmnet(cvLambda)
dev.off()


# make predictions
# ----------------

pred = predict.glmnet(model, s = cvLambda$lambda.min, newx = testx)
write.csv(data.frame(Id = 1461:2919, SalePrice = pred), "submission2.csv", row.names = FALSE)

# ridge regression coefficients at best lambda
predict.glmnet(model, s = cvLambda$lambda.min, newx = testx, type = "coefficients")
