library(ggplot2)
setwd('/Users/dodo/Desktop/data/Explatory-Data-Analysis/eda-course-materials/lesson2')

statesInfo <- read.csv('stateData.csv')

subset(stateInfo,state.region==1)

x<- statesInfo[statesInfo$state.region==1,]


reddit <- read.csv('reddit.csv')
summary(reddit)

sortted <- factor(reddit$age.range,ordered = T)
qplot(data = reddit , x = age.range)
