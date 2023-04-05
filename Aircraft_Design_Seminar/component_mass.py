import numpy as np
from prettytable import PrettyTable
import math as m
 
#estimation of components based on equations from raymer

def weight_wing():

    W = 0.0051 * (W_dg * N_z)**0.557 * S_w**0.649 * A**0.5 * (t_c_w)**-0.4 * (1+taper_r)**0.1 * m.cos(Lambda)**(-1) * S_csw**0.1

    return W
 
def weight_wing_FZE2():

    #W = mzfm * (6.67 * 10**(-3) * b_s**0.75*(1+m.sqrt(1.905/b_s)) * N_z**0.55 * ((b_s/d_root)/(mzfm/S_wing))**0.3) 
    #W = W * (1 + 0.02 - 0.05) * calibration_wing * ff_braced_wing # consideration of spoiler and 2 engines
    W = 34871 + 2*420

    return W


def weight_horizontal_tail():

    W = 0.0379 * K_uht * (1+F_w/B_h)**-0.25 * W_dg**0.639 * N_z**0.1 * S_ht**0.75 * L_t**-1 * K_y**0.709 * m.cos(Lambda_ht)**-1 * A_h**0.166 * (1+S_e/S_ht)**0.1

    return W


def weight_horizontal_tail_FZE2():

    W = 4.882 * S_hlw * k_H * (11.9119 * (S_hlw**0.2 * v_D)/(1000*m.sqrt(m.cos(phi_50_h))) - 0.287)
    W = W * calibration_h_tail * ff_tails

    return W


def weight_vertical_tail():

    W = 0.0026 * (1+H_t_H_v)**0.225 * W_dg**0.556 * N_z**0.536 * L_t**-0.5 * S_vt**0.5 * K_z**0.875 * m.cos(Lambda_vt)**-1 * A_v**0.35 * (t_c_v)**-0.5

    return W

    
def weight_vertical_tail_FZE2():

    W = 4.882 * S_slw * k_S * (11.9119 * (S_slw**0.2 * v_D)/(1000*m.sqrt(m.cos(phi_50_s))) - 0.287)
    W = W * calibration_v_tail *ff_tails

    return W


def weight_fuselage():

    W = 0.3280 * K_door * K_Lg * (W_dg * N_z)**0.5 * L**0.25 * S_f**0.302 * (1+K_ws)**0.04 * l_over_d_cruise**0.1

    return W


def weight_fuselage_FZE2():

    W = 0.23 * m.sqrt(v_D * r_H/(b_R+h_R)) *S_O**1.2
    W = W*(1+0.08+0.1)
    W += (1000 + 40*total_cargo_length) #cargo loading system
    W = W*calibration_fuselage*ff_fuselage + 220

    return W


def weight_main_landing_gear():

    W = 0.0106 * K_mp * W_l**0.888 * N_l**0.25 * L_m**0.4 * N_mw**0.321 * N_mss**-0.5 * v_stall**0.1

    return W


def weight_main_landing_gear_FZE2():

    W = k_FW * (A_Main+B_Main*MTOM**0.75+C_Main*MTOM+D_Main*MTOM**1.5)
    W = W * calibration_main_landing *ff_landing_gear/1.75 #1.75 because of leg length
    

    return W


def weight_nose_landing_gear():

    W = 0.032 * K_np * W_l**0.646 * N_l**0.2 * L_n**0.5 * N_nw**0.45

    return W


def weight_nose_landing_gear_FZE2():

    W = k_FW * (A_Nose+B_Nose*MTOM**0.75+C_Nose*MTOM+D_Nose*MTOM**1.5)
    W = W * calibration_nose_landing *ff_landing_gear/1.05 #1.05 because of leg length

    return W


def weight_nacelle_group():

    W = 0.6724 * K_ng * N_Lt**0.1 * N_w**0.294 * N_z**0.119 * W_ec**0.611 * N_en**0.984 * S_n**0.224
    W = W * calibration_nacelle *ff_nacelle

    return W


def weight_nacelle_FZE2():

    W = 0.065 * F_max_TO

    return W


def weight_engine_controls():

    W = 5 * N_en + 0.8 * L_ec
    W = W * calibration_electric

    return W


def weight_starter():

    W = 49.19 * (N_en * W_en /1000)**0.541
    W = W * calibration_electric

    return W


