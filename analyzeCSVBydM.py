

import pandas as pd
import ROOT as rt
import array 
import numpy as np
pd.set_option('display.max_columns', None)

#df = pd.read_csv('Wino1.csv', sep=' ')
#df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#print(df)
modelTypes = ["Wino","Bino","Higgsino"]
modelType = modelTypes[2]
path = modelType+"_dMcsv/"
#collect all the dfs 
dMSet = [2,5,10,15,20,30,40,50]
dfset=[]
[ dfset.append(pd.read_csv( path+modelType+"_dM"+str(x)+".csv", sep=' ')) for x in dMSet ]
for i,x in enumerate(dfset):
	dfset[i]=dfset[i].loc[:, ~dfset[i].columns.str.contains('^Unnamed')]

print(dfset[2])
#exit()

outfile = rt.TFile(modelType+"Analyze.root","RECREATE")
customBins = np.array([1,3,7,13,17,23,37,43,57],dtype='float64')
#plot in 2D dM 1 for each x0g x0z x0w 
z2d = rt.TH2D("z2d","N2 #rightarrow N1+Zstar BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
w2d = rt.TH2D("w2d","N2 #rightarrow N1+Wstar BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
g2d = rt.TH2D("g2d","N2 #rightarrow N1+#gamma BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
#profile each 2d

for dm,df in zip(dMSet, dfset):
	znp = ( df["X0ll"]+df["X0nn"]+df["X0qq"] ).to_numpy()
	wnp = ( df["X1qq"]+df["X1ln"] ).to_numpy()
	gnp = df["X0G"].to_numpy()
	[ z2d.Fill(dm,x) for x in znp ]
	[ w2d.Fill(dm,x) for x in wnp ]
	[ g2d.Fill(dm,x) for x in gnp ]

z2dprf = z2d.ProfileX()
w2dprf = w2d.ProfileX()
g2dprf = g2d.ProfileX()

outfile.WriteTObject(z2d)
outfile.WriteTObject(w2d)
outfile.WriteTObject(g2d)
outfile.WriteTObject(z2dprf)
outfile.WriteTObject(w2dprf)
outfile.WriteTObject(g2dprf)


c1 = rt.TCanvas("c1","c1")
z2dprf.SetLineColor(rt.kGreen)
z2dprf.Draw()
w2dprf.SetLineColor(rt.kBlue)
w2dprf.Draw("SAME")
g2dprf.SetLineColor(rt.kRed)
g2dprf.Draw("SAME")

#exit()

#compare Z* decay modes in 2D by dM
zqq2d = rt.TH2D("zqq2d","N2 #rightarrow N1+Zstar(qq) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
zll2d = rt.TH2D("zll2d","N2 #rightarrow N1+Zstar(ll) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
znn2d = rt.TH2D("znn2d","N2 #rightarrow N1+Zstar(#nu#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)

for dm,df in zip(dMSet,dfset):
	zqqnp = ( df["X0qq"] ).to_numpy()
	zllnp = ( df["X0ll"] ).to_numpy()
	znnnp = ( df["X0nn"] ).to_numpy()
	[ zqq2d.Fill(dm,x) for x in zqqnp ]
	[ zll2d.Fill(dm,x) for x in zllnp ]
	[ znn2d.Fill(dm,x) for x in znnnp ]
	
zqq2dprf = zqq2d.ProfileX()
zll2dprf = zll2d.ProfileX()
znn2dprf = znn2d.ProfileX()

outfile.WriteTObject(zqq2d)
outfile.WriteTObject(zll2d)
outfile.WriteTObject(znn2d)
outfile.WriteTObject(zqq2dprf)
outfile.WriteTObject(zll2dprf)
outfile.WriteTObject(znn2dprf)

c2 = rt.TCanvas("c2","c2")
zqq2dprf.SetLineColor(rt.kOrange)
zll2dprf.SetLineColor(rt.kBlack)
znn2dprf.SetLineColor(rt.kMagenta)
zqq2dprf.Draw()
zll2dprf.Draw("SAME")
znn2dprf.Draw("SAME")

#exit()
#count the number of models per dm
nmodel = rt.TH1D("nmodel", "Number of models per #Delta m; dM;nModels", len(customBins)-1, customBins)

#df.shape[0]
for i,df in enumerate(dfset):
	nmodel.SetBinContent(i+1, df.shape[0])
	
outfile.WriteTObject(nmodel)

c3 = rt.TCanvas("c3","c3")
nmodel.Draw()

#exit()

#look at BF breakdown of Zstar ll decays
zee2d = rt.TH2D("zee2d","N2 #rightarrow N1+Zstar(ee) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)
zmm2d = rt.TH2D("zmm2d","N2 #rightarrow N1+Zstar(#mu#mu) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)
ztt2d = rt.TH2D("ztt2d","N2 #rightarrow N1+Zstar(#tau#tau) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)


for dm,df in zip(dMSet,dfset):
	zeenp = ( df["X0ee"] ).to_numpy()
	zmmnp = ( df["X0mm"] ).to_numpy()
	zttnp = ( df["X0tt"] ).to_numpy()
	[ zee2d.Fill(dm,x) for x in zeenp ]
	[ zmm2d.Fill(dm,x) for x in zmmnp ]
	[ ztt2d.Fill(dm,x) for x in zttnp ]
	
zee2dprf = zee2d.ProfileX()
zmm2dprf = zmm2d.ProfileX()
ztt2dprf = ztt2d.ProfileX()

outfile.WriteTObject(zee2d)
outfile.WriteTObject(zmm2d)
outfile.WriteTObject(ztt2d)
outfile.WriteTObject(zee2dprf)
outfile.WriteTObject(zmm2dprf)
outfile.WriteTObject(ztt2dprf)

c3 = rt.TCanvas("c3","c3")
zee2dprf.SetLineColor(rt.kGreen)
zmm2dprf.SetLineColor(rt.kBlue)
ztt2dprf.SetLineColor(rt.kOrange)
zee2dprf.Draw()
zmm2dprf.Draw("SAME")
ztt2dprf.Draw("SAME")

#exit()
#look at BF breakdown of Wstar ln decays
wen2d = rt.TH2D("wen2d","N2 #rightarrow C1+Wstar(e#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)
wmn2d = rt.TH2D("wmn2d","N2 #rightarrow C1+Wstar(#mu#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)
wtn2d = rt.TH2D("wtn2d","N2 #rightarrow C1+Wstar(#tau#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,0.05)


for dm,df in zip(dMSet,dfset):
	wennp = ( df["X1en"] ).to_numpy()
	wmnnp = ( df["X1mn"] ).to_numpy()
	wtnnp = ( df["X1tn"] ).to_numpy()
	[ wen2d.Fill(dm,x) for x in wennp ]
	[ wmn2d.Fill(dm,x) for x in wmnnp ]
	[ wtn2d.Fill(dm,x) for x in wtnnp ]
	
wen2dprf = wen2d.ProfileX()
wmn2dprf = wmn2d.ProfileX()
wtn2dprf = wtn2d.ProfileX()

outfile.WriteTObject(wen2d)
outfile.WriteTObject(wmn2d)
outfile.WriteTObject(wtn2d)
outfile.WriteTObject(wen2dprf)
outfile.WriteTObject(wmn2dprf)
outfile.WriteTObject(wtn2dprf)

c4 = rt.TCanvas("c4","c4")
wen2dprf.SetLineColor(rt.kGreen)
wmn2dprf.SetLineColor(rt.kBlue)
wtn2dprf.SetLineColor(rt.kOrange)
wen2dprf.Draw()
wmn2dprf.Draw("SAME")
wtn2dprf.Draw("SAME")

#exit()

#look at BF breakdown of Wstar in chargino decays
wen2dc1 = rt.TH2D("wen2dc1","C1 #rightarrow N1+Wstar(e#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
wmn2dc1 = rt.TH2D("wmn2dc1","C1 #rightarrow N1+Wstar(#mu#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)
wtn2dc1 = rt.TH2D("wtn2dc1","C1 #rightarrow N1+Wstar(#tau#nu) BF;dM;BF",len(customBins)-1,customBins,50,0,1.)


for dm,df in zip(dMSet,dfset):
	wennpc1 = ( df["X0en"] ).to_numpy()
	wmnnpc1 = ( df["X0mn"] ).to_numpy()
	wtnnpc1 = ( df["X0tn"] ).to_numpy()
	[ wen2dc1.Fill(dm,x) for x in wennpc1 ]
	[ wmn2dc1.Fill(dm,x) for x in wmnnpc1 ]
	[ wtn2dc1.Fill(dm,x) for x in wtnnpc1 ]
	
wen2dc1prf = wen2dc1.ProfileX()
wmn2dc1prf = wmn2dc1.ProfileX()
wtn2dc1prf = wtn2dc1.ProfileX()

outfile.WriteTObject(wen2dc1)
outfile.WriteTObject(wmn2dc1)
outfile.WriteTObject(wtn2dc1)
outfile.WriteTObject(wen2dc1prf)
outfile.WriteTObject(wmn2dc1prf)
outfile.WriteTObject(wtn2dc1prf)

c5 = rt.TCanvas("c5","c5")
wen2dc1prf.SetLineColor(rt.kGreen)
wmn2dc1prf.SetLineColor(rt.kBlue)
wtn2dc1prf.SetLineColor(rt.kOrange)
wen2dc1prf.Draw()
wmn2dc1prf.Draw("SAME")
wtn2dc1prf.Draw("SAME")

exit()
#mtest = rt.TH1D("test","test mN2",100,100,1000)

#mn2 = df["m_N2"].to_numpy()
#print(mn2)
#[ mtest.Fill(abs(x)) for x in mn2 ]

#mtest.Draw()

dM=10. #-> 90% guaranteed mass so adjust bins based on dM


#create distributions of N2-C1/N2 and C1-N1/N2
n2c1_h = rt.TH1D("n2c1_h","Chargino N2 mass fraction;m_{C1}/m_{N2};N Models",20,0.9,1)
c1n1_h = rt.TH1D("c1n1_h","LSP C1 mass fraction;m_{N1}/m_{C1};N Models",20,0.9,1)

n2c1 = ((df["m_C1"].abs())/df["m_N2"].abs()).to_numpy()
print(n2c1)
[ n2c1_h.Fill(x) for x in n2c1 ]

c1 = rt.TCanvas("c1","c1")

n2c1_h.Draw("HIST")


c1n1 = ((df["m_N1"].abs())/df["m_C1"].abs()).to_numpy()
[ c1n1_h.Fill(x) for x in c1n1 ]
c1n1_h.SetLineColor(rt.kRed)
c1n1_h.Draw("HIST SAMES")

#check out BF in 1D compare (X0g X0Z X1W)
x0Z_h = rt.TH1D("x0z_h", "N1 Zstar 3bd BF",100,0,1) 
x0W_h = rt.TH1D("x0w_h", "N1 Wstar 3bd BF",100,0,1)
x0G_h = rt.TH1D("x0g_h", "N1 gamma 2bd BF",100,0,1)

x0z = ( df["X0ll"]+df["X0nn"]+df["X0qq"] ).to_numpy()
x0w = ( df["X1qq"]+df["X1ln"] ).to_numpy()
x0g = df["X0G"].to_numpy()

[ x0Z_h.Fill(x) for x in x0z ]
[ x0W_h.Fill(x) for x in x0w ]
[ x0G_h.Fill(x) for x in x0g ]

x0Z_h.SetLineColor((rt.kGreen))
x0W_h.SetLineColor((rt.kBlue))
x0G_h.SetLineColor((rt.kRed))

c2 = rt.TCanvas("c2","c2")
x0Z_h.Draw()
x0W_h.Draw("SAME")
x0G_h.Draw("SAME")


#check out BF in 1D compare N2*N1 <0 and N2*N1>0 eigenstates separate
#dfm = df.loc[ df["m_N2"]*df["m_N1"] < 0. ]
#dfp = df.loc[ df["m_N2"]*df["m_N1"] > 0. ]
df["sgn"] = (df["m_N2"] * df["m_N1"])/(df["m_N2"].abs() * df["m_N1"].abs())
dfm = df.loc[ df["sgn"] < 0. ]
dfp = df.loc[ df["sgn"] > 0. ]

print("AFTER CHECK")
print(df)
#positive case
x0Zp_h = rt.TH1D("x0zp_h", "N1 Zstar 3bd BF N2*N1>0",100,0,1) 
x0Wp_h = rt.TH1D("x0wp_h", "N1 Wstar 3bd BF N2*N1>0",100,0,1)
x0Gp_h = rt.TH1D("x0gp_h", "N1 gamma 2bd BF N2*N1>0",100,0,1)

x0zp = ( dfp["X0ll"]+dfp["X0nn"]+dfp["X0qq"] ).to_numpy()
x0wp = ( dfp["X1qq"]+dfp["X1ln"] ).to_numpy()
x0gp = dfp["X0G"].to_numpy()

[ x0Zp_h.Fill(x) for x in x0zp ]
[ x0Wp_h.Fill(x) for x in x0wp ]
[ x0Gp_h.Fill(x) for x in x0gp ]

x0Zp_h.SetLineColor((rt.kGreen))
x0Wp_h.SetLineColor((rt.kBlue))
x0Gp_h.SetLineColor((rt.kRed))

c3 = rt.TCanvas("c3","c3")
x0Zp_h.Draw()
x0Wp_h.Draw("SAME")
x0Gp_h.Draw("SAME")


#negative case
x0Zm_h = rt.TH1D("x0zm_h", "N1 Zstar 3bd BF N2*N1<0",100,0,1) 
x0Wm_h = rt.TH1D("x0wm_h", "N1 Wstar 3bd BF N2*N1<0",100,0,1)
x0Gm_h = rt.TH1D("x0gm_h", "N1 gamma 2bd BF N2*N1<0",100,0,1)

x0zm = ( dfm["X0ll"]+dfm["X0nn"]+dfm["X0qq"] ).to_numpy()
x0wm = ( dfm["X1qq"]+dfm["X1ln"] ).to_numpy()
x0gm = dfm["X0G"].to_numpy()

[ x0Zm_h.Fill(x) for x in x0zm ]
[ x0Wm_h.Fill(x) for x in x0wm ]
[ x0Gm_h.Fill(x) for x in x0gm ]

x0Zm_h.SetLineColor((rt.kGreen))
x0Wm_h.SetLineColor((rt.kBlue))
x0Gm_h.SetLineColor((rt.kRed))

c4 = rt.TCanvas("c4","c4")
x0Zm_h.Draw()
x0Wm_h.Draw("SAME")
x0Gm_h.Draw("SAME")











