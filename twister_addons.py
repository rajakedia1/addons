bl_info = {
    "name": "Twister",
    "author": "Raja kedia",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Twister Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from math import sin, cos, pi
from bpy.props import (
        IntProperty,
        )
from bpy.app.translations import pgettext_data as data_

from bpy_extras import object_utils


def add_object(self, context, num, rot):
    #rot = (pi)/num
    rot = rot *pi / 180
    verts = []
    faces = []
    for v in range(num):
        
	    (x,y,z) = (cos((2*pi*v)/num), sin((2*pi*v)/num), 0)
	    verts.append( (x,y,z) )
    for v in range(num): 
	    (x,y,z) = (cos(((2*pi*v)/num) + rot), sin(((2*pi*v)/num)+rot), 1)
	    verts.append( (x,y,z) )
    for f in range(num-1):
        (a,b,c,d) = (f,f+1,f+num+1,f+num)
        faces.append( (a,b,c,d) )
    faces.append( (num-1,0,num,2*num-1) ) 
    faces.append( [i for i in range(num-1, -1, -1)] )
    faces.append( [i for i in range(num, 2*num)] )
    edges = []
    mesh = bpy.data.meshes.new(name="Twister")
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Twister Object"""
    bl_idname = "mesh.add_twister"
    bl_label = "Add Mesh Twister"
    bl_options = {'REGISTER', 'UNDO'}

    segments = IntProperty(
            name="Segments",
            description="Number of segments for the Twister",
            min=3, max=20,
            default=6,
            )
    rota = IntProperty(
            name="Rotation",
            description="Angle of Rotation for the Twister",
            min=0, max=180,
            default= 0
            )
	
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(self, 'view_align')
        
        col = layout.column(align=True)
        col.label(text="Segments")
        col.prop(self, "segments", text="")
        
        col = layout.column(align=True)
        col.label(text="Rotation")
        col.prop(self, "rota", text="")
		
    def invoke(self, context, event):
        object_utils.object_add_grid_scale_apply_operator(self, context)
        return self.execute(context)	
		
    def execute(self, context):

        add_object(self, context, self.segments, self.rota)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Twister",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "Modeling/Objects"),
        )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
