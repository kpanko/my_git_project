"""
Name: 'step_pyramid'
Blender: 250
Group: 'AddMesh'
Tip: 'Add Step Pyramid Object...'
"""
__author__= [ "Phil Cote", "BlenderPythonTutorials.com" ]
__version__ = '.01'

# Last Update: Feb 6
# Status: Fixed some small things.
# removed the deleteMeshes bit since it didn't need to be there.
# Still TODO: Still bugs me that there are 6 variables that are guaranteed
# to be assigned but not used at the end of the last iteration.
# a few minor changes added to the comments to trigger possibly a new staging.

import bpy
from bpy.props import IntProperty, FloatProperty



def makePyramid( initialSize, stepHeight, stepWidth, numberSteps ):
    
    vertList = []
    faceList = []

    curSize = initialSize # how large each step will be overall
    
    # b = buttom, t = top, f = front, b = back, l = left, r = right
    x = y = z = 0
    voffset = 0 # refers relative vert indices to help make faces fo each step            
    sn = 0 # step number

    while sn < numberSteps:
    
        bfl = [x,y,z]
        bfr = [x+curSize, y, z]
        bbl = [x,y+curSize,z]
        bbr = [x+curSize, y+curSize, z]

        tfl  = [x,y,z-stepHeight]
        tfr = [x+curSize, y, z-stepHeight]
        tbl = [x,y+curSize,z-stepHeight]
        tbr = [x+curSize, y+curSize, z-stepHeight]

        # add to the vert buffer
        vertList.extend( bfl )
        vertList.extend( bfr )
        vertList.extend( bbl )
        vertList.extend( bbr )
        vertList.extend( tfl )
        vertList.extend( tfr)
        vertList.extend( tbl )
        vertList.extend( tbr )
        
        # side faces
        faceList.extend( [ voffset+0, voffset+1, voffset+5, voffset+4 ] )# front 
        faceList.extend( [ voffset+2, voffset+3, voffset+7, voffset+6 ] )# back
        faceList.extend( [ voffset+0, voffset+4, voffset+6, voffset+2 ] )# left
        faceList.extend( [ voffset+1, voffset+5, voffset+7, voffset+3 ] )# right   

        # connecting faces ( note: not applicable for the first iteration ).
        if voffset > 0:
          faceList.extend(  [voffset+0, voffset+1, voffset-3, voffset-4]) # front
          faceList.extend(  [voffset+2, voffset+3, voffset-1, voffset-2] ) # back
          faceList.extend(  [voffset+0, voffset+2, voffset-2, voffset-4] ) # left
          faceList.extend(  [voffset+1, voffset+3, voffset-1, voffset-3] ) # right
            


        # set up parameters for the next iteration
        curSize = curSize - ( stepWidth * 2 )
        x = x + stepWidth
        y = y + stepWidth
        z = z - stepHeight
        sn = sn + 1
        voffset = voffset + 8

        
    # cap the top.
    voffset = voffset - 8 # corrects for the unnecessary voffset change done final iteration
    faceList.extend( [voffset+4, voffset+5, voffset+7, voffset+6] )

    # cap the bottom.
    faceList.extend( [ 0, 1, 3, 2] )
    return vertList, faceList



class OBJECT_OT_PyramidOp( bpy.types.Operator ):
    
    initialSize = FloatProperty( name="Initial Size", default=2.0, min=0.0, max=5.0 )
    stepHeight= FloatProperty( name="Step Height", default=0.2, min=0.0, max=5.0 )
    stepWidth= FloatProperty( name="Step Width", default=0.2, min=0.0, max=5.0 )
    numberSteps= IntProperty( name="Number Steps", default=5, min=1, max=10 )
    
    bl_undo = True
    bl_register = True
    bl_idname="pyramid_op"


    def execute( self, context ):
        
        # use the op properties to create the pyramid faces and verts
        initSize = self.properties.initialSize
        sHeight = self.properties.stepHeight
        sWidth = self.properties.stepWidth 
        nSteps = self.properties.numberSteps
        verts, faces = makePyramid( initSize, sHeight, sWidth, nSteps )

        # load the vert and face data into a new pyramid mesh
        mesh = bpy.data.add_mesh( "pyramid" )
        mesh.add_geometry( int(len( verts )/3), 0, int(len( faces )/4) )
        mesh.verts.foreach_set( "co", verts )
        mesh.faces.foreach_set( "verts_raw", faces )

        
        scene = context.scene

        for ob in scene.objects:
            ob.selected = False

        mesh.update()

        # link the mesh data to a mesh object
        # then put it into the scene.
        ob_new = bpy.data.add_object( 'MESH', "Pyramid" )
        ob_new.data = mesh
        scene.objects.link( ob_new )

        scene.objects.active = ob_new
        ob_new.selected = True
        ob_new.location = tuple( context.scene.cursor_location )
        return( 'FINISHED', )


# standard operation registration and menu setup.
bpy.ops.add( OBJECT_OT_PyramidOp )
import dynamic_menu
menuFunc = ( lambda self, context: self.layout.operator( OBJECT_OT_PyramidOp.bl_idname, text="Pyramid" ) )
menu_item = dynamic_menu.add( bpy.types.INFO_MT_mesh_add, menuFunc )