def weight_fuel_systems():

    #W = 2.405 * V_t**0.606 * (1+V_i/V_t)**-1 * (1+V_p/V_t) * N_t**0.5
    #W = W * calibration_fuel
    W = W_tank_front + W_tank_aft

    return W


def weight_flight_control():

    W = 145.9 * N_f**0.554 * (1+N_m/N_f)**-1 * S_cs**0.2 * (I_y*10**-6)**0.07
    W = W * calibration_electric

    return W 


def weight_APU_installed():

    W = 2.2 * W_APU_uninstalled

    return W 


def weight_instruments():

    W = 4.509 * K_r * K_tp * N_c**0.541 * N_en * (L_f+B_w)**0.5
    W = W * calibration_electric

    return W 


def weight_hydraulics():

    W = 0.2673 * N_f * (L_f+B_w)**0.937
    W = W * calibration_hydraulic

    return W


def weight_electrical():

    W = 7.291 * R_kva**0.782 * L_a**0.346 * N_gen**0.1
    W = W * calibration_electric

    return W


def weight_avionics():

    W = 1.73 * W_uav**0.983
    W = W * calibration_electric

    return W


def weight_furnishings():

    W = 0.0577 * N_c**0.1 * W_c**0.393 * S_f**0.75
    W = W * calibration_furnishings

    return W


def weight_air_conditioning():

    W = 62.36 * N_p**0.25 * (V_pr/1000)**0.604 * W_uav**0.1
    W = W*calibration_air_conditioning

    return W


def weight_anti_ice():

    W = 0.002 * W_dg
    W = W*calibration_anti_ice

    return W


def weight_structure():

    W = weight_wing()+weight_fuselage()+weight_horizontal_tail()+weight_vertical_tail()+weight_main_landing_gear()+weight_nose_landing_gear()+W_pylons

    return W


def weight_structure_FZE2():

    W = weight_wing_FZE2() + weight_fuselage_FZE2() + weight_vertical_tail_FZE2() + weight_horizontal_tail_FZE2() + weight_main_landing_gear_FZE2() + weight_nose_landing_gear_FZE2() + W_pylons*lbs_to_kg

    return W


def weight_systems():

    W = weight_flight_control()+weight_engine_controls()+weight_starter()+weight_instruments()+weight_hydraulics()+weight_electrical()+weight_avionics()+weight_air_conditioning()+weight_anti_ice()+W_fp

    return W


def weight_avionics_FZE():

    W = k_St * MTOM**(2/3)

    return W


def weight_systems_FZE2(): #Control + Systems

    W = weight_avionics_FZE() + 0.08*MTOM*(1+0.2+0.15)

    return W


### Component Weights ####

def print_weights_in_kg():

    print('=================================')
    print('Component Weights and COG')
    print('=================================\n')

    weight_table = PrettyTable(['Weight breakdown','[kg]'])

    weight_table.add_row(['Structure',weight_structure()*lbs_to_kg])
    weight_table.add_row(['Equipped engines (engines + nacelle)',(2*W_ec+weight_nacelle_group()+weight_starter())*lbs_to_kg])
    weight_table.add_row(['APU',weight_APU_installed()*lbs_to_kg])
    weight_table.add_row(['Systems',weight_systems()*lbs_to_kg+weight_fuel_systems()])
    weight_table.add_row(['Furnishings',weight_furnishings()*lbs_to_kg])
    weight_table.add_row(['',''])
    weight_table.add_row(['Operator Items',W_op*lbs_to_kg])
    weight_table.add_row(['OWE',weight_fuel_systems()+(weight_structure()+weight_nacelle_group()+weight_APU_installed()+weight_systems()+weight_furnishings()+2*W_ec+W_op)*lbs_to_kg])

    weight_table.add_column('',['','','','','','','','']) #empty column

    weight_table.add_column('Structure details',['wing','fuselage','horizontal tail','vertical tail','landing gear','Pylons','',''])
    weight_table.add_column(' [kg]',[weight_wing()*lbs_to_kg,weight_fuselage()*lbs_to_kg,weight_horizontal_tail()*lbs_to_kg,weight_vertical_tail()*lbs_to_kg,weight_main_landing_gear()*lbs_to_kg + weight_nose_landing_gear()*lbs_to_kg,W_pylons*lbs_to_kg,'',''])

    weight_table.add_column('',['','','','','','','','']) #empty column

    weight_table.add_column('Systems details',['fuel systems','hydraulic','fire protection','electric','air conditioning','anti-ice','',''])
    weight_table.add_column('  [kg]',[weight_fuel_systems(),weight_hydraulics()*lbs_to_kg,W_fp*lbs_to_kg,(weight_electrical()+weight_engine_controls()+weight_starter()+weight_avionics()+weight_instruments()+weight_flight_control()) \
    *lbs_to_kg,weight_air_conditioning()*lbs_to_kg,weight_anti_ice()*lbs_to_kg,'',''])


    weight_table.float_format = '.0'

    print(weight_table)


