# ! ARGUMENTS OF THE MACRO
# !************************
# MatID 	= ARG1			! Material Number
# Smax	  = ARG2			! initial stress value to calculate strain
# Epsmax  = ARG3			! max. strain
# Epstol  = ARG4			! strain tolerance (+/-)
# E	      = ARG5			! E-Modulus
# Sy      = ARG6      ! Yield Stress
# K	      = ARG7			! Constant
# n	      = ARG8			! Constant
# PR	    = ARG9			! Poisson Ratio
# !************************

def set_ramberg_osgood(mapdl, mat_id, S_max, eps_max, eps_tol, E, K, n, PR):
    # Define stress-strain-curve in mkin-table by using Ramberg-Osgood-Law
    # calculate and define stress-strain-curve (total)
    # max 40 temperatures & 20 pairs per temp
    # *********************************************
    #E_film = E

    mapdl.run(f"_RO_initial_n={n}")
    mapdl.run(f"_RO_initial_K={K}")
    mapdl.run(f"_RO_initial_E={E}")
    mapdl.run(f"_RO_initial_eps_max={eps_max}")
    mapdl.run(f"_RO_initial_S_max={S_max}")

    status = f"initital n = {n}\n"\
             f"initital K = {K}\n"\
             f"initital E = {E}\n" \
             f"initital eps_max = {eps_max}\n"\
             f"initital S_max = {S_max}\n"



    mapdl.run("/PREP7")
    mapdl.mptemp("", "", "", "", "", "", "")
    mapdl.mptemp(1, "T")
    # E-Modulus:
    mapdl.mpdata("EX", mat_id, "", E)
    # Poisson Ratio:
    mapdl.mpdata("PRXY", mat_id, "", PR)


    # # *DIM,SSC,,20,2        define Array of 20x2
    steps = 20
    mapdl.tb("KINH", mat_id, 1, steps)  # Activate a data table
    mapdl.tbtemp(0)  # Temperature

    # * Algorithm to find the maximum Strain      *
    # *********************************************
    abort_flag = False
    while not abort_flag:
        eps = S_max / E + K * (
                S_max / E) ** n
        if (eps >= eps_max - eps_tol) and (
                eps >= eps_max + eps_tol):
            abort_flag = True
        elif eps > eps_max:
            S_max /= 1.5
        else:
            S_max *= 2.0

    # * calculate S-S-Curve
    # * be shure to get the correct initial slope *
    # *********************************************
    SIGMA = S_max / steps
    # first strain, stress:
    mapdl.tbpt("", (SIGMA / E), SIGMA)

    sigma_list = []
    strain_list = []
    for i in range(1, steps+1):
        SIGMA = i * S_max / steps
        sigma_list.append(SIGMA)
        strain_list.append((SIGMA / E) + K * (SIGMA/E) ** n)
        mapdl.tbpt("", (SIGMA / E) + K * (
                SIGMA/E) ** n, SIGMA)

    mapdl.run(f"_RO_final_S_max={S_max}")

    status += f"final S_max = {S_max}\n"

    print(status)
    from post_dpf import get_figure
    fig = get_figure(strain_list, sigma_list, "strain", "stress")
    fig.plot()