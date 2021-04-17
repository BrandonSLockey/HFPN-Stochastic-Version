from PD_sHFPN_parameters import *
from PD_sHFPN_initial_tokens import *
from PD_sHFPN_inputs import *
import numpy as np
                                                                                                                                                                            
# Cholesterol homeostasis rates 
# rate_constant * a['p_H2']**2 * a['p_O2']**1
PD_r_t_chol_trans_ER_PM = lambda a :chol_mp*  k_t_chol_trans_ER_PM * a["p_chol_ER"]
PD_r_t_27OHchol_endocyto = lambda a : mp_27OHchol* chol_mp* k_t_27OHchol_endocyto 
PD_r_t_LDLR_endocyto = lambda a : chol_mp* (((vmax_t_LDLR_endocyto * min([1, max([0.3,(m_t_LDLR_endocyto * (a["p_chol_ER"]/PD_it_p_chol_ER) + n_t_LDLR_endocyto)])]) * a["p_ApoEchol_extra"]/(Km_t_LDLR_endocyto + a["p_ApoEchol_extra"])) ) * (1+4*(a['p_LB']>LB_threshold))) #BSL: Endocytosis is always multiplied by a number between 0.3 and 1
PD_r_t_ApoEchol_cleav = lambda a : chol_mp* (vmax_t_ApoEchol_cleav * a["p_ApoEchol_EE"]* 227)/(Km_t_ApoEchol_cleav + a["p_ApoEchol_EE"] * 227)
PD_r_t_chol_LE_upreg = lambda a : chol_mp* 9.8*1e6
PD_r_t_chol_trans_ER_mito = lambda a :chol_mp* k_t_chol_trans_ER_mito * a["p_chol_ER"] 
PD_r_t_chol_trans_LE_mito = lambda a : chol_mp*k_t_chol_trans_LE_mito * a["p_chol_LE"]
PD_r_t_chol_trans_LE_ER = lambda a : chol_mp*k_t_chol_trans_LE_ER * a["p_chol_LE"]
PD_r_t_chol_trans_LE_PM = lambda a : chol_mp*k_t_chol_trans_LE_PM * a["p_chol_LE"]
PD_r_t_chol_trans_PM_ECM = lambda a :chol_mp*( k_t_chol_trans_PM_ECM * a["p_chol_PM"] * min( [3.5, max([0,(m_t_chol_trans_PM_ECM * (a["p_24OHchol_intra"]/PD_it_p_24OHchol_intra) + n_t_chol_trans_PM_ECM)])]))
PD_r_t_chol_trans_PM_ER = lambda a : chol_mp* k_t_chol_trans_PM_ER * a["p_chol_PM"]
PD_r_t_chol_trans_ER_PM = lambda a : chol_mp* k_t_chol_trans_ER_PM * a["p_chol_ER"]
PD_r_t_24OHchol_exocyto = lambda a : chol_mp* k_t_24OHchol_exocyto * a["p_24OHchol_intra"] 

PD_r_t_SNCA_bind_ApoEchol_extra = lambda a : k_t_SNCA_bind_ApoEchol_extra*a['p_SNCA_act']*a['p_ApoEchol_extra']

def function_for_MDV_delay(get_input_tokens):
    log = lambda b: (chol_mp/chol_mp)*min(60,max((-24.34*np.log(b)+309.126), 20))#(10/chol_mp)*min(60,max((-24.34*np.log(b)+309.126), 20)) #delay is between 60 to 20 seconds. chol_mp is 300. (1/300, to match speed (much faster))
    tokens = lambda a: a['p_ROS_mito']
    return log(tokens(get_input_tokens))


#PD specific (NEEDS TO BE REVIEWED)
PD_r_t_SREBP1 = lambda a: 0
PD_r_t_LB_ER_stress = lambda a: 0

