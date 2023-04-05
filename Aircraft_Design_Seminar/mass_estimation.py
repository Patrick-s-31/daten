#Maximum takeoff estimation
#Packages
import numpy as np
from prettytable import PrettyTable


def MTOW_iteration():

    m40 = np.prod(mass_fraction[0:4]) # mass at the start of cruise
    m50 = np.prod(mass_fraction[0:5]) # mass at the end of cruise
    m30 = np.prod(mass_fraction[0:3])  # mass at the start of climb

    #iteratively calculate empty weight and MTOW

    m_MTO_prev = 0
    iter_count = 0
    mL_m0 = 0.6 # empty weight fraction
    m_MTOW = (m_payload + m_crew)/(1- mKr_m0 - mL_m0)
    

    while True:
        iter_count += 1
        m_MTO_prev = m_MTOW # 
        mL_m0 = 0.63#141000/(141000+m_payload+m_crew+m_MTOW*mKr_m0) #A * pow((m_MTOW*2.20462),C) * D # Achtung m_MTO muss hier in lbs umgerechnet werden
        m_MTOW = (m_payload + m_crew)/(1- mKr_m0 - mL_m0) 


        if np.abs((m_MTOW-m_MTO_prev)/m_MTOW) < 0.005:
            break

    m_MTOW = m_MTOW*calibration_factor

    print('=================================')
    print('Mass Estimation')
    print('=================================\n')
    print('m_MTOW = %6.0f' %(m_MTOW),'kg      (after',iter_count,'iterations)\n')
    print('Empty weight = %6.0f' %(mL_m0*m_MTOW),'kg\n')
    

    partial_fuel_weights = np.zeros((10,))
    partial_fuel_weights[0] = (1-mass_fraction[0])*m_MTOW

    for j in range(1,len(partial_fuel_weights)):
        partial_fuel_weights[j] = (1-mass_fraction[j]) * np.cumprod(mass_fraction)[j-1]*m_MTOW


    flight_phase = ['Engine start/warm up','Taxi','Take-off','Climb','Cruise','Descent','Missed approach and climb','Flight to alternate, descend','Loiter (30min)','Landing, taxi, shutdown']
    #table
    fuel_weights = PrettyTable(['Fuel Weights','[kg]'])

    for i in range(len(partial_fuel_weights)):

        fuel_weights.add_row([flight_phase[i],partial_fuel_weights[i]])
    
    
    fuel_weights.add_row(['',''])
    fuel_weights.add_row(['Total fuel weight',np.sum(partial_fuel_weights)])

    fuel_weights.float_format = '.0'
    print(fuel_weights)

    print('\nImportant mmass fractions ')
    print('Average weight during cruise: \t%5.4f' %((m40+m50)/2))
    print('Weight at start of cruise: \t%5.4f' %(m40))
    print('Weight at start of climb: \t%5.4f' %(m30))

    #print(mass_fraction[4],mass_fraction[7],mass_fraction[8])


    return m_MTOW,m30,m40,m50,

#Mission parameters
range_nm = 4000 #nautical miles
range_m = range_nm * 1852 #meter
m_payload = 60000 #Kg
m_crew = 300 #Checked

mach_cruise = 0.8 
alt_cruise_ft = 36000 #feet
alt_cruise_m = alt_cruise_ft * 0.3048 #meter
a = 295.16 #calculated at cruise height
v_cruise = mach_cruise * a
v_missed_approach = 254.6 # [m/s]Abschätzung gg. anpassen!

#Assumptions
l_over_d_cruise = 24
l_over_d_loiter = 26
c_TL = 0.2003/3600  #[1/s]
loiter_time = 30 * 60 #[s]
R = range_m *0.987  

A = 1.02
C = -0.06
D = 0.95


mass_fraction = np.zeros((10,))

#with correction for hydrogen
mass_fraction[0] = 1-(1-0.99)/2.8 #Engine start, war-up
mass_fraction[1] =  1-(1-0.99)/2.8 #Taxi
mass_fraction[2] =  1-(1-0.995)/2.8 #Take-off
mass_fraction[3] =  1-(1-0.98)/2.8 #Climb
#Cruise:
mass_fraction[4] = np.exp(-1*(R*c_TL)/(v_cruise*l_over_d_cruise)) #Breguet range

mass_fraction[5] =  1-(1-0.99)/2.8 #Descent
mass_fraction[6] =  1-(1-0.988)/2.8 #Missed approach and climb
mass_fraction[7] =  np.exp(-1*(200*1852*c_TL)/(v_missed_approach*l_over_d_cruise))#1-(1-0.99)/2.8 #Flight to alternate, descend
#Loiter:
mass_fraction[8] = np.exp(-1*(loiter_time * c_TL)/(l_over_d_loiter)) #Breguet time

mass_fraction[9] =  1-(1-0.995)/2.8

#Calculation

m10_m0 = np.prod(mass_fraction)
mKr_m0 = 1 - m10_m0

calibration_factor = 0.9672

