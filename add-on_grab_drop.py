# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    'name' : 'Grab & Drop',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (3, 1, 2  ),
    'location' : 'View 3D > Tools > Grab & Drop',
    'description' : 'Grabs & drops objects',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Animation'
    }


#imports
import bpy


# duplicate object, parent and remove all animation
# when the par is an armature and there is a bone selected in pose mode, it will parent to that bone
def grab():
    # the next line is needed because selected_objects doesn't return a list that is ordered in the selection order
    obj = [i for i in bpy.context.selected_objects if i is not bpy.context.active_object][0]
    par = bpy.context.active_object
    dup = obj.copy()
    matrixcopy = obj.matrix_world.copy()
    dup.parent = par
    
    if par.type == 'ARMATURE':
        if bpy.context.selected_pose_bones:
            dup.parent_bone = bpy.context.selected_pose_bones[-1].name
            dup.parent_type = 'BONE'
        
    dup.matrix_world = matrixcopy
    dup.animation_data_clear()
    coll = bpy.context.active_object.users_collection[0] 
    coll.objects.link(dup)
    
    hide(obj)
    show(dup)

    addMarker('grab')
    
    
# duplicate object, unparent and remove all animation
def drop():
    obj = bpy.context.active_object
    matrixcopy = obj.matrix_world.copy()
    dup = obj.copy()
    if dup.parent.type == 'ARMATURE':
        dup.parent_bone = ''
    dup.parent = None

    dup.matrix_world = matrixcopy
    dup.animation_data_clear()
    coll = bpy.context.active_object.users_collection[0] 
    coll.objects.link(dup)
    
    hide(obj)
    show(dup)
    
    addMarker('drop')


def hide(obj):
    bpy.context.scene.frame_current -= 1
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path = 'hide_viewport')
    obj.keyframe_insert(data_path = 'hide_render')
    bpy.context.scene.frame_current += 1
    obj.select_set(True)
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path = 'hide_viewport')
    obj.keyframe_insert(data_path = 'hide_render')
        
        
def show(obj):
    bpy.context.scene.frame_current -= 1
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path = 'hide_viewport')
    obj.keyframe_insert(data_path = 'hide_render')
    bpy.context.scene.frame_current += 1
    obj.select_set(True)
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path = 'hide_viewport')
    obj.keyframe_insert(data_path = 'hide_render')


def addMarker(t):
    scene = bpy.context.scene
    scene.timeline_markers.new(str(t), frame=bpy.context.scene.frame_current)
    

class VIEW_3D_PT_grabanddrop(bpy.types.Panel):
    #panel attributes
    """Grab & drop objects"""
    bl_label = 'Grab & Drop'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Grab & Drop'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.operator('script.graboperator', text='Grab', icon='LINK_BLEND')
        col.operator('script.dropoperator', text='Drop', icon='SORT_ASC')

        
class SCRIPT_OT_graboperator(bpy.types.Operator):
    #operator attributes
    """Grab object"""
    bl_label = 'Grab operator'
    bl_idname = 'script.graboperator'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) == 2
    
    #execute
    def execute(self, context):
        grab()
        return {'FINISHED'}
    
    
class SCRIPT_OT_dropoperator(bpy.types.Operator):
    #operator attributes
    """Drop object"""
    bl_label = 'Drop operator'
    bl_idname = 'script.dropoperator'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) == 1 and bpy.context.active_object.parent is not None
    
    #execute
    def execute(self, context):
        drop()
        return {'FINISHED'}
    
     
#registration
classes = (
    VIEW_3D_PT_grabanddrop,
    SCRIPT_OT_graboperator,
    SCRIPT_OT_dropoperator
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()
