import numpy as np
import pickle 
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import sys


from Stochastic_PN_Architecture_v2 import * 



class Analysis:
    """Analysis class for producing plots and statistics."""
    
    def __init__(self, sn, save_all_data=True):
        """
            Args:
                sn: instance of Stochastic Net after all runs have been completed
                save_all_data (bool): whether to save every data point of the time-series data
        """
        step = 1 if save_all_data else max(1, int(len(sn.time_array)/1000))
#hfpn
        self.places = sn.petri_net_model.places # Dictionary
        self.place_ids = np.array(list(sn.petri_net_model.places.keys())) 
        self.transition_ids = np.array(list(sn.petri_net_model.transitions.keys()))
        self.token_storage = sn.timeseries_mean
        # self.mean_firings = sn.mean_firings # probably what successful firings was in our old code, but i removed it lol
        self.time_array = np.arange(0, sn.number_of_steps*0.001+0.001, 0.001)
        #print(self.time_array)
        self.place_dict = self.place_number_dict_maker()
        self.transition_dict = self.transition_dict_maker()
        
        #self.dict_of_tokens = sn.dict_of_tokens # not defined idk why
        
        
        

    @staticmethod
    def store_to_file(analysis_instance, filename):
        """Store an instance of the Analysis class to a pickle (pkl) file.

            Args:
                filename (str): name of file, without extension
        """
        with open(f"{filename}.pkl", 'wb') as filehandler:
            pickle.dump(analysis_instance, filehandler)
       

    @staticmethod
    def load_from_file(filename):
        """Load an instance of the Analysis class from a pickle file.

            Args:
                filename (str): name of file storing the Analysis instance

            Returns:
                Instance of the Analysis class 
        """
        with open(f"{filename}.pkl", 'rb') as filehandler:
            analysis_instance = pickle.load(filehandler)
            
        return analysis_instance

    def place_number_dict_maker(self):
        """Returns a dictionary that relates place id to array position."""
        place_dict = {}
        for i in range(len(self.place_ids)):
            place_dict[self.place_ids[i]] = i
        return place_dict

    def transition_dict_maker(self):
        """Returns a dictionary that relates transition id to array position."""
        transition_dict = {}
        for i in range(len(self.transition_ids)):
            transition_dict[self.transition_ids[i]] = i
        return transition_dict

    def mean_run_tokens_over_time(self, places_to_plot, title="", labels_in_legend=True, figure_size=(6.4, 4.8), logy=False):
        """
            Args:
                places_to_plot (list): list of place ids defining which token counts should be plotted
                labels_in_legend (bool): whether to use the place labels in the legend instead of the place ids
            
            Returns: 
        """
        if type(places_to_plot) == str:
            places_to_plot = [places_to_plot]
        
        # Logic example
        # place_ids = ['1', '2', '3', '4']
        # places_to_plot = ['4', '1']
        # truth values = [True, False, False, True]

        # Take the mean token count over all runs
        mean_run_tokens = np.mean(self.token_storage, axis = 0)
        # Returns a truth table of which places to plot
        truth_values = [place in places_to_plot for place in self.place_ids]
        mean_run_tokens_to_plot = mean_run_tokens[:,truth_values]

        # Extract the place ids and token values to plot
        place_ids_ordered = [self.places[place].place_id for place in self.place_ids if place in places_to_plot]
        place_labels_ordered = [self.places[place].label for place in self.place_ids if place in places_to_plot]

        tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),(148, 103, 189), 
                      (140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]
        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
        for i in range(len(tableau20)):
            r, g, b = tableau20[i]    
            tableau20[i] = (r / 255., g / 255., b / 255.)

        fig, ax = plt.subplots(1, 1, figsize=figure_size)
        for i in range(len(place_labels_ordered)):
            ax.plot(self.time_array, mean_run_tokens_to_plot[:,i], 
                      label=place_labels_ordered[i] if labels_in_legend else place_ids_ordered[i],
                      color=tableau20[i])

        Analysis.standardise_plot(ax, title , "Time (s)", "Mean token count")
        if logy:
            plt.yscale('log')
        plt.legend(fontsize=14)
        plt.show()

        return fig, ax

    # def mean_firings_over_runs_plotter(self, transitions_to_plot):
    #     """
    #         Args:
    #             transitions_to_plot  (list): list of transition ids for which mean number of firings should be plotted
    #     """
    #     truth_values = [t in transitions_to_plot for t in self.transition_ids]

    #     # Extract the transition ids and mean firing values to plot
    #     transitions_to_plot_ordered = self.transition_ids[truth_values]
    #     mean_firings_to_plot = self.mean_firings[truth_values]

    #     plt.bar(transitions_to_plot_ordered, mean_firings_to_plot)
    #     plt.title(f"Mean number of firings")
    #     plt.ylabel('Mean number of firings')
    #     plt.show()
    
    @staticmethod
    def standardise_plot(ax, title="", xlabel="", ylabel=""):
        """Formats the plot to be ready for the final report.
        
            Args:
                ax: matplotlib axis object for a particular plot
                title (str): the title of the plot
                xlabel (str): label on the x-axis
                ylabel (str): label on the y-axis
        """
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Verdana']
        ax.spines["top"].set_visible(False)   # Hide top line
        ax.spines["right"].set_visible(False) # Hide right line
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.ticklabel_format(useOffset=False)
        ax.set_title(f"{title}", fontsize=18)
        ax.set_xlabel(f"{xlabel}", fontsize=16)
        ax.set_ylabel(f"{ylabel}", fontsize=16)
        ax.set_xlim(0)
        #ax.set_ylim(0)
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        ax.tick_params(axis = "x", which = "both", bottom = False, top = False)
        ax.tick_params(axis = "y", which = "both", left = False, right = False)
        plt.grid(color=(0.9, 0.9, 0.9),linestyle="-", linewidth=1)

    def mean_token_history_for_places(self, places):
        """ Returns the mean number of tokens for the listed places.

            Args:
                places (list): list of place ids defining which token counts should be plotted
        """    
        if type(places) == str:
            places = [places]

        # Take the mean token count over all runs
        
        #NEW
        mean_run_tokens = self.token_storage
        #OLD
        # mean_run_tokens = np.mean(self.token_storage, axis = 0)
       
        # Returns a truth table of which places to plot
        truth_values = [place in places for place in self.place_ids]

        return mean_run_tokens[:,truth_values]

    def sum_tokens(self, places):
        return np.sum(self.mean_token_history_for_places(places), axis=1)

    def sum_tokens_plotter(self, places):
        data = self.sum_tokens(places)
        plt.plot(self.time_array, data)
        plt.ylim(np.min(data)-1, np.max(data)+1)

        plt.xlabel('Time (s)')
        plt.ylabel('Sum of mean number of tokens')
        plt.title(f'Sum of tokens for {[str(p) for p in places]}')
        plt.show()


    def transition_transfer_history(self, transitions):
        """ Obtain the number of tokens transferred per time step for the specified transitions.
        
            Args:
                transitions (list): list of transition ids
            Returns:
                list of found transition_ids and corresponding token_transfer_history
        """    
        ids = [t.transition_id for t in self.sn.transitions.values() if t.transition_id in transitions]
        values = [t.token_transfer_history for t in self.sn.transitions.values() if t.transition_id in transitions]
        return ids, np.array(values).transpose()

    def transition_transfer_history_plotter(self, transitions):
        ids, data = self.transition_transfer_history(transitions)
        plt.plot(data)
        diff = np.max(data) - np.min(data)
        plt.ylim(np.min(data)-0.05*diff, np.max(data)+0.05*diff)
        plt.legend([str(t) for t in ids])
        plt.xlabel('Time-step')
        plt.ylabel('Tokens transferred')
        plt.title(f'Smallest non-zero number of tokens transferred for each transition')
        plt.show()
      

