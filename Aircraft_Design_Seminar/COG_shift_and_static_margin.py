import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def COG_shift_ferry(COG,OWE): #shift of COG for loading/fueling process

    COG_plot = np.zeros((4,2))

    #ferry range
    COG_plot[0,0] = COG
    COG_plot[0,1] = OWE

    COG_plot[1,0] = (COG*OWE + 0.5*weight_fuel_aft*x_tank_aft)/(OWE+0.5*weight_fuel_aft) #front tank fueling
    COG_plot[1,1] = OWE + 0.5*weight_fuel_aft

    COG_plot[2,0] = (COG_plot[1,0]*COG_plot[1,1] + weight_fuel_front*x_tank_front)/(COG_plot[1,1]+weight_fuel_front) #aft tank fueling
    COG_plot[2,1] = COG_plot[1,1] + weight_fuel_front 

    COG_plot[3,0] = (COG_plot[2,0]*COG_plot[2,1] + 0.5*weight_fuel_aft*x_tank_aft)/(COG_plot[2,1]+0.5*weight_fuel_aft) #front tank fueling
    COG_plot[3,1] = COG_plot[2,1] + 0.5*weight_fuel_aft

    return COG_plot


def COG_shift_pallets(COG,OWE):

    COG_plot = np.zeros((n_pr+3,2))

    COG_plot[0,0] = COG
    COG_plot[0,1] = OWE

    for i in range(1,n_pr+1):

        COG_plot[i,0] = (COG_plot[i-1,0]*COG_plot[i-1,1]+weight_pallet_row*(x_p_start-(i-1)*x_p_distance))/(COG_plot[i-1,1]+weight_pallet_row)
        COG_plot[i,1] = COG_plot[i-1,1]+weight_pallet_row

    
    COG_plot[n_pr+1,0] = (COG_plot[n_pr,0]*COG_plot[n_pr,1] + weight_fuel_aft*x_tank_aft)/(COG_plot[n_pr,1]+weight_fuel_aft)
    COG_plot[n_pr+1,1] = COG_plot[n_pr,1]+weight_fuel_aft

    COG_plot[n_pr+2,0] = (COG_plot[n_pr+1,0]*COG_plot[n_pr+1,1] + weight_fuel_front*x_tank_front)/(COG_plot[n_pr+1,1]+weight_fuel_front)
    COG_plot[n_pr+2,1] = COG_plot[n_pr+1,1]+weight_fuel_front

    return COG_plot


