from PD_sHFPN_parameters import *
from PD_sHFPN_inputs import mp_ApoEchol, mp_27OHchol

conversion = 3.963e-7

# Cholesterol homeostasis intial token values
# PD_it_p_chol_LE = chol_LE_threshold
#PD_it_p_chol_LE = chol_LE_max for ER retraction (diseased)
PD_it_p_ApoEchol_EE = 2.5 * 1e3 #have been altering this since it's not in literature
PD_it_p_chol_LE = 2.65 * 1e9 
PD_it_p_chol_mito = 3.79*1e9
PD_it_p_chol_ER = 4.37*1e8
PD_it_p_chol_PM = 8.45*1e10
PD_it_p_24OHchol_extra = 4.65*1e3
PD_it_p_24OHchol_intra = 3.98*1e8
PD_it_p_27OHchol_extra = 1.72*1e3
PD_it_p_7HOCA = 0
PD_it_p_preg = 0
PD_it_p_SNCA_act_extra = 113
PD_it_p_SNCAApoEchol_extra = 0
PD_it_p_SNCAApoEchol_intra = 0
#varying
PD_it_p_ApoEchol_extra = 1.60*1e6 *mp_ApoEchol 
PD_it_p_27OHchol_intra = 3.06*1e7 *mp_27OHchol

# Calcium homeostasis intial token values
PD_it_p_Ca_cyto = 7.2*1e5
#PD_it_p_Ca_mito = 2.4*1e5 if running (with) calcium module
#PD_it_p_Ca_mito = 2968656.262 #NPCD value
PD_it_p_Ca_mito = 3e7 #AD value
PD_it_p_Ca_ER =1.8*1e9 #

# Lewy bodies pathologies initial token values 
PD_it_p_SNCA_act = 4.3383*1e8
PD_it_p_SNCAconc = 4.3383*1e8*conversion 

PD_it_p_SNCA_inact = 0
PD_it_p_SNCA_olig = 0
PD_it_p_SNCA_S = 0
PD_it_p_SNCA_M = 0
PD_it_p_SNCA_P = 0

PD_it_p_LB = 0
PD_it_p_Fe2 = 2*1e8

# Energy metabolism initial token values 
PD_it_p_cas3 = 13014.7584
PD_it_p_ATP = 5.42*10**9
PD_it_p_ADP = 5.42*10**6
PD_it_p_reducing_agents = 2.71*10**9
PD_it_p_ROS_mito = 13557.04
PD_it_p_H2O_mito = 0

# Late endosome pathology initial token values 
PD_it_p_RTN3_axon =   5344426
PD_it_p_RTN3_PN =   6655574
PD_it_p_RTN3_tot = PD_it_p_RTN3_axon + PD_it_p_RTN3_PN # not actually for initializing a place, just useful in some calculations
PD_it_p_RTN3_HMW_cyto = 0
PD_it_p_RTN3_HMW_auto = 0
PD_it_p_RTN3_HMW_lyso = 0
PD_it_p_RTN3_HMW_dys1 = 0
PD_it_p_RTN3_HMW_dys2 = 0
PD_it_p_tauP = 6.36e6
PD_it_p_tau = 3.72e7
PD_it_p_Ab=0

