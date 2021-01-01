#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import matplotlib.pyplot as plt
import numpy as np

#from scipy.signal import convolve
#get_ipython().run_line_magic('matplotlib', 'qt')
# Only run this cell once to avoid confusion with directories
# Point this to the directory where HFPN.py is relative to your working directory
cwd = os.getcwd() # Get current working directory
root_folder = os.sep + "HFPN-Stochastic-Version"
# Move to 'utils' from current directory position
sys.path.insert(0, cwd[:(cwd.index(root_folder)+len(root_folder))] + os.sep + "HFPN-Stochastic-Version" + os.sep)
from visualisation import Analysis


# In[2]:
##############################################################################
################Input File Name and Plotting Steps############################
##############################################################################
File1 = '1e6_SD0_1_DelaySD_0_1'
desired_plotting_steps = 1000000

##############################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End - BSL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##############################################################################   
analysis = {}
#analysis['HFPN_Healthy_6x10e6'] = Analysis.load_from_file('HFPN_Healthy_6x10e6')
analysis[File1] = Analysis.load_from_file(File1)
#analysis['HFPN_DJ1_6x10e6'] = Analysis.load_from_file('HFPN_DJ1_6x10e6')
# analysis['HFPN_VPS35_6x10e6'] = Analysis.load_from_file('HFPN_VPS35_6x10e6')

# analysis['HFPN_DJ1_6x10e6'] = Analysis.load_from_file('HFPN_DJ1_6x10e6')
# analysis['DJ1'] = Analysis.load_from_file('pd_DJ1_ds_smallertimestep')
# analysis['lrrk2'] = Analysis.load_from_file('pd_lrrk2_ds_smallertimestep')
# analysis['vps35'] = Analysis.load_from_file('pd_vps35_ds_smallertimestep')
# analysis['gba1_lrrk2'] = Analysis.load_from_file('pd_gba1_lrrk2_ds_smallertimestep')
# analysis['vps35_lrrk2'] = Analysis.load_from_file('pd_vps35_lrrk2_ds_smallertimestep')
# analysis['gba1_vps35_lrrk2'] = Analysis.load_from_file('pd_gba1_vps35_lrrk2_ds_smallertimestep')
# analysis['all_mutations'] = Analysis.load_from_file('pd_all_mutations_ds_smallertimestep')
# analysis['ApoEchol'] = Analysis.load_from_file('pd_2xApoE_ds_smallertimestep')
# analysis['27OHchol'] = Analysis.load_from_file('pd_2x27OH_ds_smallertimestep')
# analysis['ApoE_lrrk2_gba1'] = Analysis.load_from_file('pd_2xApoE_lrrk2_gba1_ds_smallertimestep')
# analysis['27OH_lrrk2_gba1'] = Analysis.load_from_file('pd_2x27OH_lrrk2_gba1_ds_smallertimestep')
# analysis['NPT'] = Analysis.load_from_file('pd_NPT_ds_smallertimestep')
# analysis['DNL'] = Analysis.load_from_file('pd_DNL_ds_smallertimestep')
# analysis['LAMP2A'] = Analysis.load_from_file('pd_LAMP2A_ds_smallertimestep')



# In[3]:


def smoothen(array, filter_size):
    filt=np.ones(filter_size)/filter_size
    return convolve(array[:-(filter_size-1),0],filt)
    
def create_plot(analysis, input_place_list, place_labels, mutation_list, mutation_labels, plot_title):
    t=np.arange(0,(desired_plotting_steps/1000)+0.001,0.001) #

    fig,ax=plt.subplots()
    linestep = 0.3
    line_width = 2.5
    
    for i, mutation in enumerate(mutation_list):
        for place, place_label in zip(input_place_list, place_labels):
            data = analysis[mutation].mean_token_history_for_places([place])[0:desired_plotting_steps+1] #mutation is the file_name
           # print(data[100000]) #units in time_step

            if place_label == "":
                ax.plot(t, data, label = mutation_labels[i], linewidth = line_width- i*linestep, color="black")
            else:
                ax.plot(t, data, label = mutation_labels[i]+' - '+place_label, linewidth = line_width- i*linestep, color="black")
    
    ax.legend()
    Analysis.standardise_plot(ax, title = plot_title, xlabel = "Time (s)",ylabel = "Molecule count")
    