def print_weights_in_kg_FZE2():

    print('FZE2 Formulary equations for comparison:')

    weight_table = PrettyTable(['Weight breakdown','[kg]'])

    weight_table.add_row(['Structure',weight_structure_FZE2()])
    weight_table.add_row(['Equipped engines (engines + nacelle)',(2*W_ec*lbs_to_kg+weight_nacelle_FZE2())])
    weight_table.add_row(['APU',weight_APU_installed()*lbs_to_kg])
    weight_table.add_row(['Systems',weight_systems_FZE2()])
    weight_table.add_row(['Furnishings',weight_furnishings()*lbs_to_kg])
    weight_table.add_row(['',''])
    weight_table.add_row(['Operator Items',W_op*lbs_to_kg])
    weight_table.add_row(['OWE',weight_structure_FZE2()+weight_nacelle_FZE2()+ weight_systems_FZE2()+ (weight_APU_installed()+weight_furnishings()+2*W_ec+W_op)*lbs_to_kg])

    weight_table.add_column('',['','','','','','','','']) #empty column

    weight_table.add_column('Structure details',['wing','fuselage','horizontal tail','vertical tail','landing gear','Pylons','',''])
    weight_table.add_column(' [kg]',[weight_wing_FZE2(),weight_fuselage_FZE2(),weight_horizontal_tail_FZE2(),weight_vertical_tail_FZE2(),\
    weight_main_landing_gear_FZE2() + weight_nose_landing_gear_FZE2(),W_pylons*lbs_to_kg,'',''])


    weight_table.float_format = '.0'

    print(weight_table)


def print_weights_in_kg_optimal(): #selecting the best fitting equations

    print('=================================')
    print('Component Weights and COG')
    print('=================================\n')

    print('Optimal equations from both sources with calibration factors:')

    weight_table = PrettyTable(['Weight breakdown','[kg]'])

    weight_table.add_row(['Structure',weight_structure_FZE2()])
    weight_table.add_row(['Equipped engines (engines + nacelle)',(2*W_ec+weight_nacelle_group()+weight_starter()+weight_engine_controls())*lbs_to_kg])
    weight_table.add_row(['APU',weight_APU_installed()*lbs_to_kg])
    weight_table.add_row(['Systems',weight_systems()*lbs_to_kg+weight_fuel_systems()])
    weight_table.add_row(['Furnishings',weight_furnishings()*lbs_to_kg])
    weight_table.add_row(['',''])
    weight_table.add_row(['Operator Items',W_op*lbs_to_kg])
    weight_table.add_row(['OWE',weight_structure_FZE2() + weight_fuel_systems() + (weight_systems()+weight_nacelle_group()+weight_starter()+weight_APU_installed()+weight_furnishings()+2*W_ec+W_op)*lbs_to_kg])

    weight_table.add_column('',['','','','','','','','']) #empty column

    weight_table.add_column('Structure details',['wing','fuselage','horizontal tail','vertical tail','landing gear','Pylons','',''])
    weight_table.add_column(' [kg]',[weight_wing_FZE2(),weight_fuselage_FZE2(),weight_horizontal_tail_FZE2(),weight_vertical_tail_FZE2(),\
    weight_main_landing_gear_FZE2() + weight_nose_landing_gear_FZE2(),W_pylons*lbs_to_kg,'',''])

    weight_table.add_column('',['','','','','','','','']) #empty column

    weight_table.add_column('Systems details',['fuel systems','hydraulic','fire protection','electric','air conditioning','anti-ice','',''])
    weight_table.add_column('  [kg]',[weight_fuel_systems(),weight_hydraulics()*lbs_to_kg,W_fp*lbs_to_kg,(weight_electrical()+weight_avionics()+weight_instruments()+weight_flight_control()) \
    *lbs_to_kg,weight_air_conditioning()*lbs_to_kg,weight_anti_ice()*lbs_to_kg,'',''])


    weight_table.float_format = '.0'

    print(weight_table)

    #print(weight_nacelle_group()*lbs_to_kg)
    #print(weight_engine_controls()*lbs_to_kg)
    #print(weight_starter()*lbs_to_kg)
    



