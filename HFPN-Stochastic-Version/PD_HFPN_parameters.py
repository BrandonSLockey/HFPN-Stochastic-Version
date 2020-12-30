# Late endosome pathology
k_t_LE_retro=1
RTN3_conversion_factor = 1 

# Calcium homeostasis
k_t_Ca_NCX_PMCA = 10 #multiplied by 10 compared to Gabi's paper (Gabriel, 2020)
k_t_NaK_ATPase= 0.7 
k_t_mCU1=(1*1e6)/(17854326) #rate mCU /average Ca_cyto in homeostasis
k_t_mCU2=(5000)/(17854326) #rate mCU /average Ca_cyto in homeostasis
#k_t_mNCLX=(5000)/(3.6*1e7) #rate mCU /average Ca_cyto in homeostasis
k_t_mNCLX=0.066666667
k_t_MAM=1e6/1.8e9 #rate MAM
k_t_SERCA_no_ATP=0.05638 #(1e6+100)/17854326#0.05638 #100/1785#4#3#2#6#/(5.407*1e9)
k_t_SERCA=k_t_SERCA_no_ATP/5.42e9 #rate mCU /average ATP in homeostasis
k_t_RyR_IP3R = 100/(1.8*1e9) #rate mCU /average Ca_ER in homeostasis

# Lewy body pathology
# k_t_HSP70=6.34441087613*1e-5
k_t_SNCA_aggr=1*1e-7
k_t_SNCA_fibril=6*1e-5
k_t_IRE=3.276625981873*1e-4
k_t_SNCA_degr=1.510574018*1e-4
k_t_SNCA_degr_VPS35 = 1.1329305*1e-04
p_SNCA_act_homeostasis = 4.4*1e8
LB_threshold=10
m_t_SNCA_aggr =2.1751e-9
n_t_SNCA_aggr = 9.1919e-1


# Energy metabolism
k_t_krebs = (1.63*10**(-7))*2968656.262/3e7
k_t_ATP_hydro_mito = 1.92*10**(-2)
k_t_ETC = 2.48*10**(-5)*2968656.262/3e7
k_t_ROS_metab = 5.875*1e10
k_t_ROS_metab_LB=k_t_ROS_metab*0.5 #rate inhibition by lewy bodies
k_t_ROS_metab_DJ1=1/2
#k_t_cas3_inact=7.97*1e-5
#k_t_mito_dysfunc=5.20*1e-5
#k_t_cas3_inact=(k_t_mito_dysfunc*38190.44)/13014.7584
#k_t_cas3_inact = 7.96721 * 10 ** (-3) # s^-1
#AD old
# k_t_mito_dysfunc = 9.40595 * 10 ** (-5) # s^-1#9.40595 * 10 ** (-8) # s^-1
# c_t_mito_dysfunc = 0.703 # constant rate to account for other cas3 activation processes, incorporated in this transition to simplify
# m_t_mito_dysfunc = 1.27 * 10 ** (-7)
# n_t_mito_dysfunc = 0.9957
# cas3_homeostasis = 22500
#######AD########
k_t_mito_dysfunc = 1.037984e2 # s^-1 For time step of 0.01 s, change to 1.037984e2
m_t_mito_dysfunc = 3.1855e-5
n_t_mito_dysfunc = 0.61
k_t_cas3_inact = 7.96721 * 10 ** (-3) # s^-1
#################

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
m_t_chol_trans_PM_ECM = -0.000000115253772
n_t_chol_trans_PM_ECM = 1.020833333333330
k_t_24OHchol_exocyto = 7.47488 * 10 ** (-6) # s^-1 
#PD specific
k_t_SNCA_bind_ApoEchol_extra=k_t_SNCA_aggr/1.60e6
#Link between chol and LB
m_t_SNCA_degr=-1.84406*1e-7
n_t_SNCA_degr=1.547619048


# Late endosome pathology
Km_t_phos_tau = 9.22e7
kcat_t_phos_tau = 0.146464095 
Km_t_dephos_tauP = 6.29e7
vmax_t_dephos_tauP = 1.17*1.1e6  # uM/min/ 20 units per mL PP-2A, TODO: conevert unit
p_PP_2A=1.33e7
beta_t_LE_retro = 1.667 #conversion factor of rate of retrograde transport to have it equal to anterograde transport in healthy cells 
dist_t_LE_trans = 75e4 #distance in nm from perinuclear region to axon
mchol_t_LE_retro = 2.27e-9 # scaling effect of cholesterol on retro transport
nchol_t_LE_retro = 1 - mchol_t_LE_retro * 2.65 * 1e9  # scaling effect of cholesterol on retro transport
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
p_GSK3B_act=2815005
p_cas=1
p_Ab_homeostasis=34048
