import os
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from PIL import Image
import surf2stl
import pyvista as pv
import bpy



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
image_name = 'test.jpg'
image = Image.open(image_name)
A = asarray(image)
A = A[:,:,0]


a = 5/(2*np.pi)
theta = spiral_size/(2*a) # total theta at end of spiral
x_scale = A.shape[1]/spiral_size * 1.25
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
Z_top.shape
Z_bottom.shape

print('Creating spiral facets')
#Generate surfaces and write to .stl files

#Top surface
X_body = np.concatenate(([X_in.T], [X_out.T], [X_out.T], [X_in.T], [X_in.T]),axis=0)
Y_body = np.concatenate(([Y_in.T], [Y_out.T], [Y_out.T], [Y_in.T], [Y_in.T]),axis=0)
Z_body = np.concatenate(([Z_top.T], [Z_top.T],  [Z_bottom.T],  [Z_bottom.T],  [Z_top.T]),axis=0)
surf2stl.write('Shell.stl', X_body, Y_body, Z_body)

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

Shell = pv.PolyData("Shell.stl")
Front = pv.PolyData("Front.stl")
Back = pv.PolyData("Back.stl")


merged_surface = Shell + Front + Back

merged_surface.flip_normals()
#merged_surface.clean()
#merged_surface.plot_normals(faces=True)
merged_surface.save("Full_Body.stl")


# Import the STL file
bpy.ops.import_mesh.stl(filepath="Full_Body.stl")

stl_obj = bpy.context.selected_objects[0]



# Set the dimensions of the hexagonal cylinder
height_hex = height+2
width_hex = 150 #distance between two parallel sides
Diameter_hex = width_hex/(np.cos(30*np.pi/180)) #Diameter of Circle outside Hex

#create grid of points, where hexagons will be
num_points = round(spiral_size / width_hex)+2 #in x and y respectively

hex_grid_x = np.zeros((num_points,num_points))
hex_grid_y = np.zeros((num_points,num_points))

for i in range(num_points):
    for j in range(num_points):

        if i%2 == 0:
            hex_grid_x[i,j] = j*width_hex
        else:
            hex_grid_x[i,j] = j*width_hex + width_hex/2

        hex_grid_y[i,j] = -i*width_hex*np.cos(30*np.pi/180)


#shift grid to be centered
shift_x = num_points*width_hex/2
shift_y = num_points*(width_hex*np.cos(30*np.pi/180))/2 + (width_hex*np.cos(30*np.pi/180)/2-Diameter_hex/4)
hex_grid_x = hex_grid_x - shift_x
hex_grid_y = hex_grid_y + shift_y

#create parts folder, delete contents if it already exists
if not os.path.exists('parts'):
    os.mkdir('parts')     
else:
    for f in os.listdir('parts'):
        os.remove(os.path.join('parts', f))

k = 0
#loop through all hex positions
for i in range(hex_grid_x.shape[0]):
        
    for j in range(hex_grid_x.shape[1]):

        if np.sqrt(hex_grid_x[i,j]**2 + hex_grid_y[i,j]**2) > 1.1*spiral_size/2: #no hexagons outside of spiral
            pass
        else:
            k+=1
            # Create the hexagonal cylinder
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=Diameter_hex/2, depth=height_hex)

            # Move the hexagonal cylinder to the desired position
            bpy.ops.transform.translate(value=(hex_grid_x[i,j], hex_grid_y[i,j], height/2))

            # Rotate the hexagonal cylinder
            #bpy.ops.transform.rotate(value=0.523599, orient_axis='Z')

            # Get the hex object
            hex_obj = bpy.context.selected_objects[0]
            #hex_obj.select_set(False)

            # Add a Boolean modifier to the imported STL object
            bool_mod1 = hex_obj.modifiers.new(name='bool1', type='BOOLEAN')
            bool_mod1.operation = 'INTERSECT'
            bool_mod1.object = stl_obj

            # Apply the Boolean modifier
            bpy.ops.object.modifier_apply(modifier='bool1')


            # Select the intersected mesh
            #intersected_mesh = stl_obj.data
            #bpy.context.view_layer.objects.active = intersected_mesh
            #stl_obj.select_set(True)


            # Create the hexagonal boundary
            outside_diameter = Diameter_hex
            inside_diameter = Diameter_hex-1.6/np.cos(30*np.pi/180)

            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=inside_diameter/2, depth=height)
            inside_hex = bpy.context.selected_objects[0]
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=outside_diameter/2, depth=height)
            outside_hex = bpy.context.selected_objects[0]

            #Difference between inside and outside hex
            bool_mod2 = outside_hex.modifiers.new(name='bool2', type='BOOLEAN')
            bool_mod2.operation = 'DIFFERENCE'
            bool_mod2.object = inside_hex

            bpy.ops.object.modifier_apply(modifier='bool2')

            bpy.ops.transform.translate(value=(hex_grid_x[i,j], hex_grid_y[i,j], height/2))

            #Union of boundary and spiral part
            bool_mod2 = outside_hex.modifiers.new(name='bool3', type='BOOLEAN')
            bool_mod2.operation = 'UNION'
            bool_mod2.object = hex_obj

            bpy.ops.object.modifier_apply(modifier='bool3')

            # Export the united mesh as an STL file
            output_file = 'parts/part_' + str(k) + '.stl' 
            bpy.ops.export_mesh.stl(filepath=output_file, use_selection=True)

            print('part_' + str(k) + '.stl' + ' created')




