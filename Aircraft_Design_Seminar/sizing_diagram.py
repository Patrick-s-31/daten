
#sizing_diagram

import numpy as np
import matplotlib.pyplot as plt

############# CALCULATIONS ###############

def wing_loading_landing():
    #landing
    m0_S = rho_0 / (2*g) * pow((v_ref_ldg / 1.23),2) * cA_max * 1/(m_ldg_max_m0)

    return m0_S


def wing_loading_stall(): ####### not used ######
    #stall
    m0_S = rho_0 / (2*g) * pow((v_ref_ldg / 1.23),2) * cA_max

    return m0_S


def wing_loading_optimal_cruise(m_cruise_m0):
    #optmial cruise
    m0_S = 1/(m_cruise_m0) * q_cruise/g * cA_cruise

    return m0_S


def wing_loading_LFL(m_ldg): ######## not used ######
    #Landing field length
    l_ldg = l_a + 0.51*A*m_ldg*g/(S*sigma*cA_max)
    m0_S = 1/m_ldg_max_m0 * (l_ldg-l_a)*sigma*cA_max/(0.51*A*g)

    return m0_S


def thrust_ratio_TOFL():
    #takeoff field length
    prop_fac = k_TO / (cA_max_TO * sigma * x_tofl) #slope of linear equation

    return prop_fac


def thrust_ratio_climb_OEI(m_climb_m0):
    #climb gradient OEI
    F_m0_g = m_climb_m0 * n_e/(n_e - 1) * (gamma_min_OEI + epsilon_climb)

    return F_m0_g


def thrust_ratio_cruise(m_cruise_m0):
    #cruise
    prop_fac_1 = F_F_cruise * cW_0*q_cruise/g #factors of quadratic equation
    prop_fac_2 = F_F_cruise*g/(q_cruise*np.pi*AR*e) *m_cruise_m0**2

    return prop_fac_1,prop_fac_2


def thrust_ratio_ICAC(m_ICAC_m0):
    #Initial cruise altitude capability (Reststeigfähigkeit)
    F_m0_g = F_F_cruise*m_ICAC_m0*(v_v_cruise/v_h_cruise + epsilon_cruise)

    return F_m0_g


def thrust_ratio_max_ceiling(m_ICAC_m0): ######## not used ######
    # Service ceiling (Dienstgipfelhöhe)
    F_m0_g = F_F_max*m_ICAC_m0*(v_v_max/v_h_max + epsilon_cruise)
    
    return F_m0_g



#################  PLOTS  ###############################

