bl_info = {
    'name' : 'Grab & Drop',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (3, 1, 2  ),
    'location' : 'View 3D > Tools > My Addon',
    'description' : 'Grabs & drops objects',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Animation'
    }


#imports
import bpy

# duplicate object, unparent and remove all animation
def drop():
    obj = bpy.context.active_object
    matrixcopy = obj.matrix_world.copy()
    dup = obj.copy()
    dup.parent = None
    dup.matrix_world = matrixcopy
    dup.animation_data_clear()
    bpy.context.collection.objects.link(dup)


# duplicate object, parent and remove all animation
def grab():
    # the next line is needed because selected_objects doesn't return a list that is ordered in the selection order
    obj = [i for i in bpy.context.selected_objects if i is not bpy.context.active_object][0]
    par = bpy.context.active_object
    dup = obj.copy()
    matrixcopy = obj.matrix_world.copy()
    dup.parent = par
    dup.matrix_world = matrixcopy
    dup.animation_data_clear()
    bpy.context.collection.objects.link(dup)


class VIEW_3D_PT_grabdroppanel(bpy.types.Panel):
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
        col.operator('script.graboperator', text='Grab')
        col.operator('script.dropoperator', text='Drop')

        
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
        return len(bpy.context.selected_objects) == 1
    
    #execute
    def execute(self, context):
        drop()
        return {'FINISHED'}
    
     
#registration
classes = (
    VIEW_3D_PT_grabdroppanel,
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