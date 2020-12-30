
import random
import numpy as np
import matplotlib.pyplot as plt


MAX_LABEL_CHARACTERS = 50

def check_label_length(label, limit = MAX_LABEL_CHARACTERS):
    if len(label) > limit:
            raise ValueError(f'Label \"{label}\" exceeds {MAX_LABEL_CHARACTERS} characters.')


class Place:
    def __init__(self, initial_tokens, place_id, label, continuous = True):
        """
            Args:
                initial_tokens: number of tokens that the place is initialized with
                place_id (str): unique identifier of the place
                label (str): short description of the place
                continuous (bool): whether the place is continuous or discrete
        """
        self.place_id = place_id
        self.label = label
        self.initial_tokens = initial_tokens
        self.tokens = initial_tokens
        self.continuous = continuous

    def reset(self):
        self.tokens = self.initial_tokens

    def __str__(self):
        # TODO: update
        return f"{self.label} has {self.tokens} tokens"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Place):
            return self.id == other.id
        return False


class ConsumptionSpeed: # The new input arc
    """The consumption speed describes at what rate tokens are consumed from its associated input place.
       Each input arc has an associated consumption speed, which generally depends on the concentration
       of each input place to the transition in question."""

    #BSL: downstream, consumption_place and input_places are identical, but they are passed differently in the functions contained within this class.
    def __init__(self, consumption_place, input_places, consumption_function):
        """
            Args:
                consumption_place: Place instance corresponding to the input place whose tokens are consumed
                input_places: list of Place instances corresponding to all the input places to the transition in question. 
                              These are necessary because the consumption speed generally depends on the concentration of
                              all the input places.
                consumption_function: lambda function which calculates the number of tokens to be consumed from consumption_place
        """
        self.consumption_place = consumption_place
        self.input_places = input_places
        self.consumption_function = consumption_function
    
    #BSL:
    def __str__(self):
        return f"consumption_place:{self.consumption_place}, input_places:{self.input_places},consumption_function:{self.consumption_function}"
    
    def get_input_place_tokens(self):
        input_place_tokens_dictionary = {}
        for ip in self.input_places:
            input_place_tokens_dictionary[ip.place_id] = ip.tokens 
        return input_place_tokens_dictionary

    def calculate_firing_tokens(self, time_step, stochastic_multiplier):
        self.firing_tokens = self.consumption_function(self.get_input_place_tokens()) * time_step*stochastic_multiplier
        #I can just have it at 1, with standard deviation, and multiply consumption and production by randomized 1.
        #print(self.firing_tokens, "consumption firing_tokens")
        #New argument called Type, if type = stochastic, *randomizer
        #self.firing_tokens = random.gauss(self.firing_tokens, self.firing_tokens*SD)
   

    def perform_firing(self):
        self.consumption_place.tokens -= self.firing_tokens


class ProductionSpeed: # The new output arc
    """The production speed describes at what rate tokens are produced to its associated output place.
       Each output arc has an associated production speed, which generally depends on the concentration
       of each input place to the transition in question."""

    def __init__(self, production_place, input_places, production_function):
        """
            Args:
                production_place: Place instance corresponding to the output place where tokens are produced.
                input_places (list): list of Place instances corresponding to all the input places to the transition in question. 
                                     These are necessary because the production speed generally depends on the concentration of
                                     all the input places.
                production_function: lambda function which calculates the number of tokens to be produced in production_place
        """
        self.production_place = production_place
        self.input_places = input_places
        self.production_function = production_function

    #BSL:
    def __str__(self):
        return f"production_place:{self.production_place}, input_places:{self.input_places},production_function:{self.production_function}"
    
    def get_input_place_tokens(self):
        input_place_tokens_dictionary = {}
        for ip in self.input_places:
            input_place_tokens_dictionary[ip.place_id] = ip.tokens 
        return input_place_tokens_dictionary


    def calculate_firing_tokens(self, time_step, stochastic_multiplier):
        self.firing_tokens = self.production_function(self.get_input_place_tokens()) * time_step * stochastic_multiplier
        #print(self.firing_tokens, "production firing_tokens")

    def perform_firing(self):
        self.production_place.tokens += self.firing_tokens 

