# Alzheimers HFPN subnets

# Imports
import os
import sys

from datetime import datetime

cwd = os.getcwd()
root_folder = os.sep+"HFPN-Stochastic-Version"
sys.path.insert(0, cwd[:(cwd.index(root_folder)+len(root_folder))] + os.sep+"HFPN-Stochastic-Version"+os.sep)

# Import class to work with hybrid functional Petri nets
from stochastic_hfpn import HFPN

# Import parameters, rate equations, initial tokens and firing conditions
from AD_parameters import *
from AD_rate_functions import *
from AD_initial_tokens import *
from AD_firing_conditions import *
from AD_sHFPN_inputs import *
from visualisation import Analysis

def main():
    # Initialize an empty HFPN
    pn = HFPN(time_step = time_step_size)

### Cholesterol Homeostasis
    pn.add_place(it_p_ApoEchol_extra,place_id="p_ApoEchol_extra", label="ApoE-cholesterol complex (extracellular)", continuous=True)
# Cholesterol in different organelles
    pn.add_place(it_p_chol_LE,place_id="p_chol_LE", label="Cholesterol (late endosome)", continuous=True)
    pn.add_place(it_p_chol_mito,place_id="p_chol_mito", label="Cholesterol (mitochondria)", continuous=True)
    pn.add_place(it_p_chol_ER,place_id="p_chol_ER", label="Cholesterol (ER)", continuous=True)
    pn.add_place(it_p_chol_PM,place_id="p_chol_PM", label="Cholesterol (Plasma Membrane)", continuous=True)

    # Oxysterols
    pn.add_place(it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24-hydroxycholesterol (extracellular)", continuous=True)
    pn.add_place(it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24-hydroxycholesterol (intracellular)", continuous=True)
    pn.add_place(it_p_27OHchol_extra,place_id="p_27OHchol_extra", label="27-hydroxycholesterol (extracellular)", continuous=True)
    pn.add_place(it_p_27OHchol_intra,place_id="p_27OHchol_intra", label="27-hydroxycholesterol (intracellular)", continuous=True)
    pn.add_place(it_p_7HOCA,place_id="p_7HOCA", label="7-HOCA", continuous=True)
    pn.add_place(it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
    
    ## Tau Places
    pn.add_place(it_p_GSK3b_inact, 'p_GSK3b_inact', 'Inactive GSK3 beta kinase')
    pn.add_place(it_p_GSK3b_act, 'p_GSK3b_act', 'Active GSK3 beta kinase')
    pn.add_place(it_p_tauP, 'p_tauP', 'Phosphorylated tau')
    pn.add_place(it_p_tau, 'p_tau', 'Unphosphorylated tau (microtubule)')


    ## AB Places
    pn.add_place(it_p_asec, 'p_asec', 'Alpha secretase')
    pn.add_place(it_p_APP_pm, 'p_APP_pm', 'APP (plasma membrane)') # input
    pn.add_place(it_p_sAPPa, 'p_sAPPa', 'Soluble APP alpha')
    pn.add_place(it_p_CTF83, 'p_CTF83', 'CTF83')
    pn.add_place(it_p_APP_endo, 'p_APP_endo', 'APP (endosome)')
    pn.add_place(it_p_bsec, 'p_bsec', 'Beta secretase')
    pn.add_place(it_p_sAPPb, 'p_sAPPb', 'Soluble APP beta')
    pn.add_place(it_p_CTF99, 'p_CTF99', 'CTF99')
    pn.add_place(it_p_gsec, 'p_gsec', 'Gamma secretase')
    pn.add_place(it_p_AICD, 'p_AICD', 'AICD')
    pn.add_place(it_p_Ab, 'p_Ab', 'Amyloid beta peptide')
    pn.add_place(it_p_ApoE, 'p_ApoE', 'ApoE genotype') # gene, risk factor in AD
    pn.add_place(it_p_age, 'p_age', 'Age risk factor') # 80 years old, risk factor in AD for BACE1 activity increase


 # ER retraction and collapse

    # Monomeric RTN3 (cycling between axonal and perinuclear regions)
    pn.add_place(it_p_RTN3_axon, place_id="p_RTN3_axon", label="Monomeric RTN3 (axonal)", continuous=True)
    pn.add_place(it_p_RTN3_PN, place_id="p_RTN3_PN", label="Monomeric RTN3 (perinuclear)", continuous=True)

    # HMW RTN3 (cycling between different cellular compartments)
    pn.add_place(it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)

    # Energy metabolism: ATP consumption
    pn.add_place(it_p_ATP, place_id="p_ATP", label="ATP", continuous=True)
    pn.add_place(it_p_ADP, place_id="p_ADP", label="ADP", continuous=True)
    pn.add_place(it_p_cas3, place_id="p_cas3", label="Active caspase 3", continuous=True)
    pn.add_place(it_p_reduc_mito, place_id="p_reduc_mito", label="Reducing agents (mitochondria)", continuous=True)
    pn.add_place(it_p_ROS_mito, place_id="p_ROS_mito", label="ROS (mitochondria)", continuous=True)
    pn.add_place(it_p_H2O_mito, place_id="p_H2O_mito", label="H2O (mitochondria)", continuous=True)

    ##calcium
    
    pn.add_place(it_p_Ca_cyto, "p_Ca_cyto", "Calcium (cytosol)", continuous = True)
    pn.add_place(it_p_Ca_mito, "p_Ca_mito", "Calcium (mitochondria)", continuous = True)
    pn.add_place(it_p_Ca_ER, "p_Ca_ER", "Calcium (ER)", continuous = True)

    # Discrete on/of-switches calcium pacemaking
    pn.add_place(1, "p_Ca_extra", "on1 - Calcium (extracellular)", continuous = False)
    pn.add_place(0, "p_on2","on2", continuous = False)
    pn.add_place(0, "p_on3","on3", continuous = False)
    pn.add_place(0, "p_on4","on4", continuous = False)
    

    ## Transitions
    # Cholesterol Endocytosis
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_LDLR_endocyto",
                    label						 = "LDLR endocyto",
                    input_place_ids				 = ["p_ApoEchol_extra", "p_chol_ER"],
                    firing_condition			 = fc_t_LDLR_endocyto,
                    reaction_speed_function		 = r_t_LDLR_endocyto, 
                    consumption_coefficients	 = [0,0],
                    output_place_ids			 = ["p_chol_LE"], 
                    production_coefficients		 = [354],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from LE to ER
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_ER",
                    label						 = "Chol transport LE-ER",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_ER,
                    reaction_speed_function		 = r_t_chol_trans_LE_ER,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_ER"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from LE to mito
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_mito",
                    label						 = "Chol transport LE-mito",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_mito,
                    reaction_speed_function		 = r_t_chol_trans_LE_mito,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_mito"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from LE to PM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_PM",
                    label						 = "Chol transport LE-PM",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_PM, 
                    reaction_speed_function		 = r_t_chol_trans_LE_PM,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_PM"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from PM to ER
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_PM_ER",
                    label						 = "Chol transport PM-ER",
                    input_place_ids				 = ["p_chol_PM"],
                    firing_condition			 = fc_t_chol_trans_PM_ER,
                    reaction_speed_function		 = r_t_chol_trans_PM_ER,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_ER"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from ER to PM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_ER_PM",
                    label						 = "Chol transport ER-PM",
                    input_place_ids				 = ["p_chol_ER"],
                    firing_condition			 = fc_t_chol_trans_ER_PM,
                    reaction_speed_function		 = r_t_chol_trans_ER_PM,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_PM"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport Cholesterol from ER to mito
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_ER_mito",
                    label						 = "Chol transport ER-mito",
                    input_place_ids				 = ["p_chol_ER"],
                    firing_condition			 = fc_t_chol_trans_ER_mito,
                    reaction_speed_function		 = r_t_chol_trans_ER_mito,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_mito"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Metabolisation of chol by CYP27A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP27A1_metab",
                    label						 = "Chol metab CYP27A1",
                    Km							 = Km_t_CYP27A1_metab,
                    vmax						 = vmax_t_CYP27A1_metab,
                    input_place_ids				 = ["p_chol_mito"],
                    substrate_id				 = "p_chol_mito",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_27OHchol_intra"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_CYP27A1_metab,
                    stochastic_parameters = [cholSD])

    # Metabolism of chol by CYP11A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP11A1_metab",
                    label						 = "Chol metab CYP11A1",
                    Km							 = Km_t_CYP11A1_metab,
                    vmax						 = vmax_t_CYP11A1_metab,
                    input_place_ids				 = ["p_chol_mito"],
                    substrate_id				 = "p_chol_mito",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_preg"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_CYP11A1_metab,
                    stochastic_parameters = [cholSD])

    # Metabolisation of 27OHchol by CYP7B1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP7B1_metab",
                    label						 = "27OHchol metab CYP7B1",
                    Km							 = Km_t_CYP7B1_metab,
                    vmax						 = vmax_t_CYP7B1_metab,
                    input_place_ids				 = ["p_27OHchol_intra"],
                    substrate_id				 = "p_27OHchol_intra",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_7HOCA"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_CYP7B1_metab,
                    stochastic_parameters = [cholSD])

    # Endocytosis of 27OHchol
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_27OHchol_endocyto",
                    label						 = "27OHchol endocyto",
                    input_place_ids				 = ["p_27OHchol_extra"],
                    firing_condition			 = fc_t_27OHchol_endocyto,
                    reaction_speed_function		 = r_t_27OHchol_endocyto,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_27OHchol_intra", "p_27OHchol_extra"],
                    production_coefficients		 = [1,1],
                    stochastic_parameters = [cholSD])

    # Metabolisation of chol by CYP46A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP46A1_metab",
                    label						 = "Chol metab CYP46A1",
                    Km							 = Km_t_CYP46A1_metab,
                    vmax						 = vmax_t_CYP46A1_metab,
                    input_place_ids				 = ["p_chol_ER"],
                    substrate_id				 = "p_chol_ER",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_24OHchol_intra"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_CYP46A1_metab,
                    stochastic_parameters = [cholSD])

    # Exocytosis of 24OHchol
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_24OHchol_exocyto",
                    label						 = "24OHchol exocyto",
                    input_place_ids				 = ["p_24OHchol_intra"],
                    firing_condition			 = fc_t_24OHchol_exocyto,
                    reaction_speed_function		 = r_t_24OHchol_exocyto,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_24OHchol_extra"],
                    production_coefficients		 = [1],
                    stochastic_parameters = [cholSD])

    # Transport of Chol into ECM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_PM_ECM",
                    label						 = "Chol transport PM-ECM",
                    input_place_ids				 = ["p_chol_PM", "p_24OHchol_intra"],
                    firing_condition			 = fc_t_chol_trans_PM_ECM,
                    reaction_speed_function		 = r_t_chol_trans_PM_ECM,
                    consumption_coefficients	 = [1,0],
                    output_place_ids			 = [],
                    production_coefficients		 = [],
                    stochastic_parameters = [cholSD])