# if __name__ == '__main__':
#     pn = PetriNet(number_of_runs=1)
#     # Add places for each chemical species

#     alpha = 0.5

#     it_p_ApoEchol_EE = 2.5 * 1e3 #have been altering this since it's not in literature
#     it_p_chol_LE = 2.65 * 1e9 
#     chol_mp=300
#     vmax_t_ApoEchol_cleav = 1.86 * 10 ** 5
#     Km_t_ApoEchol_cleav = 1.39 * 10 ** 7
#     pn.add_place(it_p_chol_LE, place_id="p_chol_LE",label="Chol - late endosome")
#     pn.add_place(it_p_ApoEchol_EE, place_id="p_ApoEchol_EE",label="ApoE - Early endosome")
    
#     fc_t_ApoEchol_cleav = lambda a : a["p_ApoEchol_EE"] > 1
    
#     r_t_ApoEchol_cleav = lambda a : chol_mp* (vmax_t_ApoEchol_cleav * a["p_ApoEchol_EE"]* 227)/(Km_t_ApoEchol_cleav + a["p_ApoEchol_EE"] * 227)
    
#     pn.add_transition(transition_id = 't_ApoEchol_cleav',
#                     label      =     "ApoE-chol cleav",
#                     input_place_ids         =  ['p_ApoEchol_EE'],
#                     input_arc_weights  =  [1],
#                     output_place_ids         =  ['p_chol_LE'],
#                     output_arc_weights =  [354], 
#                     distribution_type = ["grf",0,r_t_ApoEchol_cleav, fc_t_ApoEchol_cleav])
     

#     pn.run(1000, print_stats=False)
#     list_for_plot = ["p_chol_LE"]
#     pn.plot_time_evolution(list_for_plot) #we need this so that dict_of_tokens gets called
#     analysis = Analysis(pn)

#     # analysis.mean_run_tokens_over_time(['p_ApoEchol_EE', 'p_chol_LE'], 
#     #                                    title="Concentrations versus time", 
#     #                                    labels_in_legend=True)


#     # analysis.mean_firings_over_runs_plotter(['t_ApoEchol_cleav'])
#     # analysis.sum_tokens_plotter(['p_ApoEchol_EE', 'p_chol_LE'])
#     # analysis.transition_transfer_history_plotter(['t_1', 't_2'])

#     run_save_name = "ggjiaogjioa"
#     Analysis.store_to_file(analysis, run_save_name)
#     print('Network saved to : "' + run_save_name+'.pkl"')
#     # new_analysis = Analysis.load_from_file("test")
#     # new_analysis.mean_run_tokens_over_time(['p_chol_LE'], "Title A", labels_in_legend=True)

#     #fig, ax = plt.subplots(1,1,figsize=(12,6))
#     #Analysis.standardise_plot(ax, "This is the title", "X", "Y")
#     #plt.show()
    