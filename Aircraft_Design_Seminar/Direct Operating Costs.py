# Direct Operating Costs
import math

#Utilization Parameters

#OT_pa   =          #annual time of operation [h]
FT      = 9         #average flight time [h] !!!
BTS     = 0.5       #block time supplement[h]
ThOT_pa = 8760      #theoretical annual time of operation[h]
DT_pa   = 2749      #down time [h]

#Fuel Costs

BF      =  17000                   #Block Fuel [kg]!!!
K_fuel  =  0.0721 * 33.06         #fuel expenses [€/kg] (price from airbus chart €/kwh * power density kwh/kg) (75-98 $/mwh--> 86.5$/mwh 1€=1,2$ --->72.1€/mwh)
 
#Fees

K_nav = 0.76          #navigation distance [€/kg]
R     = 7400          #flight distance [km]!!! 
K_ldg = 0.01          #landing toll rate [€/kg]
K_grd = 0.1           #clearance rate [€/kg]
PL    = 60000         #payload[kg] !!!

#Maintanence 
LR    =  50                  #hourly wage
B     =  2                   #overhead rate
N_eng =  2                   #amount of engines
F_sls =   263500/ 9810       #static thrust at sea level [t] !!!
OME   =   124000/1000         #[t] !!!
MTOM  =   201000/1000         #[t] !!!

#crew

N_crew = 3                     #crew number
K_cc    = 300000               #average cockpitcrew salary Richtwert 300000 €/a 2010

#capital

IR    = 0.05                  #interest rate [%]
f_rv  = 0.1                   #restwertfaktor [-]
DP    = 14                    #depressiation duration
K_OME = 1150                  #cost per kg operating mass empty[€/kg]
M_eng = 7500                  #mass per engine [kg] !!!
K_eng = 2500                  #price per engine weight[€/kg]  !!! 
Ins   = 0.005                 #insurance rate [%]






#Calculations#

FC = (ThOT_pa - DT_pa) / (FT + BTS) 
DOC_fuel = (BF * K_fuel * FC) / FC
DOC_nav  =  (K_nav * R * math.sqrt(MTOM/50) * FC) * 1.03**30
DOC_ldg  =  (K_ldg * (MTOM * 1000)  * FC) * 1.03**30
DOC_grd  =  (K_grd * PL * FC)* 1.03**30

DOC_fees = (DOC_nav + DOC_ldg + DOC_grd) / FC

DOC_afmat = ((OME * (0.21 * FT + 13.7) + 57.5) * FC ) * 1.03**30
DOC_afper = (LR * (1+B) * ((0.655 + 0.01 * OME * FT) + 0.254 + 0.01 * OME )* FC)* 1.03**30
DOC_eng   = ((N_eng * (1.5 * F_sls + 30.5 * FT + 10.6)) * FC) * 1.03**30

DOC_maint = (DOC_afmat + DOC_afper + DOC_eng) / FC
DOC_crew =  (N_crew * K_cc * 1.03**30) /FC

A = IR * (1-f_rv * (1/(1+IR))**(DP))/ (1-(1/(1+IR))**(DP))
DOC_cap = (((K_OME * ((OME*1000) - M_eng * N_eng) + K_eng * M_eng * N_eng ) * (A + Ins))*1.03**30)/ FC




print(f"FC =  {FC}")
print(f"DOC_fuel =  {DOC_fuel}")
print(f"DOC_fees =  {DOC_fees}")
print(f"DOC_maint =  {DOC_maint}")
print(f"DOC_crew =  {DOC_crew}")
print(f"DOC_cap =  {DOC_cap}")


##################SAR Calculation###########################

l_d_heavy = 27 
l_d_airbus= 20         
#sfc =                   #specific fuel consumption
mtom_a330 = 220000            #mtom a330
v_airbus =  243,3                   #cruise speed
v_heavy =   236,2                   #


fuel_airbus = sfc * mtom_a330 * 9.81 / (v_airbus * l_d_heavy) 
fuel_heavy = sfc * MTOM * 9.81 / (v_heavy * l_d_heavy) 
delta_l_d = (l_d_heavy / l_d_airbus) * 100
delta_mtom = (MTOM / mtom_a330) * 100
delta_v = (v_heavy / v_airbus) * 100

#print(f"fuel_airbus =  {fuel_airbus}")
#print(f"fuel heavy=  {fuel_heavy}")
#print(f"delta l_d_heavy  =  {delta_l_d}")
#print(f"delta mtom =  {delta_mtom}")
#print(f"delta velocity =  {delta_v}")