def COG_shift_containers(COG,OWE):

    COG_plot = np.zeros((1,2))
    temp1 = np.zeros((n_cr_bottom_aft,2))
    temp2 = np.zeros((n_cr_bottom_front,2)) 
    temp3 = np.zeros((n_cr_top,2))
    temp4 = np.zeros((n_cr_top,2))
    temp5 =  np.zeros((2,2))

    n_rows = np.array([])

    COG_plot[0,0] = COG
    COG_plot[0,1] = OWE

    #lower level aft
    for i in range(n_cr_bottom_aft):

        if i == 0:
            temp1[i,0] = (COG*OWE+weight_AKE_row*(x_c_start_bottom_aft+(i-1)*x_AKE_distance))/(OWE+weight_AKE_row)
            temp1[i,1] = OWE+weight_AKE_row

        else:
            temp1[i,0] = (temp1[i-1,0]*temp1[i-1,1]+weight_AKE_row*(x_c_start_bottom_aft+(i-1)*x_AKE_distance))/(temp1[i-1,1]+weight_AKE_row)
            temp1[i,1] = temp1[i-1,1]+weight_AKE_row

    #lower level front
    for i in range(n_cr_bottom_front):

        if i == 0:
            temp2[i,0] = (temp1[n_cr_bottom_aft-1,0]*temp1[n_cr_bottom_aft-1,1]+weight_AKE_row*(x_c_start_bottom_front-(i-1)*x_AKE_distance))/(temp1[n_cr_bottom_aft-1,1]+weight_AKE_row)
            temp2[i,1] = temp1[n_cr_bottom_aft-1,1]+weight_AKE_row

        else:
            temp2[i,0] = (temp2[i-1,0]*temp2[i-1,1]+weight_AKE_row*(x_c_start_bottom_front-(i-1)*x_AKE_distance))/(temp2[i-1,1]+weight_AKE_row)
            temp2[i,1] = temp2[i-1,1]+weight_AKE_row

    #upper level first collumn
    for i in range(n_cr_top):

        if i == 0:
            temp3[i,0] = (temp2[n_cr_bottom_front-1,0]*temp2[n_cr_bottom_front-1,1]+weight_AMJ_row*(x_c_start_top-(i-1)*x_AMJ_distance))/(temp2[n_cr_bottom_front-1,1]+weight_AMJ_row)
            temp3[i,1] =temp2[n_cr_bottom_front-1,1]+weight_AMJ_row

        else:
            temp3[i,0] = (temp3[i-1,0]*temp3[i-1,1]+weight_AMJ_row*(x_c_start_top-(i-1)*x_AMJ_distance))/(temp3[i-1,1]+weight_AMJ_row)
            temp3[i,1] = temp3[i-1,1]+weight_AMJ_row

    #upper level second collumn
    for i in range(n_cr_top):

        if i == 0:
            temp4[i,0] = (temp3[n_cr_top-1,0]*temp3[n_cr_top-1,1]+weight_AMJ_row*(x_c_start_top-(i-1)*x_AMJ_distance))/(temp3[n_cr_top-1,1]+weight_AMJ_row)
            temp4[i,1] =temp3[n_cr_top-1,1]+weight_AMJ_row

        else:
            temp4[i,0] = (temp4[i-1,0]*temp4[i-1,1]+weight_AMJ_row*(x_c_start_top-(i-1)*x_AMJ_distance))/(temp4[i-1,1]+weight_AMJ_row)
            temp4[i,1] = temp4[i-1,1]+weight_AMJ_row



    temp5[0,0] = (temp4[n_cr_top-1,0]*temp4[n_cr_top-1,1] + weight_fuel_aft*x_tank_aft)/(temp4[n_cr_top-1,1]+weight_fuel_aft)  #fuel aft
    temp5[0,1] = temp4[n_cr_top-1,1]+weight_fuel_aft

    temp5[1,0] = (temp5[0,0]*temp5[0,1] + weight_fuel_front*x_tank_front)/(temp5[0,1]+weight_fuel_front) #fuel front
    temp5[1,1] = temp5[0,1]+weight_fuel_front

    COG_plot = np.append(COG_plot, temp1, axis=0)
    COG_plot = np.append(COG_plot, temp2, axis=0)
    COG_plot = np.append(COG_plot, temp3, axis=0)
    COG_plot = np.append(COG_plot, temp4, axis=0)
    COG_plot = np.append(COG_plot, temp5, axis=0)

    return COG_plot


def static_margin(COG_plot):

    static_m = np.zeros((len(COG_plot),2))

    x_N = (x_N_MAC-0.25)*MAC+x_25_MAC

    for i in range(len(COG_plot)):

        static_m[i,0] = (x_N-COG_plot[i,0])/MAC * 100
        static_m[i,1] = (COG_plot[i,1])

    return static_m


###PLOTS#######