##############################################################################
############## OTHER PLOT PARAMETERS YOU WANT#################################
##############################################################################
    plt.xlim([0,20]) #x axis range in seconds
    #plt.ylim([3.7e9,3.791e9]) #y axis range in tokens
    
    #DASHED LINES
    # plt.axvline(x=1500, linestyle='--', color ='black')
    # plt.axvline(x=1550, linestyle='--', color ='black')
    #plt.axhline(y=80000, linestyle='--', color ='black', label = "p_ROS_mito Threshold = 80k")
    #plt.legend()
##############################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End - BSL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##############################################################################    
    plt.show()

def plot_stacked_bars(ax, legend, all_data, xs, labels, width):

    cum_sum = np.zeros_like(all_data[:,0])
    for i in range(len(labels)):
        data = all_data[:,i]
        rects = ax.bar(xs, data, width, bottom=cum_sum, label=labels[i])
        cum_sum += data    
    
def create_bar_chart(analysis, places_a, places_a_labels, places_b, places_b_labels, mutation_list, mutation_labels, plot_title):
#     for mutation in mutation_list:
#         for place in places_a:
#             print(place)
#             print(analysis[mutation].mean_token_history_for_places(place)[-1])
#     for mutation in mutation_list:
#         for place in places_b:
#             print(place)
#             print(analysis[mutation].mean_token_history_for_places(place)[-1])
    final_token_count_a = [[analysis[mutation].mean_token_history_for_places(place)[-1] for place in places_a] for mutation in mutation_list]
    final_token_count_b = [[analysis[mutation].mean_token_history_for_places(place)[-1] for place in places_b] for mutation in mutation_list]
    print(np.array(final_token_count_a).shape)
    print(np.array(final_token_count_b).shape)
    final_token_count_a = np.sum(final_token_count_a, 2) # remove dimension 3
    final_token_count_b = np.sum(final_token_count_b, 2) # remove dimension 3

    # normalize data

    final_token_count_a = final_token_count_a / np.sum(final_token_count_a[0,:])
    final_token_count_b = final_token_count_b / np.sum(final_token_count_b, 1)[:,None]

    final_token_count_a *= 100
    final_token_count_b *= 100
    
    width = 0.5
    
    FIGURESIZE = (14,7)
    fig, ax = plt.subplots(1, 1, figsize=FIGURESIZE)

    bar_positions_a = np.array(range(len(mutation_list)))
    bar_positions_b = max(bar_positions_a) + 2 + np.array(range(len(mutation_list)))
    
    plot_stacked_bars(ax,legend=mutation_list, all_data=final_token_count_a, xs=bar_positions_a, labels=places_a_labels,width=width)
    plot_stacked_bars(ax,legend=mutation_list, all_data=final_token_count_b, xs=bar_positions_b, labels = places_b_labels,width=width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('% Molecule Count', fontsize=16)
    ax.set_title(plot_title, fontsize=18)
    ax.set_xticks(np.concatenate((bar_positions_a, bar_positions_b)))
    ax.set_xticklabels(np.concatenate((mutation_labels, mutation_labels)), rotation=-25, ha='left', fontsize=12)

    #ax.set_ylim((0,150))

    plt.legend(fontsize=14, loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.show()
    
##############################################################################
################Calcium Relevant Graphs - BSL#################################
##############################################################################

def create_histogram(analysis, bins):
    plt.hist(analysis[File1].delay_list_t_B, bins=bins, edgecolor='black', linewidth=1.2)
    print("NOTE, these are t_B transitions only")
    
    
def calculate_mean_of_delay(analysis):
    list_1 = analysis[File1].delay_list_t_A
    the_mean_t_A = np.mean(list_1)
    print("Mean of delay_list t_A:", the_mean_t_A)
    list_2 = analysis[File1].delay_list_t_B
    the_mean_t_B = np.mean(list_2)
    print("Mean of delay_list t_B:", the_mean_t_B)
    list_3 = analysis[File1].delay_list_t_D
    the_mean_t_D = np.mean(list_3)
    print("Mean of delay_list t_D:", the_mean_t_D)

    
def calculate_TRUE_calcium_stochasticity_for_p_on4():
    """
    This can take a long time since the list is huge.
    """
    data = analysis[File1].mean_token_history_for_places(['p_on4'])[0:desired_plotting_steps+1]
    #data is in a 2 dimensional array for
    list_of_lists = data.tolist()
    normal_list = [item for sublist in list_of_lists for item in sublist]

    list_2 = []

    count = 0

    for index,number in enumerate(normal_list): 
        if number == 0:
            count = count+1
        if number ==1 and normal_list[index-1]==0:
            list_2.append(int(count))
            count = 0
        if number == 0 and index == (len(normal_list)-1): #So situations where we reach the end of the list and we are stuck with a zero are still counted.
            list_2.append(int(count))

    #print(list_2)
    print("Mean Delay over Whole Run for p_on_4:", np.mean(list_2), "timesteps")
    
def calculate_TRUE_calcium_stochasticity_for_p_Ca_extra():
    """
    This can take a long time since the list is huge.
    """
    data = analysis[File1].mean_token_history_for_places(['p_Ca_extra'])[0:desired_plotting_steps+1]
    #data is in a 2 dimensional array for
    list_of_lists = data.tolist()
    normal_list = [item for sublist in list_of_lists for item in sublist]

    list_2 = []

    count = 0

    for index,number in enumerate(normal_list): 
        if number == 0:
            count = count+1
        if number ==1 and normal_list[index-1]==0:
            list_2.append(int(count))
            count = 0
        if number == 0 and index == (len(normal_list)-1): #So situations where we reach the end of the list and we are stuck with a zero are still counted.
            list_2.append(int(count))

    #print(list_2)
    print("Mean Delay over Whole Run for p_Ca_extra:", np.mean(list_2), "timesteps")
    
def calculate_TRUE_calcium_stochasticity_for_p_on3():
    """
    This can take a long time since the list is huge.
    """
    data = analysis[File1].mean_token_history_for_places(['p_on3'])[0:desired_plotting_steps+1]
    #data is in a 2 dimensional array for
    list_of_lists = data.tolist()
    normal_list = [item for sublist in list_of_lists for item in sublist]

    list_2 = []

    count = 0

    for index,number in enumerate(normal_list): 
        if number == 0:
            count = count+1
        if number ==1 and normal_list[index-1]==0:
            list_2.append(int(count))
            count = 0
        if number == 0 and index == (len(normal_list)-1): #So situations where we reach the end of the list and we are stuck with a zero are still counted.
            list_2.append(int(count))

    #print(list_2)
    print("Mean Delay over Whole Run for p_on3:", np.mean(list_2), "timesteps")
    
##############################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End - BSL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##############################################################################   

calculate_TRUE_calcium_stochasticity_for_p_on4()
calculate_TRUE_calcium_stochasticity_for_p_Ca_extra()
calculate_TRUE_calcium_stochasticity_for_p_on3()

# # Bar charts

# In[ ]:


# create_bar_chart(analysis, 
#                  places_a = ['p_ROS_mito', 'p_Ca_cyto'], 
#                  places_a_labels = ['p_ROS_mito', 'p_Ca_cyto'], 
#                  places_b = ['p_RTN3_HMW_dys1','p_RTN3_HMW_dys2','p_RTN3_HMW_lyso'], 
#                  places_b_labels=['Dystrophic neurites I', 'Dystrophic_neurites II','Lyso'], 
#                  mutation_list = ['healthy', 'chol600'], 
#                  mutation_labels = ['healthy', 'chol600'],
#                  plot_title = 'PD - RTN3 distribution')


# In[ ]:


# create_bar_chart(analysis, 
#                  places_a = ['p_RTN3_axon','p_RTN3_PN'], 
#                  places_a_labels = ['Axon', 'Perinuclear region'], 
#                  places_b = ['p_RTN3_HMW_dys1','p_RTN3_HMW_dys2','p_RTN3_HMW_lyso'], 
#                  places_b_labels=['Dystrophic neurites I', 'Dystrophic_neurites II','Lyso'], 
#                  mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A', 'healthy'], 
#                  mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
#                  plot_title = 'PD - RTN3 distribution and therapeutics')


# # Plotting

# ## Energy metabolism 

# In[4]:
# create_plot(analysis, 
#             input_place_list = ['p_chol_mito'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_Healthy_6x10e6'], 
#             mutation_labels = ['HFPN_Healthy_6x10e6'],
#             plot_title = 'PD - p_chol_mito')


# create_plot(analysis, 
#             input_place_list = ['p_27OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_DJ1_6x10e6'], 
#             mutation_labels = ['HFPN_DJ1_6x10e6'],
#             plot_title = 'PD - p_27OHchol_intra')
# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_DJ1_6x10e6'], 
#             mutation_labels = ['HFPN_DJ1_6x10e6'],
#             plot_title = 'PD - p_24OHchol_intra')
# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_DJ1_6x10e6'], 
#             mutation_labels = ['HFPN_DJ1_6x10e6'],
#             plot_title = 'PD - p_cas3')



create_plot(analysis, 
            input_place_list = ['p_on4'], 
            place_labels = [""], 
            mutation_list = [File1], 
            mutation_labels = [File1],
            plot_title = 'PD - p_on4')

create_histogram(analysis, 20)

calculate_mean_of_delay(analysis)

# create_plot(analysis, 
#             input_place_list = ['p_chol_LE'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_Healthy_6x10e6'], 
#             mutation_labels = ['HFPN_Healthy_6x10e6'],
#             plot_title = 'PD - p_chol_LE')

# create_plot(analysis, 
#             input_place_list = ['p_ApoEchol_extra'], 
#             place_labels = [""], 
#             mutation_list = ['HFPN_Healthy_6x10e6'], 
#             mutation_labels = ['HFPN_Healthy_6x10e6'],
#             plot_title = 'PD - p_ApoEchol_extra')

# create_plot(analysis, 
#             input_place_list = ['p_ApoEchol_EE'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_ApoEchol_EE')

# create_plot(analysis, 
#             input_place_list = ['p_7HOCA'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_7HOCA')

# create_plot(analysis, 
#             input_place_list = ['p_preg'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_preg')

# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_extra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_extra')

# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_intra')

# create_plot(analysis, 
#             input_place_list = ['p_ROS_mito'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_ROS_mito')
# create_plot(analysis, 
#             input_place_list = ['p_H2O_mito'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_H2O_mito')
# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_cas3')
# create_plot(analysis, 
#             input_place_list = ['p_Ca_cyto'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_Ca_cyto')
# create_plot(analysis, 
#             input_place_list = ['p_Ca_mito'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_Ca_mito')
# create_plot(analysis, 
#             input_place_list = ['p_Ca_ER'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_Ca_ER')
# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_intra')
# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_intra')
# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_intra')
# create_plot(analysis, 
#             input_place_list = ['p_24OHchol_intra'], 
#             place_labels = [""], 
#             mutation_list = ['DJ1_500k_HFPN'], 
#             mutation_labels = ['DJ1_500k_HFPN'],
#             plot_title = 'PD - p_24OHchol_intra')



# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['testlol'], 
#             mutation_labels = ['testlol'],
#             plot_title = 'PD - p_cas3')

# create_plot(analysis, 
#             input_place_list = ['p_H2O_mito'], 
#             place_labels = [""], 
#             mutation_list = ['testlol'], 
#             mutation_labels = ['testlol'],
#             plot_title = 'PD - p_H2O_mito')

# create_plot(analysis, 
#             input_place_list = ['p_chol_mito'], 
#             place_labels = [""], 
#             mutation_list = ['testlol'], 
#             mutation_labels = ['testlol'],
#             plot_title = 'PD - p_chol_mito')

# # ## Lewy body formation

# # In[ ]:


# create_plot(analysis, 
#             input_place_list = ['p_ATP'], 
#             place_labels = [""], 
#             mutation_list = ['healthy', 'chol600'], 
#             mutation_labels = ['healthy', 'chol600'],
#             plot_title = 'PD - Lewy body formation')


# # ## Chol (LB and cas3)

# # In[ ]:


# #THE CORRECT ONE FOR CHOL
# create_plot(analysis, 
#             input_place_list = ['p_LB'], 
#             place_labels = [""], 
#             mutation_list = ['healthy','gba1_lrrk2','27OHchol','27OH_lrrk2_gba1','ApoEchol','ApoE_lrrk2_gba1'], 
#             mutation_labels = ['Healthy','GBA1 + LRRK2','2x 27OH-chol','2x 27OH-chol + LRRK2 + GBA1','2x APOE-chol','2x APOE-chol + LRRK2 + GBA1'],
#             plot_title = 'PD - Lewy body formation and high levels chol')
# #THE CORRECT ONE FOR CHOL
# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['healthy','gba1_lrrk2','27OHchol','27OH_lrrk2_gba1','ApoEchol','ApoE_lrrk2_gba1'], 
#             mutation_labels = ['Healthy','GBA1 + LRRK2','2x 27OH-chol','2x 27OH-chol + LRRK2 + GBA1','2x APOE-chol','2x APOE-chol + LRRK2 + GBA1'],
#             plot_title = 'PD - Active Caspase-3 and high levels chol')


# # ## Therapeutics

# # In[ ]:


# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A', 'healthy'], 
#             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
#             plot_title = 'PD - Active Caspase-3 and therapeutics')
# # create_plot(analysis, 
# #             input_place_list = ['p_SNCA_olig'], 
# #             place_labels = [""], 
# #             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A','healthy'], 
# #             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
# #             plot_title = 'PD - SNCA oligomerisation and therapeutics')
# create_plot(analysis, 
#             input_place_list = ['p_LB'], 
#             place_labels = [""], 
#             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A','healthy'], 
#             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
#             plot_title = 'PD - Lewy body formation and therapeutics')


# # # Computing the mean

# # In[ ]:


# mean_healthy = np.mean(analysis['healthy'].token_storage[:,50000:,analysis['healthy'].place_dict["p_ATP"]])
# print("healthy", mean_healthy)
# mean_lrrk2 = np.mean(analysis['lrrk2'].token_storage[:,50000:,analysis['lrrk2'].place_dict["p_ATP"]])
# print("lrrk2", mean_lrrk2)


# # In[ ]:


# # create_plot(['p_LB'],"Lewy body formation")


# # In[ ]:


# # create_plot(['p_SNCA_olig'],"SNCA olgiomerisation")


# # In[ ]:



# ## Lewy body formation

# In[ ]:



# ## Chol (LB and cas3)

# In[ ]:


#THE CORRECT ONE FOR CHOL
# create_plot(analysis, 
#             input_place_list = ['p_LB'], 
#             place_labels = [""], 
#             mutation_list = ['healthy','gba1_lrrk2','27OHchol','27OH_lrrk2_gba1','ApoEchol','ApoE_lrrk2_gba1'], 
#             mutation_labels = ['Healthy','GBA1 + LRRK2','2x 27OH-chol','2x 27OH-chol + LRRK2 + GBA1','2x APOE-chol','2x APOE-chol + LRRK2 + GBA1'],
#             plot_title = 'PD - Lewy body formation and high levels chol')
# #THE CORRECT ONE FOR CHOL
# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['healthy','gba1_lrrk2','27OHchol','27OH_lrrk2_gba1','ApoEchol','ApoE_lrrk2_gba1'], 
#             mutation_labels = ['Healthy','GBA1 + LRRK2','2x 27OH-chol','2x 27OH-chol + LRRK2 + GBA1','2x APOE-chol','2x APOE-chol + LRRK2 + GBA1'],
#             plot_title = 'PD - Active Caspase-3 and high levels chol')


# # ## Therapeutics

# # In[ ]:


# create_plot(analysis, 
#             input_place_list = ['p_cas3'], 
#             place_labels = [""], 
#             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A', 'healthy'], 
#             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
#             plot_title = 'PD - Active Caspase-3 and therapeutics')
# # create_plot(analysis, 
# #             input_place_list = ['p_SNCA_olig'], 
# #             place_labels = [""], 
# #             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A','healthy'], 
# #             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
# #             plot_title = 'PD - SNCA oligomerisation and therapeutics')
# create_plot(analysis, 
#             input_place_list = ['p_LB'], 
#             place_labels = [""], 
#             mutation_list = ['all_mutations', 'lrrk2', 'DNL','NPT','LAMP2A','healthy'], 
#             mutation_labels = ['Combined diseased state','LRRK2','LRRK2 + DNL151','Combined diseased state + NPT200','Combined diseased state + LAMP2A', 'Healthy'],
#             plot_title = 'PD - Lewy body formation and therapeutics')


# # # Computing the mean

# # In[ ]:


# mean_healthy = np.mean(analysis['healthy'].token_storage[:,50000:,analysis['healthy'].place_dict["p_ATP"]])
# print("healthy", mean_healthy)
# mean_lrrk2 = np.mean(analysis['lrrk2'].token_storage[:,50000:,analysis['lrrk2'].place_dict["p_ATP"]])
# print("lrrk2", mean_lrrk2)


# In[ ]:


# create_plot(['p_LB'],"Lewy body formation")


# In[ ]:


# create_plot(['p_SNCA_olig'],"SNCA olgiomerisation")


# In[ ]:







# # In[ ]:


# create_plot(['p_chol_LE'],"Cholesterol late endosomes")



# In[ ]:




