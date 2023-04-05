#Main function to call all other functions
from mass_estimation import *
from sizing_diagram import *
from component_mass import *
from COG_shift_and_static_margin import *
from empennage_design import *
from range import *

 
masses = MTOW_iteration() #returns vector containing [m0,m30,m40,m50]

#print(mass_fraction)

S,F = plot_sizing_diagram(masses) #takes the MTOW from mass estimation, returns Wing area and Thrust, also plot as pdf


print_weights_in_kg_optimal() #best from both
COG,OWE,MTOM = COG_calculation_optimal() #returns Center of Gravity in meters and OWE

COG_z_calculation_optimal() #in z-direction

plot_COG_shift_and_static_margin(COG,OWE,MTOM) #plots a pdf for each mission (container, pallet, ferry) showing shift of COG and static margin

empennage_design()

range_iteration_loop(19000,OWE)