### COG calculations ###

def COG_calculation_optimal(): #in kgs and meters!

    sum_of_masses = weight_structure_FZE2() + weight_fuel_systems() + (weight_nacelle_group()+weight_APU_installed()+weight_systems()+2*W_ec)*lbs_to_kg

    masses_times_distance = x_wing*weight_wing_FZE2() + x_fuselage*weight_fuselage_FZE2() + x_h_tail*weight_horizontal_tail_FZE2() + x_v_tail*weight_vertical_tail_FZE2() \
    + x_nose_landing_gear*weight_nose_landing_gear_FZE2() + x_main_landing_gear*weight_main_landing_gear_FZE2() + x_pylons*W_pylons*lbs_to_kg + x_APU*weight_APU_installed()*lbs_to_kg \
    + x_engine*(2*W_ec+weight_nacelle_FZE2()+weight_starter()+weight_engine_controls())*lbs_to_kg + x_electric*(weight_electrical()+weight_avionics()+weight_instruments()+weight_flight_control())*lbs_to_kg \
    + x_hydraulic*weight_hydraulics()*lbs_to_kg + x_air_conditioning*weight_air_conditioning()*lbs_to_kg + x_anti_ice*weight_anti_ice()*lbs_to_kg + x_tank_front*W_tank_front + x_tank_aft*W_tank_aft

    COG = masses_times_distance/sum_of_masses

    MAC_percent = (COG - x_start_MAC)/MAC * 100


    print('\nCenter of of Gravity (at OWE) = %3.2f m' %(COG))
    print('%% of MAC = %3.1f%%\n' %(MAC_percent))

    OWE = weight_structure_FZE2() + weight_fuel_systems() + (weight_systems()+weight_nacelle_group()+weight_starter()+weight_APU_installed()+weight_furnishings()+2*W_ec+W_op)*lbs_to_kg

    print('MTOM = %7.0f [kg]' %(OWE+60000+300+16330))
    print('MLW = %7.0f [kg]' %(OWE+60000+300+1768))

    return COG,OWE,MTOM


