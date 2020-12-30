from PD_HFPN_parameters import *
from PD_HFPN_inputs import mp_ApoEchol, mp_27OHchol

# Cholesterol homeostasis intial token values
# it_p_chol_LE = chol_LE_threshold
#it_p_chol_LE = chol_LE_max for ER retraction (diseased)
it_p_ApoEchol_EE = 2.5 * 1e3 #have been altering this since it's not in literature
it_p_chol_LE = 2.65 * 1e9 
it_p_chol_mito = 3.79*1e9
it_p_chol_ER = 4.37*1e8
it_p_chol_PM = 8.45*1e10
it_p_24OHchol_extra = 4.65*1e3
it_p_24OHchol_intra = 3.98*1e8
it_p_27OHchol_extra = 1.72*1e3
it_p_7HOCA = 0
it_p_preg = 0
it_p_SNCA_act_extra = 113
it_p_SNCAApoEchol_extra = 0
it_p_SNCAApoEchol_intra = 0
#varying
it_p_ApoEchol_extra = 1.60*1e6 *mp_ApoEchol
it_p_27OHchol_intra = 3.06*1e7 *mp_27OHchol

# Calcium homeostasis intial token values
it_p_Ca_cyto = 7.2*1e5
#it_p_Ca_mito = 2.4*1e5 if running (with) calcium module
#it_p_Ca_mito = 2968656.262 #NPCD value
it_p_Ca_mito = 3e7 #AD value
it_p_Ca_ER =1.8*1e9 #

# Lewy bodies pathologies initial token values 
it_p_SNCA_act = 4.3383*1e8
it_p_SNCA_inact = 0
it_p_SNCA_olig = 0
it_p_LB = 0
it_p_Fe2 = 2*1e8

# Energy metabolism initial token values 
it_p_cas3 = 13014.7584
it_p_ATP = 5.42*10**9
it_p_ADP = 5.42*10**6
it_p_reduc_mito = 2.71*10**9
it_p_ROS_mito = 13557.04
it_p_H2O_mito = 0

# Late endosome pathology initial token values 
it_p_RTN3_axon =   5344426
it_p_RTN3_PN =   6655574
it_p_RTN3_tot = it_p_RTN3_axon + it_p_RTN3_PN # not actually for initializing a place, just useful in some calculations
it_p_RTN3_HMW_cyto = 0
it_p_RTN3_HMW_auto = 0
it_p_RTN3_HMW_lyso = 0
it_p_RTN3_HMW_dys1 = 0
it_p_RTN3_HMW_dys2 = 0
it_p_tauP = 6.36e6
it_p_tau = 3.72e7
it_p_Ab=0

