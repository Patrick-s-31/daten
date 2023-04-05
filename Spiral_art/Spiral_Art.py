import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from PIL import Image
import surf2stl
#import PyMesh
#from pymesh import stl
import igl
import pyvista as pv



def arclength(theta):
    l = a/2 * (theta * np.sqrt(1 + theta**2) + np.arcsinh(theta))
    return l

def equation(theta):
    f = arclength(theta) - point_s[i]
    return f 

resolution = 100000 #[line segments]
spiral_size = 800 #[mm]
height = 2 #[mm]

#initialization
amplitude_out = np.zeros((resolution))
amplitude_in = np.zeros((resolution))
angle = np.zeros((resolution));
amplitude = np.zeros((resolution));

#import image
image = Image.open('test_2.jpg')
A = asarray(image)
A = A[:,:,0]


a = 5/(2*np.pi)
theta = spiral_size/(2*a) # total theta at end of spiral
x_scale = A.shape[0]/spiral_size * 1.25
y_scale = A.shape[1]/spiral_size * 1.25
angle[0] = 0
amplitude[0] = 3

s_total = arclength(theta)
point_ds = s_total/(resolution-1)
point_s = np.linspace(0,s_total,resolution)

for i in range(1,resolution):
    angle[i] = float(fsolve(equation,angle[i-1]))

amplitude = amplitude[0] + a*angle

x_spine = amplitude*np.cos(angle);
y_spine = amplitude*np.sin(angle);

default_thickness = 0.4 #twice

for k in range(resolution):
    if np.round(A.shape[0]/2-y_scale*y_spine[k]) > A.shape[0]-1 or np.round(A.shape[1]/2+x_scale*x_spine[k]) > A.shape[1]-1 or np.round(A.shape[0]/2-y_scale*y_spine[k]) < 0 or np.round(A.shape[1]/2+x_scale*x_spine[k]) < 0:
        
        amplitude_out[k] = amplitude[k]+default_thickness
        amplitude_in[k] = amplitude[k]-default_thickness

    else:
        amplitude_out[k] = amplitude[k]+2-1.6*np.double(A[int(np.round(A.shape[0]/2-y_scale*y_spine[k])),int(np.round(A.shape[1]/2+x_scale*x_spine[k]))])/255
        amplitude_in[k] = amplitude[k]-2+1.6*np.double(A[int(np.round(A.shape[0]/2-y_scale*y_spine[k])),int(np.round(A.shape[1]/2+x_scale*x_spine[k]))])/255


X_out = amplitude_out*np.cos(angle)
Y_out = amplitude_out*np.sin(angle)

X_in = amplitude_in*np.cos(angle)
Y_in = amplitude_in*np.sin(angle)

Z_bottom = np.zeros((resolution))
Z_top = np.repeat(height,resolution)

#print(Z_top.shape)


#Generate surfaces and write to .stl files

#Top surface
X_body = np.append([X_in.T] , [X_out.T],axis=0)
Y_body = np.append([Y_in.T], [Y_out.T],axis=0)
Z_body = np.append([Z_top.T] , [Z_top.T],axis=0)
surf2stl.write('Top.stl', X_body, Y_body, Z_body)

#Inside surface
X_body = np.append([X_in.T] , [X_in.T],axis=0)
Y_body = np.append([Y_in.T], [Y_in.T],axis=0)
Z_body = np.append([Z_top.T] , [Z_bottom.T],axis=0)
surf2stl.write('Inside.stl', X_body, Y_body, Z_body)

#Bottom surface
X_body = np.append([X_in.T] , [X_out.T],axis=0)
Y_body = np.append([Y_in.T], [Y_out.T],axis=0)
Z_body = np.append([Z_bottom.T] , [Z_bottom.T],axis=0)
surf2stl.write('Bottom.stl', X_body, Y_body, Z_body)

#Outside surface
X_body = np.append([X_out.T] , [X_out.T],axis=0)
Y_body = np.append([Y_out.T], [Y_out.T],axis=0)
Z_body = np.append([Z_top.T] , [Z_bottom.T],axis=0)
surf2stl.write('Outside.stl', X_body, Y_body, Z_body)

#Front surface
X_body = np.array([[X_in[0], X_out[0]],[X_in[0], X_out[0]]])
Y_body = np.array([[Y_in[0], Y_out[0]],[Y_in[0], Y_out[0]]])
Z_body = np.array([[Z_top[0], Z_top[0]],[Z_bottom[0], Z_bottom[0]]])
surf2stl.write('Front.stl', X_body, Y_body, Z_body)

#Back surface
X_body = np.array([[X_in[-1], X_out[-1]],[X_in[-1], X_out[-1]]])
Y_body = np.array([[Y_in[-1], Y_out[-1]],[Y_in[-1], Y_out[-1]]])
Z_body = np.array([[Z_top[-1], Z_top[-1]],[Z_bottom[-1], Z_bottom[-1]]])
surf2stl.write('Back.stl', X_body, Y_body, Z_body)


#import surfaces, stitch surfaces and correct normals

Top = pv.PolyData("Top.stl")
Inside = pv.PolyData("Inside.stl")
Bottom = pv.PolyData("Bottom.stl")
Outside = pv.PolyData("Outside.stl")
Front = pv.PolyData("Front.stl")
Back = pv.PolyData("Back.stl")


merged_surface = Top + Inside + Bottom + Outside + Front + Back

merged_surface.flip_normals()
#merged_surface.clean()
#merged_surface.plot_normals(faces=False)

plot = pv.Plotter()
#plot.add_mesh(merged_surface, color='gray',)
plot.set_background(color=[0.9, 0.9, 0.9])


merged_surface.save("Full_Body.stl")
#plot.add_mesh(merged_surface ,color='gray' ,show_edges=True)

#Create Hexagons and resulting parts

hex = pv.Cylinder(center=(0.0, 0.0, height/2), direction=(0.0, 0.0, 1.0), radius=(75)/np.cos(30*np.pi/180), height=height+1, resolution=6, capping=True).triangulate().subdivide(4,"linear")

temp = merged_surface.boolean_intersection(hex).fill_holes(5).clean()
#plot.add_mesh(temp ,color='gray' ,show_edges=True)
#plot.show()

hex1 = pv.Cylinder(center=(0.0, 0.0, height/2), direction=(0.0, 0.0, 1.0), radius=75/np.cos(30*np.pi/180), height=2.2, resolution=6, capping=True).triangulate().subdivide(4,"linear",)
hex2 = pv.Cylinder(center=(0.0, 0.0, height/2), direction=(0.0, 0.0, 1.0), radius=(75-0.8)/np.cos(30*np.pi/180), height=3.0, resolution=6, capping=True).triangulate().subdivide(4,"linear")
hex_boundary = hex1.boolean_difference(hex2).clean().fill_holes(30)
hex_boundary.save("boundary.stl")

temp.boolean_union(hex_boundary)#.clean().fill_holes(3)
plot.add_mesh(temp ,color='gray' ,show_edges=True)
#plot.add_mesh(hex_boundary ,color='gray' ,show_edges=True)
#plot.add_mesh(hex)
plot.show()

temp.save("part1.stl")


