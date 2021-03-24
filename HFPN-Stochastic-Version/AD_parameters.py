'''Parameters'''

from AD_initial_tokens import *

# multiplicative rate factors for increasing rates of slow modules
Abeta_multiplier = 100
tau_multiplier = 10
chol_multiplier = 300
ER_multiplier = 10

neurone_cell_volume = 9008e-15 # L
avagadros_constant = 6.022e23 # mol-1

# Cholesterol homeostasis
# downregulation via chol in ER, linear approximation y = m*x+n
m_t_LDLR_endocyto = - 1.0682
n_t_LDLR_endocyto = 2.0682

fr_t_CYP46A1_metab = 0.08 # CYP46A1-accessible portion of ER cholesterol (to scale Km)
Km_t_CYP46A1_metab = 5.70 * 10 ** 6 / fr_t_CYP46A1_metab
vmax_t_CYP46A1_metab = 3.46 * 10 ** 3

st_t_CYP27A1_metab = 0.13158 # CYP27A1-accessible portion of mitochondrial cholesterol (to scale Km)
Km_t_CYP27A1_metab = 4.77 * 10 ** 7 / st_t_CYP27A1_metab
vmax_t_CYP27A1_metab = 2.56 * 10 ** 3

Km_t_CYP7B1_metab = 2.02 * 10 ** 7
vmax_t_CYP7B1_metab = 4.32 * 10 ** 3

st_t_CYP11A1_metab = 0.13158 # CYP11A1-accessible portion of mitochondrial cholesterol (to scale Km)
Km_t_CYP11A1_metab = 7.59 * 10 ** 7 / st_t_CYP11A1_metab # CHANGED BASED ON SOURCE 2 DATA TO SEE IF IT'S BETTER
vmax_t_CYP11A1_metab = 6.35 * 10 ** 4

Km_t_ApoEchol_cleav = 1.39 * 10 ** 7
vmax_t_ApoEchol_cleav = 1.86 * 10 ** 5

Km_t_LDLR_endocyto = 1.30 * 10 ** 6
vmax_t_LDLR_endocyto = 3.61633 * 10 ** 4

k_t_EE_mat = 0.000924196 # s^-1

k_t_chol_trans_LE_ER = 2.55357 * 10 ** (-4) # s^-1

k_t_chol_trans_LE_mito = 2.36 * 10 ** (-6) # s^-1

k_t_chol_trans_LE_PM = 0.002406761 # s^-1

k_t_chol_trans_ER_PM = 1.725 * 10 ** (-3) # s^-1

k_t_chol_trans_PM_ER = 1.56 * 10 ** (-6) # s^-1

k_t_chol_trans_ER_mito = 1.1713 * 10 ** (-4) # s^-1

k_t_27OHchol_endocyto = 2.65627 * 10 ** 2 # constant rate molecules/second, vary to represent different dietary cholesterol intakes

k_t_chol_trans_PM_ECM = 8.2859 * 10 ** (-5) # s^-1

# upregulation via 24-OHC, linear approximation y = m*x+n
m_t_chol_trans_PM_ECM = 0.2356
n_t_chol_trans_PM_ECM = 0.7644

k_t_24OHchol_exocyto = 7.47488 * 10 ** (-6) # s^-1 

disease_multiplier_27OH = 1 # set to true 


# ER Retraction & Collapse

beta_t_LE_retro = 1.667 #conversion factor of rate of retrograde transport to have it equal to anterograde transport in healthy cells 
dist_t_LE_trans = 75e4 #distance in nm from perinuclear region to axon
mchol_t_LE_retro = 2.27e-9 # scaling effect of cholesterol on retro transport
nchol_t_LE_retro = 1 - mchol_t_LE_retro * it_p_chol_LE # scaling effect of cholesterol on retro transport
vmax_t_LE_retro = 892 #Vmax in nm/s
Km_t_LE_retro = 3510864000 #K_M in particles of ATP
vmax_t_LE_antero = 814 #Vmax in nm/s
Km_t_LE_antero = 614040000 #K_M in particles of ATP
ATPcons_t_LE_trans = 0 # dist_t_LE_trans / 8 # each step of the motor consumes 1 ATP & travels 8 nm; total ATP consumed = number of steps

k_t_RTN3_exp = 113.3
Ab_t_RTN3_aggregation = 641020
dec_t_RTN3_aggregation = 0.762

k_t_RTN3_auto = 0.011111111

k_t_RTN3_lyso = 0.000826667

mitprop_t_RTN3_dys_auto = 0.885


# Abeta Pathology
k_t_asec_exp = 96.8
mchol_t_asec_exp = 7.19184e-9
nchol_t_asec_exp = -1.86
k_t_asec_degr = 1.60e-5

