
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from prettytable import PrettyTable

def detailed_fuel_calculation(m_fuel,OWE):
    '''adds all (sub-) sections to determine total range, time, and final MTOW'''

    m_fuel_usable = m_fuel/1.05 #[kg] initial minus unusable 5%
    max_ramp_weight = OWE + 60000 + 300 + m_fuel

    #Engine-start, warm up, Taxi (0-2)########################################################################

    m_fuel_02 = warm_up_taxi() 
    MTOM = max_ramp_weight - m_fuel_02

    # Take-off (2-3)########################################################################

    m_fuel_23,R_23,T_23 = takeoff()
    m_climb_start = MTOM - m_fuel_23
    
    # first Climb (3-4)########################################################################

    m_fuel_34,R_34,T_34 = climb1(m_climb_start)
    m_cruise_start = m_climb_start - m_fuel_34

    #### Now from back to front!!!

    m_landing_end = max_ramp_weight - m_fuel_usable

    # Landing (9-10)########################################################################
    
    m_fuel_910,R_910,T_910 = landing(m_landing_end)
    m_loiter_end = m_landing_end + m_fuel_910

    # Loiter (8-9)########################################################################
    
    m_fuel_89,R_89,T_89 = loiter(m_loiter_end)
    m_descent2_end = m_loiter_end + m_fuel_89

    # Descent (7*-8)########################################################################

    m_fuel_78,R_78,T_78 = descent2(m_descent2_end)
    m_alternate_end = m_descent2_end + m_fuel_78

    # Flight to alternate (7-7*)########################################################################

    range_alternate = 200*1852 - climb2(100)[1] - descent2(1000)[1] # calling climb and descent just to get the range of that segment

    m_fuel_77star,R_77star,T_77star = flight_to_alternate(m_alternate_end,range_alternate)
    m_climb2_end = m_alternate_end + m_fuel_77star

    # Second climb (6-7)########################################################################

    m_fuel_67,R_67,T_67 = climb2(m_climb2_end)
    m_descent1_end = m_climb2_end + m_fuel_67

    # First descent (5-6)########################################################################

    m_fuel_56,R_56,T_56,iteration = descent1(m_descent1_end)
    m_cruise_end = m_descent1_end + m_fuel_56

    # CRUISE (5-6)########################################################################

    m_fuel_45,R_45,T_45 = cruise(m_cruise_start,m_cruise_end)
    
    # Total range, time, and fuel

    Range = R_23 + R_34 + R_45 + R_56 + R_910
    Time = T_23 + T_34 + T_45 + T_56 + T_910
    Fuel = m_fuel_23 + m_fuel_34 + m_fuel_45 + m_fuel_56 + m_fuel_67 + m_fuel_77star + m_fuel_78 + m_fuel_89 + m_fuel_910

    segment_fuel = np.array([m_fuel_02,m_fuel_23,m_fuel_34,m_fuel_45,m_fuel_56,m_fuel_67,m_fuel_77star,m_fuel_78,m_fuel_89,m_fuel_910])

    return Range,Time,Fuel,segment_fuel,[R_23,R_34,R_45,R_56,R_910]


def warm_up_taxi():
    '''returns fuel weight, Range, and Time for engine start, warm up and taxi segment'''

    T = 25*60 #20 minutes 
    m_fuel = fuel_flow_idle*T

    return m_fuel

def takeoff():
    '''returns fuel weight, Range, and Time for takeoff segment'''

    T = 60 #[s]
    m_fuel = fuel_flow_takeoff*T
    R = 0

    return m_fuel,R,T


def climb1(m_aircraft):
    '''returns fuel weight, Range, and Time for first climb segment'''

    m_beginning = m_aircraft
    R_total = 0
    T_total = 0
    m_fuel_total = 0
    c_TL = 0.9*C_TL_standard

    for j in range(len(L_D_climb1)):

        T_section = (FL_climb1[j+1]-FL_climb1[j])/ROC_climb1[j]
        T = T_section/time_discretization

        for i in range(time_discretization):

            gamma = np.arcsin(ROC_climb1[j]/v_climb1[j])
            R = v_climb1[j]*np.cos(gamma)*T

            m_fuel = c_TL*((1/L_D_climb1[j]) + gamma) * m_beginning * T
            m_beginning -= m_fuel

            R_total += R
            m_fuel_total += m_fuel

        T_total += T_section

    return m_fuel_total,R_total,T_total


def landing(m_landing_end):
    '''returns fuel weight, Range, and Time for first landing segment'''

    gamma = np.arcsin(ROC_landing/v_landing)
    c_TL = 4*C_TL_standard
    m_end = m_landing_end
    T_idle = 15*60 #10minutes taxi and shutdown
    R_total = 0
    T_total = 0
    m_fuel_total = 0



    T_section = (FL_landing[1]-FL_landing[0])/ROC_landing
    T = T_section/time_discretization
    gamma = np.arcsin(ROC_landing/v_landing)
    R = v_landing*np.cos(gamma)*T

    for i in range(time_discretization):

        m_fuel = c_TL*((1/L_D_landing) + gamma) * T * m_end / (1-c_TL*((1/L_D_landing) + gamma) * T)

        if m_fuel < fuel_flow_idle*T:
            m_fuel = fuel_flow_idle*T

        m_end += m_fuel

        
        R_total += R
        m_fuel_total += m_fuel


    m_fuel_total += fuel_flow_idle*T_idle #for taxi and shutdown

    T_total += T_section

    return m_fuel_total,R_total,T_total