def plot_COG_shift_and_static_margin(COG,OWE,MTOM):
    OWE += 863

    print('=================================')
    print('Shift of COG and static margin')
    print('=================================\n')
    print('pdf plots')
    print('\t"Ferry_range.pdf"')
    print('\t"Pallet_loading.pdf"')
    print('\t"Container_loading.pdf"')
    print('have been created.\n')

    ##### Ferry range #########################################################################

    COG_plot1 = COG_shift_ferry(COG,OWE)

    fig, (ax1, ax2) = plt.subplots(2)

    #fig.suptitle('Shift of COG and static margin for ferry range')
    fig.set_figheight(6)

    plt.subplots_adjust(left=0.2,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.3,
                    hspace=0.3)


    ax1.plot((COG_plot1[:,0]- x_start_MAC)/MAC * 100 , COG_plot1[:,1],'limegreen',label='Fuel')
    ax1.plot([(COG_plot1[-4,0]- x_start_MAC)/MAC * 100,(COG_plot1[-1,0]- x_start_MAC)/MAC * 100],[ COG_plot1[-4,1] ,COG_plot1[-1,1]],'firebrick',label='Ideal detanking',linestyle='dashed', alpha=0.7)
    ax2.plot(static_margin(COG_plot1)[:,0] , static_margin(COG_plot1)[:,1],'limegreen')
    ax2.plot([static_margin(COG_plot1)[-4,0],static_margin(COG_plot1)[-1,0]],[static_margin(COG_plot1)[-4,1],static_margin(COG_plot1)[-1,1]],'firebrick',linestyle='dashed', alpha=0.7)

    ax2.vlines(5,100000,240000,color='orange',linestyle='dashed')
    ax2.vlines(30,100000,240000,color='orange',linestyle='dashed')

    ax1.hlines(COG_plot1[-1,1],20,70,color='dimgray',linestyle='dashed', alpha=0.6)
    ax1.annotate('MTOW',(25,COG_plot1[-1,1]+4000))

    ax2.hlines(COG_plot1[-1,1],-10,45,color='dimgray',linestyle='dashed', alpha=0.6)

    ax1.set_xlabel('\% MAC')
    ax1.set_ylabel('Weight [kg]')
    ax1.set_ylim(120000,240000)
    ax1.set_xlim(20,70)
    ax1.grid()

    ax2.set_xlabel('\% Static margin')
    ax2.set_ylabel('Weight [kg]')
    ax2.set_ylim(120000,240000)
    ax2.axvspan(-15, 5, facecolor='0.2', alpha=0.3)
    ax2.axvspan(30, 45, facecolor='0.2', alpha=0.3)
    ax2.set_xlim(-10,45)
    ax2.grid()

    ax1.legend()

    #plt.show()
    plt.savefig("Ferry_range.pdf")
    plt.close()


    #### Pallet loading #######################################################################

    COG_plot2 = COG_shift_pallets(COG,OWE)

    fig, (ax1, ax2) = plt.subplots(2)

    #fig.suptitle('Shift of COG and static margin for pallet loading')
    fig.set_figheight(6)

    plt.subplots_adjust(left=0.2,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.3,
                    hspace=0.3)


    ax1.plot((COG_plot2[:-2,0]- x_start_MAC)/MAC * 100 , COG_plot2[:-2,1],label='Payload')
    ax1.plot((COG_plot2[-3:,0]- x_start_MAC)/MAC * 100 , COG_plot2[-3:,1],'limegreen',label='Fuel')
    ax1.plot([(COG_plot2[-3,0]- x_start_MAC)/MAC * 100,(COG_plot2[-1,0]- x_start_MAC)/MAC * 100],[ COG_plot2[-3,1] ,COG_plot2[-1,1]],'firebrick',label='Ideal detanking',linestyle='dashed', alpha=0.7)
    ax2.plot(static_margin(COG_plot2)[:-2,0] , static_margin(COG_plot2)[:-2,1])
    ax2.plot(static_margin(COG_plot2)[-3:,0] , static_margin(COG_plot2)[-3:,1],'limegreen')
    ax2.plot([static_margin(COG_plot2)[-3,0],static_margin(COG_plot2)[-1,0]],[static_margin(COG_plot2)[-3,1],static_margin(COG_plot2)[-1,1]],'firebrick',linestyle='dashed', alpha=0.7)
    

    ax2.vlines(5,100000,240000,color='orange',linestyle='dashed')
    ax2.vlines(30,100000,240000,color='orange',linestyle='dashed')

    ax1.hlines(COG_plot2[-1,1],20,70,color='dimgray',linestyle='dashed', alpha=0.6)
    ax1.annotate('MTOW',(25,COG_plot2[-1,1]+4000))

    ax2.hlines(COG_plot2[-1,1],-10,45,color='dimgray',linestyle='dashed', alpha=0.6)

    ax1.set_xlabel('\% MAC')
    ax1.set_ylabel('Weight [kg]')
    ax1.set_ylim(120000,240000)
    ax1.set_xlim(20,70)
    ax1.grid()

    ax2.set_xlabel('\% Static margin')
    ax2.set_ylabel('Weight [kg]')
    ax2.set_ylim(120000,240000)
    ax2.axvspan(-15, 5, facecolor='0.2', alpha=0.3)
    ax2.axvspan(30, 45, facecolor='0.2', alpha=0.3)
    ax2.set_xlim(-10,45)
    ax2.grid()

    ax1.legend()

    #plt.show()
    plt.savefig("Pallet_loading.pdf")
    plt.close()


    #### Container loading #######################################################################

    COG_plot3 = COG_shift_containers(COG,OWE)

    fig, (ax1, ax2) = plt.subplots(2)

    #fig.suptitle('Shift of COG and static margin for container loading')
    fig.set_figheight(6)

    plt.subplots_adjust(left=0.2,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.3,
                    hspace=0.3)


    ax1.plot((COG_plot3[:-2,0]- x_start_MAC)/MAC * 100 , COG_plot3[:-2,1],label='Payload')
    ax1.plot((COG_plot3[-3:,0]- x_start_MAC)/MAC * 100 , COG_plot3[-3:,1],'limegreen',label='Fuel')
    ax1.plot([(COG_plot3[-3,0]- x_start_MAC)/MAC * 100,(COG_plot3[-1,0]- x_start_MAC)/MAC * 100],[ COG_plot3[-3,1] ,COG_plot3[-1,1]],'firebrick',label='Ideal detanking',linestyle='dashed', alpha=0.7)
    ax2.plot(static_margin(COG_plot3)[:-2,0] , static_margin(COG_plot3)[:-2,1])
    ax2.plot(static_margin(COG_plot3)[-3:,0] , static_margin(COG_plot3)[-3:,1],'limegreen')
    ax2.plot([static_margin(COG_plot3)[-3,0],static_margin(COG_plot3)[-1,0]],[static_margin(COG_plot3)[-3,1],static_margin(COG_plot3)[-1,1]],'firebrick',linestyle='dashed', alpha=0.7)

    ax2.vlines(5,100000,240000,color='orange',linestyle='dashed')
    ax2.vlines(30,100000,240000,color='orange',linestyle='dashed')

    ax1.hlines(COG_plot3[-1,1],20,70,color='dimgray',linestyle='dashed', alpha=0.6)
    ax1.annotate('MTOW',(25,COG_plot3[-1,1]+4000))

    ax2.hlines(COG_plot3[-1,1],-10,45,color='dimgray',linestyle='dashed', alpha=0.6)

    ax1.set_xlabel('\% MAC')
    ax1.set_ylabel('Weight [kg]')
    ax1.set_ylim(120000,240000)
    ax1.set_xlim(20,70)
    ax1.grid()

    ax2.set_xlabel('\% Static margin')
    ax2.set_ylabel('Weight [kg]')
    ax2.set_ylim(120000,240000)
    ax2.axvspan(-15, 5, facecolor='0.2', alpha=0.3)
    ax2.axvspan(30, 45, facecolor='0.2', alpha=0.3)
    ax2.set_xlim(-10,45)
    ax2.grid()

    ax1.legend()


    #plt.show()
    plt.savefig("Container_loading.pdf")
    plt.close()




x_N_MAC = 0.524#0.5192 #Neutral point of aircraft in MAC
#x_N = 33.978 #Neutral point of aircraft  
x_tank_front = 13 #[m]
x_tank_aft = 51.62 

x_p_start = 38.5 #position of first loaded pallet row
x_p_distance = 4
x_c_start_top = 44.2#43.8 #position of first loaded container row (top floor)
x_c_start_bottom_front = 30.45#32.52
x_c_start_bottom_aft = 36.7#39.87
x_AMJ_distance = 3.225
x_AKE_distance = 1.58


weight_fuel_front = 5297-278#4075-210 #[kg] #fuel weight
weight_fuel_aft = 11089-584#12225-650
weight_pallet_row = 2*6000 #[kg] weight of a row of pallets
weight_AMJ_row = 1950 #(single container)
weight_AKE_row = 2*506

n_pr = 5 #number of pallet rows
n_cr_top = 12 #number of container rows
n_cr_bottom_front = 7 #9
n_cr_bottom_aft = 6 #4

MAC = 5.029
x_25_MAC = 30.8
x_start_MAC = x_25_MAC - 0.25*MAC