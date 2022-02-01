



import os

cmd=''
model = ["Wino","Bino","Higgsino"]
model = model[2]
for ModelNum in range(10,100):
	cmd =  "ls -d $PWD/"+model+"/"+str(ModelNum)+"* > "+model+"Lists/"+model+"Models"+str(ModelNum)+".list"
	os.system(cmd)


