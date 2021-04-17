#MUTATIONS (BINARY)
PD_it_p_GBA1 = 0
PD_it_p_LRRK2_mut = 0
PD_it_p_VPS35 = 0
PD_it_p_DJ1 = 0

#THERAPEUTICS (BINARY)
PD_it_p_NPT200 = 0 #i.c.w. with all mutations
PD_it_p_DNL151 = 0 #i.c.w. LRRK2
PD_it_p_LAMP2A = 0 #i.c.w. with all mutations

#LEVEL OF CHOLESTEROL (1 OR 2X)
chol_mp=300
mp_27OHchol=1 #1 or 2
mp_ApoEchol=1 #1 or 2

# Number of runs and timesteps
number_runs = 1
number_time_steps = 20000
time_step_size = 0.001

#To run model without Stochasticity, Set SD to 0.

#Should change SD to be sqrt(n) which is a better rule of thumb. maybe lambda function which takes number of place tokens, then you sqrt the SD.

cholSD = 0.2 # cholesterol module
SD = 0.2
DelaySD = 0.2 #calcium clock and MDVs

PD_collect_rate_analytics = ["no","no"] #first element consumption rate analytics, second element production rate analytics. i.e. ["no", "yes"], means don't collect consumption rate, but collect production rate analytics.
dont_collect = ["no","no"]
CaSD = 0 #CaSD = 0 or breaks.

#NOTE MDV DELAY FUNCTION NEEDS TO BE CORRECTED

# Output file name
run_save_name = 'dassda'