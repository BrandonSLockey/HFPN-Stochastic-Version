'''Firing Conditions'''

from AD_initial_tokens import *
from AD_parameters import *
from AD_rate_functions import *

# Cholesterol homeostasis
fc_t_LDLR_endocyto = lambda a : a["p_ApoEchol_extra"] > 1
fc_t_ApoEchol_cleav = lambda a : a["p_ApoEchol_EE"] > 1
fc_t_chol_trans_LE_ER = lambda a : a["p_chol_LE"] > 1
fc_t_chol_trans_LE_mito = lambda a : a["p_chol_LE"] > 1
fc_t_chol_trans_LE_PM = lambda a : a["p_chol_LE"] > 1
fc_t_chol_trans_PM_ER = lambda a : a["p_chol_PM"] > 1
fc_t_chol_trans_ER_PM = lambda a : a["p_chol_ER"] > 0
fc_t_chol_trans_ER_mito = lambda a : a["p_chol_ER"] > 0
fc_t_27OHchol_endocyto = lambda a : a["p_27OHchol_extra"] > 1
fc_t_24OHchol_exocyto = lambda a : a["p_24OHchol_intra"] > 0
fc_t_chol_trans_PM_ECM = lambda a : a["p_chol_PM"] > 0

fc_t_CYP27A1_metab = lambda a : True
fc_t_CYP11A1_metab = lambda a : True
fc_t_CYP7B1_metab = lambda a : True
fc_t_CYP46A1_metab = lambda a : True

# ER Retraction & Collapse
fc_t_RTN3_exp = lambda a: True
fc_t_LE_retro = lambda a : a['p_RTN3_axon'] > 1 and a['p_ATP'] > 1
fc_t_LE_antero = lambda a : a['p_RTN3_PN'] > 1 and a['p_ATP'] > 1

fc_t_RTN3_aggregation = lambda a : (a["p_RTN3_axon"] + a["p_RTN3_PN"]) > (it_p_RTN3_tot * (1 - (1-dec_t_RTN3_aggregation) * max(0,(a['p_Ab'] - it_p_Ab))/(Ab_t_RTN3_aggregation - it_p_Ab))) # proportional reduction in RTN3 aggregation threshold based on Ab level
fc_t_RTN3_auto = lambda a : a['p_RTN3_HMW_cyto'] > 1 and a['p_RTN3_axon'] > 1
fc_t_RTN3_lyso = lambda a : a['p_RTN3_HMW_auto'] > 1
fc_t_RTN3_dys_auto = lambda a : a['p_RTN3_HMW_cyto'] > 1 and a['p_RTN3_axon'] < it_p_RTN3_axon # any reduction in functional tubular ER from starting value can cause dysfunctional autophagosome formation
fc_t_RTN3_dys_lyso = lambda a : a["p_RTN3_HMW_auto"] > 1

# Abeta Pathology
fc_t_asec_degr = lambda a : a['p_asec'] > 1
fc_t_asec_exp = lambda a : True

fc_t_APP_endocyto = lambda a : a['p_APP_pm'] > 1
fc_t_APP_exp = lambda a : True
fc_t_APP_endo_event = lambda a : a['p_APP_endo'] > 1

fc_t_bsec_exp = lambda a : True
fc_t_bsec_degr = lambda a : a['p_bsec'] > 1

fc_t_gsec_exp = lambda a : True
fc_t_gsec_degr = lambda a : a['p_gsec'] > 1

fc_t_Ab_degr = lambda a : a['p_Ab'] > 1

fc_t_APP_asec_cleav = lambda a : True
fc_t_APP_bsec_cleav = lambda a : True
fc_CTF99_gsec_cleav = lambda a : True


fc_t_Ab_nuc1 = lambda a : a['p_Abconc'] > 0
fc_t_Ab_nuc2 = lambda a : a['p_Abconc'] > 0
fc_t_Ab_dis1 = lambda a : a['p_Ab_S'] > 0
fc_t_Ab_elon = lambda a : a['p_Ab_S'] > 0
fc_t_Ab_fib = lambda a :  a['p_Ab_P'] > 0
fc_t_Ab_M_frag = lambda a :  a['p_Ab_M'] > 0
fc_t_Ab_P_phag = lambda a :  a['p_Ab_P'] > 0



# Tau Pathology
fc_t_GSK3b_exp_deg = lambda a : True
fc_t_actv_GSK3b = lambda a : True
fc_t_inactv_GSK3b = lambda a : True # TODO: might need condition for constant speed-funciton
fc_t_phos = lambda a : True

fc_t_phos_tau = lambda a : True
fc_t_dephos_tau = lambda a : True


# Calcium Homeostasis
fc_t_Ca_imp = lambda a : a['p_Ca_extra']>0
fc_t_mCU = lambda a : a['p_Ca_cyto']>it_p_Ca_cyto
fc_t_mNCLX = lambda a : a['p_Ca_mito']>0
fc_t_MAM = lambda a : a['p_Ca_ER']>it_p_Ca_cyto #and a['p_Ca_mito']<2.8*1e7 or a['p_Ca_mito']>3.2*1e7
fc_t_RyR_IP3R = lambda a : a['p_Ca_extra']==0
fc_t_SERCA = lambda a : a['p_ATP']>0
fc_t_NCX_PMCA = lambda a : a['p_on3'] >0
fc_t_NaK_ATPase = lambda a: a['p_on3']>0
fc_t_A = lambda a: a['p_on4']>0 
fc_t_B = lambda a: a['p_on6']== 500000 
fc_t_C = lambda a: a['p_on2']== 500000 
fc_t_D = lambda a: a['p_on3']>0 
fc_t_E = lambda a: a['p_on5']>0 
fc_t_F = lambda a: a['p_Ca_extra'] == 500000
fc_t_G = lambda a: a['p_on7'] == 500000
fc_t_H = lambda a: a['p_on8'] == 500000


# Energy metabolism
fc_t_krebs = lambda a : a['p_ADP'] > 3
fc_t_ATP_hydro_mito = lambda a : a['p_ATP'] > 1
fc_t_ETC = lambda a : a['p_reduc_mito'] > 0 and a['p_ADP'] > 1
fc_t_ROS_metab = lambda a : a['p_ROS_mito'] > 1
fc_t_mito_dysfunc = lambda a : a['p_ROS_mito'] > 0
fc_t_cas3_inact = lambda a : a['p_cas3'] > 1
fc_t_ROS_gener_Ab = lambda a : a["p_Ab"] > it_p_Ab