'''Initial tokens'''

conversion = 3.963e-7

# Cholesterol homeostasis
it_p_ApoEchol_extra = 1.60*10**6
it_p_ApoEchol_EE = 2.5 * 10 **3 
it_p_chol_LE = 2.65 * 10 ** 9 
it_p_chol_mito = 3.79*10**9
it_p_chol_ER = 4.37*10**8
it_p_chol_PM = 8.45*10**10
it_p_24OHchol_extra = 4.65*10**3
it_p_24OHchol_intra = 3.98*10**8
it_p_27OHchol_intra = 3.06*10**7
it_p_27OHchol_extra = 1.72*10**3
it_p_7HOCA = 0
it_p_preg = 0


# ER Retraction & Collapse
it_p_RTN3_axon =   5344426
it_p_RTN3_PN =   6655574
it_p_RTN3_tot = it_p_RTN3_axon + it_p_RTN3_PN # not actually for initializing a place, just useful in some calculations
it_p_RTN3_HMW_cyto = 0
it_p_RTN3_HMW_auto = 0
it_p_RTN3_HMW_lyso = 0
it_p_RTN3_HMW_dys1 = 0
it_p_RTN3_HMW_dys2 = 0


# Abeta Pathology
it_p_asec = 6.05e6
it_p_APP_pm = 3.49e6
it_p_sAPPa = 0 # sink
it_p_CTF83 = 0 # sink
it_p_APP_endo = 1.91e6
it_p_bsec = 6.73e5
it_p_sAPPb = 0 # sink
it_p_CTF99 = 1930 #
it_p_gsec = 3.37e6
it_p_AICD = 0 # sink
it_p_Ab = 34048 #34048 # 
it_p_Abconc = 34048*conversion
it_p_ApoE = 0 # 0 if healthy/non-risk genotype, 1 for ApoE4 risk factor allele
it_p_age = 0 # 0 if young/no age risk factor, 1 representing 80 years of age risk factor (affects BACE1 activity)
it_p_CD33 = 0 #1 for CD33 mutation which causes overexpression/activity
it_p_Ab_S = 0
it_p_Ab_M = 0
it_p_Ab_P = 0

# Tau Pathology
it_p_GSK3b_inact = 2684994
it_p_GSK3b_act = 2815005
it_p_tauP = 6.36e6
it_p_tau = 3.72e7
it_p_PP_2A = 1.33e7


# Calcium Homeostasis
it_p_Ca_cyto = 7.2*1e5
it_p_Ca_mito = 3 * 10 ** 7 
it_p_Ca_ER = 1.8*1e9
it_p_ADP = 5.42*10**6
it_p_ATP = 5.42*10**9 


# Energy Metabolism
it_p_cas3 = 13014.7584
it_p_ATP = 5.42*10**9
it_p_ADP = 5.42*10**6
it_p_reduc_mito = 2.71*10**9
it_p_ROS_mito = 13557.04
it_p_H2O_mito = 0