def loiter(m_loiter_end):
    '''returns fuel weight, Range, and Time for loiter segment'''

    T = loiter_time #[s]
    R = T*v_loiter
    c_TL = C_TL_standard

    m_fuel = m_loiter_end * np.exp((T * c_TL)/(L_D_loiter)) - m_loiter_end  #Brequet for time

    return m_fuel,R,T


def descent2(m_aircraft):
    '''returns fuel weight, Range, and Time for second descent segment'''

    m_end = m_aircraft
    R_total = 0
    T_total = 0
    m_fuel_total = 0
    c_TL = 4*C_TL_standard


    for j in range(-1,-len(L_D_descent2)-1,-1):

        T_section = (FL_descent2[j]-FL_descent2[j-1])/ROC_descent2[j]
        T = T_section/time_discretization
        gamma = np.arcsin(ROC_descent2[j]/v_descent2[j])
        R = v_descent2[j]*np.cos(gamma)*T

        for i in range(time_discretization):

            m_fuel = c_TL*((1/L_D_descent2[j]) + gamma) * T * m_end / (1-c_TL*((1/L_D_descent2[j]) + gamma) * T)

            if m_fuel < fuel_flow_idle*T:
                m_fuel = fuel_flow_idle*T

            m_end += m_fuel


            R_total += R
            m_fuel_total += m_fuel

        T_total += T_section

    return m_fuel_total,R_total,T_total


def flight_to_alternate(m_alternate_end,range_alternate):
    '''returns fuel weight, Range, and Time for flight to alternate segment'''
    
    R = range_alternate
    T = R/v_alternate #[s]
    c_TL = C_TL_standard

    m_fuel = m_alternate_end * np.exp((R * c_TL)/(v_alternate * L_D_alternate)) - m_alternate_end

    return m_fuel,R,T


def climb2(m_aircraft):
    '''returns fuel weight, Range, and Time for second climb segment'''

    m_end = m_aircraft
    R_total = 0
    T_total = 0
    m_fuel_total = 0
    c_TL = 0.9*C_TL_standard

    for j in range(len(L_D_climb2)):

        T_section = (FL_climb2[j+1]-FL_climb2[j])/ROC_climb2[j]
        T = T_section/time_discretization

        for i in range(time_discretization):

            gamma = np.arcsin(ROC_climb2[j]/v_climb2[j])
            R = v_climb2[j]*np.cos(gamma)*T

            m_fuel = c_TL*((1/L_D_climb2[j]) + gamma) * T * m_end / (1-c_TL*((1/L_D_climb2[j]) + gamma) * T)
            m_end += m_fuel

            R_total += R
            m_fuel_total += m_fuel

        T_total += T_section

    return m_fuel_total,R_total,T_total


def descent1(m_aircraft):
    '''returns fuel weight, Range, and Time for first descent segment'''

    m_end = m_aircraft
    R_total = 0
    T_total = 0
    m_fuel_total = 0
    c_TL = 4*C_TL_standard

    iteration = 0

    for j in range(-1,-len(L_D_descent1)-1,-1):

        T_section = (FL_descent1[j]-FL_descent1[j-1])/ROC_descent1[j]
        T = T_section/time_discretization
        gamma = np.arcsin(ROC_descent1[j]/v_descent1[j])
        R = v_descent1[j]*np.cos(gamma)*T

        for i in range(time_discretization):

            m_fuel = c_TL*((1/L_D_descent1[j]) + gamma) * T * m_end / (1-c_TL*((1/L_D_descent1[j]) + gamma) * T)

            if m_fuel < fuel_flow_idle*T:
                m_fuel = fuel_flow_idle*T
                iteration +=1

            m_end += m_fuel

            R_total += R
            m_fuel_total += m_fuel

        T_total += T_section

    return m_fuel_total,R_total,T_total,iteration


def cruise(m_beginning,m_end):
    '''returns fuel weight, Range, and Time for cruise segment'''

    c_TL = C_TL_standard

    m_fuel = m_beginning - m_end

    R = v_cruise/c_TL * L_D_cruise * np.log(m_beginning/m_end)

    T = R/v_cruise

    return m_fuel,R,T