class ContinuousTransition:
    """A continuous transition contains (i) a firing condition, usually expressed in terms of the input concentrations,
       (ii) the collection of all consumption speeds, and (iii) the collection of all production speeds."""

    def __init__(self, transition_id, label, firing_condition, consumption_speeds, production_speeds, stochastic_parameters):
        """
            Args:
                transition_id (str): unique identifier of a transition
                label (str): short description of the transition
                firing_condition: lambda function which describes the criteria for the transition to fire
                consumption_speeds (list): each element is the consumption speed from an input place
                production_speeds (list): each element is the production speed to an output place
        """
        self.transition_id = transition_id
        self.label = label
        self.firing_condition = firing_condition
        self.consumption_speeds = consumption_speeds
        self.production_speeds = production_speeds
        self.stochastic_parameters = stochastic_parameters
        self.firings = 0
        
    #BSL:
    def __str__(self):
        return f"transition_id:{self.transition_id}, label:{self.label},firing_condition:{self.firing_condition},consumption_speeds:{self.consumption_speeds},production_speeds:{self.production_speeds},firings:{self.firings}"

    def get_input_place_tokens(self):
        input_place_tokens_dictionary = {}
        for cs in self.consumption_speeds:
            input_place_tokens_dictionary[cs.consumption_place.place_id] = cs.consumption_place.tokens 
        print(input_place_tokens_dictionary)
        return input_place_tokens_dictionary

    def reset(self):
        """Reset firing count for each transiton to 0 after each run."""
        self.firings = 0

    def fire(self, time_step):
        """The function first checks whether the firing condition is satisfied. If it is, it first
           calculates the amount tokens that will be transferred/produced from/to each place. Finally,
           this transfer is actually performed.
        """
        
        input_place_tokens = self.get_input_place_tokens()

        # Check if the firing condition of the transition is satisfied
        if self.firing_condition(input_place_tokens) == True:
    
            # Calculate number of tokens that will be consumed or produced from firing
            #randomizer = 
            randomized_value=random.gauss(1,self.stochastic_parameters[0])
            print(randomized_value)
            for cs in self.consumption_speeds:
                cs.calculate_firing_tokens(time_step, randomized_value)

            for ps in self.production_speeds:
                ps.calculate_firing_tokens(time_step, randomized_value)

            # store least non-zero transfer count
            token_transfers = [s.firing_tokens for s in self.consumption_speeds if s.firing_tokens != 0] + \
                              [s.firing_tokens for s in self.production_speeds if s.firing_tokens != 0]
            if len(token_transfers) == 0: 
                token_transfers.append(0)

            # Execute the actual firing by looping through all ConsumptionSpeed and ProductionSpeed instances
            for cs in self.consumption_speeds:
                cs.perform_firing()

            for ps in self.production_speeds:
                ps.perform_firing()

            # Increment number of firings by 1
            self.firings += 1

            
class DiscreteTransition(ContinuousTransition):

    def __init__(self, transition_id, label, firing_condition, consumption_speeds, production_speeds,stochastic_parameters, delay):
        """In addition to the arguments specified in the super class ContinuousTransition, a delay function must 
           be specified for a discrete transition.

            Args:
                delay (int): number of time-steps after which transition is fired if firing_condition still holds true.
        """

        # Initialize everything from the super class
        super(DiscreteTransition, self).__init__(transition_id, label, firing_condition, consumption_speeds, production_speeds,stochastic_parameters)

        self.delay = delay
        self.delay_counter = 0 # Counter for consecutive no. of steps where firing condition still holds true


    def fire(self, time_step):
        """Check if the firing condition is satisfied during the delay."""
        input_place_tokens = self.get_input_place_tokens()

        if self.firing_condition(input_place_tokens) == True:

            if self.delay_counter == int(self.delay/time_step):
                # fire with a time_step of 1, as discrete transition tokens should be transferred in their entirety
                super().fire(1)
                self.delay_counter = 0
            else:
                self.delay_counter += 1
        else:
            # Reset firing condition
            self.delay_counter = 0


