library(DMwR)

# testing data
test = read.csv("test.csv", header = TRUE)
head(test)
summary(test)
dim(test)


# handle missing values in test data
# -----------------------------------

# find variables with NA's
data.frame(sort(sapply(test, function(i) sum(is.na(i))), decreasing = TRUE))
naVars = names(sort(sapply(test, function(i) sum(is.na(i))), decreasing = TRUE)[1:33])

# NA for factor variables is not a literal NA, according to the codebook
facVars = names(test[, sapply(test, is.factor)])	# find factor variables
naFacVars = intersect(naVars, facVars)			# find factor variables with NA
for (i in naFacVars) {
	# append "None" to factor levels
	test[[i]] = factor(test[[i]], levels = c(levels(test[[i]]), "None"))
	test[[i]][is.na(test[[i]])] = "None"		# replace NA with None
}

lapply(test, levels)


# replace actual NA in data with k-NN algorithm
testImp = knnImputation(test)				# since response variable is unavailable

head(testImp)
colnames(testImp)[colSums(is.na(testImp)) > 0]		# check no NA remains in data


# handle different data types
# ---------------------------

table(sapply(test, class))
table(sapply(testImp, class))

naIntVars = setdiff(naVars, naFacVars)			# find integer variables with NA
for (i in naIntVars) {
	testImp[[i]] = as.integer(round(testImp[[i]]))
}
table(sapply(testImp, class))

write.csv(testImp, "testImp.csv", row.names = FALSE)
