---
  title: "kickstarter-clustering-kMeans"
  author: "Joe Hernandez"
  date: "April-June 2018"
  output: word_document
---
  
# Load in data
campks <- read.csv("/Users/joehernandez/Desktop/Syracuse University Data Science/IST 565/Project/ks-projects-2016.csv")
campks <- na.omit(campks)
str(campks)

# Remove unnecessary columns and convert to integers
campks_unlabel <- campks[,-c(1:5, 6, 8, 10, 12)]
row.names(campks_unlabel) <- campks$ID
campks_unlabel$pledged <- as.integer(campks_unlabel$pledged)
campks_unlabel$usd.pledged <- as.integer(campks_unlabel$usd.pledged)
campks_unlabel$usd.pledged <- format(campks_unlabel$usd.pledged, scientific = FALSE)
campks_unlabel$usd.pledged <- strtoi(campks_unlabel$usd.pledged, base =0L)
campks_unlabel$profit <- campks_unlabel$pledged - campks_unlabel$goal
str(campks_unlabel)

# Build kMeans algorithm in R
# 15 clusters to differentiate based on main categories
model_r <- kmeans(campks_unlabel, 15)
model_r
# View centroids
model_r$centers
# View cluster assignment
cluster_assignment <- data.frame(campks, model_r$cluster)
View(cluster_assignment)

# Visualize cluster results for kMeans model using Principal Components analysis
library(cluster)
clusplot(campks_unlabel,model_r$cluster,color=TRUE,shade=TRUE,labels=2, lines = 0)


#Decision tree
library("RWeka")
m=J48(state~., data = campks)
m=J48(state~., data = campks, control=Weka_control(U=FALSE, M=2, C=0.5))

e <- evaluate_Weka_classifier(m, numFolds = 10, seed = 1, class = TRUE)
e

pred=predict(m, newdata = campks, type = c("class"))
myids=c("ID")
id_col=campks[myids]
newpred=cbind(id_col, pred)
colnames(newpred)=c("main_category", "state")
View(newpred)

write.csv(newpred, file="/Users/joehernandez/Desktop/Syracuse University Data Science/IST 565/Project/ks-projects-2016-pred.csv", row.names=FALSE)

InfoGainAttributeEval(state ~., data = campks)


