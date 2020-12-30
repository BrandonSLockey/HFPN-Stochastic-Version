#MUTATIONS (BINARY)
it_p_GBA1 = 1
it_p_LRRK2_mut = 0
it_p_VPS35 = 0
it_p_DJ1 = 0

#THERAPEUTICS (BINARY)
it_p_NPT200 = 0 #i.c.w. with all mutations
it_p_DNL151 = 0 #i.c.w. LRRK2
it_p_LAMP2A = 0 #i.c.w. with all mutations

#LEVEL OF CHOLESTEROL (1 OR 2X)
chol_mp=300
mp_27OHchol=1 #1 or 2
mp_ApoEchol=1 #1 or 2

# Number of runs and timesteps
number_runs = 1
number_time_steps = 6000000
time_step_size = 0.001

# Output file name
run_save_name = 'HFPN_GBA1_6x10e6'