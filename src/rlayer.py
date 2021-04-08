def getlheight(filelist):
	for i in range(len(filelist)):
		if ";Layer height:" in filelist[i]:
			value=filelist[i]
			value=value[value.index(':')+2:]
			return(value)

def getnlayers(filelist):
	for i in range(len(filelist)):
		if ";LAYER_COUNT:" in filelist[i]:
			value=filelist[i]
			value=value[value.index(':')+1:]
			return(value)

def makefile(filelist):
	writer.writelines(filelist)

def overridefan(filelist):
	topop=[]
	for i in range(len(filelist)): 
		if "M106" in filelist[i]:
			topop.append(i)
	for i in range(len(topop)):
		filelist.pop(topop[i]-i)
	return filelist

def getfirst(filelist,vlayer):
	endlayer=";LAYER:"+str(vlayer)
	zerolayer=";LAYER:0"
	value2=0
	for i in range(len(filelist)):
		if zerolayer in filelist[i]:
			value1=i
		if endlayer in filelist[i] and value2==0:
			value2=i
		for j in range(value2,0,-1):
			if "E" in filelist[j] and ";" not in filelist[j]:
				evalue=filelist[j][filelist[j].index('E'):]
				break
	for i in range(value2-value1):
		filelist.pop(value1)
	filelist.insert(value1,"G92 "+str(evalue))
	return(filelist)	

def getlast(filelist,flayer):
	flayer=";LAYER:"+str(int(flayer))
	for i in range(len(filelist)):
		if flayer in filelist[i]:
			value1=i
		if "M140 S0" in filelist[i]:
			value2=i
			break
	for i in range(value2-value1):
		filelist.pop(value1)
	return(filelist)

def zadjust(filelist,ilayer,flayer,delta):
	ilayer=";LAYER:"+str(ilayer)+'\n'
	flayer=";LAYER:"+str(flayer-1)+'\n'
	value2=0
	value1=0
	layercounter=0
	for i in range(len(filelist)):
		line=filelist[i] 
		if ilayer == line:
			value1=i
		if flayer == line:
			value2=i
	for i in range(value1,value2,1):
		line=filelist[i]
		if "Z" in line and ";" not in line:
			zetaindex=line.index("Z")
			zeta=line[zetaindex+1:]
			prefix=line[:zetaindex+1]
			zeta2=str(format(float(zeta)-delta,'.2f'))
			filelist[i]=prefix+zeta2+'\n'
			layercounter=layercounter+1
	return(filelist)

def addfan(filelist,ilayer,fanlayers):
	layers=[]
	layercount=0
	for i in range(len(filelist)):
		line=filelist[i]
		if line==";LAYER:"+str(ilayer+layercount+1)+'\n' and layercount<fanlayers:
			layers.append(i)
			layercount=layercount+1
	for i in range(layercount):
		line="M106 S"+str(float((i+1)*255.0/len(layers)))+'\n'
		filelist.insert(layers[i]+i,line)
	return(filelist)

filename = "CE3_cubo20x20" # to input
rlayer = 2 # to input, layers to remove in top and bottom
fanl = 2 #layer where fan at 100%, lineal

reader = open(f'{filename}.gcode','r') 
writer = open(f'{filename}R.gcode','w') # processed file

glist = reader.readlines()

layerh=float(getlheight(glist)) # parameters
nlayers=int(getnlayers(glist))
zremove=layerh*rlayer
startlayer=rlayer
endlayer=nlayers-rlayer

glist=overridefan(glist) #modifications
glist=getfirst(glist,startlayer)
glist=getlast(glist,endlayer)
glist=zadjust(glist,startlayer,endlayer,zremove)
glist=addfan(glist,startlayer,fanl)

makefile(glist)


