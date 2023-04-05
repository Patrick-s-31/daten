import numpy as np  

def empennage_design():

    S_horizontal = vc_H * (S_ref * mac) / (r_H *correction_h)

    S_vertical = vc_V * (S_ref * b) /(r_V *correction_v )

    print('=================================')
    print('Empennage Sizing')
    print('=================================\n')
    print('Area:')
    print('Horizontal tail: %4.2f' %(S_horizontal),'m2')
    print('Vertical tail: %4.2f' %(S_vertical),'m2')


S_ref = 366 
mac = 4.3
b = 70
r_H = 37.5 # [m]
r_V = 38.5 # [m]

vc_H = 1.0
vc_V = 0.09
    
#S_vertical = 51.4 #[m2]
    
#S_horizontal = 71.45 #[m2]


correction_h = 1.371
correction_v = 1.496