# Calcium homeostasis rates
PD_r_t_Ca_imp = lambda a : 1.44*1e8
PD_r_t_mCU = lambda a : k_t_mCU1 *a['p_Ca_cyto'] #*(a['p_Ca_mito']<=3*1e7) + (a['p_Ca_mito']>3*1e7)*k_t_mCU2*a['p_Ca_cyto']
#In mNCLX transport still need to incoorporate 'p_LRRK2_mut' either in rate eq. or firing condition
PD_r_t_mNCLX = lambda a : k_t_mNCLX*a['p_Ca_mito']*(1-0.5*(a['p_LRRK2_mut']>0)) #Ca/s
PD_r_t_MAM = lambda a : k_t_MAM*a['p_Ca_ER'] #Ca/s #/(1+(a['p_Ca_mito']-PD_it_p_Ca_mito))
PD_r_t_RyR_IP3R = lambda a : k_t_RyR_IP3R*a['p_Ca_ER'] #100 #Ca/s
#WITHOUT ATP
PD_r_t_SERCA = lambda a : k_t_SERCA_no_ATP*a['p_Ca_cyto']#Ca/s
#WITH ATP
# PD_r_t_SERCA = lambda a : k_t_SERCA*a['p_Ca_cyto']*a['p_ATP'] #Ca/s
PD_r_t_NCX_PMCA = lambda a: (k_t_Ca_NCX_PMCA*a['p_Ca_cyto'])*(a['p_Ca_cyto']<=7.5*1e7)+ (k_t_Ca_NCX_PMCA/10*a['p_Ca_cyto'])*(a['p_Ca_cyto']>7.5*1e7)
def PD_r_t_SNCA_degr(a):
    multiplier = 1 - 0.2*(a['p_LRRK2_mut']>0)+0.16*((a['p_LRRK2_mut']>0)*(a['p_DNL151']>0))
    rate_healthy = (k_t_SNCA_degr*a['p_SNCA_act'])*(a['p_VPS35']==0)
    rate_VPS35 = (k_t_SNCA_degr_VPS35*a['p_SNCA_act'])*(a['p_VPS35']>0)
    cholesterol = min( [1, max([6.25e-1,(m_t_SNCA_degr*(a["p_27OHchol_intra"]-PD_it_p_27OHchol_intra) + n_t_SNCA_degr)])])
    #print(m_t_SNCA_degr*(a["p_27OHchol_intra"]-PD_it_p_27OHchol_intra) + n_t_SNCA_degr)
    DJI = (1-0.4*a['p_DJ1'])
    LAMP2A = (1+2*(a['p_LAMP2A']==1))
    speedup = 30
    return multiplier*(rate_healthy+rate_VPS35)*cholesterol*DJI*LAMP2A*speedup
# Lewy bodies pathologies rates
# PD_r_t_SNCA_degr = lambda a : (((((1-0.2*(a['p_LRRK2_mut']>0))*k_t_SNCA_degr*a['p_SNCA_act'])*(a['p_VPS35']==0) + ((1-0.2*(a['p_LRRK2_mut']>0))*k_t_SNCA_degr_VPS35*a['p_SNCA_act'])*(a['p_VPS35']>0)) * min( [1, max([6.25e-1,(m_t_SNCA_degr*(a["p_27OHchol_intra"]-PD_it_p_27OHchol_intra) + n_t_SNCA_degr)])]))*(1-0.4*a['p_DJ1']))*30
PD_r_t_SNCA_aggr = lambda a : ((k_t_SNCA_aggr*a['p_SNCA_act'])*(a['p_ROS_mito']<80000)+(1.7*k_t_SNCA_aggr*a['p_SNCA_act'])*(a['p_ROS_mito']>80000) *  min( [1.13, max([1,(m_t_SNCA_aggr * a["p_tauP"] + n_t_SNCA_aggr)])]))*30*(1-0.6*(a['p_NPT200']==1))
PD_r_t_SNCA_fibril = lambda a : k_t_SNCA_fibril*a['p_SNCA_olig']*30
# PD_r_t_LB_ER_stress = lambda a : 1
# PD_r_t_SREBP1 = lambda a : 1
PD_r_t_IRE = lambda a : k_t_IRE*a['p_Fe2']*30

# Energy metabolism rates
PD_r_t_ETC = lambda a : (1-0.2*(a['p_LRRK2_mut']>0)) * k_t_ETC * a['p_ADP'] * a['p_Ca_mito'] * a['p_reducing_agents'] / a['p_chol_mito']  / a['p_ROS_mito']**0.5
PD_r_t_krebs = lambda a : k_t_krebs * a['p_ADP'] * a['p_Ca_mito']
PD_r_t_ATP_hydro_mito = lambda a : k_t_ATP_hydro_mito * a['p_ATP']
PD_r_t_ROS_metab = lambda a : ((k_t_ROS_metab * a['p_ROS_mito'] / a['p_chol_mito'])*(a['p_LB']<LB_threshold) +(k_t_ROS_metab_LB * a['p_ROS_mito'] / a['p_chol_mito'])*(a['p_LB']>=LB_threshold))*(1-k_t_ROS_metab_DJ1*(a['p_DJ1']>0))
PD_r_t_mito_dysfunc = lambda a : k_t_mito_dysfunc * a['p_ROS_mito']
PD_r_t_cas3_inact = lambda a : k_t_mito_dysfunc * a['p_ROS_mito'] / cas3_homeostasis
#PD_r_t_mito_dysfunc = lambda a : c_t_mito_dysfunc + k_t_mito_dysfunc * a["p_ROS_mito"] * (m_t_mito_dysfunc * a["p_ROS_mito"] + n_t_mito_dysfunc) #from AD
PD_r_t_mito_dysfunc = lambda a : k_t_mito_dysfunc * (m_t_mito_dysfunc * a["p_ROS_mito"] + n_t_mito_dysfunc) 
PD_r_t_cas3_inact = lambda a : k_t_cas3_inact * a["p_cas3"]