k_t_APP_endocyto = 9.67e-5
dis_t_APP_endocyto = 0.0832033 # Compatible with the ApoE4 0/1 input representing 0 alleles & 2 alleles
k_t_APP_exp = 45000 
dis_t_APP_exp = 0.25 # representing Apoe4 contribution to parameter change
m_t_APP_exp = 0.5/(693.444*it_p_ROS_mito)
n_t_APP_exp = 1 - it_p_ROS_mito * m_t_APP_exp
k_t_APP_endo_event = .0001435 

k_t_bsec_exp = 11.138 
mchol_t_bsec_exp = 1.52842e-8
nchol_t_bsec_exp = 0.532332
nRTN_t_bsec_exp = 1.78571
mRTN_t_bsec_exp = -(nRTN_t_bsec_exp-1)/it_p_RTN3_axon
mROS_t_bsec_exp = .5/it_p_ROS_mito
nROS_t_bsec_exp = 0.5
k_t_bsec_degr = 1.655e-5
mchol_t_APP_bsec_cleav = 8.13035e-12
nchol_t_APP_bsec_cleav = 0.312985106
age_t_APP_bsec_cleav = 0.44

k_t_gsec_exp = 53.92 
k_t_gsec_degr = 1.6e-5 # assume same as asec and bsec for now - may update later

k_t_Ab_degr = 0.00188

Km_t_APP_asec_cleav = 19034084
kcat_t_APP_asec_cleav = 0.0474783

Km_t_APP_bsec_cleav = 37972323
kcat_t_APP_bsec_cleav = 0.002

Km_t_CTF99_gsec_cleav = 169223
kcat_t_CTF99_gsec_cleav = 0.00167


Km_t_Ab_elon = 17343360
Vmax_t_Ab_elon = 1.108

# Tau Pathology
k_t_actv_GSK3b = 8.33e-3
m_t_act_GSK3b = 4.07e-7 # TODO: tune this, increase m to increase effect
n_t_act_GSK3b = 1 - m_t_act_GSK3b * it_p_Ab
dis_t_act_GSK3b = 0.433

k_t_inactv_GSK3b = 7.95e-3

Km_t_phos_tau = 9.22e7
kcat_t_phos_tau = 0.146464095 

Km_t_dephos_tauP = 6.29e7
vmax_t_dephos_tauP = 1.17*1.1e6  # uM/min/ 20 units per mL PP-2A, TODO: conevert unit

k_t_p_GSK3b_deg = 100*1.6e-5 #  (standard protein degradation rate)
k_t_p_GSK3b_exp = k_t_p_GSK3b_deg * it_p_GSK3b_inact


# Calcium Homeostasis
k_t_NCX_PMCA = 10 #multiplied by 10 compared to Gabi's paper (Gabriel, 2020)
k_t_NaK_ATPase= 0.70 
k_t_mCU1=(1*1e6)/(17854326) #rate mCU /average Ca_cyto in homeostasis
k_t_mCU2=(5000)/(17854326) #rate mCU /average Ca_cyto in homeostasis
#k_t_mNCLX=(5000)/(3.6*1e7) #rate mCU /average Ca_cyto in homeostasis
k_t_mNCLX=0.066666667
k_t_MAM=1e6/1.8e9 #rate MAM
k_t_SERCA_no_ATP=0.05638 #(1e6+100)/17854326#0.05638 #100/1785#4#3#2#6#/(5.407*1e9)
k_t_SERCA_ATP=k_t_SERCA_no_ATP/5.42e9 #rate mCU /average ATP in homeostasis
k_t_RyR_IP3R = 100/(1.8*1e9) #rate mCU /average Ca_ER in homeostasis


# Energy metabolism
k_t_krebs = (1.63*10**(-7))*2968656.262/3e7 
k_t_ATP_hydro_mito = 1.92*10**(-2)
k_t_ETC = 2.48*10**(-5)*2968656.262/3e7 
m_t_ETC_inhib_Ab = -1.6438e-6 # -7.5786*10**(-7)
n_t_ETC_inhib_Ab = 1.0559681024 #1 - m_t_ETC_inhib_Ab * it_p_Ab
k_t_ROS_metab = 5.875*10**10
k_t_mito_dysfunc = 1.0495e2 # s^-1 For time step of 0.01 s, change to 1.037984e2
m_t_mito_dysfunc = 3.1855e-5
n_t_mito_dysfunc = 0.61
m_t_mito_dysfunc_Ab = 1.27 * 10 ** (-7)
n_t_mito_dysfunc_Ab = 0.9957
k_t_cas3_inact = 7.96721 * 10 ** (-3) # s^-1
k_t_ROS_gener_Ab = 8.4e-1 # s^-1  maximum is 7e3