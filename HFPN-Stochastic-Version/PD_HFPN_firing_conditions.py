from PD_HFPN_parameters import *
from PD_HFPN_initial_tokens import *

# Cholesterol homeostasis firing conditions
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
#PD specific
fc_t_SNCA_bind_ApoEchol_extra = lambda a : a['p_ApoEchol_extra']>0 and a['p_SNCA_act']>4.34*1e8
fc_t_SNCAApoEchol_endocyto = lambda a : a['p_SNCAApoEchol_extra']>0
fc_t_trans_SNCAApoEchol_intra_EE = lambda a : a['p_SNCAApoEchol_intra']>0
fc_t_SNCAApoEchol_olig = lambda a :  a['p_SNCAApoEchol_intra']>0
fc_t_SNCA_exocyto= lambda a : a['p_SNCA_act']>0
fc_t_chol_LE_upreg= lambda a : a['p_GBA1']>0

# Calcium homeostasis firing conditions
fc_t_Ca_imp = lambda a : a['p_Ca_extra']==1
fc_t_mCU = lambda a : a['p_Ca_cyto']>it_p_Ca_cyto
fc_t_mNCLX = lambda a : a['p_Ca_mito']>0
fc_t_MAM = lambda a : a['p_Ca_ER']>it_p_Ca_cyto #and a['p_Ca_mito']<2.8*1e7 or a['p_Ca_mito']>3.2*1e7
fc_t_RyR_IP3R = lambda a : a['p_Ca_extra']==0
fc_t_SERCA = lambda a : a['p_ATP']>0
fc_t_Ca_NCX = lambda a : 1

# Lewy bodies pathology firing conditions 
fc_t_SNCA_degr = lambda a : a['p_SNCA_act']>0
fc_t_SNCA_aggr = lambda a : a['p_SNCA_act']>5.2*1e8
fc_t_SNCA_fibril = lambda a : a['p_SNCA_olig']>0
fc_t_LB_ER_stress = lambda a : (a['p_LB']>10)*(a['p_GRP78']==0)
fc_t_SREBP1 = lambda a : a['p_GRP78']>0
fc_t_IRE = lambda a : 1

# Energy metabolism firing conditions 

fc_t_mito_dysfunc = lambda a : a['p_ROS_mito']>0 #80000
fc_t_krebs = lambda a : a['p_ADP'] > 3
fc_t_ATP_hydro_mito = lambda a : a['p_ATP'] > 1
fc_t_ETC = lambda a : a['p_reduc_mito'] > 0 and a['p_ADP'] > 1
fc_t_ROS_metab = lambda a : a['p_ROS_mito'] > 1
fc_t_cas3_inact = lambda a : a['p_cas3']>1


# ER Retraction & Collapse
# # Late endosome pathology firing conditions 
# #In retrograde transport still need to incoorporate 'p_LRRK2_mut','p_VPS35','p_LB' either in rate eq. or firing condition
# fc_t_LE_retro = lambda a : a['p_ATP']>0
# fc_t_LE_antero = lambda a : a['p_ATP']>0
fc_t_RTN3_exp = lambda a: True
fc_t_LE_retro = lambda a : a['p_RTN3_axon'] > 0 and a['p_ATP'] > 0
fc_t_LE_antero = lambda a : a['p_RTN3_PN'] > 0 and a['p_ATP'] > 0

fc_t_RTN3_aggregation = lambda a : (a["p_RTN3_axon"] + a["p_RTN3_PN"]) > (it_p_RTN3_tot * (1 - (1-dec_t_RTN3_aggregation) * (p_Ab_homeostasis - it_p_Ab)/(Ab_t_RTN3_aggregation - it_p_Ab))) # proportional reduction in RTN3 aggregation threshold based on Ab level
fc_t_RTN3_auto = lambda a : a['p_RTN3_HMW_cyto'] > 1 and a['p_RTN3_axon'] > 1
fc_t_RTN3_lyso = lambda a : a['p_RTN3_HMW_auto'] > 1
fc_t_RTN3_dys_auto = lambda a : a['p_RTN3_HMW_cyto'] > 1 and a['p_RTN3_axon'] < it_p_RTN3_axon # any reduction in functional tubular ER from starting value can cause dysfunctional autophagosome formation
fc_t_RTN3_dys_lyso = lambda a : a["p_RTN3_HMW_auto"] > 1