# Late endosome pathology rates
# #In retrograde transport still need to incoorporate 'p_LRRK2_mut','p_VPS35','p_LB' either in rate eq. or firing condition
# PD_r_t_LE_retro = lambda a : beta*(vmax_dyn*a['p_ATP']/(Km_dyn+a['p_ATP'])*(1+alpha*((a['p_chol_LE']-chol_LE_threshold)/(chol_LE_max-chol_LE_threshold))))/distance*PD_it_p_RTN3_axon
# PD_r_t_LE_antero = lambda a : (vmax_kin*a['p_ATP'])/(Km_kin+a['p_ATP'])/distance*PD_it_p_RTN3_PN

PD_r_t_LE_retro = lambda a : (1+0.8*(a['p_LRRK2_mut']>0))*(beta_t_LE_retro * vmax_t_LE_retro * a['p_ATP'] / (Km_t_LE_retro + a['p_ATP']) * max((mchol_t_LE_retro * a['p_chol_LE'] + nchol_t_LE_retro), 1) / dist_t_LE_trans * a['p_RTN3_axon'] * a['p_tau']/PD_it_p_tau * (1-0.5*(a['p_LB']>LB_threshold)))
PD_r_t_LE_antero = lambda a : (vmax_t_LE_antero * a['p_ATP']) / (Km_t_LE_antero + a['p_ATP']) / dist_t_LE_trans * a['p_RTN3_PN'] * a['p_tau']/PD_it_p_tau
PD_r_t_RTN3_exp = lambda a : k_t_RTN3_exp

PD_r_t_RTN3_aggregation = lambda a : 0.1 * ((a["p_RTN3_axon"] + a["p_RTN3_PN"]) - (PD_it_p_RTN3_tot * (1 - (1-dec_t_RTN3_aggregation) * (p_Ab_homeostasis - PD_it_p_Ab)/(Ab_t_RTN3_aggregation - PD_it_p_Ab)))) # kinetics not measured and dont really matter; only equilibrium/threshold matters. just assume that 10% of excess RTN3 above threshold aggregates every second (for smoothness)
PD_r_t_RTN3_auto = lambda a : a["p_RTN3_HMW_cyto"] * k_t_RTN3_auto * (a["p_RTN3_axon"] / PD_it_p_RTN3_axon) # autophagosomes per second (each containing 1 oligomer), scaled by the proportion of functional ER left
PD_r_t_RTN3_lyso = lambda a : a["p_RTN3_HMW_auto"] * k_t_RTN3_lyso * (a["p_tau"]/PD_it_p_tau) # rate of transport across axon, scaled by the proportion of functional tau left
PD_r_t_RTN3_dys_auto = lambda a : a["p_RTN3_HMW_cyto"] * k_t_RTN3_auto * max(0,(1 - a["p_RTN3_axon"] / PD_it_p_RTN3_axon)) # any reduction in normal autophagosome formation due to lack of ER instead goes to this transition at the same rate
PD_r_t_RTN3_dys_lyso = lambda a : a["p_RTN3_HMW_auto"] * k_t_RTN3_lyso * max(0,(1 - a["p_tau"]/PD_it_p_tau)) # any reduction in normal lysosomal processing instead goes to this transitoin. didn't incorporate transport-inhibiting effect of dystrophic neurites yet
# def PD_r_t_RTN3_dys_lyso(a):
#     print('step')
#     print(a["p_tau"]/PD_it_p_tau)
#     print(a["p_RTN3_HMW_auto"] * k_t_RTN3_lyso * max(0,(1 - a["p_tau"]/it_p_tau)))
#     print(a["p_tau"],PD_it_p_tau)
#     return a["p_RTN3_HMW_auto"] * k_t_RTN3_lyso * max(0,(1 - a["p_tau"]/PD_it_p_tau))

PD_vmax_scaling_t_phos_tau = lambda a : 2815005*(a['p_SNCA_act']<p_SNCA_act_homeostasis) +2815005*1.25*(a['p_SNCA_act']>=p_SNCA_act_homeostasis)
PD_vmax_scaling_t_dephos_tauP = lambda a : 1 