def range_iteration_loop(m_fuel_initial,OWE):
    '''calls detailed fuel calculation function and changes fuel mass, until range is 4000nm'''

    m_fuel = m_fuel_initial

    # Full payload #########################################################

    range_p = detailed_fuel_calculation(m_fuel,OWE)[0] / 1852

    #iteration = 0
    while True:

        if abs(range_p-range_specification) < 0.5:
            break

        if range_p > range_specification:
            m_fuel -= max(1,0.1*abs(range_p-range_specification))
            range_p = detailed_fuel_calculation(m_fuel,OWE)[0] / 1852

        else:
            m_fuel += max(1,0.1*abs(range_p-range_specification))
            range_p = detailed_fuel_calculation(m_fuel,OWE)[0] / 1852


    time = detailed_fuel_calculation(m_fuel,OWE)[1]/60
    # Ferry range #########################################################

    range_f = detailed_fuel_calculation(m_fuel,OWE-60000)[0] / 1852

    ferry_range = np.zeros((11,2))
    
    ferry_range[0,0] = detailed_fuel_calculation(m_fuel,OWE)[0] / 1852
    ferry_range[0,1] = 60000

    weight_decrement = 60000/(len(ferry_range)-1)

    for i in range(1,len(ferry_range)):
        ferry_range[i,0] = detailed_fuel_calculation(m_fuel,OWE-i*weight_decrement)[0] / 1852
        ferry_range[i,1] = 60000-i*weight_decrement


    
    print('\n=================================')
    print('Payload and range')
    print('=================================\n')

    print('Range with full payload: \t%5.1f nm' %(range_p))
    print('Ferry range: \t\t\t%5.1f nm\n' %(range_f))
    print('Total fuel weight: \t\t%5.0f kg\n' %(m_fuel))

    print('Time for payload mission: \t%3.0f min' %(time))

    max_ramp_weight = OWE+60000+300+m_fuel
    MTOW =  max_ramp_weight - warm_up_taxi()

    flight_phase = ['Engine start/warm up/Taxi','Take-off','Climb','Cruise','Descent','Missed approach and climb','Flight to alternate','Descent','Loiter (30min)','Landing, taxi, shutdown']
    #table
    fuel_weights = PrettyTable(['Final fuel Weights','[kg]'])

    partial_fuel_weights = detailed_fuel_calculation(m_fuel,OWE)[3]


    for i in range(len(partial_fuel_weights)):

        fuel_weights.add_row([flight_phase[i],partial_fuel_weights[i]])
    

    fuel_weights.float_format = '.0'
    print(fuel_weights)

    #print(partial_fuel_weights)
    print('---------------------------------')
    print('Final MTOW: %6.0f kg\n' %(MTOW))

    print('pdf plot "payload_range.pdf" has been created\n')


    fig, ax = plt.subplots()

    fig.suptitle('Payload-Range')
    fig.set_figheight(4)

    ax.hlines(60000,0,range_p)
    #ax.plot(ferry_range[:,0],ferry_range[:,1],color='gray',linestyle='dashed')
    ax.plot([range_p,range_f],[60000,0])
    ax.plot(range_p,60000,'ro')
    ax.annotate('Design Point',(range_p+100,60000+200))
    ax.vlines(range_p,0,60000,color='black',linestyle='dashed', alpha=0.7)

    ax.set_xlabel('Range [nm]')
    ax.set_ylabel('Payload [kg]')
    ax.grid()

    ax.set_ylim(0,80000)
    ax.set_xlim(0,8000)

    plt.savefig("payload_range.pdf")
    plt.close()

 


L_D_climb1 = np.array([19,21,20,23])
L_D_cruise = 26.29
L_D_descent1 = np.array([23,21,20])
L_D_climb2 = np.array([21,21,23])
L_D_alternate = 26.29
L_D_descent2 = np.array([23,22,20])
L_D_loiter = 28
L_D_landing = 19

v_climb1 = np.array([175,290,290,450]) * 0.5144 #[knots] converted to m/s
v_cruise = 236
v_descent1 = np.array([450,360,230]) * 0.5144
v_climb2 = np.array([290,290,360]) * 0.5144
v_alternate = 254
v_descent2 = np.array([360,360,300]) * 0.5144
v_loiter = 232
v_landing = 175 * 0.5144

ROC_climb1 = np.array([2000,2500,2200,1500]) * 0.00508 #[ft/min] converted to m/s
ROC_descent1 = np.array([-1800,-1700,-1100]) * 0.00508 #    [-1500,-3600,-1600]
ROC_climb2 = np.array([2000,2500,1800]) * 0.00508
ROC_descent2 = np.array([-1600,-1600,-1200]) * 0.00508
ROC_landing = -1000 * 0.00508

FL_climb1 = np.array([0,5000,15000,24000,39000]) * 0.3048
FL_descent1 = np.array([39000,24000,10000,1500]) * 0.3048
FL_climb2 = np.array([0,8000,14000,18000]) * 0.3048
FL_descent2 = np.array([18000,14000,10000,1500]) * 0.3048
FL_landing = np.array([1500,0]) * 0.3048

time_discretization = 10
C_TL_standard = 0.545/(3600*2.8)

range_specification = 4000 #[nm]
loiter_time = 30*60

fuel_flow_takeoff = 0.9*C_TL_standard* 591000 / 9.81
fuel_flow_idle = 0.039#  10% of 0.39kg/s hydrogen cruise
