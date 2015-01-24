# plot network of sender -> receipient activity from Enron email logs
# Input: output (enron.csv) from parseEmail.py
# 23-Jan-15  Yen Low 

#source("~/scripts/R/utils.R")
#source("http://bioconductor.org/biocLite.R")
#installnewpackage(c("graph", "Rgraphviz", "chron"))
#biocLite("graph")
#biocLite("Rgraphviz")

require("igraph")
#require("Rgraphviz")  #doesn't allow edge weights
require("chron")

#read sender, receipient, date, time
edges <- read.csv("enron.csv", header=FALSE, as.is=TRUE)
#get all possible unique userids
userids <- unique(c(edges$V1, edges$V2))

#create adjacency matrix
adjMat = matrix(0, nrow=length(userids), ncol=length(userids))
rownames(adjMat) <- userids
colnames(adjMat) <- userids

#format dates
edges$date <- chron(dates=edges$V3, times=edges$V4,
                    format=c(dates="Y/m/d", times="h:m:s"))
#keep only sender-receipient pair
edges <- edges[, -c(3,4)]

for (i in 1:nrow(edges)) {
  x = edges$V1[i]
  y = edges$V2[i]
  adjMat[x, y] <- adjMat[x,y] + 1
}

####### Using igraph
gwt=graph.adjacency(adjMat,diag=F,mode="directed",weighted=TRUE)

#remove insig nodes
threshold=50
deletedVertices=names(degree(gwt))[degree(gwt)<threshold]
gwt2=gwt-deletedVertices

#delete insig edges
deletededges=E(gwt2)[abs(E(gwt2)$weight)<threshold]
gwt2=gwt2-deletededges

#plot(gwt2)
layout=layout.fruchterman.reingold(gwt2,weights=E(gwt2)$weight,area=1000*vcount(gwt2)^2)
png("emailNetwork.png",width=7,height=7,units="in",res=150)
plot(gwt2,layout=layout,vertex.shape="circle",vertex.size=2,
     vertex.color="white",vertex.label=V(gwt2)$name,
     vertex.label.cex=1,vertex.label.family="Helvetica",
     vertex.label.color="black",vertex.label.font=2,
	edge.arrow.width=0.5,edge.width=E(gwt2)$weight/100)
dev.off()


####### Using RGraphViz
#create graph object
#g2 <- new("graphAM", adjMat = adjMat, edgemode="directed",
#          values=list(weight="weight"))

#deg = degree(g2)
#biggies = names(deg$outDegree[which(deg$outDegree > 10)])
#g2a = as(g2, "graphNEL")
#gsa = subGraph(biggies, g2a)
#png("emailNetwork.png",width=7,height=7,units="in",res=150)
#plot(gsa, attrs=list(node=list(color="black", fillcolor="black", shape="plaintext", fontcolor="black"),
#            edge=list(color="gray")))
#dev.off()

