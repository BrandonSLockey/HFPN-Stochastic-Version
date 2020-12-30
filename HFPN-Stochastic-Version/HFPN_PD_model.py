import os
import sys

cwd = os.getcwd() # Get current working directory
root_folder = os.sep + "PN_Alzheimers_Parkinsons"
# Move to 'utils' from current directory position
sys.path.insert(0, cwd[:(cwd.index(root_folder)+len(root_folder))] + os.sep + "HFPN model" + os.sep + "utils" + os.sep)

# Import HFPN class to work with hybrid functional Petri nets
from hfpn import HFPN

# Import initial token, firing conditions and rate functions
from PD_HFPN_initial_tokens import *
from PD_HFPN_rate_functions import *
from PD_HFPN_firing_conditions import *
from PD_HFPN_inputs import *
from visualisation import Analysis

def main():
    # Initialize an empty HFPN
    pn = HFPN(time_step = time_step_size) #unit = s/A.U.

    ## Define places

   #  # Cholesterol homeostasis
    pn.add_place(it_p_chol_PM, "p_chol_PM","Chol - perinuclear region", continuous = True)
    pn.add_place(it_p_chol_LE, "p_chol_LE", "Chol - late endosome", continuous = True)
    pn.add_place(it_p_chol_ER, "p_chol_ER", "Chol - ER", continuous = True)
    pn.add_place(it_p_chol_mito, "p_chol_mito", "Chol - mitochondria", continuous = True)
    pn.add_place(it_p_27OHchol_extra, "p_27OHchol_extra","27-OH chol - extracellular", continuous = True)
    pn.add_place(it_p_27OHchol_intra, "p_27OHchol_intra","27-OH chol - intracellular", continuous = True)
    pn.add_place(it_p_ApoEchol_extra, "p_ApoEchol_extra","ApoE - extracellular", continuous = True)
    pn.add_place(it_p_ApoEchol_EE, "p_ApoEchol_EE","ApoE - Early endosome", continuous = True)
    pn.add_place(it_p_7HOCA, "p_7HOCA","7-HOCA", continuous = True)
    pn.add_place(it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
    pn.add_place(it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24OHchol extra", continuous=True)
    pn.add_place(it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24OHchol intra", continuous=True)

    #  # PD specific places in cholesterol homeostasis
    pn.add_place(it_p_GBA1, "p_GBA1","GBA1", continuous = False)
    pn.add_place(it_p_SNCA_act_extra, "p_SNCA_act_extra","a-synuclein - extracellular", continuous = True)
    pn.add_place(it_p_SNCAApoEchol_extra, "p_SNCAApoEchol_extra","a-synuclein-ApoE complex - extracellular", continuous = True)
    pn.add_place(it_p_SNCAApoEchol_intra, "p_SNCAApoEchol_intra","a-synuclein-ApoE complex - intracellular", continuous = True)

    #  # Energy metabolism
    pn.add_place(it_p_ROS_mito, "p_ROS_mito", "ROS - mitochondria", continuous = True)
    pn.add_place(it_p_H2O_mito, "p_H2O_mito", "H2O - mitochondria", continuous = True)
    pn.add_place(it_p_reduc_mito, "p_reduc_mito", "Reducing agents - mitochondria", continuous = True)
    pn.add_place(it_p_cas3, "p_cas3","caspase 3 - mitochondria", continuous = True)
    pn.add_place(it_p_DJ1, "p_DJ1","DJ1 mutant", continuous = True)
    
    #  # Calcium homeostasis
    pn.add_place(it_p_Ca_cyto, "p_Ca_cyto", "Ca - cytosole", continuous = True)
    pn.add_place(it_p_Ca_mito, "p_Ca_mito","Ca - mitochondria", continuous = True)
    pn.add_place(it_p_Ca_ER, "p_Ca_ER", "Ca - ER", continuous = True)
    pn.add_place(it_p_ADP, "p_ADP","ADP - Calcium ER import", continuous = True)
    pn.add_place(it_p_ATP, "p_ATP","ATP - Calcium ER import", continuous = True)

    #  # Discrete on/of-switches calcium pacemaking

    pn.add_place(1, "p_Ca_extra", "on1 - Ca - extracellular", continuous = False)
    pn.add_place(0, "p_on2","on2", continuous = False)
    pn.add_place(0, "p_on3","on3", continuous = False)
    pn.add_place(0, "p_on4","on4", continuous = False)
    
      # Lewy bodies
    pn.add_place(it_p_SNCA_act, "p_SNCA_act","SNCA - active", continuous = True)
    pn.add_place(it_p_VPS35, "p_VPS35", "VPS35", continuous = True)
    pn.add_place(it_p_SNCA_inact, "p_SNCA_inact", "SNCA - inactive", continuous = True)
    pn.add_place(it_p_SNCA_olig, "p_SNCA_olig", "SNCA - Oligomerised", continuous = True)
    pn.add_place(it_p_LB, "p_LB", "Lewy body", continuous = True)
    pn.add_place(it_p_Fe2, "p_Fe2", "Fe2 iron pool", continuous = True)
    
      # Late endosome pathology 
    pn.add_place(it_p_LRRK2_mut, "p_LRRK2_mut","LRRK2 - mutated", continuous = True)
      # Monomeric RTN3 (cycling between axonal and perinuclear regions)
    pn.add_place(it_p_RTN3_axon, place_id="p_RTN3_axon", label="monomeric RTN3 (axonal)", continuous=True)
    pn.add_place(it_p_RTN3_PN, place_id="p_RTN3_PN", label="monomeric RTN3 (perinuclear)", continuous=True)

      # HMW RTN3 (cycling between different cellular compartments)
    pn.add_place(it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
    pn.add_place(it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)

      # Two places that are NOT part of this subpathway, but are temporarily added for establishing proper connections
      # They will be removed upon merging of subpathways
    pn.add_place(it_p_tau, place_id="p_tau", label = "Unphosphorylated tau", continuous = True)
    pn.add_place(it_p_tauP, place_id="p_tauP", label = "Phosphorylated tau", continuous = True)
    
    # Drug places 
    pn.add_place(it_p_NPT200, place_id="p_NPT200", label = "Drug NPT200", continuous = True)
    pn.add_place(it_p_DNL151, place_id="p_DNL151", label = "Drug DNL151", continuous = True)
    pn.add_place(it_p_LAMP2A, place_id="p_LAMP2A", label = "Drug LAMP2A", continuous = True)
    
    ## Define transitions
    
    # Cholesterol Endocytosis
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_LDLR_endocyto",
                    label 						 = "LDLR endocyto",
                    input_place_ids				 = ["p_ApoEchol_extra", "p_chol_ER","p_LB"],
                    firing_condition			 = fc_t_LDLR_endocyto,
                    reaction_speed_function		 = r_t_LDLR_endocyto, 
                    consumption_coefficients	 = [0,0,0],
                    output_place_ids			 = ["p_ApoEchol_EE"],
                    production_coefficients		 = [1])

    # # Cleavage of cholesteryl esters
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_ApoEchol_cleav",
                    label 						 = "ApoE-chol cleav",
                    input_place_ids				 = ["p_ApoEchol_EE"],
                    firing_condition			 = fc_t_ApoEchol_cleav,
                    reaction_speed_function		 = r_t_ApoEchol_cleav, 
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_LE"],
                    production_coefficients		 = [354])

    # Transport Cholesterol from LE to ER
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_ER",
                    label 						 = "Chol transport LE-ER",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_ER,
                    reaction_speed_function		 = r_t_chol_trans_LE_ER,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_ER"],
                    production_coefficients		 = [1])

    # Transport Cholesterol from LE to mito
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_mito",
                    label 						 = "Chol transport LE-mito",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_mito,
                    reaction_speed_function		 = r_t_chol_trans_LE_mito,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_mito"],
                    production_coefficients		 = [1])

    # Transport Cholesterol from LE to PM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_LE_PM",
                    label 						 = "Chol transport LE-PM",
                    input_place_ids				 = ["p_chol_LE"],
                    firing_condition			 = fc_t_chol_trans_LE_PM, 
                    reaction_speed_function		 = r_t_chol_trans_LE_PM,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_PM"],
                    production_coefficients		 = [1])

    # Transport Cholesterol from PM to ER
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_PM_ER",
                    label 						 = "Chol transport PM-ER",
                    input_place_ids				 = ["p_chol_PM"],
                    firing_condition			 = fc_t_chol_trans_PM_ER,
                    reaction_speed_function		 = r_t_chol_trans_PM_ER,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_ER"],
                    production_coefficients		 = [1])

    # Transport Cholesterol from ER to PM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_ER_PM",
                    label 						 = "Chol transport ER-PM",
                    input_place_ids				 = ["p_chol_ER"],
                    firing_condition			 = fc_t_chol_trans_ER_PM,
                    reaction_speed_function		 = r_t_chol_trans_ER_PM,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_PM"],
                    production_coefficients		 = [1])

    # Transport Cholesterol from ER to mito
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_ER_mito",
                    label 						 = "Chol transport ER-mito",
                    input_place_ids				 = ["p_chol_ER"],
                    firing_condition			 = fc_t_chol_trans_ER_mito,
                    reaction_speed_function		 = r_t_chol_trans_ER_mito,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_chol_mito"],
                    production_coefficients		 = [1])

    # Metabolisation of chol by CYP27A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP27A1_metab",
                    label 						 = "Chol metab CYP27A1",
                    Km							 = Km_t_CYP27A1_metab,
                    vmax						 = vmax_t_CYP27A1_metab,
                    input_place_ids				 = ["p_chol_mito"],
                    substrate_id				 = "p_chol_mito",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_27OHchol_intra"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = lambda a : chol_mp)

    # Metabolism of chol by CYP11A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP11A1_metab",
                    label 						 = "Chol metab CYP11A1",
                    Km							 = Km_t_CYP11A1_metab,
                    vmax						 = vmax_t_CYP11A1_metab,
                    input_place_ids				 = ["p_chol_mito"],
                    substrate_id				 = "p_chol_mito",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_preg"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = lambda a : chol_mp)

    # Metabolisation of 27OHchol by CYP7B1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP7B1_metab",
                    label 						 = "27OHchol metab CYP7B1",
                    Km							 = Km_t_CYP7B1_metab,
                    vmax						 = vmax_t_CYP7B1_metab,
                    input_place_ids				 = ["p_27OHchol_intra"],
                    substrate_id				 = "p_27OHchol_intra",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_7HOCA"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = lambda a : chol_mp)

    # Endocytosis of 27OHchol
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_27OHchol_endocyto",
                    label 						 = "27OHchol endocyto",
                    input_place_ids				 = ["p_27OHchol_extra"],
                    firing_condition			 = fc_t_27OHchol_endocyto,
                    reaction_speed_function		 = r_t_27OHchol_endocyto,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_27OHchol_intra", "p_27OHchol_extra"],
                    production_coefficients		 = [1,1])

    # Metabolisation of chol by CYP46A1
    pn.add_transition_with_michaelis_menten(
                    transition_id				 = "t_CYP46A1_metab",
                    label 						 = "Chol metab CYP46A1",
                    Km							 = Km_t_CYP46A1_metab,
                    vmax						 = vmax_t_CYP46A1_metab,
                    input_place_ids				 = ["p_chol_ER"],
                    substrate_id				 = "p_chol_ER",
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_24OHchol_intra"],
                    production_coefficients		 = [1],
                    vmax_scaling_function		 = lambda a : chol_mp)

    # Exocytosis of 24OHchol
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_24OHchol_exocyto",
                    label 						 = "24OHchol exocyto",
                    input_place_ids				 = ["p_24OHchol_intra"],
                    firing_condition			 = fc_t_24OHchol_exocyto,
                    reaction_speed_function		 = r_t_24OHchol_exocyto,
                    consumption_coefficients	 = [1],
                    output_place_ids			 = ["p_24OHchol_extra"],
                    production_coefficients		 = [1])

    # Transport of Chol into ECM
    pn.add_transition_with_speed_function(
                    transition_id				 = "t_chol_trans_PM_ECM",
                    label 						 = "Chol transport PM-ECM",
                    input_place_ids				 = ["p_chol_PM", "p_24OHchol_intra"],
                    firing_condition			 = fc_t_chol_trans_PM_ECM,
                    reaction_speed_function		 = r_t_chol_trans_PM_ECM,
                    consumption_coefficients	 = [1,0],
                    output_place_ids			 = [],
                    production_coefficients		 = [])


    # PD specific

    pn.add_transition_with_speed_function(
                        transition_id = 't_SNCA_bind_ApoEchol_extra',
                        label = 'Extracellular binding of SNCA to chol',
                        input_place_ids = ['p_ApoEchol_extra','p_SNCA_act'],
                        firing_condition = fc_t_SNCA_bind_ApoEchol_extra,
                        reaction_speed_function = r_t_SNCA_bind_ApoEchol_extra,
                        consumption_coefficients = [0,30], 
                        output_place_ids = ['p_SNCA_olig'],         
                        production_coefficients = [1])

    pn.add_transition_with_speed_function(
                        transition_id = 't_chol_LE_upreg',
                        label = 'Upregulation of chol in LE',
                        input_place_ids = ['p_GBA1'],
                        firing_condition = fc_t_chol_LE_upreg,
                        reaction_speed_function = r_t_chol_LE_upreg,
                        consumption_coefficients = [0], # GBA1 is an enzyme
                        output_place_ids = ['p_chol_LE'],         
                        production_coefficients = [1])
    
    # # Calcium homeostasis
    
    pn.add_transition_with_speed_function(
                        transition_id = 't_Ca_imp',
                        label = 'L-type Ca channel',
                        input_place_ids = ['p_Ca_extra'],
                        firing_condition = fc_t_Ca_imp,
                        reaction_speed_function = r_t_Ca_imp,
                        consumption_coefficients = [0], # Need to review this 
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1]) # Need to review this 


    pn.add_transition_with_speed_function(
                        transition_id = 't_mCU',
                        label = 'Ca import into mitochondria via mCU',
                        input_place_ids = ['p_Ca_cyto','p_Ca_mito'],
                        firing_condition = fc_t_mCU,
                        reaction_speed_function = r_t_mCU,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_Ca_mito'],         
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_MAM',
                        label = 'Ca transport from ER to mitochondria',
                        input_place_ids = ['p_Ca_ER','p_Ca_mito'],
                        firing_condition = fc_t_MAM,
                        reaction_speed_function = r_t_MAM,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_Ca_mito'],         
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_RyR_IP3R',
                        label = 'Ca export from ER',
                        input_place_ids = ['p_Ca_extra','p_Ca_ER'],
                        firing_condition = fc_t_RyR_IP3R,
                        reaction_speed_function = r_t_RyR_IP3R,
                        consumption_coefficients = [0,1], 
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_SERCA',
                        label = 'Ca import to ER',
                        input_place_ids = ['p_Ca_cyto','p_ATP'],
                        firing_condition = fc_t_SERCA,
                        reaction_speed_function = r_t_SERCA,
                        consumption_coefficients = [1,1], #!!!!! Need to review this 0 should be 1
                        output_place_ids = ['p_Ca_ER','p_ADP'],         
                        production_coefficients = [1,1]) # Need to review this

    pn.add_transition_with_speed_function(
                        transition_id = 't_NCX_PMCA',
                        label = 'Ca efflux to extracellular space',
                        input_place_ids = ['p_Ca_cyto','p_on3'],
                        firing_condition = lambda a: a['p_on3']==1,
                        reaction_speed_function = r_t_NCX_PMCA,
                        consumption_coefficients = [1,0], 
                        output_place_ids = [],         
                        production_coefficients = [])
    pn.add_transition_with_speed_function(
                        transition_id = 't_mNCLX',
                        label = 'Ca export from mitochondria via mNCLX',
                        input_place_ids = ['p_Ca_mito','p_LRRK2_mut'],
                        firing_condition = fc_t_mNCLX,
                        reaction_speed_function = r_t_mNCLX,
                        consumption_coefficients = [1,0], 
                        output_place_ids = ['p_Ca_cyto'],         
                        production_coefficients = [1]) 

    # # Discrete on/off-switches calcium pacemaking

    pn.add_transition_with_speed_function(
                        transition_id = 't_A',
                        label = 'A',
                        input_place_ids = ['p_on4'],
                        firing_condition = lambda a: a['p_on4']==1,
                        reaction_speed_function = lambda a: 1,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_Ca_extra'],         
                        production_coefficients = [1],
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
                        production_coefficients = [1])
    
   # Lewy bodies pathology
    pn.add_transition_with_speed_function(
                        transition_id = 't_SNCA_degr',
                        label = 'SNCA degradation by CMA',
                        input_place_ids = ['p_SNCA_act','p_VPS35','p_LRRK2_mut','p_27OHchol_intra','p_DJ1', 'p_DNL151', 'p_LAMP2A'],
                        firing_condition = fc_t_SNCA_degr,
                        reaction_speed_function = r_t_SNCA_degr,
                        consumption_coefficients = [1,0,0,0,0,0,0], 
                        output_place_ids = ['p_SNCA_inact'],         
                        production_coefficients = [1])

    pn.add_transition_with_speed_function(
                        transition_id = 't_SNCA_aggr',
                        label = 'SNCA aggregation',
                        input_place_ids = ['p_SNCA_act','p_Ca_cyto','p_ROS_mito', 'p_tauP', 'p_NPT200'],
                        firing_condition = fc_t_SNCA_aggr,
                        reaction_speed_function = r_t_SNCA_aggr,
                        consumption_coefficients = [30,0,0,0,0], #should be reviewed if Ca is consumed
                        output_place_ids = ['p_SNCA_olig'],         
                        production_coefficients = [1])

    pn.add_transition_with_speed_function(
                        transition_id = 't_SNCA_fibril',
                        label = 'SNCA fibrillation',
                        input_place_ids = ['p_SNCA_olig'],
                        firing_condition = fc_t_SNCA_fibril,
                        reaction_speed_function = r_t_SNCA_fibril,
                        consumption_coefficients = [100], 
                        output_place_ids = ['p_LB'],         
                        production_coefficients = [1])

    pn.add_transition_with_speed_function(
                        transition_id = 't_IRE',
                        label = 'IRE',
                        input_place_ids = ['p_Fe2'],
                        firing_condition = fc_t_IRE,
                        reaction_speed_function = r_t_IRE,
                        consumption_coefficients = [0], 
                        output_place_ids = ['p_SNCA_act'],         
                        production_coefficients = [1])
    
    # Energy metabolism
    pn.add_transition_with_speed_function(
                        transition_id = 't_ATP_hydro_mito',
                        label = 'ATP hydrolysis in mitochondria',
                        input_place_ids = ['p_ATP'],
                        firing_condition = fc_t_ATP_hydro_mito,
                        reaction_speed_function = r_t_ATP_hydro_mito,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_ADP'],         
                        production_coefficients = [1])
    pn.add_transition_with_speed_function(
                        transition_id = 't_ROS_metab',
                        label = 'ROS neutralisation',
                        input_place_ids = ['p_ROS_mito','p_chol_mito','p_LB','p_DJ1'],
                        firing_condition = fc_t_ROS_metab,
                        reaction_speed_function = r_t_ROS_metab,
                        consumption_coefficients = [1,0,0,0], 
                        output_place_ids = ['p_H2O_mito'],         
                        production_coefficients = [1])
    # #Link of krebs to calcium homeostasis
    pn.add_transition_with_speed_function(
                        transition_id = 't_krebs',
                        label = 'Krebs cycle',
                        input_place_ids = ['p_ADP','p_Ca_mito'],
                        firing_condition = fc_t_krebs,
                        reaction_speed_function = r_t_krebs,
                        consumption_coefficients = [1,0], # Need to review this
                        output_place_ids = ['p_reduc_mito','p_ATP'],         
                        production_coefficients = [4,1])
    #Link of ETC to calcium and cholesterol
    pn.add_transition_with_speed_function(
                        transition_id = 't_ETC',
                        label = 'Electron transport chain',
                        input_place_ids = ['p_reduc_mito', 'p_ADP', 'p_Ca_mito', 'p_chol_mito','p_ROS_mito','p_LRRK2_mut'],
                        firing_condition = fc_t_ETC,
                        reaction_speed_function = r_t_ETC,
                        consumption_coefficients = [22/3,22,0,0,0,0], # Need to review this
                        output_place_ids = ['p_ATP', 'p_ROS_mito'],         
                        production_coefficients = [22,0.005])


    # # Output transitions: Cas3 for apoptosis
    pn.add_transition_with_speed_function(
                        transition_id = 't_mito_dysfunc',
                        label = 'Mitochondrial complex 1 dysfunction',
                        input_place_ids = ['p_ROS_mito'],
                        firing_condition = fc_t_mito_dysfunc,
                        reaction_speed_function = r_t_mito_dysfunc,
                        consumption_coefficients = [1], 
                        output_place_ids = ['p_cas3'],         
                        production_coefficients = [1])
    pn.add_transition_with_speed_function(
                        transition_id = 't_cas3_inact',
                        label = 'Caspase 3 degredation',
                        input_place_ids = ['p_cas3'],
                        firing_condition = fc_t_cas3_inact,
                        reaction_speed_function = r_t_cas3_inact,
                        consumption_coefficients = [1], # Need to review this
                        output_place_ids = [],         
                        production_coefficients = [])
    
    # Late endosome pathology
    pn.add_transition_with_michaelis_menten(transition_id = 't_phos_tau',
                        label = 'Phosphorylation of tau',
                        Km = Km_t_phos_tau, 
                        vmax = kcat_t_phos_tau, 
                        input_place_ids = ['p_tau', 'p_SNCA_act'],
                        substrate_id = 'p_tau',
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_tauP'],
                        production_coefficients = [1],
                        vmax_scaling_function = vmax_scaling_t_phos_tau)

    pn.add_transition_with_michaelis_menten(transition_id = 't_dephos_tauP',
                        label = 'Dephosphorylation of tau protein',
                        Km = Km_t_dephos_tauP, 
                        vmax = vmax_t_dephos_tauP, 
                        input_place_ids = ['p_tauP', 'p_Ca_cyto'],
                        substrate_id = 'p_tauP',
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_tau'],
                        production_coefficients = [1],
                        vmax_scaling_function = vmax_scaling_t_dephos_tauP)

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_exp',
                        label = 'Expression rate of RTN3',
                        input_place_ids = [], 
                        firing_condition = fc_t_RTN3_exp,
                        reaction_speed_function = r_t_RTN3_exp, 
                        consumption_coefficients = [],
                        output_place_ids = ['p_RTN3_PN'],
                        production_coefficients = [1])

    pn.add_transition_with_speed_function(
                        transition_id = 't_LE_retro',
                        label = 'retrograde transport of LEs & ER',
                        input_place_ids = ['p_ATP','p_chol_LE','p_RTN3_axon', 'p_tau','p_LRRK2_mut','p_LB'], 
                        firing_condition = fc_t_LE_retro,
                        reaction_speed_function = r_t_LE_retro, 
                        consumption_coefficients = [ATPcons_t_LE_trans, 0, 1, 0,0,0],
                        output_place_ids = ['p_ADP','p_RTN3_PN'],
                        production_coefficients = [ATPcons_t_LE_trans, 1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_LE_antero',
                        label = 'anterograde transport of LEs & ER',
                        input_place_ids = ['p_ATP','p_RTN3_PN', 'p_tau'], # didn't connect p_tau yet
                        firing_condition = fc_t_LE_antero,
                        reaction_speed_function = r_t_LE_antero, # get later from NPCD
                        consumption_coefficients = [ATPcons_t_LE_trans, 1, 0], # tune these coefficients based on PD
                        output_place_ids = ['p_ADP','p_RTN3_axon'],
                        production_coefficients = [ATPcons_t_LE_trans, 1]) # tune these coefficients based on PD

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_aggregation',
                        label = 'aggregation of monomeric RTN3 into HMW RTN3',
                        input_place_ids = ['p_RTN3_axon', 'p_RTN3_PN'], 
                        firing_condition = fc_t_RTN3_aggregation, # tune aggregation limit later
                        reaction_speed_function = r_t_RTN3_aggregation,
                        consumption_coefficients = [1, 1],
                        output_place_ids = ['p_RTN3_HMW_cyto'],
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_auto',
                        label = 'functional autophagy of HMW RTN3',
                        input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                        firing_condition = fc_t_RTN3_auto, 
                        reaction_speed_function = r_t_RTN3_auto,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_auto'],
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_lyso',
                        label = 'functional delivery of HMW RTN3 to the lysosome',
                        input_place_ids = ['p_RTN3_HMW_auto', 'p_tau'], 
                        firing_condition = fc_t_RTN3_lyso, 
                        reaction_speed_function = r_t_RTN3_lyso,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_lyso'],
                        production_coefficients = [1]) 

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_dys_auto',
                        label = 'dysfunctional autophagy of HMW RTN3',
                        input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                        firing_condition = fc_t_RTN3_dys_auto, 
                        reaction_speed_function = r_t_RTN3_dys_auto,
                        consumption_coefficients = [1, 0],
                        output_place_ids = ['p_RTN3_HMW_dys1'],
                        production_coefficients = [1]) # tune later when data are incorporated

    pn.add_transition_with_speed_function(
                        transition_id = 't_RTN3_dys_lyso',
                        label = 'dysfunctional delivery of HMW RTN3 to the lysosome',
                        input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
                        firing_condition = fc_t_RTN3_dys_lyso, 
                        reaction_speed_function = r_t_RTN3_dys_lyso,
                        consumption_coefficients = [1, 0, 0],
                        output_place_ids = ['p_RTN3_HMW_dys2'],
                        production_coefficients = [1]) # tune later when data are incorporated
    
    # Run the network
    pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps)
    analysis = Analysis(pn)
    
    # Save the network
    Analysis.store_to_file(analysis, run_save_name)

    print('Network saved to : "' + run_save_name+'.pkl"')
    
if __name__ == "__main__":
    main()