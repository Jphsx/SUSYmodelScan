

def getBF(decayBlock,  nda, Xino, ff ):
	#nda is number of daughters in decay
	#Xino is pdgcode of susy daughter
	#ff is the list of fermions allowed in the decay being summed (abs(pdg))
	
	BFsum=0.
	for line in decayBlock:
		if(line[0] == '#' or line[0] == 'DECAY'):
			continue
		if(int(line[1]) == nda):
			if( abs(int(line[2])) == Xino ):
				for i in range(3,(3+(nda-1))):
					pdg = abs(int(line[i]))
					if( pdg in ff ):
						if( i == (3+(nda-2)) ):
							BFsum = BFsum + float( line[0] ) 
					else:
						break
	return BFsum
	
def concatToLine( objects ):
	cmd=''
	for obj in objects:
		cmd += str(obj)+" "
		
	return cmd

#scan through list of SLHA models and aggregate those with specific masses
#listname="HiggsinoListofLists.list"
#outname = "Higgsino1.csv"
#listname="BinoListofLists.list"
#outname = "Bino1.csv"
listname="WinoListofLists.list"
outname = "Wino1.csv"


fout = open(outname,"w")
fout.write("ModelNum m_N2 m_N1 m_C1 dM X0G X0qq X0ll X0nn X1qq X1ln \n")

listoflists=[]
with open(listname) as f1:
	listoflists = f1.readlines()
	
#print(listoflists)

#scan 1 list at a time and scan 1 file at a time from every list
#try selecting with specific neutralino masses
#try selecting with specific mass splitting
N2_req = 300.
N1_req = 290.
C1_req = 275.
Mass_variance = 0.5

quarks = [1,2,3,4,5]
nu = [ 12,14,16 ]
lep = [ 11,13,15 ]
lepnu = [ 11,12,13,14,15,16 ]
gamma = [22]
modelCount=0
for ilist in listoflists:
	with open(ilist.rstrip()) as f2:
		slhafiles = f2.readlines()

		for slha in slhafiles:
			#print(slha)
			with open(slha.rstrip()) as f3:
				model = f3.readlines()
				inMassBlock=False
				inDecayBlock=False
				#for each model store the mass block
				mass_block_content = []
				decay_block_content = []
				for line in model:

					#print(line)
					line2 = line.split()
					#print(line2)
					if(len(line2) > 2):
						if(  (str(line2[0]) == 'BLOCK') and (str(line2[1]) == 'MASS')):
							inMassBlock=True
						
						if(inMassBlock and (str(line2[0])=='BLOCK') and (str(line2[1]) != 'MASS') ):
							inMassBlock=False
							#break
						if(inMassBlock):
							#print(line)
							mass_block_content.append(line2)
							
					if(len(line2) > 1):
						if( str(line2[0]) == 'DECAY' and str(line2[1]) == '1000023'):
							inDecayBlock=True
						
						if(inDecayBlock and (str(line2[0])=='#') and (str(line2[1])=='PDG')):
							inDecayBlock=False
							break
						if(inDecayBlock):
							decay_block_content.append(line2)
						
							
				#scan mass block
				#print(mass_block_content)
				M_N1,M_N2, M_C1 = 0.,0.,0.
			#	modelCount = 0
				#print("MODEL")
				for masslist in mass_block_content:
					if(masslist[0] != 'BLOCK' or masslist[0] != '#'):
						if(masslist[0] == '1000022'):
							M_N1 = float(masslist[1])
						if(masslist[0] == '1000023'):
							M_N2 = float(masslist[1])
						if(masslist[0] == '1000024'):
							M_C1 = float(masslist[1])
				#print("N1 ",M_N1, " N2 ",M_N2, " M_C1 ", M_C1)
				#M_N1,M_N2,M_C1 = abs(M_N1), abs(M_N2), abs(M_C1)
				#print("N1 ",M_N1, " N2 ",M_N2, " M_C1 ", M_C1)
				#dM_N1, dM_N2 = ( abs( M_N1 - N1_req ) ), ( abs(M_N2 - N2_req) )
				#print(dM_N1, dM_N2)
				#if( (dM_N1 < Mass_variance) and (dM_N2 < Mass_variance) ):
				#	modelCount = modelCount + 1
				#	print("N1 ",M_N1, " N2 ",M_N2, " M_C1 ", M_C1)	
				#	print(modelCount)
				DM = N2_req - N1_req
				DMC = N2_req - C1_req
				dM = abs(M_N2) - abs(M_N1)
				dMC = abs(M_N2) - abs(M_C1)
				if( abs(DM-dM) <= Mass_variance):# and abs(DMC-dMC) <= Mass_variance ):
					#print("MODEL ",slha)
					modelCount = modelCount + 1
					#print("N1 ",M_N1, " N2 ",M_N2, " M_C1 ", M_C1)
					#for decay in decay_block_content:
					#	print(decay)
					
					X0qqBF=getBF(decay_block_content, 3,1000022, quarks)
					X0llBF=getBF(decay_block_content, 3,1000022, lep)
					X0nunuBF=getBF(decay_block_content,3,1000022, nu)
					X1qqBF=getBF(decay_block_content,3,1000024,quarks)
					X1lnuBF=getBF(decay_block_content,3,1000024,lepnu)
					
					X0g = getBF(decay_block_content, 2, 1000022, gamma)
					#print("ModelNum m_N2 m_N1 m_C1 dM X0G X0qq X0ll X0nn X1qq X1ln")
					#print(slha, M_N2, M_N1, M_C1, dM, X0g, X0qqBF, X0llBF, X0nunuBF, X1qqBF, X1lnuBF)
					mdl = slha.split("/")
					mdl = mdl[-1].rstrip()
					cmd = concatToLine([mdl, M_N2, M_N1, M_C1, dM, X0g, X0qqBF, X0llBF, X0nunuBF, X1qqBF, X1lnuBF] )
					fout.write(cmd+"\n")
					#fout.write("%s %d %d %d %d" % (slha, M_N2, M_N1, M_C1, dM))
					#fout.write("%d %d %d %d %d %d \n" % (X0g, X0qqBF, X0llBF, X0nunuBF, X1qqBF, X1lnuBF))
					#print()
					#TotalBF=X0qqBF+X0llBF+X0nunuBF+X1qqBF+X1lnuBF+X0g
					#print("TOTAL BF = ", TotalBF)
					#if(modelCount%1000 == 0):
					#	print("models selected = ",modelCount)
						
					
print("total models selected = ", modelCount)						
fout.close()
f1.close()
f2.close()
f3.close()				
				
			
		