def COG_z_calculation_optimal(): #in kgs and meters!

    sum_of_masses = weight_structure_FZE2() + weight_fuel_systems() + (weight_nacelle_group()+weight_APU_installed()+weight_systems()+2*W_ec)*lbs_to_kg

    masses_times_distance = z_wing*weight_wing_FZE2() + z_fuselage*weight_fuselage_FZE2() + z_h_tail*weight_horizontal_tail_FZE2() + z_v_tail*weight_vertical_tail_FZE2() \
    + z_nose_landing_gear*weight_nose_landing_gear_FZE2() + z_main_landing_gear*weight_main_landing_gear_FZE2() + z_pylons*W_pylons*lbs_to_kg + z_APU*weight_APU_installed()*lbs_to_kg \
    + z_engine*(2*W_ec+weight_nacelle_FZE2()+weight_starter()+weight_engine_controls())*lbs_to_kg + z_electric*(weight_electrical()+weight_avionics()+weight_instruments()+weight_flight_control())*lbs_to_kg \
    + z_hydraulic*weight_hydraulics()*lbs_to_kg + z_air_conditioning*weight_air_conditioning()*lbs_to_kg + z_anti_ice*weight_anti_ice()*lbs_to_kg + z_tank_front*W_tank_front + z_tank_aft*W_tank_aft

    COG_z = masses_times_distance/sum_of_masses

    print('\nCenter of of Gravity in z-direction = %3.2f m\n' %(COG_z))


    ##### fuselage group and wing group separately for wing positioning ######

    mass_fuselage_group =  weight_fuselage_FZE2() + weight_horizontal_tail_FZE2() + weight_vertical_tail_FZE2() \
    + weight_nose_landing_gear_FZE2() + weight_main_landing_gear_FZE2() + weight_APU_installed()*lbs_to_kg \
    + (weight_electrical()+weight_avionics()+weight_instruments()+weight_flight_control())*lbs_to_kg \
    + weight_hydraulics()*lbs_to_kg + weight_air_conditioning()*lbs_to_kg + W_tank_front + W_tank_aft +W_op*lbs_to_kg +weight_furnishings()*lbs_to_kg


    mass_wing = weight_wing_FZE2() \
    + W_pylons*lbs_to_kg \
    + (2*W_ec+weight_nacelle_FZE2()+weight_starter()+weight_engine_controls())*lbs_to_kg \
    + weight_anti_ice()*lbs_to_kg


    COG_fuselage = (x_fuselage*weight_fuselage_FZE2() + x_h_tail*weight_horizontal_tail_FZE2() + x_v_tail*weight_vertical_tail_FZE2() \
    + x_nose_landing_gear*weight_nose_landing_gear_FZE2() + x_main_landing_gear*weight_main_landing_gear_FZE2()+ x_APU*weight_APU_installed()*lbs_to_kg \
    + x_electric*(weight_electrical()+weight_avionics()+weight_instruments()+weight_flight_control())*lbs_to_kg \
    + x_hydraulic*weight_hydraulics()*lbs_to_kg + x_air_conditioning*weight_air_conditioning()*lbs_to_kg + x_tank_front*W_tank_front + x_tank_aft*W_tank_aft \
    + W_op*lbs_to_kg*x_fuselage+weight_furnishings()*lbs_to_kg*x_fuselage)/mass_fuselage_group


    COG_wing_group = (x_wing*weight_wing_FZE2() + x_pylons*W_pylons*lbs_to_kg \
    + x_engine*(2*W_ec+weight_nacelle_FZE2()+weight_starter()+weight_engine_controls())*lbs_to_kg \
    + x_anti_ice*weight_anti_ice()*lbs_to_kg)/mass_wing



    print('Fuselage group weight: \t%5.0f kg' %(mass_fuselage_group))
    print('COG: \t\t\t%4.2f m' %(COG_fuselage))
    print('Wing group weight: \t%5.0f kg' %(mass_wing))
    print('COG: \t\t\t%4.2f m' %(COG_wing_group),'\n')



    return COG_z

#### Variables that need to be changed !!! #####################################
lbs_to_kg = 0.4535924
ft_to_m = 0.3048

### FZE2 (torenbeek) equation in SI units

v_D = 256 # design diving speed
r_H = 37.804 # lever horizontal tail
b_R = 6.238 # width fuselage
h_R = 6.77 # height fuselage
S_O = 1221 # Total area fuselage

S_hlw = 43.21 # Horizontal tail area
k_H = 1.1# 
phi_50_h = 31.23*np.pi/180 #  sweep horizontal tail
S_slw = 51.4 # vertical tail area
h_slw = 9.18 #vertical tail height
b_hlw = 14.9 # horizontal tail span
k_S = 1 + 0.15* (S_hlw*b_hlw)/(S_slw*h_slw)#
phi_50_s = 36*np.pi/180 # sweep vertical tail

MTOM = 202000 #

### Raymer Variables in ft and lbs!!! ####
B_w = 75.94/ft_to_m # wing span
L_ec = 2*20.5/ft_to_m # length from engine front to cockpit, total if multiengine
L_a = 112/ft_to_m # electrical routing distance, generators to avionics to cockpit
L_f = 69.47/ft_to_m # total fuselage length
N_Lt = 5.39/ft_to_m # length of nacelle ,for a330 5.76 m
N_w = 3.48/ft_to_m # width of nacelle ,for a330 3.72 m
S_cs = 1555 # total area of control surfaces
S_f = 13142 # wetted area fuselage
S_n = 1260 # wetted area nacelle
V_pr = 37000 # volume of pressurized area
W_dg = 202000/lbs_to_kg # design gross weight


#### Variables that don't need to be changed !!! #####################################

#### Toreenbeek ####

phi_50 = 22*np.pi/180 # sweep at 50% MAC
b_wing = 80 # Wing span
b_s = b_wing/m.cos(phi_50) # 
S_wing = 361.28 # Wing area
d_root = 0.6 # wing thickness at root
mzfm = 198000 # maximum zero fuel mass
k_FW = 1
A_Nose = 9.1 
B_Nose = 0.082 
C_Nose = 0 
D_Nose = 2.97E-6 