class HFPN:
    """Hybrid functional Petri net (HPFN) with the option to specify a time-step in seconds."""

    def __init__(self, time_step = 0.001, printout=False): 
        """
            Args:
                time_step: size of the time increment, in seconds
                printout (bool): Whether to print out number of tokens in each place for each time-step
        """
        self.places = {}
        self.transitions = {}
        self.time_step = time_step # time-step in seconds
        self.printout = printout
        
            #BSL:
    def __str__(self):
        return f"places:{self.places}, transitions:{self.transitions},time_step:{self.time_step}"

    def set_initial_tokens_for(self, place_id, initial_tokens):
        self.places[place_id].initial_tokens = initial_tokens
        self.places[place_id].tokens = initial_tokens

    def add_place(self, initial_tokens, place_id, label, continuous = True):
        """Add a place to the Petri net.

            Args:
                initial_tokens (int): initial number of tokens in this place
                place_id (str): unique identifier of this place
                label (str): description of the place
                continuous (bool): whether the place is continuous or discrete
        """
        check_label_length(label) # Check whether the label is too long

        # Check whether the place_id contains a space
        if ' ' in place_id:
            raise ValueError(f"Place_id should not contain any spaces {place_id}. Did you reverse place_id and label?")

        if place_id in self.places.keys():
            print(f"Warning: Place {place_id} already exists.")
        else:
            place = Place(initial_tokens, place_id, label, continuous)
            self.places[place_id] = place

    def add_transition( self,
                        transition_id,
                        label,
                        input_place_ids,
                        firing_condition,
                        consumption_speed_functions,
                        output_place_ids,
                        production_speed_functions,
                        stochastic_parameters,
                        delay = -1):
        """Adds a transition to the hybrid functional Petri net.

            Args: 
                transition_id (str): unique identifier of the transition
                label (str): short description of the transition
                input_place_ids (list): list with place_id for each input place
                firing_condition: lambda function which returns a Boolean
                consumption_speed_functions (list): list of lambda functions, each of which returns a float or int
                output_place_ids (list): list with place_id for each output place
                production_speed_functions (list): list of lambda functions, each of which returns a float or int
                delay (float): the delay, in seconds, associated with a discrete transition. If not specified, a continuous transition is assumed.
        """
        # Check if function inputs are functions
        for function in consumption_speed_functions+production_speed_functions+[firing_condition]:
            if not callable(function): #BSL: lambda functions are functions, and functions are callable
                raise TypeError(f"Transition {transition_id} contains a non-function consumption speed function/production speed function or firing condition: {function}")
        # Check if input/output places exist
        for place_id in input_place_ids+output_place_ids: 
            if place_id not in self.places.keys():
                raise ValueError(f"Place {place_id} in transition {transition_id} has not been defined")
        # Check that the parameters of the function have been passed properly
        if len(input_place_ids) != len(consumption_speed_functions):
            raise ValueError(f"Unequal numbers of input places and input arc weights in transition {label}")
        if len(output_place_ids) != len(production_speed_functions):
            raise ValueError(f"Unequal numbers of output places and output arc weights in transition {label}")

        check_label_length(label) # Check whether the label is too long

        # Check whether the transition_id contains a space
        if ' ' in transition_id:
            raise ValueError(f"Transition_id should not contain any spaces {transition_id}. Did you reverse transition_id and label?")

        if transition_id in self.transitions.keys():
            print(f"Warning: Transition {transition_id} already exists.")
        else:

            # Translate input_places from strings to Place instances
            
            consumption_speeds = []
            for ipid, csf in zip(input_place_ids, consumption_speed_functions):
                consumption_speeds.append(ConsumptionSpeed(self.places[ipid], self.places_from_keys(input_place_ids), csf)) #first two are identical
                
            
            production_speeds = []
            for opid, psf in zip(output_place_ids, production_speed_functions):
                production_speeds.append(ProductionSpeed(self.places[opid], self.places_from_keys(input_place_ids), psf))


            if delay == -1: # user wants continous transition as delay is not specified
                transition = ContinuousTransition(transition_id, label, firing_condition, consumption_speeds, production_speeds, stochastic_parameters)
                # Check if continuous transition  is linked to discrete output place, which is not allowed.
                output_places = self.places_from_keys(output_place_ids)
                for op in output_places:
                    if op.continuous == False:
                        raise ValueError(f"A continuous transition ({transition_id}) cannot be linked to a discrete output place ({op.place_id}).")             
            else:         
                transition = DiscreteTransition(transition_id, label, firing_condition, consumption_speeds, production_speeds, stochastic_parameters, delay)
            self.transitions[transition_id] = transition
    
        
    def add_transition_with_speed_function( self,
                        transition_id,
                        label,
                        input_place_ids,
                        firing_condition,
                        reaction_speed_function,
                        consumption_coefficients,
                        output_place_ids,
                        production_coefficients,
                        stochastic_parameters,
                        delay = -1):
        """Add transition to HFPN wherein all consumption/production speeds are defined as proportional to a given reaction_speed_function.

            Args: 
                transition_id (str): unique identifier of the transition
                label (str): short description of the transition
                input_place_ids (list): list with place_id for each input place
                firing_condition: lambda function which returns a Boolean
                reaction_speed_function: lambda function which returns the number of tokens to transfer with dependence on input_places
                consumption_coefficients (list): list of numbers relating the consumption speed of the input places
                output_place_ids (list): list with place_id for each output place
                production_coefficients (list): list of numbers relating the production speed of the output places
                delay (float): the delay, in seconds, associated with a discrete transition. If not specified, a continuous transition is assumed.
        """
        # Nested lambda function, see https://www.geeksforgeeks.org/nested-lambda-function-in-python/
        for function in [reaction_speed_function, firing_condition]:
            if not callable(function):
                raise TypeError(f"Transition {transition_id} contains a non-function reaction speed function or firing condition: {function}")
        function = lambda f, n : lambda a : f(a) * n  #BSL: you are multiply by n because n is the stoichiometry of the reaction.

        consumption_speed_functions = [function(reaction_speed_function, cc) for cc in consumption_coefficients]
        production_speed_functions  = [function(reaction_speed_function, pc) for pc in production_coefficients]

        self.add_transition(
            transition_id = transition_id,
            label = label,
            input_place_ids = input_place_ids,
            firing_condition = firing_condition,
            consumption_speed_functions = consumption_speed_functions,
            output_place_ids = output_place_ids,
            production_speed_functions = production_speed_functions,
            stochastic_parameters=stochastic_parameters,
            delay = delay)

    def add_transition_with_mass_action( self,
                        transition_id,
                        label,
                        rate_constant,
                        input_place_ids,
                        firing_condition,
                        consumption_coefficients, 
                        output_place_ids,
                        production_coefficients,
                        stochastic_parameters,
                        delay = -1):

        """Adds a transition to the HFPN where all firing rates are defined based on mass action.

            Args: 
                transition_id (str): unique identifier of the transition
                label (str): short description of the transition
                rate_constant (float): number multiplied by mass action rate equation to produce overall reaction speed 
                input_place_ids (list): list with place_id for each input place
                firing_condition: lambda function which returns a Boolean
                consumption_coefficients (list): list of numbers relating the consumption speed of the input places
                output_place_ids (list): list with place_id for each output place
                production_coefficients (list): list of numbers relating the production speed of the output places 
                delay (float): the delay, in seconds, associated with a discrete transition. If not specified, a continuous transition is assumed.
        """

        mass_action_function = lambda a : rate_constant * np.prod([a[place_id] ** ratio for place_id, ratio in zip(input_place_ids, consumption_coefficients)])

        self.add_transition_with_speed_function(
            transition_id = transition_id,
            label = label,
            input_place_ids = input_place_ids,
            firing_condition = firing_condition,
            reaction_speed_function = mass_action_function,
            consumption_coefficients = consumption_coefficients,
            output_place_ids = output_place_ids,
            production_coefficients = production_coefficients,
            stochastic_parameters = stochastic_parameters,
            delay = delay)


    def add_transition_with_michaelis_menten(    self,
                                                transition_id,
                                                label,
                                                Km,
                                                vmax,
                                                input_place_ids,
                                                substrate_id,
                                                consumption_coefficients,
                                                output_place_ids,
                                                production_coefficients,
                                                stochastic_parameters,
                                                vmax_scaling_function = (lambda a : 1)):
        """Adds a transition to the HFPN where firing rates are defined based on Michaelis Menten.

            Args: 
                transition_id (str): unique identifier of the transition
                label (str): short description of the transition
                Km (float): Michaelis Menten Km, substrate concentration for speed to be vmax/2
                vmax (float): Michaelis Menten vmax, maximum speed transition can achieve
                input_place_ids (list): list with place_id for each input place
                substrate_id (str): id of substrate of reaction
                consumption_coefficients (list): list of numbers relating the consumption speed of the input places
                output_place_ids (list): list with place_id for each output place
                production_coefficients (list): list of numbers relating the production speed of the output places
                vmax_scaling_function: lambda function specifying how promoters/inhibitors affect vmax
        """

        speed_function = lambda a : vmax * a[substrate_id] / (Km + a[substrate_id])
        function = lambda f, g : lambda a : f(a) * g(a) # compound the two funtions
        scaled_speed_function = function(speed_function, vmax_scaling_function)


        self.add_transition_with_speed_function(
            transition_id = transition_id,
            label = label,
            input_place_ids = input_place_ids,
            firing_condition = lambda a : True,
            reaction_speed_function = scaled_speed_function,
            consumption_coefficients = consumption_coefficients,
            output_place_ids = output_place_ids,
            production_coefficients = production_coefficients,
            stochastic_parameters = stochastic_parameters)


    
    def places_from_keys(self, keys): 
        #print(keys, "Keys") #debug
        #for key in keys:
            #print(self.places[key], "self.places[key]") #each component of the dictionary is a place, so its accessing __str__ of Place
        return [self.places[key] for key in keys]

    def find_places_transitions(self, string, case_sensitive = True, search_places=True, search_transitions=True):
        if search_places == True:
            print(f"List of all place id's containing {string}:")
            for pid in self.places.keys():
                if case_sensitive == True:
                    if string in pid:
                        print(f"{pid}")
                else: 
                    if string.lower() in pid.lower():
                        print(f"{pid}")

        if search_transitions== True:
            print(f"\nList of all transitions id's containing {string}:")
            for tid in self.transitions.keys():
                if case_sensitive == True:
                    if string in tid:
                        print(f"{tid}")
                else: 
                    if string.lower() in tid.lower():
                        print(f"{tid}")

    def find_places_transitions_labels(self, string, case_sensitive = True, search_places=True, search_transitions=True):
        if search_places == True:
            print(f"List of all place labels containing {string}:")
            for place in self.places.values():
                if case_sensitive == True:
                    if string in place.label:
                        print(f"{place.label}")
                else:
                    if string.lower() in place.label.lower():
                        print(f"{place.label}")

        if search_transitions== True:
            print(f"\nList of all transitions labels containing {string}:")
            for transition in self.transitions.values():
                if case_sensitive == True:
                    if string in transition.label:
                        print(f"{transition.label}")
                else:
                    if string.lower() in transition.label.lower():
                        print(f"{transition.label}")

    def run_single_step(self):
        """For each time-step, generate random order of all transitions and execute sequentially.

            Returns:
                tokens (list): list with number of tokens in each place
                firings (list): list with number of firings for each transitions
        """

        ordered_transitions = list(self.transitions.values())
        random_order_transitions = random.sample(ordered_transitions, len(ordered_transitions))
        
        for t in random_order_transitions:
            t.fire(self.time_step)


            
        # Store tokens weights for each place at specific time step 
        tokens = [place.tokens for place in self.places.values()]

        # Store cumulative number of firings for each transition at specific time step
        firings = [t.firings for t in self.transitions.values()]

        # Check if time step has resulted in negative token count and raise value error 
        if any(token < 0 for token in tokens):
            # Array and list necessary to select using truth values
            place_ids = np.array(list(self.places.keys()))
            neg_token_truth_value = [token < 0 for token in tokens]
            neg_place_ids = place_ids[neg_token_truth_value]
            neg_place_tokens = np.array(tokens)[neg_token_truth_value]
            print(f"Warning: negative token count of {neg_place_tokens} in {neg_place_ids}.")
        
        return tokens, firings
        

    def run(self, number_time_steps, storage_interval=1):
        """Execute a run with a set amount of time-steps.

            Args:
                number_time_steps (int): number of time-steps
                storage_interval (int): number of time-steps between tokens being stored, default = 1  
                                        (e.g. storage_interval = 2: tokens stored for every 2nd time-step)
            Returns:
                single_run_tokens: 2D numpy array where first dimension is time step and second dimension is places
                single_run_total_firings: 1D numpy array where dimension is transitions.
        """

        single_run_tokens = np.zeros((int(number_time_steps/storage_interval)+1, len(self.places)))
        #populating the columns in the first row with the place tokens
        single_run_tokens[0] = [place.tokens for place in self.places.values()] # add initial conditions
                
        single_run_firings = np.zeros((int(number_time_steps/storage_interval)+1, len(self.transitions)))
        single_run_firings[0] = [trans.firings for trans in self.transitions.values()]

        for t in range(number_time_steps):
            tokens, firings = self.run_single_step()
            
            # store current values at regular intervals
            if t % storage_interval == 0:
                single_run_tokens[int(t/storage_interval)+1] = tokens
                single_run_firings[int(t/storage_interval)+1] = firings

        # Determine how many times transition fired in single run
        single_run_total_firings = single_run_firings[-1,:]
        
        return single_run_tokens, single_run_total_firings


    def run_many_times(self, number_runs, number_time_steps, storage_interval=1):
        """Runs multiple iterations of the HFPN.
        
            Args: 
                number_runs (int): total number of runs
                number_time_steps (int): number of time steps for each run
                storage_interval (int): number of time-steps between tokens being stored, default = 1  
                                        (e.g. storage_interval = 2: tokens stored for every 2nd time-step)
        """
        if storage_interval == -1:
            storage_interval = max(1, int(number_time_steps/1000))
        
        if number_time_steps % storage_interval != 0:
            raise ValueError('Number of time-steps should be a multiple of 1000')

        # Store time (in seconds) at each time step 
        self.time_array = np.arange(0, self.time_step*(number_time_steps+1), self.time_step*storage_interval)
        #time_step*number_time_steps gives you the total time.
        #print(self.time_array) brandoggy
        
        # First dimension = run number, second dimension = time step, third dimension = place 
        self.token_storage = np.zeros((number_runs, int(number_time_steps/storage_interval)+1, len(self.places)))
        

        # First dimension = run number, second dimension = transition
        self.firings_storage = np.zeros((number_runs, len(self.transitions)))
       

        for i in range(number_runs):
            self.token_storage[i], self.firings_storage[i] = self.run(number_time_steps, storage_interval)
            self.reset_network()

        # Store mean number of firings for each transition across all runs
        self.mean_firings = np.mean(self.firings_storage, axis = 0)

        
    def reset_network(self):
        """Resets the token values for each place and number of firings for each transition."""
        # Loop through places and reset the network 
        for place in self.places.values():
            place.reset()
        # Loop through transitions and reset number of firings
        for t in self.transitions.values():
            t.reset() 
            
   
