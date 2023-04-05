import numpy as np
import scipy.integrate as integrate
#input
S = 361.6 # [m2]
b = 60.304 # [m]
aspect_ratio = 9.25 # [-]
mac = 7.270 # [m]
sweep_angle = 29.755 # [°]
taper_ratio = 0.251 # [-]
dihedral = 5.000 # [°]
winglet_lenght = 1.82 # [m]

mach_cruise = 0.82
a = 296.5 # speed of sound at cruise altitude [m/s]
v_cruise = mach_cruise * a


kin_visco_cruise = 13.3 * 10**(-6) #check this!!!!
Re_MAC = mac * v_cruise / kin_visco_cruise

print(Re_MAC)



ca_max_profile = 1.2 #was muss man hier annehmen?
lambda_k = 0.5122 
eta_k = 0.295871
lambda_ = 0.2195

# def integrand(x):
#     if x < 0.096925:
#         l_eta = 9.183
#     elif x >= 0.096925 and x < 0.295871:
#         l_eta = (1-(1-lambda_k)/eta_k*x)*12.146
#     else:
#         l_eta = (lambda_k - (lambda_k-lambda_)/(1-eta_k)*(x-eta_k))*12.146
    
#     return double(b * ca_max_profile * l_eta) 

f1= lambda x: 9.183

f2= lambda x: (1-(1-lambda_k)/eta_k*x)*12.146

f3= lambda x: (lambda_k - (lambda_k-lambda_)/(1-eta_k)*(x-eta_k))*12.146

integration = (integrate.quad(f1, 0, 0.096925) + integrate.quad(f2, 0.096925, 0.295871) + integrate.quad(f3, 0.295871, 1))

cA_max_wing = 1/S