A_Main = 18.1 
B_Main = 0.0131 
C_Main = 0.019 
D_Main = 2.23E-5 

k_St = 0.492 
F_max_TO = 2*72800 # lbf or N?

### Raymer Variables in ft and lbs!!! ####

l_over_d_cruise = 20.8
taper_r = 0.235 #taper ratio
Lambda = 30*np.pi/180 #wing sweep at 25%MAC
Lambda_ht = 30*np.pi/180
Lambda_vt = 39.5*np.pi/180
t_c_w = 0.15 #thickness over chord at root
t_c_v = 0.09
v_stall = 116 #knots

A = 9.26
A_h = 5.2
A_v = 7.5
B_h = 19.404/ft_to_m
D = 5.64/ft_to_m
F_w = 3.01/ft_to_m
H_t_H_v = 0
I_y = 3.5E5
K_door = 1.12
K_Lg = 1
K_mp = 1
K_ng = 1.017
K_np = 1 
K_p = 1
K_r = 1
K_tp = 1
K_tr = 1.18
K_uht = 1.143
K_ws = 0.63 #0.75*((1+2*taper_r)/(1+taper_r))*B_w*m.tan(Lambda/L)
K_y = 26.4
K_z = 0.9*26.85/ft_to_m
L = 47.7/ft_to_m
L_m = 141
L_n = 90
L_t = 26.85/ft_to_m
M = 0.82
N_c = 3
N_en = 2
N_f = 7
N_gen = N_en 
N_l = 1.5*2.5 
N_m = 1
N_mss = 3
N_mw = 8
N_nw = 2
N_p = N_c
N_t = 2
N_z = 1.5*2.5
R_kva = 50
S_csw = 1172
S_e = 200
S_ht = 769
S_r = 183 
S_vt = 548 
S_w = 3892.23
V_i = 9446
V_p = 7925 
V_t = 17371
W_c = 60000/lbs_to_kg 
W_en = 13500*0.92**3 #
W_ec = 2.331*W_en**0.901*K_p*K_tr
W_l =  176000/lbs_to_kg
W_uav = 1000 
W_pylons = 3000/lbs_to_kg
W_fp = 250/lbs_to_kg #fire protection
W_op = 2500/lbs_to_kg #operator Items
W_APU_uninstalled = 191.5/lbs_to_kg #

total_cargo_length = 38.82 + 12.59 + 6.27 #top level plus bottom level

W_tank_front = 4795#3530 # #structural mass [kg]
W_tank_aft = 8963#10102 #

### "fudge factors" from Raymer ####

ff_wing = 0.85
ff_tails = 0.83
ff_fuselage = 0.85
ff_nacelle = 0.85
ff_landing_gear = 0.95
ff_braced_wing = 0.70


### COG Positions of each component in meters

MAC = 5.029
x_25_MAC = 30.8#32.7
x_start_MAC = x_25_MAC - 0.25*MAC

# abstand CS zu Nase -2.16

x_wing = x_25_MAC+1.303
z_wing = 2

x_fuselage = 30#31.15 
z_fuselage = 0.07

x_h_tail = 69.97
z_h_tail = 11.44

x_v_tail = 62.78
z_v_tail = 5.2

x_nose_landing_gear = 5
z_nose_landing_gear = -4.5

x_main_landing_gear = 33.92
z_main_landing_gear = -4.4

x_pylons = x_25_MAC-4.8
z_pylons = 0.85

x_APU = 3.5
z_APU = -2.5

x_engine = x_25_MAC-4.8
z_engine = 0.85

x_electric = 18.01#24
z_electric = -1.5

x_hydraulic = x_wing
z_hydraulic = 1.2

x_air_conditioning = 25
z_air_conditioning = 0

x_anti_ice = x_wing
z_anti_ice = 2

x_tank_front = 13
z_tank_front = -1.89

x_tank_aft = 50.48
z_tank_aft = 0.3


##### Correction Factors #####
calibration_wing = 1.083
calibration_fuselage = 0.933
calibration_h_tail = 0.79
calibration_v_tail = 0.73
calibration_main_landing = 1.27
calibration_nose_landing = 1.27
calibration_furnishings = 1.36
calibration_nacelle = 1.5
calibration_electric = 1.79
calibration_hydraulic = 7.5
calibration_fuel = 1.4
calibration_air_conditioning = 1.5
calibration_anti_ice = 1.6