def plot_sizing_diagram(masses):
    
    #weights from mass estimation.py:
    m0 = 199800#masses[0] #[kg] from mass estimation!
    m_climb_m0 = masses[1]
    m_cruise_m0 = (masses[2] + masses[3])/2 #mittlere cruise masse
    m_ICAC_m0 = masses[2]
    m_ldg = m_ldg_max_m0*m0

    #print(m_cruise_m0)


    x1 = np.linspace(0,800,10)
    y1 = x1*thrust_ratio_TOFL()

    x2 = wing_loading_landing()
    y2 = 0.7

    #x3 = wing_loading_stall()
    #y3 = 0.7

    x4 = 800
    y4 = thrust_ratio_climb_OEI(m_climb_m0)

    x5 = wing_loading_optimal_cruise(m_cruise_m0)
    y5 = 0.7

    x6 = 800
    y6 = thrust_ratio_ICAC(m_ICAC_m0)

    x7 = 800
    y7 = thrust_ratio_max_ceiling(m_ICAC_m0)

    #x8 = wing_loading_LFL()
    #y8 = 0.7

    prop_facs = thrust_ratio_cruise(m_cruise_m0)
    x9 = np.linspace(1,801,50)
    y9 = prop_facs[0]/x9 + prop_facs[1]*x9


    #Design Point#
    x_design = 636 #A330-200
    y_design = 0.28 #A330-200

    S_design = 1/x_design*m0
    F_design = y_design*m0*g

    print('\n=================================')
    print('Sizing Diagram')
    print('=================================\n')
    print('Wing area = %3.1f' %(S_design), 'm2', '\nThrust = %6.0f' %(F_design),'N\n')


    #### Latex font ##########
    plt.rcParams.update({
    "text.usetex": True,
    #"font.family": "Helvetica"
    })

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Computer Modern Roman'
    ####################################


    fig, ax = plt.subplots()

    fig.suptitle('Sizing Diagram')

    ax.plot(x1, y1, 'r', label = 'TOFL')
    ax.vlines(x2,0,y2, 'b', label = 'Approach speed')
    #ax.vlines(x3,0,y3, 'y', label = 'Stall')
    ax.hlines(y4, 0, x4, 'k', label = 'Climb OEI')
    ax.vlines(x5,0,y5, 'g','--', label = 'Optimal cruise')
    ax.hlines(y6, 0, x6, 'm', label = 'ICAC')
    ax.hlines(y7, 0, x7, 'c', label = 'Service ceiling')
    #ax.vlines(x8,0,y8, 'violet', label = 'Landing length')
    ax.plot(x9, y9, 'y', label = 'Cruise')
    ax.plot(x_design, y_design, 'ko', label = 'Design Point')

    ax.set_xlabel('$m_0/S$')
    ax.set_ylabel('$F/(m_0\cdot g)$')


    ax.set_ylim(0,0.9)
    ax.legend(loc='upper left', shadow=True)

    #plt.ion()
    #plt.show(block = False)
    plt.savefig("sizing_diagram.pdf")
    plt.close()
     
    



    return S_design,F_design


######### GLOBAL VARIABLES ###########

g = 9.81 #[m/s´2]
S = 317.63 #[m^2] from iteration of sizing diagram
l_over_d_cruise = 26.29
epsilon_cruise = 1 / l_over_d_cruise
cA_max = 2.7
cW_0 = 0.0178
e = 0.85 #oswald factor, assumed
AR = 18.12 #Aspect ratio of wing 
m_ldg_max_m0 = 0.928 #aus Vorgabe

mach_cruise = 0.8
a = 295.16 # speed of sound at cruise altitude [m/s]
x_tofl = 3000 #[m]
v_cruise = a * mach_cruise #[m/s] 
v_ref_ldg = 145 * 0.5144 #[m/s]
rho_0 = 1.225 #[kg/m3] 

cA_max_TO = 0.8 * cA_max # assumption from lecture
k_TO = 2.45 #[m3/kg] twin-jet
sigma = 1 #[rho/rho_0] at sea level

l_over_d_climb = 19 # was muss hier angenommen werden?
n_e = 2 #number of engines
epsilon_climb = 1 / l_over_d_climb
gamma_min_OEI = 1.37 * np.pi/180


alt_cruise_ft = 39000 # feet
alt_cruise_m = alt_cruise_ft * 0.3048 # meter
rho_cruise = 0.317 # density at cruise altitude [g/m^3]
cA_cruise = 0.672
q_cruise = rho_cruise/2 * v_cruise**2

F_F_cruise = 5.5 #Thrust ratio in cruise, taken from a graph from lecture, usually 4-5

F_F_max = 6 #Thrust ratio at highest altitude (12634m)
v_v_max = 0.5 #climb velocity for maximal altitude
v_v_cruise = 1.5 #climb velocity for cruise altitude (lecture)
v_h_max = 230 #236 #horizontal velocity (from mach number) [m/s], assumption that it flies at same mach number
v_h_cruise = v_cruise #horizontal velocity (from mach number) [m/s]


l_a = 305 #[m] Obstacle clear distance
A = 0.66 #Factor for landing distance




# A330 200 hat m0/S von 636 kg(m^2), 647661 N Schub gesamt


