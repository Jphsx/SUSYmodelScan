

import pandas as pd
import ROOT as rt
pd.set_option('display.max_columns', None)

df = pd.read_csv('Wino1.csv', sep=' ')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print(df)

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