#tau
    ## Transitions
    pn.add_transition_with_speed_function(
                    transition_id				 = 't_GSK3b_exp_deg',
                    label						 = 'GSK3beta expression and degradation',
                    input_place_ids				 = ['p_GSK3b_inact'], 
                    firing_condition			 = fc_t_GSK3b_exp_deg,
                    reaction_speed_function		 = r_t_GSK3b_exp_deg,
                    consumption_coefficients	 = [0], 
                    output_place_ids			 = ['p_GSK3b_inact'],
                    production_coefficients		 = [1],
                    stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_actv_GSK3b',
                    label						 = 'GSK3beta activation',
                    input_place_ids				 = ['p_GSK3b_inact', 'p_ApoE', 'p_Ab'], 
                    firing_condition			 = fc_t_actv_GSK3b,
                    reaction_speed_function		 = r_t_actv_GSK3b,
                    consumption_coefficients	 = [1, 0, 0], 
                    output_place_ids			 = ['p_GSK3b_act'],
                    production_coefficients		 = [1],
                    stochastic_parameters = [SD])


    pn.add_transition_with_speed_function(
                    transition_id				 = 't_inactv_GSK3b',
                    label						 = 'GSK3beta inactivation',
                    input_place_ids				 = ['p_GSK3b_act'], 
                    firing_condition			 = fc_t_inactv_GSK3b, 
                    reaction_speed_function		 = r_t_inactv_GSK3b,
                    consumption_coefficients	 = [1], 
                    output_place_ids			 = ['p_GSK3b_inact'],
                    production_coefficients		 = [1],
                    stochastic_parameters = [SD])
        

    pn.add_transition_with_michaelis_menten(
                    transition_id				 = 't_phos_tau',
                    label						 = 'Phosphorylation of tau',
                    Km							 = Km_t_phos_tau, 
                    vmax						 = kcat_t_phos_tau, 
                    input_place_ids				 = ['p_tau', 'p_GSK3b_act', 'p_cas3'],
                    substrate_id				 = 'p_tau',
                    consumption_coefficients	 = [1, 0, 0],
                    output_place_ids			 = ['p_tauP'],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_phos_tau,
                    stochastic_parameters = [SD])


    pn.add_transition_with_michaelis_menten(
                    transition_id				 = 't_dephos_tauP',
                    label						 = 'Dephosphorylation of tau protein',
                    Km							 = Km_t_dephos_tauP, 
                    vmax						 = vmax_t_dephos_tauP, 
                    input_place_ids				 = ['p_tauP', 'p_Ca_cyto'],
                    substrate_id				 = 'p_tauP',
                    consumption_coefficients	 = [1, 0],
                    output_place_ids			 = ['p_tau'],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = vmax_scaling_t_dephos_tauP,
                    stochastic_parameters = [SD])



    ## AB Transitions
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = 't_APP_asec_cleav',
                    label						 = 'Alpha cleavage of APP',
                    Km = Km_t_APP_asec_cleav, 
                    vmax = kcat_t_APP_asec_cleav,
                    input_place_ids				 = ['p_APP_pm', 'p_asec', 'p_chol_PM'],
                    substrate_id = 'p_APP_pm', 
                    consumption_coefficients	 = [1, 0, 0],
                    output_place_ids = ['p_sAPPa', 'p_CTF83'],
                    production_coefficients = [1, 1],
                    vmax_scaling_function = vmax_scaling_t_APP_asec_cleav,
                    stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_asec_exp',
                    label						 = 'Alpha secretase expression',
                    input_place_ids				 = ['p_24OHchol_intra'],
                    firing_condition			 = fc_t_asec_exp,
                    reaction_speed_function		 = r_t_asec_exp,
                    consumption_coefficients	 = [0], 
                    output_place_ids = ['p_asec'], # none
                    production_coefficients = [1],
                    stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                    transition_id				 = 't_asec_degr',
                    label						 = 'Alpha secretase degradation',
                    input_place_ids				 = ['p_asec'],
                    firing_condition			 = fc_t_asec_degr,
                    reaction_speed_function		 = r_t_asec_degr,
                    consumption_coefficients	 = [1], 
                    output_place_ids = [], # none
                    production_coefficients = [],
                    stochastic_parameters = [SD])# none

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_APP_exp',
                    label						 = 'APP expression rate',
                    input_place_ids				 = ['p_ApoE', 'p_ROS_mito'],
                    firing_condition			 = fc_t_APP_exp,
                    reaction_speed_function		 = r_t_APP_exp,
                    consumption_coefficients	 = [0, 0], 
                    output_place_ids = ['p_APP_pm'],
                    production_coefficients = [1],
                    stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_APP_endocyto',
                    label						 = 'endocytosis',
                    input_place_ids				 = ['p_APP_pm', 'p_ApoE'], 
                    firing_condition			 = fc_t_APP_endocyto,
                    reaction_speed_function		 = r_t_APP_endocyto,
                    consumption_coefficients	 = [1, 0], 
                    output_place_ids = ['p_APP_endo'],
                    production_coefficients = [1],
                    stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                    transition_id				 = 't_APP_endo_event',
                    label						 = 'APP-utilizing cellular events',
                    input_place_ids				 = ['p_APP_endo'], 
                    firing_condition			 = fc_t_APP_endo_event,
                    reaction_speed_function		 = r_t_APP_endo_event,
                    consumption_coefficients	 = [1], 
                    output_place_ids = [],
                    production_coefficients = [],
                    stochastic_parameters = [SD])

    pn.add_transition_with_michaelis_menten(
                    transition_id				 = 't_APP_bsec_cleav',
                    label						 = 'Beta cleavage of APP',
                    Km = Km_t_APP_bsec_cleav, 
                    vmax = kcat_t_APP_bsec_cleav,
                    input_place_ids				 = ['p_APP_endo', 'p_bsec', 'p_chol_PM', 'p_age'],
                    substrate_id = 'p_APP_endo', 
                    consumption_coefficients	 = [1, 0, 0, 0],
                    output_place_ids = ['p_sAPPb', 'p_CTF99'],
                    production_coefficients = [1, 1],
                    vmax_scaling_function = vmax_scaling_t_APP_bsec_cleav,
                    stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_bsec_exp',
                    label						 = 'Beta secretase expression',
                    input_place_ids				 = ['p_ROS_mito', 'p_27OHchol_intra', 'p_RTN3_axon'],
                    firing_condition			 = fc_t_bsec_exp,
                    reaction_speed_function		 = r_t_bsec_exp, 
                    consumption_coefficients	 = [0, 0, 0], 
                    output_place_ids = ['p_bsec'], # none
                    production_coefficients = [1],
                    stochastic_parameters = [SD])# none
    
    pn.add_transition_with_speed_function(
                    transition_id				 = 't_bsec_degr',
                    label						 = 'Beta secretase degradation',
                    input_place_ids				 = ['p_bsec'],
                    firing_condition			 = fc_t_bsec_degr,
                    reaction_speed_function		 = r_t_bsec_degr, 
                    consumption_coefficients	 = [1], 
                    output_place_ids = [], # none
                    production_coefficients = [],
                    stochastic_parameters = [SD])# none

    pn.add_transition_with_michaelis_menten(
                    transition_id				 = 't_CTF99_gsec_cleav',
                    label						 = 'Gamma secretase cleavage of CTF99',
                    Km = Km_t_CTF99_gsec_cleav, 
                    vmax = kcat_t_CTF99_gsec_cleav,
                    input_place_ids				 = ['p_CTF99', 'p_gsec', 'p_chol_PM'],
                    substrate_id = 'p_CTF99', 
                    consumption_coefficients	 = [1, 0, 0],
                    output_place_ids = ['p_Ab', 'p_AICD'],
                    production_coefficients = [1, 1],
                    vmax_scaling_function = vmax_scaling_t_CTF99_gsec_cleav,
                    stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_gsec_exp',
                    label						 = 'Gamma secretase expression',
                    input_place_ids				 = ['p_ROS_mito'],
                    firing_condition			 = fc_t_gsec_exp,
                    reaction_speed_function		 = r_t_gsec_exp, 
                    consumption_coefficients	 = [0], 
                    output_place_ids = ['p_gsec'], 
                    production_coefficients = [1],
                    stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                    transition_id				 = 't_gsec_degr',
                    label						 = 'Gamma secretase degradation',
                    input_place_ids				 = ['p_gsec'],
                    firing_condition			 = fc_t_gsec_degr,
                    reaction_speed_function		 = r_t_gsec_degr, 
                    consumption_coefficients	 = [1], 
                    output_place_ids = [], # none
                    production_coefficients = [],
                    stochastic_parameters = [SD])# none

    pn.add_transition_with_speed_function(
                    transition_id				 = 't_Ab_degr',
                    label						 = 'Ab degradation',
                    input_place_ids				 = ['p_Ab'], 
                    firing_condition			 = fc_t_Ab_degr,
                    reaction_speed_function		 = r_t_Ab_degr,
                    consumption_coefficients	 = [1], 
                    output_place_ids = [],
                    production_coefficients = [],
                    stochastic_parameters = [SD])# TODO - fix ratio


   
    
    

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_exp',
                        label = 'Expression rate of RTN3',
                        input_place_ids = [], 
                        firing_condition = fc_t_RTN3_exp,
                        reaction_speed_function = r_t_RTN3_exp, 
                        consumption_coefficients = [],
                        output_place_ids = ['p_RTN3_PN'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_LE_retro',
                        label = 'retrograde transport of LEs & ER',
                        input_place_ids = ['p_ATP','p_chol_LE','p_RTN3_axon', 'p_tau'], # didn't connect p_tau or p_chol_LE yet
                        firing_condition = fc_t_LE_retro,
                        reaction_speed_function = r_t_LE_retro, # get later from PD
                        consumption_coefficients = [ATPcons_t_LE_trans, 0, 1, 0], # tune these coefficients based on PD
                        output_place_ids = ['p_ADP','p_RTN3_PN'],
                        production_coefficients = [ATPcons_t_LE_trans, 1],
                        stochastic_parameters = [SD])# tune these coefficients based on PD

    pn.add_transition_with_speed_function(
                        transition_id = 't_LE_antero',
                        label = 'anterograde transport of LEs & ER',
                        input_place_ids = ['p_ATP','p_RTN3_PN', 'p_tau'], # didn't connect p_tau yet
                        firing_condition = fc_t_LE_antero,
                        reaction_speed_function = r_t_LE_antero, # get later from NPCD
                        consumption_coefficients = [ATPcons_t_LE_trans, 1, 0], # tune these coefficients based on PD
                        output_place_ids = ['p_ADP','p_RTN3_axon'],
                        production_coefficients = [ATPcons_t_LE_trans, 1],
                        stochastic_parameters = [SD])# tune these coefficients based on PD

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_aggregation',
                        label = 'aggregation of monomeric RTN3 into HMW RTN3',
                        input_place_ids = ['p_RTN3_axon', 'p_RTN3_PN', 'p_Ab'], 
                        firing_condition = fc_t_RTN3_aggregation, # tune aggregation limit later
                        reaction_speed_function = r_t_RTN3_aggregation,
                        consumption_coefficients = [1, 1, 0],
                        output_place_ids = ['p_RTN3_HMW_cyto'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_auto',
                        label = 'functional autophagy of HMW RTN3',
                        input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                        firing_condition = fc_t_RTN3_auto, 
                        reaction_speed_function = r_t_RTN3_auto,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_auto'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_lyso',
                        label = 'functional delivery of HMW RTN3 to the lysosome',
                        input_place_ids = ['p_RTN3_HMW_auto', 'p_tau'], 
                        firing_condition = fc_t_RTN3_lyso, 
                        reaction_speed_function = r_t_RTN3_lyso,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_lyso'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_dys_auto',
                        label = 'dysfunctional autophagy of HMW RTN3',
                        input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                        firing_condition = fc_t_RTN3_dys_auto, 
                        reaction_speed_function = r_t_RTN3_dys_auto,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_dys1'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])# tune later when data are incorporated

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_dys_lyso',
                        label = 'dysfunctional delivery of HMW RTN3 to the lysosome',
                        input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
                        firing_condition = fc_t_RTN3_dys_lyso, 
                        reaction_speed_function = r_t_RTN3_dys_lyso,
                        consumption_coefficients = [1, 0, 0],
                        output_place_ids = ['p_RTN3_HMW_dys2'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD])# tune later when 
  
    
    # Transitions
    pn.add_transition_with_speed_function(  
                transition_id = 't_krebs', 
                label = 'Krebs cycle', 
                input_place_ids = ['p_ADP', 'p_Ca_mito', "p_Ab"],
                firing_condition = fc_t_krebs,
                reaction_speed_function = r_t_krebs,
                consumption_coefficients = [1, 0, 0],
                output_place_ids = ['p_reduc_mito', 'p_ATP'], 
                production_coefficients = [4,1],
                stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(  
                transition_id = 't_ATP_hydro_mito', 
                label = 'ATP hydrolysis by cellular processes', 
                input_place_ids = ['p_ATP'],
                firing_condition = fc_t_ATP_hydro_mito,
                reaction_speed_function = r_t_ATP_hydro_mito,
                consumption_coefficients = [1],
                output_place_ids = ['p_ADP'], 
                production_coefficients = [1],
                stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(  
                transition_id = 't_ETC', 
                label = 'Electron transport chain', 
                input_place_ids = ['p_reduc_mito', 'p_ADP', 'p_Ca_mito', 'p_ROS_mito', 'p_chol_mito', "p_Ab"],
                firing_condition = fc_t_ETC,
                reaction_speed_function = r_t_ETC,
                consumption_coefficients = [22/3.96, 440, 0, 0, 0, 0],
                output_place_ids = ['p_ATP', 'p_ROS_mito'], 
                production_coefficients = [440, 0.06],
                stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(  
                transition_id = 't_ROS_metab', 
                label = 'Neutralization of ROS', 
                input_place_ids = ['p_ROS_mito', 'p_chol_mito'],
                firing_condition = fc_t_ROS_metab,
                reaction_speed_function = r_t_ROS_metab,
                consumption_coefficients = [1, 0],
                output_place_ids = ['p_H2O_mito'], 
                production_coefficients = [1],
                stochastic_parameters = [SD])

    # Output transitions: Cas3 for apoptosis
    pn.add_transition_with_speed_function(
                        transition_id = 't_mito_dysfunc',
                        label = 'Mitochondrial complex 1 dysfunction',
                        input_place_ids = ['p_ROS_mito','p_Ab'],
                        firing_condition = fc_t_mito_dysfunc,
                        reaction_speed_function = r_t_mito_dysfunc,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_cas3'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])
    # Cas3 inactivation
    pn.add_transition_with_speed_function(
                        transition_id = 't_cas3_inact',
                        label = 'Caspase 3 inactivation',
                        input_place_ids = ['p_cas3'],
                        firing_condition = fc_t_cas3_inact,
                        reaction_speed_function = r_t_cas3_inact,
                        consumption_coefficients = [1], 
                        output_place_ids = [],         
                        production_coefficients = [],
                        stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_ROS_gener_Ab',
                        label = 'ROS generation by Abeta',
                        input_place_ids = ['p_Ab'],
                        firing_condition = fc_t_ROS_gener_Ab,
                        reaction_speed_function = r_t_ROS_gener_Ab,
                        consumption_coefficients = [0], 
                        output_place_ids = ["p_ROS_mito"],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])




  

    # Add transitions
    pn.add_transition_with_speed_function(
                        transition_id = 't_Ca_imp',
                        label = 'VGCC/NMDA import channels',
                        input_place_ids = ['p_Ca_extra'],
                        firing_condition = fc_t_Ca_imp,
                        reaction_speed_function = r_t_Ca_imp,
                        consumption_coefficients = [0],  
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_mCU',
                        label = 'Ca import into mitochondria via mCU',
                        input_place_ids = ['p_Ca_cyto', 'p_Ca_mito'],
                        firing_condition = fc_t_mCU,
                        reaction_speed_function = r_t_mCU,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_Ca_mito'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_MAM',
                        label = 'Ca transport from ER to mitochondria',
                        input_place_ids = ['p_Ca_ER', 'p_Ca_mito'],
                        firing_condition = fc_t_MAM,
                        reaction_speed_function = r_t_MAM,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_Ca_mito'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])
                        

    pn.add_transition_with_speed_function(
                        transition_id = 't_RyR_IP3R',
                        label = 'Ca export from ER',
                        input_place_ids = ['p_Ca_extra', 'p_Ca_ER'],
                        firing_condition = fc_t_RyR_IP3R,
                        reaction_speed_function = r_t_RyR_IP3R,
                        consumption_coefficients = [0,1], 
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_SERCA',
                        label = 'Ca import to ER',
                        input_place_ids = ['p_Ca_cyto','p_ATP'],
                        firing_condition = fc_t_SERCA,
                        reaction_speed_function = r_t_SERCA,
                        consumption_coefficients = [1,0.5], 
                        output_place_ids = ['p_Ca_ER','p_ADP'],         
                        production_coefficients = [1,0.5],
                        stochastic_parameters = [SD])

    pn.add_transition_with_speed_function(
                        transition_id = 't_NCX_PMCA',
                        label = 'Ca efflux to extracellular space',
                        input_place_ids = ['p_Ca_cyto','p_on3'],
                        firing_condition = lambda a: a['p_on3']==1,
                        reaction_speed_function = r_t_NCX_PMCA,
                        consumption_coefficients = [1,0], 
                        output_place_ids = [],         
                        production_coefficients = [],
                        stochastic_parameters = [SD])
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_mNCLX',
                        label = 'Ca export from mitochondria via mNCLX',
                        input_place_ids = ['p_Ca_mito'],
                        firing_condition = fc_t_mNCLX,
                        reaction_speed_function = r_t_mNCLX,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

    # Discrete on/of-switches calcium pacemaking
    pn.add_transition_with_speed_function(
                        transition_id = 't_A',
                        label = 'A',
                        input_place_ids = ['p_on4'],
                        firing_condition = lambda a: a['p_on4']==1,
                        reaction_speed_function = lambda a: 1,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_Ca_extra'],         
                        production_coefficients = [1],
                        stochastic_parameters = [CaSD, DelaySD],
                        delay=0.5) 
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_B',
                        label = 'B',
                        input_place_ids = ['p_Ca_extra'],
                        firing_condition = lambda a: a['p_Ca_extra']==1,
                        reaction_speed_function = lambda a: 1,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_on2'],         
                        production_coefficients = [1],
                        stochastic_parameters = [CaSD, DelaySD],
                        delay=0.5) 
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_C',
                        label = 'C',
                        input_place_ids = ['p_on2'],
                        firing_condition = lambda a: a['p_on2']==1,
                        reaction_speed_function = lambda a: 1,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_on3'],         
                        production_coefficients = [1],
                        stochastic_parameters = [CaSD, DelaySD],
                        delay=0) 
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_D',
                        label = 'D',
                        input_place_ids = ['p_on3'],
                        firing_condition = lambda a: a['p_on3']==1,
                        reaction_speed_function = lambda a: 1,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_on4'],         
                        production_coefficients = [1],
                        stochastic_parameters = [CaSD, DelaySD],
                        delay=0.5)

    # Link to energy metabolism in that it needs ATP replenishment
    pn.add_transition_with_mass_action(
                        transition_id = 't_NaK_ATPase',
                        label = 'NaK ATPase',
                        rate_constant =  k_t_NaK_ATPase,
                        input_place_ids = ['p_ATP', 'p_on3'],
                        firing_condition = lambda a: a['p_on3']==1,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_ADP'],         
                        production_coefficients = [1],
                        stochastic_parameters = [SD])

 # Run the network
    start_time = datetime.now()
    pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps)
    analysis = Analysis(pn)
    execution_time = datetime.now()-start_time
    print('\n\ntime to execute:', execution_time)
    # Save the network
    
    start_time = datetime.now()    
    print("")
    print("Generating Pickle File...")
    print("")
    print("Starting Time is: ", start_time)
    Analysis.store_to_file(analysis, run_save_name)
    print("")
    print('Network saved to : "' + run_save_name+'.pkl"')
    execution_time = datetime.now()-start_time
    print('\n\nPickling Time:', execution_time)

if __name__ == '__main__':
    main()
