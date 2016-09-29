# install.packages("randomForest")
# install.packages("DMwR")
library(randomForest)
library(DMwR)


# training data
train = read.csv("train.csv", header = TRUE)
head(train)
summary(train)
dim(train)


# impute missing values in train data via random forest
# -----------------------------------------------------

# find variables with NA's
data.frame(sort(sapply(train, function(i) sum(is.na(i))), decreasing = TRUE))
naVars = names(sort(sapply(train, function(i) sum(is.na(i))), decreasing = TRUE)[1:19])

# NA for factor variables is not a literal NA, according to the codebook
facVars = names(train[, sapply(train, is.factor)])	# find factor variables
naFacVars = intersect(naVars, facVars)			# find factor variables with NA
for (i in naFacVars) {
	# append "None" to factor levels
	train[[i]] = factor(train[[i]], levels = c(levels(train[[i]]), "None"))
	train[[i]][is.na(train[[i]])] = "None"		# replace NA with None
}

lapply(train, levels)


# replace actual NA in data with randomForest's imputation function
trainImp = rfImpute(SalePrice ~ ., train)		# requires response variable

head(trainImp)
colnames(trainImp)[colSums(is.na(trainImp)) > 0]	# check no NA remains in data


# handle different data types
# ---------------------------

table(sapply(train, class))
table(sapply(trainImp, class))

naIntVars = setdiff(naVars, naFacVars)			# find integer variables with NA
for (i in naIntVars) {
	trainImp[[i]] = as.integer(round(trainImp[[i]]))
}
table(sapply(trainImp, class))

write.csv(trainImp, "trainImp.csv", row.names = FALSE)
