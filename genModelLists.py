



import os

cmd=''
for ModelNum in range(10,100):
	cmd =  "ls -d $PWD/Higgsino/"+str(ModelNum)+"* > HiggsinoLists/HiggsinoModels"+str(ModelNum)+".list"
	os.system(cmd)


