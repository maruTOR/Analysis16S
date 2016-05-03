# ver 1.2# date: 140528

file = commandArgs(trailingOnly=TRUE)[1]
prefix = commandArgs(trailingOnly=TRUE)[2]
ofile = paste(prefix,".pdf",sep="")
ofile2 = paste(prefix,"_legend.pdf",sep="")
#
data = read.table(file,sep="\t",header=T,row.names=1)
data = as.matrix(data)
#
sums = apply(data,2,sum)
normalize = function(x,sums){
	x / sums * 100
}
data2 = t(apply(data,1,normalize,sums))
#
labels = rownames(data2)
num = length(labels)
#
if(sum(labels=="Others") == 1) num = num - 1
if(sum(labels=="Undetermined") == 1) num = num - 1
#
colors = c("#E41A1C","#377EB8","#4DAF4A","#984EA3","#FF7F00","#FFFF33","#A65628",
	"#F781BF","#66C2A5","#FC8D62","#8DA0CB","#E78AC3","#A6D854","#FFD92F",
	"#E5C494","#B3B3B3","#8DD3C7","#FFFFB3","#BEBADA","#FB8072","#80B1D3",
	"#FDB462","#B3DE69","#FCCDE5","#D9D9D9","#BC80BD","#CCEBC5","#FFED6F",
	"#A6CEE3","#1F78B4","#B2DF8A","#33A02C","#FB9A99","#E31A1C","#FDBF6F",
	"#FF7F00","#CAB2D6","#6A3D9A","#FFFF99","#B15928")
cols = colors[1:num]
if(sum(labels=="Others") == 1) cols = c(cols,"#444444")
if(sum(labels=="Undetermined") == 1) cols = c(cols,"#000000")
names(cols) = labels

pdf(ofile)
par(mar=c(7,4,4,2))
barplot(data2,col=cols,border=cols,las=2)
dev.off()
#
pdf(ofile2)
par(mar=c(5,4,4,2))
plot.new()
legend(x=0.1,y=0.9,legend=rownames(data2),fill=cols,border=cols)
dev.off()