if __name__ == '__main__':

    # Initialize an empty Petri net
    pn = HFPN(time_step=0.001, printout=True)

    # Add places for each chemical species
    pn.add_place(initial_tokens=20, place_id="p_H2", label="Hydrogen", continuous=True)
    pn.add_place(20, place_id="p_O2", label="Oxygen", continuous=True)
    pn.add_place(0, place_id="p_H2O", label="Water", continuous=True)
    pn.add_place(0, place_id="p_I", label="Inhibitor", continuous=True)

    rate_constant = 0.001

    ### Add the same transition in three different ways:
    # 1. Directly using speed_functions
    # pn.add_transition(  transition_id = 't_a',
    #                     label = 'Example transition a',
    #                     input_place_ids = ['p_H2', 'p_O2', 'p_I'],
    #                     firing_condition = lambda a : (a['p_H2'] >= 0 or a['p_O2'] >= 0) and a['p_I'] <= 0.01,
    #                     consumption_speed_functions = [lambda a : rate_constant * a['p_H2']**2 * a['p_O2']**1 * 2, 
    #                                                    lambda a : rate_constant * a['p_H2']**2 * a['p_O2']**1 * 1,
    #                                                    lambda a : 0],
    #                     output_place_ids = ['p_H2O'],
    #                     production_speed_functions = [lambda a : rate_constant * a['p_H2']**2 * a['p_O2']**1 * 2],
    #                     delay = 0.00
    # )

    # 2. Using one shared reaction_speed_function for each species 
    pn.add_transition_with_speed_function(
                        transition_id = 't_b',
                        label = 'Example transition b',
                        input_place_ids = ['p_H2', 'p_O2', 'p_I'],
                        firing_condition = lambda a : a['p_H2'] >= 0 or a['p_O2'] >= 0 and a['p_I'] <= 0.01,
                        reaction_speed_function = lambda a : rate_constant * a['p_H2']**2 * a['p_O2']**1,
                        consumption_coefficients = [2, 1, 0], 
                        output_place_ids = ['p_H2O'],
                        production_coefficients = [2],
                        stochastic_parameters=[0.1])

    # # 3. Using mass-action as the shared reaction_speed_function
    # pn.add_transition_with_mass_action(  transition_id = 't_c',
    #                     label = 'Example transition c',
    #                     rate_constant = rate_constant,
    #                     input_place_ids = ['p_H2', 'p_O2', 'p_I'],
    #                     firing_condition = lambda a : a['p_H2'] >= 0 and a['p_O2'] >= 0 and a['p_I'] <= 0.01,
    #                     consumption_coefficients = [2, 1, 0],
    #                     output_place_ids = ['p_H2O'],
    #                     production_coefficients = [2]
    # )

    # # Adding transition using Michaelis Menten
    # pn.add_transition_with_michaelis_menten(transition_id = 't_michaelis_menten',
    #                                     label = 'Michaelis Menten test',
    #                                     Km = 1,
    #                                     vmax = 1,
    #                                     input_place_ids = ['p_H2', 'p_O2'],
    #                                     substrate_id = 'p_H2',
    #                                     consumption_coefficients = [1, 0],
    #                                     output_place_ids = ['p_H2O'],
    #                                     production_coefficients = [1],
    #                                     vmax_scaling_function = lambda a : 1)

    pn.run_many_times(1,10, -1)
    print('shape of token_storage:', pn.token_storage.shape)
    print('time array:', pn.time_array)
